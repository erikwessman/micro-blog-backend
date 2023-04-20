article_schema = {
    "title": "Article",
    "description": "Record of a article",
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
        },
        "author": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "description": {
            "type": "string",
            "minLength": 1,
            "maxLength": 500
        },
        "date": {
            "type": "number"
        },
        "categories": {
            "type": "array",
            "maxItems": 5,
            "uniqueItems": True,
            "items": {
                "type": "string",
                "minLength": 1,
                "maxLength": 100
            }
        },
        "image": {
            "type": "object",
            "properties": {
                "src": {
                    "type": "string"
                },
                "alt": {
                    "type": "string"
                },
                "caption": {
                    "type": "string"
                }
            },
            "required": [
                "src"
            ]
        },
        "content": {
            "type": "string",
            "minLength": 1,
            "maxLength": 5000
        }
    },
    "required": [
        "title",
        "author",
        "date",
        "categories",
        "content"
    ]
}

article_user_schema = {
    "title": "User article",
    "description": "Record of an article created by a user",
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
        },
        "description": {
            "type": "string",
            "minLength": 1,
            "maxLength": 500
        },
        "categories": {
            "type": "array",
            "maxItems": 5,
            "uniqueItems": True,
            "items": {
                "type": "string",
                "minLength": 1,
                "maxLength": 100
            }
        },
        "image": {
            "type": "object",
            "properties": {
                "src": {
                    "type": "string"
                },
                "alt": {
                    "type": "string"
                },
                "caption": {
                    "type": "string"
                }
            },
            "required": [
                "src"
            ]
        },
        "content": {
            "type": "string",
            "minLength": 1,
            "maxLength": 5000
        }
    },
    "required": [
        "title",
        "categories",
        "content"
    ]
}
