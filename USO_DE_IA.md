# Uso de IA no Desenvolvimento

A IA foi utilizada como apoio pontual ao longo do desenvolvimento, principalmente para tirar dúvidas conceituais, validar trechos de código e acelerar partes de configuração menos relacionadas ao conteúdo da disciplina.

---

## Prompts utilizados

### Dúvidas conceituais

**Prompt:**
> "Qual a diferença prática entre KMP e Boyer-Moore para textos em português? Em quais cenários um supera o outro?"

Usado para embasar a escolha de implementação e a análise comparativa do relatório. A resposta ajudou a entender por que Boyer-Moore tende a ser sublinear em alfabetos grandes (como o português com acentuação), mas KMP garante O(N+M) independente do padrão.

---

### Strategy Pattern

**Prompt:**
> "Como implementar o Strategy Pattern em Python usando ABC? Quero uma interface onde cada algoritmo seja uma classe separada com um método search()."

A IA gerou um esboço da classe base. A integração com o dataclass `SearchResult` e o método `execute()` que mede tempo foi escrita manualmente, assim como o registro dos algoritmos no dicionário do endpoint.

---

### FastAPI e upload de arquivo

**Prompt:**
> "Como receber um arquivo `.txt` via multipart/form-data no FastAPI junto com outros campos de formulário?"

Usado para resolver a integração do `UploadFile` com os parâmetros `algorithm` e `pattern` no mesmo endpoint. A IA mostrou o uso correto de `File(...)` e `Form(...)`.

---

### OpenTelemetry

**Prompt:**
> "Como criar um histogram e um counter com o SDK OpenTelemetry Python e exportar via OTLP gRPC?"

A IA mostrou a estrutura básica do `MeterProvider` e `TracerProvider`. A configuração do `BatchSpanProcessor`, os nomes das métricas com prefixo `motorbusca_` e a integração com o endpoint do Collector foram ajustados manualmente após testes.

---

**Prompt:**
> "Como adicionar spans filhos dentro de um span pai no OpenTelemetry Python, usando context manager?"

Usado para estruturar os três spans (`load_document`, `execute_algorithm`, `format_response`) dentro do span pai `search_request`. O aninhamento com `with tracer.start_as_current_span(...)` funcionou conforme esperado sem ajustes.

---

### Docker e infraestrutura

**Prompt:**
> "Qual a configuração mínima do OpenTelemetry Collector para receber OTLP gRPC, exportar métricas para Prometheus e traces para Tempo?"

A IA gerou o esqueleto do `otel-collector-config.yaml`. Foi necessário ajustar o namespace do exportador Prometheus (`motorbusca`) e resolver um conflito de porta entre o Collector e o Tempo (ambos queriam a 4317 no host), mapeando o Tempo para 14317.

---

**Prompt:**
> "Como provisionar automaticamente um datasource Prometheus e um datasource Tempo no Grafana via arquivo YAML?"

Usado para não configurar manualmente o Grafana a cada `docker compose up`. A IA gerou o arquivo base; o `tracesToMetrics` linkando Tempo ao Prometheus foi adicionado depois consultando a documentação do Grafana.

---

**Prompt:**
> "Como escrever uma query PromQL para calcular a média de um histogram (sum/count) agrupada por label?"

Usado para corrigir os painéis do dashboard que estavam sem dados. A versão com `rate()` não funcionava com poucas amostras; a IA sugeriu usar `sum(_sum) / sum(_count)` para média acumulada, que resolveu o problema.

---

### Interface web

**Prompt:**
> "Como enviar um arquivo junto com campos de texto via `fetch` usando `FormData` em JavaScript?"

Usado para conectar o frontend ao endpoint `/search` do backend. A lógica de fallback (rodar o algoritmo localmente em JS quando o backend não responde) foi ideia e implementação próprias.

---

**Prompt:**
> "Como fazer drag and drop de arquivo em HTML puro sem biblioteca?"

A IA mostrou o uso de `dragover`, `dragleave` e `drop` com `e.preventDefault()`. O visual do estado de hover e o badge com o nome do arquivo foram implementados manualmente no CSS.
