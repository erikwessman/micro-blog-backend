comment_schema = {
    "title": "Comment",
    "description": "Record of a comment",
    "type": "object",
    "properties": {
        "author": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "date": {
            "type": "number"
        },
        "content": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1000
        },
        "article_id": {
            "type": "string",
            "minLength": 1,
            "maxLength": 24
        }
    },
    "required": ["author", "date", "content", "article_id"]
}

comment_user_schema = {
    "title": "User comment",
    "description": "Record of comment created by a user",
    "type": "object",
    "properties": {
        "content": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1000
        },
        "article_id": {
            "type": "string",
            "minLength": 1,
            "maxLength": 24
        }
    },
    "required": ["content", "article_id"]
}
