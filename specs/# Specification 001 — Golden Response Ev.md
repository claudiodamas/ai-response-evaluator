# Specification 001 — Golden Response Evaluation

## 1. Objective

Implement a deterministic evaluation component that compares a candidate AI response against a predefined **Golden Response** and produces a structured evaluation result.

The component MUST evaluate whether the candidate response satisfies the expected answer according to defined evaluation criteria.

The evaluation system MUST NOT require an external LLM for the initial implementation.

---

# 2. Definitions

## 2.1 Query

The original question or instruction provided to the AI model.

Example:

```text
What is the capital of Brazil?
```

## 2.2 Golden Response

The reference answer considered acceptable for the given query.

A Golden Response represents the expected content and quality of an ideal response.

Example:

```text
The capital of Brazil is Brasília.
```

The Golden Response is a reference, not necessarily the only valid answer.

## 2.3 Candidate Response

The AI-generated response being evaluated.

Example:

```text
Brasília is the capital of Brazil.
```

## 2.4 Evaluation Criteria

The dimensions used to determine whether a candidate response is acceptable.

The initial implementation MUST support:

* correctness;
* relevance;
* completeness;
* clarity.

---

# 3. Evaluation Input

The evaluator MUST accept:

```json
{
  "query": "What is the capital of Brazil?",
  "golden_response": "The capital of Brazil is Brasília.",
  "candidate_response": "Brasília is the capital of Brazil."
}
```

All three fields are required.

### Validation

The evaluator MUST reject:

* missing `query`;
* missing `golden_response`;
* missing `candidate_response`;
* empty strings;
* strings containing only whitespace.

The evaluator MUST NOT silently replace missing values.

---

# 4. Evaluation Criteria

## 4.1 Correctness

Correctness measures whether the candidate response contains information that is factually consistent with the Golden Response and does not introduce contradictory information.

### Score

```text
0 = Incorrect
1 = Partially correct
2 = Correct
```

### Rules

**0 — Incorrect**

The candidate provides an answer that contradicts the expected answer or is fundamentally wrong.

Example:

Golden:

```text
The capital of Brazil is Brasília.
```

Candidate:

```text
The capital of Brazil is São Paulo.
```

Score: `0`

---

**1 — Partially correct**

The candidate contains some correct information but is incomplete or contains a minor factual problem.

Example:

```text
Brazil's capital is Brasília, located in Brazil's southeast.
```

The first statement is correct, but the location is incorrect.

Score: `1`

---

**2 — Correct**

The candidate communicates the correct factual answer without contradiction.

Example:

```text
Brasília is the capital of Brazil.
```

Score: `2`

---

# 5. Relevance

Relevance measures whether the candidate directly addresses the Query without unnecessary unrelated content.

### Score

```text
0 = Irrelevant
1 = Mostly relevant
2 = Directly relevant
```

### Rules

**0 — Irrelevant**

The candidate does not answer the query.

**1 — Mostly relevant**

The candidate answers the query but contains substantial unrelated information.

**2 — Directly relevant**

The candidate directly addresses the query with minimal unnecessary information.

---

# 6. Completeness

Completeness measures whether the candidate contains the essential information required to answer the Query.

The Golden Response defines the minimum expected information.

### Score

```text
0 = Missing essential information
1 = Partially complete
2 = Complete
```

A candidate does not need to reproduce the Golden Response word-for-word.

Semantic equivalence MUST be considered acceptable.

Example:

Golden:

```text
The capital of Brazil is Brasília.
```

Candidate:

```text
Brasília.
```

This MAY receive:

```text
Correctness: 2
Relevance: 2
Completeness: 1
```

because the answer is correct but provides less information than the reference.

---

# 7. Clarity

Clarity measures whether the response is understandable and appropriately structured.

### Score

```text
0 = Unclear
1 = Understandable
2 = Clear
```

The candidate MUST NOT be penalized merely for using different wording from the Golden Response.

Grammar, organization, ambiguity and unnecessarily confusing language MAY affect the score.

---

# 8. Overall Score

The evaluator MUST calculate the overall score using:

```text
overall_score =
(
  correctness +
  relevance +
  completeness +
  clarity
) / 8 * 100
```

The resulting score MUST be between `0` and `100`.

Example:

```text
correctness = 2
relevance = 2
completeness = 2
clarity = 2

overall_score = 100
```

---

# 9. Evaluation Result

The evaluator MUST return a structured result.

Example:

```json
{
  "overall_score": 100,
  "criteria": {
    "correctness": 2,
    "relevance": 2,
    "completeness": 2,
    "clarity": 2
  },
  "passed": true,
  "feedback": "The candidate response correctly and clearly answers the query."
}
```

---

