<img src="https://github.com/user-attachments/assets/560aed51-cc84-457d-b928-484b6c1d060f" width="500" height="500"/>

# daver

## Setting Up the Test MySQL Database

1. Copy or create a `.env` file in the project root:
```env
MYSQL_ROOT_PASSWORD=pizzatime
MYSQL_DATABASE=daver_db
MYSQL_USER=daver
MYSQL_PASSWORD=pizzatime
```

   
2. Start the MySQL container:
```bash
docker compose up -d
```
3. Olympics Test Data should be created automatically on first startup.