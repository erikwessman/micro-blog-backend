comment_schema = {
    "type": "object",
    "properties": {
        "author": {
            "type": "string"
        },
        "date": {
            "type": "number"
        },
        "content": {
            "type": "string"
        },
        "article_id": {
            "type": "string"
        }
    },
    "required": ["author", "date", "content", "article_id"]
}

comment_user_schema = {
    "type": "object",
    "properties": {
        "content": {
            "type": "string"
        },
        "article_id": {
            "type": "string"
        }
    },
    "required": ["content", "article_id"]
}
