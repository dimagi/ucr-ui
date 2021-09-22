import json
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_DIR = BASE_DIR / 'schemas'
EXPRESSION_DIR = SCHEMA_DIR / 'expressions'


def generate_schema():
    print('generating schema')
    print(BASE_DIR, SCHEMA_DIR, EXPRESSION_DIR)
    expression_schemas = []
    for expression_file in sorted(os.listdir(EXPRESSION_DIR)):
        print(expression_file)
        with open(EXPRESSION_DIR / expression_file) as f:
            expression_schema = json.loads(f.read())
            expression_schemas.append(expression_schema)

    expression_schema = {
        "type": "array",
        "title": "Expressions",
        "items": {
            "oneOf": expression_schemas
        }
    }
    with open(SCHEMA_DIR / 'expression-oneof.json', 'w') as f:
        f.write(f'{json.dumps(expression_schema, indent=2)}\n')


if __name__ == "__main__":
    generate_schema()
