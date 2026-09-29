# Agent Instructions

This file contains repository-specific instructions for coding agents working on
this project.

## Project Overview

This is a small educational FastAPI application demonstrating OpenAI Responses
API function calling. The application exposes a `/chat` endpoint, lets the model
select one or more local tools, executes those tools, and returns their outputs
to the model for a final response.

The current tools use static demo data. Do not describe their output as live or
real-time data.

## Environment

- Python 3.14 or newer
- Dependency and command runner: `uv`
- Application server: FastAPI with Uvicorn
- OpenAI SDK: Responses API
- Required environment variable: `OPENAI_API_KEY`

Install dependencies:

```bash
uv sync
```

Run the application:

```bash
uv run uvicorn main:app --reload
```

Run all tests:

```bash
uv run python -m unittest discover -s tests -v
```

## Repository Layout

- `main.py`: FastAPI routes and the tool-calling loop.
- `tools.py`: Local Python tool implementations.
- `tool_definitions.py`: JSON schemas sent to the model.
- `tests/test_tool_calling.py`: Unit tests with mocked OpenAI responses.
- `docs/TOOL_CALLING.md`: Detailed explanation of the tool-calling flow.
- `README.md`: Setup and usage documentation.

## Architecture Rules

- Keep tool implementation code in `tools.py`.
- Keep model-visible tool schemas in `tool_definitions.py`.
- Register every schema in `TOOLS` inside `main.py`.
- Register every implementation in `AVAILABLE_TOOLS` using the exact schema
  name.
- Return JSON-serializable dictionaries from tool functions.
- Keep tool schemas strict with `additionalProperties: False`.
- Preserve support for zero, one, or multiple function calls in one response.
- Return each result as `function_call_output` with the original `call_id`.
- Continue model turns using `previous_response_id`.
- Keep the tool-round limit to prevent endless model/tool loops.

## Adding or Changing a Tool

1. Add or update the Python function in `tools.py`.
2. Add or update its strict schema in `tool_definitions.py`.
3. Update both `TOOLS` and `AVAILABLE_TOOLS` in `main.py`.
4. Add tests for known input, unknown input, and routing behavior.
5. Update `README.md` or `docs/TOOL_CALLING.md` when behavior changes.

## Testing Rules

- Do not make real OpenAI API calls in unit tests.
- Mock `client.responses.create` and inspect continuation inputs.
- Cover direct model responses, single-tool calls, and multiple-tool calls.
- Verify that `call_id` and `previous_response_id` are preserved.
- Run the full test suite after code or schema changes.

## Security

- Never commit `.env` or a real API key.
- Use `.env.example` only as a placeholder template.
- Do not print secrets in routes, logs, tests, or error messages.
- Execute only functions registered in `AVAILABLE_TOOLS`.
- Treat model-generated tool names and arguments as untrusted input.

## Change Discipline

- Keep changes focused on the requested behavior.
- Preserve unrelated user changes in the working tree.
- Prefer small, readable functions over new abstractions for this educational
  project.
- Keep documentation examples synchronized with the actual commands and API
  response shape.
