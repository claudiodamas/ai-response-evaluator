# SPEC 001 — API Foundation

## Goal

Create the initial REST API for the AI Response Evaluator.

## Requirements

- The API must run using FastAPI.
- The API must expose a health check endpoint.
- The health check must return HTTP 200.
- The response must indicate that the API is running.

## Acceptance Criteria

### AC1 — Health Check

Given that the API is running

When the client sends GET /health

Then the API must return HTTP 200

And the response must contain:

{
  "status": "ok"
}