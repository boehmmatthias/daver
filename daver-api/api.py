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
    response: str
    sql_query: Optional[str] = None
    
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
    analyzed_schema = get_analyzed_schema(db_config=db_config, model='gemma3:4b')
    print('Schema analyzed successfully.')
    return analyzed_schema

def process_chat_query(message: str, chat_history: List[ChatMessage], schema_analysis: dict) -> tuple:
    """Process user query and generate SQL"""
    
    # Step 1: Preprocess natural language query
    preprocess_prompt = f"""Convert this natural language query into a clear, technical instruction:
    User query: {message}
    
    Available database schema: {json.dumps(schema_analysis, indent=2)}
    
    Return a structured query intent."""
    
    processed_query = call_ollama("llama3.1:8b", preprocess_prompt)
    
    # Step 2: Generate SQL
    sql_prompt = f"""Generate SQL query for this request:
    Processed query: {processed_query}
    
    Database schema: {json.dumps(schema_analysis, indent=2)}
    
    Return only valid SQL query."""
    
    sql_query = call_ollama("sqlcoder:15b", sql_prompt)
    
    # Step 3: Generate natural language response
    response_prompt = f"""Create a user-friendly response explaining what this SQL query does:
    SQL: {sql_query}
    Original request: {message}
    
    Be conversational and explain the results."""
    
    response = call_ollama("llama3.1:8b", response_prompt)
    
    return response, sql_query.strip()

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
        response_text, sql_query = process_chat_query(
            request.message, 
            chat_history, 
            schema_analysis
        )
        
        # Add assistant response to history
        assistant_message = ChatMessage(
            role="assistant",
            content=response_text,
            timestamp=datetime.now()
        )
        chat_history.append(assistant_message)
        
        # Limit chat history size
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]
            CHAT_SESSIONS[chat_id] = chat_history
        
        return ChatResponse(
            chat_id=chat_id,
            response=response_text,
            sql_query=sql_query if sql_query and sql_query != response_text else None
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