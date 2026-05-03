# Uso de IA no Desenvolvimento

## Prompts principais utilizados

### 1. Interface web

**Prompt:**
> "Leia este documento de enunciado e faça a interface web do motor de busca em HTML puro. Inclua upload de arquivo, dropdown com os 4 algoritmos, campo de busca, botão pesquisar e área de resultados mostrando: encontrado, tempo em ms, ocorrências, posições, N e M."

**O que produziu:** A estrutura HTML completa com CSS e os 4 algoritmos implementados em JavaScript, funcionando em modo offline (sem backend).

**O que foi ajustado manualmente:** Adicionada lógica de fallback para quando o backend está indisponível; corrigido o comportamento do FormData para envio do arquivo ao backend.

**Onde foi genérico:** O tratamento de erros HTTP inicial era superficial — foi necessário especificar o comportamento de fallback.

---

### 2. Backend com Strategy Pattern e OpenTelemetry

**Prompt:**
> "Implemente o backend em Python com FastAPI. Use o Strategy Pattern com uma classe base SearchStrategy e SearchResult. Implemente os 4 algoritmos sem usar indexOf ou contains. Instrumente com OpenTelemetry: um trace por requisição com spans para load_document, execute_algorithm e format_response; métricas search_duration_ms (histogram), search_requests_total (counter) e document_size_chars (histogram); logs no início e fim de cada busca."

**O que produziu:** `main.py`, `telemetry.py` e todos os arquivos de algoritmo com a estrutura Strategy correta.

**O que foi ajustado manualmente:** Os nomes das métricas foram padronizados com o prefixo `motorbusca_` para corresponder às queries do Prometheus no dashboard Grafana.

**Onde errou:** A versão inicial exportava os spans para stdout em vez do OTEL Collector — foi corrigido passando `insecure=True` e o endpoint correto.

---

### 3. Infraestrutura de observabilidade

**Prompt:**
> "Gere o docker-compose com: app FastAPI, OTEL Collector, Prometheus, Grafana e Tempo. Inclua os arquivos de configuração de cada serviço e um dashboard Grafana provisionado automaticamente com: tempo médio por algoritmo, total de buscas por algoritmo e comparação visual."

**O que produziu:** `docker-compose.yml`, `otel-collector-config.yaml`, `tempo.yaml`, `prometheus.yml` e o JSON do dashboard com 10 painéis.

**O que foi ajustado manualmente:** O mapeamento de porta do Tempo no docker-compose (evitar colisão com o OTEL Collector na porta 4317); adicionado `stream_over_http_enabled: true` no `tempo.yaml`.

**Onde foi genérico:** As queries PromQL do dashboard precisaram de ajuste fino no prefixo de namespace (`motorbusca_`) e no sufixo `_total` gerado automaticamente pelo SDK.
