
DATATYPE = {
    "type": "string",
    "enum": [
        "date",
        "datetime",
        "string",
        "integer",
        "decimal",
    ],
    "default": "string"
}


OPERATOR = {
    "type": "string",
    "enum": [
        "eq",
        "not_eq",
        "in",
        "in_multi",
        "any_in_multi",
        "lt",
        "lte",
        "gt",
        "gte",
    ],
    "default": "eq"
}
