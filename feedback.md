EVALUATION REPORT
Nexus2.0
Post-Evaluation Feedback Report
India AI Impact Buildathon
Presented by HCL GUVI
Problem Statement: Agentic Honey-Pot for Scam Detection & Intelligence
Extraction
OVERALL READINESS SCORE
0/100
Executive Summary
Nexus2.0, your endpoint returned a plain text "Too Many Requests" response instead of the JSON
structure required by the Agentic Honey-Pot for Scam Detection problem. This violates the API contract
and prevents the evaluator from parsing scam detection results, leading to a zero score. In production,
such a mismatch would break downstream services that expect a strict JSON payload. The gap is
concrete, measurable, and fully learnable with focused effort on response formatting and error handling.
Overall Readiness Score
0
The submission could not be evaluated due to endpoint accessibility issues. The
API endpoint failed to respond to evaluation requests, resulting in a score of
0/100.
Key Strengths
Successfully deployed a live HTTP POST endpoint on Render, showing basic DevOps capability
Implemented the required request body fields (sessionId, message, conversationHistory, met
Set up a multi turn session skeleton that captures conversation context, indicating an und
Key Gaps
× Endpoint returns a plain text "Too Many Requests" message rather than a JSON object with {
× No explicit handling of rate limit or overload conditions; the server hits a 429 error bef
× Missing validation of input schema and output schema, causing the API contract to be broke
Evaluation Methodology
How Your Solution Was Evaluated
Code was not inspected directly
Evaluation based on observable system b...
Multiple test scenarios were executed
API endpoint responses were analyzed
Test Types Used
Standard functional test cases
Invalid and malformed input cases
API response format validation
Error handling and edge case scenarios
Skills Assessment
Core Logic & Correctness
Error Handling & Edge Cases
Scalability & Load Handling
API / I/O Robustness
LLM Prompting & Control
System Thinking
What Worked Well
The URL was reachable and the server responded, confirming that the deployment pipeline wa
Your request payload adhered to the required field names, which is a good start for schema
0/100
0/100
0/100
0/100
0/100
0/100
Observed Breakdowns
× Invalid response type: HTTP 200/429 returned with plain text instead of JSON, causing "inv
× Rate limiting triggered early, suggesting insufficient concurrency handling or missing ret
× No JSON schema validation on inbound request, so malformed or missing fields could cause s
Personalized Learning Roadmap
Top 3 Skill Gaps Identified
1
API Contract Compliance – JSON Response Structure
Your service returned a raw text "Too Many Requests" which does not match the required JSON schema
{status, reply}. In production, clients will reject such payloads, causing downstream failures. Fix by
defining a response model (e.g., using FastAPI's pydantic BaseModel) and always serializing to JSON,
even for error cases. Example: ```python from fastapi import FastAPI, HTTPException from pydantic
import BaseModel class Reply(BaseModel): status: str reply: str @app.post("/scam") async def
2
Rate Limiting & Proper HTTP Status Management
The server responded with HTTP 429 "Too Many Requests" without a structured JSON error body, which
broke the evaluator's parser. Implement a middleware that catches rate limit exceptions and returns a
JSON error payload, e.g., `{ "error": "rate_limit", "message": "Too many requests" }` with status code 429.
Use libraries like `slowapi` or `express-rate-limit` to control traffic and ensure graceful degradation.
3
Input Validation and Schema Enforcement
There was no validation of required fields (sessionId, message, etc.), so malformed inputs could slip
through and cause unexpected server errors. Use request schema validation (pydantic, Joi, or
marshmallow) to reject bad payloads early with a clear JSON error response (400 Bad Request). This
also protects downstream LLM prompting logic from receiving incomplete data.
Suggested Learning Path
Immediate Priority (next 2 weeks)
→ Define and enforce a strict JSON response model using FastAPI/Flask and pydantic o...
→ Implement proper HTTP status codes with JSON error bodies for rate limiting and va...
→ Learn to use a rate limiting middleware (e.g., slowapi) and test with load generat...
→ Hands on exercise: Refactor the current endpoint to always return `{ "status": ......
Production Readiness (next 4–6 weeks)
→ Advanced API design: OpenAPI spec generation, automated contract testing with Sche...
→ Observability: add structured logging, health checks, and Prometheus metrics for r...
→ Domain specific depth: Prompt engineering for scam detection LLMs, ensuring determ...
→ Capstone: Re implement the Agentic Honey Pot, pass the full test suite, and deploy...
Ready to Bridge These Gaps?
The right path can transform your career. With HCL GUVI, book a personalized career consultation
today to gain clear guidance and take confident steps toward your goals.