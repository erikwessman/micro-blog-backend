# micro-blog-backend

## How to run

1. Install the necessary dependencies by running the following command in the root directory:

`pip install -r requirements.txt`

2. Create a `.env` file that specifies the following:

* **DB_HOST** - URL of your MongoDB instance
* **DB_PORT** - Port of your MongoDB instance
* **DB_NAME** - Can be any name, used to connect to a specific database
* **JWT_KEY** - Can be any secure key, used to sign the JSON Web Tokens
* **ADMIN_KEY** - Can be any secure key, used to authenticate admin-only API endpoints

3. Start your MongoDB instance
4. Start the application by running the following command, in the root directory:

`flask --app src/main.py run`

*or, if using venv*

`(chmod +X start.sh)`

`./start.sh`