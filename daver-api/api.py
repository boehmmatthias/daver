from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yaml
import json
import uuid
import os
from datetime import datetime
from typing import Dict, List, Optional
import ollama
import sys

from nlparser.natural_language_parser import get_processed_query
from querygenerator.query_generator import get_database_query
from queryjudge.query_judge import judge_sql_responses

sys.path.append('../')
import os

from schemaanalyzer.schema_analyzer import get_analyzed_schema


app = FastAPI(title="Daver API", description="Natural Language Database Query System")

# CORS middleware for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime = None

class ChatRequest(BaseModel):
    message: str
    chat_id: Optional[str] = None

class ChatResponse(BaseModel):
    chat_id: str
    fetched_data: dict
    sql_query: str
    additional_information: str
    
class AnalysisStatus(BaseModel):
    status: str
    message: str

# Storage
UPLOAD_DIR = "uploads"
ANALYSIS_DIR = "analysis"
CHAT_SESSIONS: Dict[str, List[ChatMessage]] = {}

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

# Utility functions
def load_config():
    """Load the current database configuration"""
    config_path = os.path.join(UPLOAD_DIR, "config.yaml")
    if not os.path.exists(config_path):
        raise HTTPException(status_code=404, detail="No configuration file found")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_analysis_path():
    """Get path to the schema analysis file"""
    return os.path.join(ANALYSIS_DIR, "schema_analysis.yaml")

def call_ollama(model: str, prompt: str, system_prompt: str = None) -> str:
    """Helper function to call Ollama models"""
    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = ollama.chat(model=model, messages=messages)
        return response['message']['content']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")

def analyze_schema_with_ollama(config: dict) -> dict:
    """Analyze database schema using Ollama"""
    
    db_config = config['database']
    print(db_config)
    analyzed_schema = get_analyzed_schema(db_config=db_config, model='phi4:14b')
    print('Schema analyzed successfully.')
    return analyzed_schema

def process_chat_query(message: str, chat_history: List[ChatMessage], schema_analysis: str) -> str:
    """Process user query and generate SQL"""
    
    message = message.strip()
    processed_query = get_processed_query(message, model='phi4:14b', host='http://localhost:11434')
    print(f'Processed query: {processed_query}')
    
    n_queries = 10

    sql_responses = [get_database_query(processed_query, schema_analysis, model='deepseek-coder:6.7b').replace('\n',' ') for _ in range(n_queries)]

    response = judge_sql_responses(sql_responses, message, processed_query, schema_analysis, model='deepseek-coder:6.7b')
    resp_json = json.loads(response)
    if 'thinking' in resp_json:
        print(f'Thinking: {resp_json["thinking"]}')
    response = resp_json['choice']
    idx = int(response.lower().removeprefix('response '))
    return sql_responses[idx]

# API Endpoints

@app.post("/upload-config")
async def upload_config(config_file: UploadFile = File(..., description="YAML configuration file")):
    """Upload database configuration file via form data"""
    if not config_file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
        
    if not (config_file.filename.endswith('.yaml') or config_file.filename.endswith('.yml')):
        raise HTTPException(status_code=400, detail="File must be a YAML file (.yaml or .yml)")
    
    config_path = os.path.join(UPLOAD_DIR, "config.yaml")
    
    try:
        content = await config_file.read()
        # Validate YAML format
        yaml.safe_load(content)
        
        with open(config_path, 'wb') as f:
            f.write(content)
        print("Configuration written successfully")
            
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"Invalid YAML format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    return analyze_schema()

def analyze_schema():
    """Analyze database schema and store results"""
    print("Analyzing schema")
    try:
        config = load_config()
        
        # Perform schema analysis
        analysis_result = analyze_schema_with_ollama(config)
        
        # Store analysis results
        analysis_path = get_analysis_path()
        with open(analysis_path, 'w') as f:
            f.write(analysis_result)
        
        return AnalysisStatus(
            status="completed",
            message="Schema analysis completed and stored successfully"
        )
        
    except Exception as e:
        print(f"Analysis failed: {str(e)}")
        return AnalysisStatus(
            status="error", 
            message=f"Analysis failed: {str(e)}"
        )

def fetch_data(sql_query: str, db_config: dict) -> dict:
    """Fetch data from the database using the generated SQL query"""
    import mysql.connector
    connection = None
    cursor = None
    data = {}
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql_query)
        results = cursor.fetchall()
        data = {'result': results}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return data

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the database system"""
    try:
        # Load schema analysis
        analysis_path = get_analysis_path()
        if not os.path.exists(analysis_path):
            raise HTTPException(status_code=404, detail="No schema analysis found. Please analyze schema first.")
        
        with open(analysis_path, 'r') as f:
            yaml_file = yaml.load(f, Loader=yaml.FullLoader)
            analyzed_schema = yaml.dump(yaml_file)
        
        # Get or create chat session
        chat_id = request.chat_id or str(uuid.uuid4())
        if chat_id not in CHAT_SESSIONS:
            CHAT_SESSIONS[chat_id] = []
        
        chat_history = CHAT_SESSIONS[chat_id]
        
        # Add user message to history
        user_message = ChatMessage(
            role="user", 
            content=request.message,
            timestamp=datetime.now()
        )
        chat_history.append(user_message)
        
        # Process query
        sql_query = process_chat_query(
            request.message, 
            chat_history, 
            analyzed_schema
        )
        print(f"Generated SQL Query: {sql_query}")
        # Fetch data from the database
        db_config = load_config()['database']
        fetched_data = fetch_data(sql_query, db_config)

        # Add assistant response to history
        generated_query_message = ChatMessage(
            role="query",
            content=sql_query,
            timestamp=datetime.now()
        )
        chat_history.append(generated_query_message)
        
        # Limit chat history size
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]
            CHAT_SESSIONS[chat_id] = chat_history
        
        return ChatResponse(
            chat_id=chat_id,
            sql_query=sql_query,
            additional_information='',
            fetched_data=fetched_data,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

@app.get("/chat/{chat_id}/history")
async def get_chat_history(chat_id: str):
    """Get chat history for a session"""
    if chat_id not in CHAT_SESSIONS:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    return {"chat_id": chat_id, "messages": CHAT_SESSIONS[chat_id]}

@app.get("/status")
async def get_status():
    """Get system status"""
    config_exists = os.path.exists(os.path.join(UPLOAD_DIR, "config.yaml"))
    analysis_exists = os.path.exists(get_analysis_path())
    
    return {
        "config_uploaded": config_exists,
        "schema_analyzed": analysis_exists,
        "active_chats": len(CHAT_SESSIONS)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)