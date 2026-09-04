# SPEC 002 — UI Design System: Duelo de Respostas

## 1. Propósito

Definir o padrão visual e comportamental da página de avaliação comparativa. Esta especificação complementa a especificação funcional (SDD), os testes (TDD) e o modelo de domínio (DDD), registrando decisões de interface que devem ser reutilizadas ao criar novas páginas do produto.

O objetivo é garantir que novas experiências mantenham a mesma hierarquia visual, linguagem, acessibilidade e comportamento de estados, sem depender de interpretação individual de cada implementação.

---

## 2. Princípios de interface

| Princípio | Regra de aplicação |
| --- | --- |
| Comparação clara | Respostas concorrentes devem sempre aparecer lado a lado em telas amplas e com marcadores A/B visíveis. |
| Resultado explicado | Uma nota nunca aparece isolada: deve estar acompanhada de contexto textual da avaliação. |
| Continuidade | Após uma ação, preservar os dados digitados até que a pessoa escolha limpá-los. |
| Feedback imediato | Toda ação assíncrona deve expor estado de carregamento, sucesso ou falha no mesmo contexto da ação. |
| Informação em camadas | Contexto e explicações secundárias usam menor contraste e tamanho que a decisão principal. |

---

## 3. Design tokens

Os valores abaixo são a fonte de verdade para interfaces do produto. Novas páginas devem reutilizá-los antes de introduzir cores, tamanhos ou raios novos.

### 3.1 Cores

| Token | Valor | Uso |
| --- | --- | --- |
| `--color-canvas` | `#090D1B` | Fundo principal. |
| `--color-surface` | `#111827` | Cards, formulários e painéis. |
| `--color-surface-muted` | `#0C1220` | Campos de entrada e itens de histórico. |
| `--color-border` | `#34415A` | Bordas padrão. |
| `--color-text` | `#F8F7F3` | Texto principal. |
| `--color-text-muted` | `#AEB7CA` | Texto de apoio. |
| `--color-accent` | `#F5A7BD` | Ações principais, ênfases e foco. |
| `--color-success` | `#8ED5BD` | Sucesso e estado concluído. |
| `--color-error` | `#FFB4B4` | Erros e falhas de requisição. |
| `--color-answer-a` | `#F9CF73` | Marcador da resposta A. |
| `--color-answer-b` | `#99D9D0` | Marcador da resposta B. |

### 3.2 Tipografia e espaçamento

| Token | Valor | Uso |
| --- | --- | --- |
| `--font-sans` | `DM Sans, sans-serif` | Corpo, controles e navegação. |
| `--font-display` | `Playfair Display, serif` | Títulos e pontuações. |
| `--font-mono` | `DM Mono, monospace` | Rótulos técnicos, eyebrow e metadados. |
| `--radius-sm` | `8px` | Inputs e botões. |
| `--radius-md` | `12px` | Cards e avisos. |
| `--radius-lg` | `16px` | Formulários principais. |
| `--space-1` a `--space-6` | `4, 8, 12, 18, 26, 42px` | Espaçamento interno e entre blocos. |

---

## 4. Estrutura da página

```
App shell
├── Topbar
│   ├── Marca
│   └── Ação “Histórico”
├── Hero
│   ├── Eyebrow
│   ├── Título
│   └── Texto de apoio
├── Comparison form
│   ├── Campo de contexto/pergunta
│   ├── Resposta A
│   ├── Resposta B
│   └── Ações: limpar / avaliar
├── Feedback de carregamento (condicional)
├── Resultado (condicional)
│   ├── Score card A
│   ├── Separador VS
│   ├── Score card B
│   └── Contexto da avaliação
└── Painel de histórico (modal lateral, condicional)
```

A largura máxima do conteúdo é `1090px`. A topbar usa largura máxima de `1220px`. O conteúdo deve manter margem lateral mínima de `18px` em dispositivos móveis.

---

## 5. Especificação de componentes

### 5.1 Campo de comparação

