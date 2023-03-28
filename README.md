# micro-blog-backend

## How to run

1. Install dependencies:

    `pip install -r requirements.txt`

2. Create `.env` in root with:

* **DB_HOST** - URL of your MongoDB instance
* **DB_PORT** - Port of your MongoDB instance
* **DB_NAME** - Can be any name, used to connect to a specific database
* **JWT_KEY** - Can be any secure key, used to sign the JSON Web Tokens
* **ADMIN_KEY** - Can be any secure key, used to authenticate admin-only API endpoints

3. Start a MongoDB instance

4. Start the application:

    `flask --app src/main.py run`

## How to test

1. Run the command:

    `pytest src/tests/`