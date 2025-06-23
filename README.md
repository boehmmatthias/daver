<img src="https://github.com/user-attachments/assets/560aed51-cc84-457d-b928-484b6c1d060f" width="500" height="500"/>

# Daver - A conversational SQL interface for fetching data using natural language

## Project Members
- Matthias Böhm, K11907932
- Lukas Kurz, K12007739

## Setting up a local instance of daver

### Requirements:

Have Docker and Docker Compose installed on your machine.

### Database Setup

1. Copy or create a `.env` file in the project root:
```env
MYSQL_ROOT_PASSWORD=pizzatime
MYSQL_DATABASE=daver_db
MYSQL_USER=daver
MYSQL_PASSWORD=pizzatime
```

### AI Model Setup

There are 2 options for setting up the AI models:

1. **Using Ollama** (Recommended because the models run way faster): 
   - Install [Ollama](https://ollama.com/docs/installation) on your machine.
   - Download the required models using:
     ```bash
     ollama pull phi4-mini:3.8b
     ollama pull gemma3:4b
     ollama pull deepseek-coder:6.7b
     ```
     
    In the `.env` file, set the `OLLAMA_HOST` variable to point to your Ollama instance:
    ```env
        OLLAMA_HOST=http://host.docker.internal:11434
    ```

2. **Using Docker**:
   - If you prefer to run the models in Docker, you can use the provided `docker-compose.yml` file.
   - Make sure you allocate enough resources to the models in your Docker settings. Should be at least 16GB of RAM.
   - The models will be pulled automatically when you start the project.
   - We recommend using Ollama locally instead of Docker for better performance.
   
### Start the project:
```bash
./start-daver.sh # or
./start-daver.sh -d # for detached mode
```

A database with some sample data will be created automatically. The test data was obtained from the databasestar sample databases (https://github.com/bbrumm/databasestar/tree/main/sample_databases/sample_db_olympics)

### Accessing the Application

You can access the application at `http://localhost:8080` in your web browser. The application provides a simple interface to interact with the database using natural language queries.

For the database config file you can use the daver_sample_config.yaml file in the root directory.

The database config file should look like this:
```yaml
database:
  host: "db"
  port: 3306
  username: "daver"
  password: "pizzatime"
  database: "daver_db"
```