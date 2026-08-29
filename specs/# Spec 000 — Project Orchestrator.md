# Spec 000 — Project Orchestrator

## 1. Project

**Name:** AI Response Evaluator API

**Purpose:**
Build a small production-oriented REST API for evaluating AI-generated responses against configurable evaluation criteria.

The project exists primarily to demonstrate a Spec-Driven Development workflow in which specifications are the source of truth for implementation, testing, validation, and project evolution.

---

# 2. Development Philosophy

The project MUST follow the following development loop:

```text
SPECIFICATION
      ↓
ANALYSIS
      ↓
IMPLEMENTATION PLAN
      ↓
IMPLEMENTATION
      ↓
AUTOMATED TESTS
      ↓
VALIDATION
      ↓
CHECKPOINT
      ↓
NEXT SPECIFICATION
```

No functionality may be implemented without an associated specification.

The implementation MUST NOT introduce behavior that is not defined or implied by an approved specification.

When requirements are ambiguous, contradictory, or incomplete, the agent MUST stop and request clarification rather than making assumptions.

---

# 3. Role of the AI Development Agent

The AI agent acts as a **Spec-Driven Development Orchestrator and Implementation Agent**.

The agent is responsible for:

1. Understanding the current project state.
2. Identifying what has already been implemented.
3. Identifying missing functionality.
4. Determining the next logical development stage.
5. Creating or requesting the next specification.
6. Creating an implementation plan based exclusively on the specification.
7. Implementing the approved specification.
8. Creating or updating automated tests.
9. Running the test suite.
10. Validating that implementation matches the specification.
11. Reporting the checkpoint result.
12. Determining the next required specification.

The agent MUST NOT skip stages merely because the implementation appears simple.

---

# 4. Source of Truth

The `specs/` directory is the project's source of truth.

Specifications MUST use sequential numbering:

```text
specs/
├── 000-project-orchestrator.md
├── 001-...
├── 002-...
├── 003-...
└── ...
```

Each specification MUST have:

* objective;
* scope;
* functional requirements;
* non-functional requirements when applicable;
* input/output definitions;
* acceptance criteria;
* error cases;
* dependencies;
* validation criteria.

---

# 5. Specification Lifecycle

Every feature follows this lifecycle:

```text
DRAFT
  ↓
REVIEW
  ↓
APPROVED
  ↓
IMPLEMENTED
  ↓
TESTED
  ↓
VALIDATED
  ↓
COMPLETED
```

A specification MUST NOT be considered completed until:

* implementation exists;
* automated tests exist;
* tests pass;
* acceptance criteria have been verified;
* no known contradiction exists between specification and implementation.

---

# 6. Project Development Sequence

The agent SHOULD guide the project through the following sequence.

The exact specifications may be split differently when technically justified, but the agent MUST preserve the dependency order.

---

## CHECKPOINT 0 — Project Definition

Current specification:

```text
000-project-orchestrator.md
```

Goal:

Establish the project development rules and orchestration process.

Validation:

* Project purpose is defined.
* SDD workflow is defined.
* Specification lifecycle is defined.
* Checkpoint mechanism is defined.

When this checkpoint is satisfied, proceed to Checkpoint 1.

---

# CHECKPOINT 1 — Project Architecture

Create the next specification defining the initial technical architecture.

Expected specification:

```text
001-project-architecture.md
```

The architecture specification SHOULD define:

* Python version;
* FastAPI;
* project structure;
* application entry point;
* testing strategy;
* dependency management;
* configuration strategy;
* persistence strategy;
* API conventions;
* error handling conventions.

The architecture MUST remain intentionally simple.

Do not introduce infrastructure that is unnecessary for demonstrating the project.

### Exit Criteria

The project structure can be created without implementing business functionality.

After architecture is approved and implemented:

```text
CHECKPOINT 1 → COMPLETE
```

Proceed to Checkpoint 2.

---

# CHECKPOINT 2 — Health Check

Create:

```text
002-health-check.md
```

Define:

```text
GET /health
```

Expected behavior:

```json
{
  "status": "ok"
}
```

Acceptance criteria MUST include:

* HTTP 200;
* valid JSON;
* expected status field;
* automated test.

### Exit Criteria

The application starts successfully and the health endpoint passes all tests.

