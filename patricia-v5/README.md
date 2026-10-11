# Patrícia v5 — estado de conversa e avisos de venda

Este diretório versiona os componentes de estado e encaminhamento de avisos de venda já publicados no servidor. O projeto na raiz mantém sua implementação inicial; estes arquivos não constituem uma distribuição completa da v5.

Quando um cliente relata que um imóvel foi vendido, o estado registra um aviso persistente. O worker encaminha o relato ao administrador verificado da mesma empresa, confirma o recibo do provedor e preserva a confirmação em replays. Um aviso de venda não altera automaticamente o status de um anúncio.

## Componentes

- `backend/behavior_state.py`: estado por empresa/cliente, aviso idempotente e preservação da confirmação em replays.
- `backend/sold_notice_worker.py`: polling paginado, validação de empresa/cliente/identidade, bloqueio de QA no envio automático e ausência de retry cego após resultado incerto.
- `tests/test_sold_notice_worker.py`: isolamento, colisão de identidade, duplicação, QA e recibos inválidos.

## Integração no gateway existente

A integração publicada utiliza os adaptadores existentes de contato verificado e envio com journal persistente:

```python
from sold_notice_worker import SoldNoticeWorker
from visit_owner_contact import resolve_owner_contact
from completion_progress import send as send_owner_notice

# Após inicializar BEHAVIOR e iniciar a fila de conversas:
SoldNoticeWorker(BEHAVIOR, resolve_owner_contact, send_owner_notice).start()
```

O worker não recebe números de telefone do pedido. O adaptador resolve o administrador verificado no banco e mantém idempotência do envio. Os adaptadores de Supabase, contatos e transporte pertencem à instalação existente e não foram incluídos neste snapshot.

## Validação

```bash
python3 -m unittest discover -s patricia-v5/tests -p test_sold_notice_worker.py
```

Foram aprovados 10 testes em três ciclos. No servidor, 32 arquivos de testes passaram. Um único aviso de QA ao administrador foi aceito pelo WhatsApp; três replays diretos e três pelo gateway preservaram o recibo sem duplicação. Este teste não representa uma venda real.

## Integração de rotas

Na verificação de 11/10/2026, Geocoding respondeu corretamente em três execuções. Directions legada retornou REQUEST_DENIED. O teste da Routes API foi bloqueado pelo domínio permitido na credencial n8n antes de alcançar o Google; sua habilitação no Google Cloud não pôde ser confirmada.

A candidata de migração permanece fora da produção até obter resultados reais corretos. Endereços com números fictícios pertencem somente aos conjuntos explicitamente identificados de QA. Não há credenciais, payloads de clientes ou dados do catálogo neste diretório.
