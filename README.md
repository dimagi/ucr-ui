The UCR UI
----------

A proof-of-concept implementation for creating editable UCRs using [JSON schemas](https://json-schema.org/).

At a high-level, the idea is to:

1. Create JSON schemas for the various elements of UCR (starting with expressions, indicators, and filters).
2. Leverage a tool like [`json-editor`](https://github.com/json-editor/json-editor) to use those schemas to build
   an editing interface for the UCR components.
3. Integrate this editing UI with CommCare (likely as an API-driven external service to start, then eventually 
   in a more integrated way).

At the moment, this library primarily demonstrates a PoC for bullet-point 1.

# Using this Project

The Python code in `./src/` is used to generate complex schemas from the schemas of individual UCR elements.

To generate these schemas run:

```bash
python src/schema_generator.py
```

## Inputs

The input files with individual UCR elements are in the `./schemas/` folder. They include:

- `./schemas/expressions/`: one file per expression type.
- `./schemas/filters/`: one file per filter type.
- `./schemas/indicators/`: one file per indicator type.

Filters are complete. For expressions and indicators, only a subset of schemas has been implemented, though it is 
believed that all UCR elements can be represented this way.

## Outputs

The key outputs of this library are in the `./schemas/outputs/` folder. These include:

- `single-expression.json`: a JSON schema for a single UCR expression object. 
   This could be plugged in anywhere in CommCare that uses expressions.
- `single-filter.json`: a JSON schema for a single UCR filter object. 
   This could be plugged in anywhere in CommCare that uses filters, including the UCR Data Source UI.
- `multi-indicator.json`: a JSON schema for a list of expression indicator objects.
   This can be used as a replacement for the "Configured indicators" section of the UCR data source UI.

## Testing

The easiest way to test these outputs is to use the online [JSON-Editor sandbox](https://pmk65.github.io/jedemov2/dist/demo.html).
You can paste any schema in to the "Schema" tab, click "Generate Form" on top, and then play with the resulting UI.

# Technical Notes

## Project Roadmap

1. Get to high confidence that all important UCR elements can be represented as JSON Schemas and edited by JSON Editor.
   Filters are complete. Indicators and expressions currently have high confidence. So this is close, if not done.
2. Explore options for integrating the editing UIs into CommCare HQ.
3. Explore the dynamic creation of the individual schemas from CommCare HQ's Python code, so that they can be kept
   in sync.
4. Consider building a more user-friendly interface to replace the bare-bones (and confusing!) JSON-Editor.

## Eventual Data Source Schema

These fields can be edited in the current UI. A "final" UI might incorporate all of them, though only the complex
JSON fields flagged with a "*" are the important candidates.

- Table ID
- Source Type (form/case)
- Display Name
- Description
- *Base item expression
- *Filter
- *Indicators
- *Named expressions
- *Named filters
- Data source ID
