import json
import os
from pathlib import Path
from typing import List

import enums

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_DIR = BASE_DIR / 'schemas'
OUTPUT_DIR = SCHEMA_DIR / 'outputs'
EXPRESSION_DIR = SCHEMA_DIR / 'expressions'
FILTER_DIR = SCHEMA_DIR / 'filters'


def generate_schemas():
    print('generating schema')
    print(BASE_DIR, SCHEMA_DIR, EXPRESSION_DIR)
    expression_schemas = _load_schemas(EXPRESSION_DIR)

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
    with open(OUTPUT_DIR / 'single-expression.json', 'w') as f:
        f.write(_schema_to_json(single_expression_schema))

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

    with open(OUTPUT_DIR / 'multi-expression.json', 'w') as f:
        f.write(_schema_to_json(multi_expression_schema))


    # indicators
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
    with open(OUTPUT_DIR / 'multi-indicator.json', 'w') as f:
        f.write(_schema_to_json(multi_indicator_schema))

    # filters
    filter_schemas = _load_schemas(FILTER_DIR)
    single_filter_schema = {
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
        "oneOf": filter_schemas,
        "definitions": {
            "expression": single_expression_schema,
            "operator": enums.OPERATOR,
        }
    }
    with open(OUTPUT_DIR / 'single-filter.json', 'w') as f:
        f.write(_schema_to_json(single_filter_schema))


def _load_schemas(directory: Path) -> List[dict]:
    all_schemas = []
    for schema_file in sorted(os.listdir(directory)):
        print(schema_file)
        with open(directory / schema_file) as f:
            schema = json.loads(f.read())
            all_schemas.append(schema)
    return all_schemas


def _schema_to_json(schema: dict) -> str:
    return f'{json.dumps(schema, indent=2)}\n'


if __name__ == "__main__":
    generate_schemas()
