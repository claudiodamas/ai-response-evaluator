# SPEC 002 — Evaluation API

## 1. Objetivo

Criar a primeira funcionalidade de negócio da AI Response Evaluator API.

A API deverá permitir criar uma avaliação de uma resposta gerada por um LLM e consultar as avaliações existentes.

Nesta primeira versão, os dados serão mantidos em memória. A persistência em PostgreSQL será adicionada em uma etapa posterior.

---

## 2. Escopo

A funcionalidade deverá permitir:

* criar uma avaliação;
* validar os dados recebidos;
* consultar todas as avaliações;
* consultar uma avaliação específica pelo ID;
* retornar erros HTTP apropriados;
* testar os comportamentos automaticamente.

---

## 3. Modelo de avaliação

Cada avaliação deverá possuir:

* `id`: identificador único;
* `prompt`: prompt utilizado para gerar a resposta;
* `response`: resposta produzida pelo LLM;
* `score`: nota da resposta;
* `feedback`: comentário sobre a qualidade da resposta.

### Regras

* `prompt` é obrigatório;
* `response` é obrigatório;
* `score` é obrigatório;
* `score` deve estar entre `0` e `10`;
* `feedback` é obrigatório;
* `id` deve ser gerado pela API;
* o cliente não deve enviar o `id`.

---

## 4. Endpoint — Criar avaliação

### Request

```http
POST /evaluations
Content-Type: application/json
```

Body:

```json
{
  "prompt": "Explain what RAG is.",
  "response": "RAG combines retrieval with generation.",
  "score": 9,
  "feedback": "Accurate and concise explanation."
}
```

### Response esperada

Status:

```http
201 Created
```

Body:

```json
{
  "id": "generated-id",
  "prompt": "Explain what RAG is.",
  "response": "RAG combines retrieval with generation.",
  "score": 9,
  "feedback": "Accurate and concise explanation."
}
```

---

## 5. Endpoint — Listar avaliações

### Request

```http
GET /evaluations
```

### Response esperada

Status:

```http
200 OK
```

Body:

```json
[
  {
    "id": "generated-id",
    "prompt": "Explain what RAG is.",
    "response": "RAG combines retrieval with generation.",
    "score": 9,
    "feedback": "Accurate and concise explanation."
  }
]
```

Se não existirem avaliações, a API deverá retornar:

```json
[]
```

---

## 6. Endpoint — Buscar avaliação

### Request

```http
GET /evaluations/{evaluation_id}
```

### Comportamento

Quando o ID existir, retornar:

```http
200 OK
```

Quando o ID não existir, retornar:

```http
404 Not Found
```

---

## 7. Validação

A API deverá rejeitar requisições inválidas.

Exemplos:

### Score abaixo do mínimo

```json
{
  "prompt": "Example",
  "response": "Example",
  "score": -1,
  "feedback": "Example"
}
```

Resultado:

```http
422 Unprocessable Entity
```

### Score acima do máximo

```json
{
  "prompt": "Example",
  "response": "Example",
  "score": 11,
  "feedback": "Example"
}
```

Resultado:

```http
422 Unprocessable Entity
```

### Campo obrigatório ausente

Resultado:

```http
422 Unprocessable Entity
```

---

## 8. Critérios de aceitação

A implementação será considerada concluída quando:

* [ ] `POST /evaluations` criar uma avaliação válida;
* [ ] a API gerar automaticamente o ID;
* [ ] avaliações puderem ser listadas;
* [ ] uma avaliação puder ser buscada pelo ID;
* [ ] ID inexistente retornar `404`;
* [ ] `score` aceitar valores de `0` a `10`;
* [ ] `score` fora desse intervalo for rejeitado;
* [ ] campos obrigatórios forem validados;
* [ ] os testes automatizados cobrirem os comportamentos principais;
* [ ] todos os testes passarem;
* [ ] a implementação permanecer compatível com a arquitetura definida na SPEC 001.

---

## 9. Estratégia de implementação

A implementação deverá seguir TDD.

Ordem obrigatória:

```text
SPEC
 ↓
TESTES
 ↓
TESTES FALHAM
 ↓
IMPLEMENTAÇÃO MÍNIMA
 ↓
TESTES PASSAM
 ↓
REFACTOR
 ↓
TESTES PASSAM NOVAMENTE
```

Nenhuma funcionalidade deverá ser implementada antes de existir um teste correspondente.

---

## 10. Limitações desta versão

Esta versão não deverá implementar:

* PostgreSQL;
* autenticação;
* integração com LLM;
* RAG;
* tool calling;
* MCP;
* Docker;
* deploy.

Essas funcionalidades serão introduzidas em specs posteriores.

A implementação atual deverá, entretanto, manter uma estrutura que permita adicionar essas funcionalidades posteriormente sem reescrever a API inteira.
