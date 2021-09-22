import json
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_DIR = BASE_DIR / 'schemas'
EXPRESSION_DIR = SCHEMA_DIR / 'expressions'


def generate_schemas():
    print('generating schema')
    print(BASE_DIR, SCHEMA_DIR, EXPRESSION_DIR)
    expression_schemas = []
    for expression_file in sorted(os.listdir(EXPRESSION_DIR)):
        print(expression_file)
        with open(EXPRESSION_DIR / expression_file) as f:
            expression_schema = json.loads(f.read())
            expression_schemas.append(expression_schema)

    # see https://github.com/jdorn/json-editor/issues/619 for inspiration
    single_expression_schema = {
      "type": "object",
      "options": {
        "keep_oneof_values": False
      },
      "properties": {
        "type": {
          "type": "string",
          "options": {
            "hidden": True
          }
        }
      },
      "oneOf": expression_schemas,
    }
    with open(SCHEMA_DIR / 'single-expression.json', 'w') as f:
        f.write(f'{json.dumps(single_expression_schema, indent=2)}\n')

    multi_expression_schema = {
        "type": "array",
        "title": "Expressions",
        "items": single_expression_schema,
    }
    with open(SCHEMA_DIR / 'multi-expression.json', 'w') as f:
        f.write(f'{json.dumps(multi_expression_schema, indent=2)}\n')


if __name__ == "__main__":
    generate_schemas()