- Cada input possui rótulo permanente; placeholder não substitui rótulo.
- A resposta A usa marcador circular amarelo; a resposta B usa marcador circular verde-água.
- Textareas possuem altura inicial mínima de `155px` e podem ser redimensionadas verticalmente.
- Em foco, usar borda de destaque e anel de foco na cor de acento.
- O botão primário fica desabilitado durante o envio, com texto `Avaliando…`.

### 5.2 Estado de carregamento

- Exibir abaixo do formulário imediatamente após o envio.
- Deve ter spinner animado, título `A IA está avaliando as respostas` e explicação curta.
- O formulário permanece visível e seus valores são preservados.
- O estado desaparece ao receber sucesso ou erro.

### 5.3 Resultado

- Exibir somente após resposta bem-sucedida da API ou seleção no histórico.
- Exibir duas notas em cards simétricos, com uma casa decimal e sufixo `/10`.
- O conteúdo original de cada resposta deve ser mostrado no card correspondente.
- A justificativa deve ficar em bloco de menor destaque visual, rotulado como `O que foi avaliado`.
- Não alterar ou limpar campos do formulário ao receber o resultado.

### 5.4 Histórico

- Abrir como painel lateral sobreposto, sem trocar de rota.
- Carregar dados ao abrir o painel.
- Cada item apresenta pergunta truncada e metadados `A {nota} · B {nota}`.
- Ao selecionar um item, fechar o painel e renderizar aquele resultado abaixo do formulário.
- Incluir estados: carregando, vazio e erro.

---

## 6. Estados e mensagens

| Estado | Gatilho | Apresentação |
| --- | --- | --- |
| Inicial | Primeiro acesso | Formulário preenchível; resultado oculto. |
| Carregando | POST em andamento | Botão desabilitado e bloco de loading. |
| Sucesso | POST `201` | Resultado atualizado abaixo do formulário. |
| Erro de validação | API retorna `422` | Mensagem no formulário, próxima às ações. |
| Erro de conexão | Falha de rede/API | Mensagem clara, sem apagar o conteúdo digitado. |
| Histórico vazio | GET retorna lista vazia | Texto informativo no painel. |

Mensagens de erro não devem expor detalhes internos, chaves ou URLs sensíveis.

---

## 7. Responsividade

| Largura | Comportamento |
| --- | --- |
| `> 650px` | Respostas e score cards em duas colunas. |
| `≤ 650px` | Respostas e score cards em uma coluna; separador VS entre os cards. |
| Todas | Topbar, formulário e painel devem permanecer operáveis sem rolagem horizontal. |

---

## 8. Acessibilidade

- Contraste de texto normal deve atender ao mínimo WCAG AA.
- Todos os campos possuem `label` associado.
- Mensagens de erro e resultado dinâmico usam região `aria-live`.
- Botões têm nomes acessíveis, inclusive o botão de fechar o histórico.
- O painel de histórico usa `role="dialog"` e `aria-modal="true"`.
- Estados de foco devem ser visíveis e não depender somente de mudança de cor.
- O loading é anunciado por texto, não apenas por animação.

---

## 9. Critérios de aceite de UI

- [ ] Uma pessoa consegue identificar qual campo pertence à resposta A e à B sem ler o placeholder.
- [ ] Durante a avaliação, há feedback visível abaixo do formulário e não é possível submeter novamente.
- [ ] Ao concluir, notas, respostas e justificativa aparecem sem remover o conteúdo digitado.
- [ ] A pessoa pode limpar os campos explicitamente ou enviar outra comparação sobre o resultado existente.
- [ ] O histórico pode ser aberto, exibe os estados vazios/carregando e permite revisitar uma avaliação.
- [ ] A interface funciona em 320px de largura sem rolagem horizontal.
- [ ] A navegação por teclado alcança todos os controles relevantes e mostra foco visível.

---

## 10. Evolução de novas páginas

Ao implementar uma nova página, criar uma subseção ou spec própria contendo:

1. objetivo e tarefa principal da pessoa usuária;
2. composição a partir dos componentes definidos nesta spec;
3. estados assíncronos e mensagens esperadas;
4. breakpoint ou exceção responsiva, se existir;
5. critério de aceite visual e acessível.

Alterações nos tokens ou componentes compartilhados devem ser feitas primeiro nesta especificação e, depois, refletidas na implementação.
