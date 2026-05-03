# Motor de Busca em Documentos

Aplicação web para pesquisa de palavras e trechos em documentos de texto, com quatro algoritmos de substring search implementados via Strategy Pattern e observabilidade completa com OpenTelemetry.

---

## Funcionalidades

- Upload de documentos `.txt`
- Seleção do algoritmo em tempo de execução via dropdown
- Quatro algoritmos implementados: Força Bruta, KMP, Rabin-Karp e Boyer-Moore
- Resultados: encontrado, ocorrências, posições, tempo (ms), N e M
- Telemetria com OpenTelemetry (traces, métricas e logs)
- Dashboard Grafana com comparação visual entre algoritmos

---

## Estrutura do Projeto

```
motor-de-busca/
├── app/
│   ├── main.py               # FastAPI — endpoints e orquestração
│   ├── telemetry.py          # Setup OpenTelemetry (traces, métricas, logs)
│   ├── algorithms/
│   │   ├── base.py           # Interface SearchStrategy + SearchResult
│   │   ├── bruteforce.py     # Força Bruta O(N·M)
│   │   ├── kmp.py            # KMP O(N+M)
│   │   ├── rabinkarp.py      # Rabin-Karp O(N+M) esperado
│   │   └── boyermoore.py     # Boyer-Moore O(N/M) melhor caso
│   └── requirements.txt
├── frontend/
│   └── index.html            # Interface web (single page)
├── otel/
│   ├── otel-collector-config.yaml
│   └── tempo.yaml
├── grafana/
│   └── provisioning/
│       ├── datasources/datasources.yaml
│       └── dashboards/
│           ├── dashboards.yaml
│           └── search-dashboard.json
├── prometheus/
│   └── prometheus.yml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/) instalados

---

## Como Executar

### 1. Subir todos os serviços

```bash
docker compose up --build
```

Aguarde todos os serviços iniciarem (cerca de 30–60 s na primeira vez).

### 2. Acessar a aplicação

| Serviço      | URL                         |
|--------------|-----------------------------|
| Aplicação    | http://localhost:8000       |
| Grafana      | http://localhost:3000       |
| Prometheus   | http://localhost:9090       |

Credenciais Grafana: **admin / admin**

O dashboard é provisionado automaticamente em **Motor de Busca → Motor de Busca — Observabilidade**.

### 3. Derrubar os serviços

```bash
docker compose down
```

Para remover volumes (dados persistidos):

```bash
docker compose down -v
```

---

## Como Usar

1. Acesse http://localhost:8000
2. Clique em **selecionar arquivo** ou arraste um `.txt` para a área de upload
3. Escolha o algoritmo no dropdown (ou nos pills de seleção rápida)
4. Digite o termo ou trecho a pesquisar
5. Clique em **Pesquisar** (ou pressione Enter)
6. O painel de resultados exibe: encontrado, tempo em ms, ocorrências, posições, N e M

---

## Algoritmos

Todos implementados sem uso de `indexOf()`, `contains()` ou similares.

| Algoritmo     | Complexidade (pior caso) | Estratégia principal                        |
|---------------|--------------------------|---------------------------------------------|
| Força Bruta   | O(N·M)                   | Comparação caractere a caractere            |
| KMP           | O(N+M) garantido         | Tabela de falhas para evitar retrocesso     |
| Rabin-Karp    | O(N+M) esperado          | Hash rolante com verificação por igualdade  |
| Boyer-Moore   | O(N/M) melhor caso       | Heurística bad-character, direita para esquerda |

### Strategy Pattern

```
SearchStrategy (ABC)
    └── execute(text, pattern) → SearchResult
          ├── BruteForce.search()
          ├── KMP.search()
          ├── RabinKarp.search()
          └── BoyerMoore.search()
```

A troca de algoritmo ocorre em runtime via dicionário keyed pelo valor do dropdown — sem if/else, conforme o padrão.

---

## Observabilidade

### Traces (Tempo)

Cada requisição `/search` gera um trace com três spans:

1. `load_document` — leitura e decodificação do arquivo
2. `execute_algorithm` — execução do algoritmo selecionado
3. `format_response` — serialização do resultado

Acesse traces em: **Grafana → Explore → Tempo**

### Métricas (Prometheus)

| Métrica                               | Tipo      | Labels                    |
|---------------------------------------|-----------|---------------------------|
| `motorbusca_search_duration_ms`       | Histogram | algorithm, found          |
| `motorbusca_search_requests_total`    | Counter   | algorithm, found          |
| `motorbusca_document_size_chars`      | Histogram | algorithm                 |

### Logs

Cada busca gera dois logs estruturados via OpenTelemetry:

- **Início:** algoritmo utilizado, N (tamanho do texto), M (tamanho do padrão)
- **Fim:** tempo de execução em ms e número de ocorrências

---

## Documentos de Teste (obrigatórios)

| Documento                    | Onde obter                                                          |
|------------------------------|---------------------------------------------------------------------|
| Bíblia                       | https://www.gutenberg.org/ebooks/10 (Plain Text UTF-8)             |
| Os Lusíadas — Camões         | https://www.gutenberg.org/ebooks/3333                              |
| A Catedral e o Bazar         | https://catb.org/~esr/writings/cathedral-bazaar/ (salvar como txt) |
| Obra escolhida pelo grupo    | Qualquer domínio público — sugestão: https://www.gutenberg.org     |

---

## Uso de IA

Consulte o arquivo `USO_DE_IA.md` para prompts utilizados, aprendizados e correções realizadas durante o desenvolvimento.
