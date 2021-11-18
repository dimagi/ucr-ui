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
            "datatype": enums.DATATYPE,
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
    }
    full_single_filter_schema = {
        "$ref": "#/definitions/filter",
        "definitions": {
            "filter": single_filter_schema,
            "expression": single_expression_schema,
            "operator": enums.OPERATOR,
        }
    }
    with open(OUTPUT_DIR / 'single-filter.json', 'w') as f:
        f.write(_schema_to_json(full_single_filter_schema))

    # data source - this is incomplete but could be easily added
    data_source = {
        "type": "object",
        "properties": {
            "table_id": {
                "description": "The name of the underlying DB table to use.",
                "type": "string"
            },
            "configured_filter": {
                "$ref": "#/definitions/filter"
            },
            "configured_indicators": {
                "type": "array",
                "title": "Indicators",
                "items": {
                    "$ref": "#/definitions/indicator"
                },
            },
        },
        "definitions": {
            "datatype": enums.DATATYPE,
            "expression": single_expression_schema,
            "indicator": indicator_schema,
            "filter": single_filter_schema,
            "operator": enums.OPERATOR,
        }
    }
    with open(OUTPUT_DIR / 'data-source.json', 'w') as f:
        f.write(_schema_to_json(data_source))


def _load_schemas(directory: Path) -> List[dict]:
    all_schemas = []
    for schema_file in sorted(os.listdir(directory)):
        with open(directory / schema_file) as f:
            schema = json.loads(f.read())
            all_schemas.append(schema)
    return all_schemas


def _schema_to_json(schema: dict) -> str:
    return f'{json.dumps(schema, indent=2)}\n'


if __name__ == "__main__":
    generate_schemas()
