user_schema = {
    "title": "User",
    "description": "Record of a user",
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "email": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        },
        "password": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        }
    },
    "required": ["username", "email", "password"]
}

user_login_schema = {
    "title": "User login",
    "description": "Record of a user's login",
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "password": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        }
    },
    "required": ["username", "password"]
}