# 10. Pass Threshold

A candidate response MUST be considered passing when:

```text
overall_score >= 75
```

Otherwise:

```text
passed = false
```

The threshold MUST be configurable in the implementation.

The default threshold MUST be `75`.

---

# 11. Golden Response Matching

The evaluator MUST NOT require exact string matching.

The following responses SHOULD be considered equivalent:

Golden:

```text
The capital of Brazil is Brasília.
```

Candidate:

```text
Brasília is Brazil's capital.
```

Candidate:

```text
Brazil has its capital in Brasília.
```

Differences in:

* capitalization;
* punctuation;
* sentence structure;
* word order;
* minor stylistic choices

MUST NOT automatically cause failure.

---

# 12. Contradiction Handling

A candidate response containing information that directly contradicts the Golden Response MUST receive a reduced correctness score.

Example:

Golden:

```text
The capital of Brazil is Brasília.
```

Candidate:

```text
The capital of Brazil is Brasília, but Brazil's official capital is Rio de Janeiro.
```

The candidate MUST NOT receive a perfect correctness score.

---

# 13. Additional Information

Additional information MUST NOT automatically be considered incorrect.

The evaluator SHOULD determine whether additional information:

1. supports the answer;
2. is neutral;
3. contradicts the expected answer;
4. is irrelevant.

Only contradictory or materially misleading information MUST negatively affect correctness.

---

# 14. Determinism

The initial evaluator MUST be deterministic.

Given identical inputs:

```text
query
+
golden_response
+
candidate_response
```

the evaluator MUST produce the same result.

The initial implementation MUST NOT depend on:

* external APIs;
* network requests;
* random values;
* current date/time;
* external LLM calls.

---

# 15. Acceptance Criteria

## Scenario 1 — Perfect response

Given:

```text
Query:
What is the capital of Brazil?

Golden Response:
The capital of Brazil is Brasília.

Candidate Response:
Brasília is the capital of Brazil.
```

Expected:

```text
correctness = 2
relevance = 2
completeness = 2
clarity = 2
overall_score = 100
passed = true
```

---

## Scenario 2 — Incorrect response

Given:

```text
Candidate Response:
The capital of Brazil is São Paulo.
```

Expected:

```text
correctness = 0
passed = false
```

---

## Scenario 3 — Partially correct response

Given:

```text
Candidate Response:
Brasília is the capital of Brazil, located in southeastern Brazil.
```

Expected:

```text
correctness < 2
```

because the response contains incorrect additional information.

---

## Scenario 4 — Equivalent wording

Given:

```text
Golden:
The capital of Brazil is Brasília.

Candidate:
Brazil's capital city is Brasília.
```

Expected:

```text
correctness = 2
passed = true
```

---

## Scenario 5 — Empty candidate

Given:

```text
Candidate Response:
""
```

Expected:

```text
HTTP/API validation error
```

The evaluator MUST NOT perform an evaluation.

---

## Scenario 6 — Relevant but incomplete

Given:

```text
Golden:
The capital of Brazil is Brasília.

Candidate:
Brasília.
```

Expected:

```text
correctness = 2
relevance = 2
completeness < 2
```

---

# 16. Implementation Constraints

The implementation MUST separate:

```text
Input Validation
       ↓
Evaluation Logic
       ↓
Score Calculation
       ↓
Result Generation
```

The API layer MUST NOT contain the evaluation rules directly.

The evaluation logic SHOULD be independently testable without starting the HTTP server.

---

# 17. Testing Requirements

Automated tests MUST cover:

* valid evaluation;
* invalid input;
* empty input;
* correct response;
* incorrect response;
* partially correct response;
* equivalent wording;
* irrelevant response;
* incomplete response;
* contradictory additional information;
* score calculation;
* pass threshold;
* deterministic output.

Every acceptance criterion MUST have at least one automated test.

---

# 18. Future Extension

The initial implementation MUST remain deterministic.

Future specifications MAY introduce an LLM-based evaluator.

If an LLM evaluator is introduced, it MUST preserve the same evaluation contract:

```text
query
golden_response
candidate_response
        ↓
evaluation_result
```

The LLM integration MUST be isolated behind an evaluator interface so that the deterministic evaluator can continue to be used for testing.

---

# 19. Definition of Done

This specification is complete when:

* [ ] Input model exists.
* [ ] Validation rules are implemented.
* [ ] Evaluation criteria are implemented.
* [ ] Score calculation is implemented.
* [ ] Pass threshold is implemented.
* [ ] Evaluation result follows the defined schema.
* [ ] Automated tests cover all acceptance criteria.
* [ ] All tests pass.
* [ ] Implementation does not depend on an external LLM.
* [ ] Implementation behavior matches this specification.
