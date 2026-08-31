# SPEC 002 — Pairwise Evaluation & History API

## 1. Objetivo

Permitir a avaliação comparativa lado a lado (*Side-by-Side / Pairwise Evaluation*) entre duas respostas geradas por IA (*Left Response* e *Right Response*) para uma mesma consulta de busca (*Query*), além de disponibilizar a consulta de histórico de avaliações por e-mail de usuário.

Nesta fase inicial, os dados de histórico são persistidos em memória para um usuário padrão estático.

---

## 2. Escopo

A funcionalidade compreende:
* Receber uma consulta de busca e duas respostas candidatas (esquerda e direita);
* Validar que nenhum dos campos obrigatórios esteja ausente ou vazio;
* Gerar notas avaliativas (`left_score` e `right_score`) e um comentário/justificativa (`comment`);
* Gerar automaticamente um identificador único (`id`);
* Atribuir a avaliação a um e-mail de usuário (`user_email`);
* Armazenar o histórico de avaliações em memória;
* Disponibilizar um endpoint para listar o histórico filtrado pelo e-mail do usuário.

---

## 3. Modelo de Dados

### 3.1 Entrada de Comparação (`ComparisonRequest`)
* `query` (string, obrigatório): pergunta ou busca realizada.
* `left_response` (string, obrigatório): resposta da IA do lado esquerdo.
* `right_response` (string, obrigatório): resposta da IA do lado direito.

### 3.2 Resultado de Avaliação / Item de Histórico (`ComparisonEvaluation`)
* `id` (string, gerado pela API): identificador único.
* `user_email` (string): e-mail associado ao histórico (ex: `user@example.com`).
* `query` (string): pergunta original avaliada.
* `left_response` (string): resposta do lado esquerdo.
* `right_response` (string): resposta do lado direito.
* `left_score` (float/int): nota atribuída à resposta esquerda (0 a 10).
* `right_score` (float/int): nota atribuída à resposta direita (0 a 10).
* `comment` (string): comentário explicativo sobre o desempenho comparativo das respostas.

---

## 4. Endpoint — Criar Avaliação Comparativa

### Request
```http
POST /evaluations
Content-Type: application/json
```

Body:
```json
{
  "query": "Qual é a capital do Brasil?",
  "left_response": "A capital do Brasil é Brasília.",
  "right_response": "A capital do Brasil é Buenos Aires."
}
```

### Response Esperada
Status: `201 Created`

Body:
```json
{
  "id": "generated-uuid",
  "user_email": "user@example.com",
  "query": "Qual é a capital do Brasil?",
  "left_response": "A capital do Brasil é Brasília.",
  "right_response": "A capital do Brasil é Buenos Aires.",
  "left_score": 10.0,
  "right_score": 0.0,
  "comment": "Avaliação comparativa concluída com sucesso."
}
```

---

## 5. Endpoint — Consultar Histórico por E-mail

### Request
```http
GET /evaluations/history?email=user@example.com
```

### Response Esperada
Status: `200 OK`

Body:
```json
[
  {
    "id": "generated-uuid",
    "user_email": "user@example.com",
    "query": "Qual é a capital do Brasil?",
    "left_response": "A capital do Brasil é Brasília.",
    "right_response": "A capital do Brasil é Buenos Aires.",
    "left_score": 10.0,
    "right_score": 0.0,
    "comment": "Avaliação comparativa concluída com sucesso."
  }
]
```

Se o usuário não possuir avaliações registradas, retornar:
```json
[]
```

---

## 6. Validações e Erros

A API deverá rejeitar:
* Ausência de `query`, `left_response` ou `right_response` (HTTP `422 Unprocessable Entity`).
* Campos preenchidos apenas com espaços em branco ou vazios (HTTP `422 Unprocessable Entity`).

---

## 7. Critérios de Aceitação

* [ ] `POST /evaluations` cria uma avaliação comparativa e retorna HTTP 201 com `id`, `user_email`, `left_score`, `right_score` e `comment`.
* [ ] A API gera automaticamente identificadores únicos para cada avaliação.
* [ ] Campos vazios ou ausentes no POST retornam HTTP 422.
* [ ] `GET /evaluations/history` retorna a lista de avaliações do histórico do usuário com HTTP 200.
* [ ] `GET /evaluations/history` retorna lista vazia `[]` quando não houver registros para o e-mail.
* [ ] Todos os testes automatizados cobrem os critérios e passam com 100% de sucesso.