Then:

```text
CHECKPOINT 2 → COMPLETE
```

Proceed to Checkpoint 3.

---

# CHECKPOINT 3 — Evaluation Domain Model

Create the specification for the core evaluation entity.

Expected concept:

```text
Evaluation
```

The specification MUST define:

* identifier;
* input prompt;
* AI response;
* evaluation criteria;
* score;
* created timestamp;
* status where applicable.

The specification MUST define validation rules.

Do NOT implement an AI provider yet.

### Exit Criteria

The domain model and its validation behavior are covered by automated tests.

Then proceed to Checkpoint 4.

---

# CHECKPOINT 4 — Create Evaluation

Create the specification for:

```text
POST /evaluations
```

Define:

* request schema;
* validation;
* response schema;
* identifier generation;
* persistence;
* error behavior.

Acceptance criteria MUST include successful and invalid requests.

### Exit Criteria

A valid evaluation can be created and invalid evaluations are rejected according to the specification.

Proceed to Checkpoint 5.

---

# CHECKPOINT 5 — Retrieve Evaluation

Create the specification for:

```text
GET /evaluations/{id}
```

Define:

* successful retrieval;
* nonexistent resource;
* response format;
* error behavior.

### Exit Criteria

All acceptance criteria pass automated tests.

Proceed to Checkpoint 6.

---

# CHECKPOINT 6 — List Evaluations

Create the specification for:

```text
GET /evaluations
```

The specification SHOULD define:

* pagination or a deliberately limited first version;
* ordering;
* response structure;
* empty result behavior.

Do not add filtering unless required by the specification.

### Exit Criteria

The endpoint works and tests cover the defined behavior.

Proceed to Checkpoint 7.

---

# CHECKPOINT 7 — Evaluation Criteria

Create the specification defining evaluation criteria.

Examples:

```text
accuracy
relevance
clarity
safety
```

The criteria model MUST be configurable rather than hard-coded into individual endpoints where practical.

Define:

* criterion name;
* description;
* weight;
* validation;
* score range.

### Exit Criteria

Criteria can be represented and validated independently.

Proceed to Checkpoint 8.

---

# CHECKPOINT 8 — Rule-Based Evaluation

Before introducing an external LLM, implement a deterministic evaluation mechanism.

Create the specification defining a simple evaluator.

The evaluator MUST produce deterministic results for the same input.

This creates a testable baseline before external AI integration.

### Exit Criteria

The evaluator is independently testable and produces reproducible results.

Proceed to Checkpoint 9.

---

# CHECKPOINT 9 — LLM Provider Abstraction

Create the specification for integrating an LLM.

The architecture MUST separate:

```text
Evaluation Service
        ↓
LLM Provider Interface
        ↓
Provider Implementation
```

The business logic MUST NOT depend directly on a specific provider.

The specification MUST define:

* provider interface;
* request format;
* response format;
* timeout behavior;
* failure behavior;
* configuration requirements.

Do not require a real API key for automated tests.

### Exit Criteria

The LLM integration can be mocked during testing.

Proceed to Checkpoint 10.

---

# CHECKPOINT 10 — AI Evaluation

Create the specification for AI-assisted evaluation.

Define:

* prompt construction;
* evaluation criteria sent to the model;
* expected structured response;
* parsing;
* validation;
* score normalization;
* failure handling.

The AI response MUST NOT be trusted blindly.

The application MUST validate the model output before accepting it.

### Exit Criteria

Valid model responses are accepted and malformed model responses are rejected safely.

Proceed to Checkpoint 11.

---

# CHECKPOINT 11 — Automated Test Strategy

Create a specification for the project's testing strategy.

Tests SHOULD be divided into:

```text
Unit Tests
Integration Tests
API Tests
```

External LLM calls MUST be mocked.

The specification MUST define the minimum critical behavior that must always be covered.

### Exit Criteria

The complete test suite can run without external services or credentials.

Proceed to Checkpoint 12.

---

# CHECKPOINT 12 — API Error Contract

Create a specification standardizing API errors.

Define:

* error response structure;
* validation errors;
* resource-not-found errors;
* internal errors;
* external provider errors.

All endpoints MUST follow the same contract.

### Exit Criteria

Error behavior is consistent across the API.

Proceed to Checkpoint 13.

