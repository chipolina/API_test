class Getschema:
    @staticmethod
    def schema_create_char():
        schema_create_char = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "properties": {
                "result": {
                    "type": "object",
                    "properties": {
                        "education": {
                            "type": "string"
                        },
                        "height": {
                            "type": "number"
                        },
                        "identity": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        },
                        "universe": {
                            "type": "string"
                        },
                        "weight": {
                            "type": "number"
                        }
                    },
                    "required": [
                        "education",
                        "height",
                        "identity",
                        "name",
                        "universe",
                        "weight"
                    ]
                }
            },
            "required": [
                "result"
            ]}
        return schema_create_char

    @staticmethod
    def schema_update_char():
        schema_update_char = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "properties": {
                "result": {
                    "type": "object",
                    "properties": {
                        "education": {
                            "type": "string"
                        },
                        "height": {
                            "type": "number"
                        },
                        "identity": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        },
                        "universe": {
                            "type": "string"
                        },
                        "weight": {
                            "type": "number"
                        }
                    },
                    "required": [
                        "education",
                        "height",
                        "identity",
                        "name",
                        "universe",
                        "weight"
                    ]
                }
            },
            "required": [
                "result"
            ]
        }
        return schema_update_char

    @staticmethod
    def schema_get_char():
        schema_get_char = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "properties": {
                "education": {
                    "type": "string"
                },
                "height": {
                    "type": "integer"
                },
                "identity": {
                    "type": "string"
                },
                "name": {
                    "type": "string"
                },
                "other_aliases": {
                    "type": "string"
                },
                "universe": {
                    "type": "string"
                },
                "weight": {
                    "type": "number"
                }
            },
            "required": [
                "education",
                "height",
                "identity",
                "name",
                "other_aliases",
                "universe",
                "weight"
            ]
        }
        return schema_get_char
