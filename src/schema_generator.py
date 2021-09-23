import json
import os
from pathlib import Path

import enums

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
        "items": {
            "$ref": "#/definitions/expression"
        },
        "definitions": {
            "expression": single_expression_schema,
        }
    }

    with open(SCHEMA_DIR / 'multi-expression.json', 'w') as f:
        f.write(_schema_to_json(multi_expression_schema))


    # indicator
    with open(SCHEMA_DIR / 'indicators' / 'expression.json') as f:
        indicator_schema = json.loads(f.read())

    multi_indicator_schema = {
        "type": "array",
        "title": "Indicators",
        "items": {
            "$ref": "#/definitions/indicator"
        },
        "definitions": {
            "indicator": indicator_schema,
            "expression": single_expression_schema,
            "datatype": enums.DATATYPE
        }
    }
    with open(SCHEMA_DIR / 'multi-indicator.json', 'w') as f:
        f.write(_schema_to_json(multi_indicator_schema))


def _schema_to_json(schema):
    return f'{json.dumps(schema, indent=2)}\n'

if __name__ == "__main__":
    generate_schemas()
