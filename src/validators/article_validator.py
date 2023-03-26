article_schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string"
        },
        "author": {
            "type": "string"
        },
        "description": {
            "type": "string"
        },
        "date": {
            "type": "number"
        },
        "categories": {
            "type": "array",
            "items": {
                "type": "string"
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
            "required": ["src"]
        },
        "content": {
            "type": "string"
        },
        "required": ["title", "author", "date", "categories", "content"]
    }
}

article_user_schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string"
        },
        "description": {
            "type": "string"
        },
        "categories": {
            "type": "array",
            "items": {
                "type": "string"
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
            "required": ["src"]
        },
        "content": {
            "type": "string"
        },
        "required": ["title", "categories", "content"]
    }
}
