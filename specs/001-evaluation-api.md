# SPEC 001 — AI Response Evaluator REST API

## 1. Objetivo

Definir a arquitetura base da API REST com **FastAPI**, incluindo o monitoramento de saúde do serviço (`/health`), a funcionalidade de **Avaliação Comparativa de Respostas de IA (*Pairwise Evaluation / Left vs Right*)** e a consulta de **Histórico de Avaliações por Usuário**.

Nesta fase inicial, os dados de histórico são persistidos em memória para um usuário padrão estático (`user@example.com`).

---

## 2. Escopo e Requisitos Gerais

* A API deve ser construída utilizando **FastAPI**.
* O serviço deve expor um endpoint para verificação de status (`health check`).
* A API deve permitir receber uma consulta de busca (*Query*) e duas respostas candidatas (*Left Response* e *Right Response*).
* A API deve validar que nenhum campo obrigatório esteja ausente ou contenha apenas espaços em branco.
* A API deve calcular e retornar notas avaliativas (`left_score`, `right_score`), comentário explicativo (`comment`) e identificador único gerado automaticamente (`id`).
* A API deve armazenar o histórico de avaliações em memória associado ao e-mail do usuário (`user_email`).
* A API deve permitir a consulta do histórico filtrado por e-mail via query parameter.

---

## 3. Modelo de Dados

### 3.1 Entrada de Comparação (`ComparisonRequest`)
* `query` (string, obrigatório): pergunta ou busca realizada (não vazia).
* `left_response` (string, obrigatório): resposta da IA do lado esquerdo (não vazia).
* `right_response` (string, obrigatório): resposta da IA do lado direito (não vazia).

### 3.2 Resultado de Avaliação / Item de Histórico (`ComparisonEvaluation`)
* `id` (string, gerado pela API): identificador único (UUID).
* `user_email` (string): e-mail associado ao histórico (ex: `user@example.com`).
* `query` (string): pergunta original avaliada.
* `left_response` (string): resposta do lado esquerdo.
* `right_response` (string): resposta do lado direito.
* `left_score` (float/int): nota atribuída à resposta esquerda (0 a 10).
* `right_score` (float/int): nota atribuída à resposta direita (0 a 10).
* `comment` (string): comentário/justificativa da avaliação.

---

## 4. Endpoints da API

### 4.1 `GET /health` (Health Check)
* **Status:** `200 OK`
* **Response Body:**
  ```json
  {
    "status": "ok"
  }
  ```

---

### 4.2 `POST /evaluations` (Criar Avaliação Comparativa)
* **Headers:** `Content-Type: application/json`
* **Request Body:**
  ```json
  {
    "query": "Qual é a capital do Brasil?",
    "left_response": "A capital do Brasil é Brasília.",
    "right_response": "A capital do Brasil é Buenos Aires."
  }
  ```
* **Status:** `201 Created`
* **Response Body:**
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

### 4.3 `GET /evaluations/history` (Consultar Histórico por E-mail)
* **Query Parameter:** `email` (string, obrigatório)
* **Exemplo:** `GET /evaluations/history?email=user@example.com`
* **Status:** `200 OK`
* **Response Body:**
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
* Se não houver avaliações para o e-mail, retornar: `[]`

---

## 5. Validações e Tratamento de Erros

A API deverá rejeitar requisições inválidas com `422 Unprocessable Entity`:
* Ausência de `query`, `left_response` ou `right_response`.
* Campos preenchidos apenas com espaços em branco ou vazios.

---

## 6. Critérios de Aceitação

* [ ] `GET /health` retorna status 200 com `{"status": "ok"}`.
* [ ] `POST /evaluations` cria uma avaliação comparativa e retorna status 201 com `id`, `user_email`, `left_score`, `right_score` e `comment`.
* [ ] A API gera automaticamente identificadores únicos para cada avaliação.
* [ ] Campos vazios, ausentes ou com apenas espaços no POST retornam status 422.
* [ ] `GET /evaluations/history` retorna a lista de avaliações do histórico do usuário com status 200.
* [ ] `GET /evaluations/history` retorna lista vazia `[]` quando não houver registros para o e-mail informado.
* [ ] Todos os testes automatizados cobrem os critérios e passam com 100% de sucesso.