---

# CHECKPOINT 13 — Documentation

Create the specification for developer-facing documentation.

The documentation SHOULD include:

* project purpose;
* architecture;
* development workflow;
* API usage;
* local setup;
* testing;
* specification workflow;
* design decisions.

The README MUST explicitly explain that the project was developed using Spec-Driven Development.

### Exit Criteria

A new developer can understand and run the project.

Proceed to Checkpoint 14.

---

# CHECKPOINT 14 — CI

Create the specification for continuous integration.

The CI pipeline SHOULD:

1. install dependencies;
2. run tests;
3. fail when tests fail.

Keep CI intentionally simple.

### Exit Criteria

Every relevant repository change can be automatically validated.

Proceed to Checkpoint 15.

---

# CHECKPOINT 15 — SDD Demonstration Scenario

This checkpoint exists specifically to demonstrate SDD to a recruiter or interviewer.

The agent MUST create a controlled change to an existing feature.

Example:

Initial requirement:

```text
An evaluation has a score from 0 to 10.
```

Change:

```text
An evaluation must support scores from 0 to 100.
```

The agent MUST demonstrate:

```text
SPEC CHANGE
     ↓
IMPACT ANALYSIS
     ↓
IMPLEMENTATION PLAN
     ↓
CODE CHANGE
     ↓
TEST UPDATE
     ↓
VALIDATION
```

The old behavior MUST NOT remain accidentally supported if the new specification replaces it.

### Exit Criteria

The repository history clearly demonstrates that a specification change caused corresponding implementation and test changes.

---

# 7. Autonomous Progression Rules

After every completed checkpoint, the agent MUST:

1. Inspect the repository.
2. Identify completed specifications.
3. Identify incomplete specifications.
4. Determine the next dependency-safe feature.
5. State which specification should be created next.
6. Explain why that specification is the next logical step.
7. Create the specification only when the requirements are sufficiently clear.
8. Otherwise ask the human for clarification.
9. Never implement the next feature before its specification is approved.

The agent MUST maintain the sequence automatically.

---

# 8. Checkpoint Report Format

At the end of every implementation cycle, the agent MUST report:

```text
CHECKPOINT: <number>

SPEC:
<specification name>

STATUS:
COMPLETE / BLOCKED / FAILED

IMPLEMENTED:
- ...

TESTS:
- ...

VALIDATION:
- ...

SPECIFICATION COMPLIANCE:
PASS / FAIL

NEXT STEP:
<next specification>

REASON:
<why this is the next step>
```

---

# 9. Stop Conditions

The agent MUST stop and request human input when:

* requirements are ambiguous;
* two specifications conflict;
* implementation would require an architectural decision not defined by the specification;
* a security-sensitive behavior is undefined;
* an external service is required but credentials/configuration are unavailable;
* tests contradict the specification;
* implementation requires behavior outside the current scope.

The agent MUST NOT silently invent requirements to continue.

---

# 10. Implementation Rules

The agent MUST:

* prefer small changes;
* keep functions focused;
* avoid unnecessary abstractions;
* avoid speculative features;
* write tests for acceptance criteria;
* preserve existing functionality unless the specification explicitly changes it;
* update tests when specifications change;
* keep implementation traceable to a specification.

The agent SHOULD use AI-assisted coding when available, but AI-generated code is never considered correct merely because it was generated.

Correctness is established through:

```text
SPECIFICATION
+
TESTS
+
VALIDATION
```

---

# 11. Definition of Done

A feature is DONE only when:

```text
[✓] Specification exists
[✓] Specification approved
[✓] Implementation plan created
[✓] Code implemented
[✓] Automated tests created
[✓] Tests pass
[✓] Acceptance criteria validated
[✓] No known specification violations
[✓] Checkpoint completed
[✓] Next specification identified
```

---

# 12. Final Project Goal

The final repository MUST demonstrate not only a working API, but a reproducible Spec-Driven Development process.

A reviewer should be able to inspect the repository and understand:

```text
WHAT was requested
       ↓
WHY it was required
       ↓
HOW it was planned
       ↓
HOW it was implemented
       ↓
HOW it was tested
       ↓
HOW changes propagated
```

The project is successful when the specification can be followed from requirement to implementation and back from implementation to specification.
