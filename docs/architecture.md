# Arquitetura

## Componentes

- n8n: orquestra webhooks, normalizacao, IA, persistencia, WhatsApp, calendario e e-mail.
- Supabase Postgres: dados estruturados de clientes, imoveis, conversas, agendamentos e auditoria.
- pgvector: embeddings de imoveis, descricoes e pistas visuais.
- WhatsApp provider: Cloud API, WAHA ou Evolution API.
- OpenAI/modelo configuravel: extracao de intencao, embeddings, transcricao e resposta.
- Google Calendar: consulta agenda de corretores e cria eventos.
- SMTP/Gmail: confirmacao para cliente e notificacao para corretor.
- GitHub: versiona workflows, migrations, docs e scripts.

## Fluxo completo

1. Cliente envia mensagem no WhatsApp.
2. Provedor chama o webhook do n8n.
3. O workflow principal normaliza o payload para um contrato interno.
4. O tipo de mensagem define o processamento: texto direto, audio/video para transcricao, imagem/video para descricao visual quando disponivel.
5. Cliente e conversa sao criados ou atualizados no Supabase.
6. A mensagem recebida e persistida.
7. O node de IA extrai intencao e atributos imobiliarios.
8. O texto normalizado gera embedding.
9. A RPC `search_properties_hybrid` combina filtros SQL, texto, atributos, descricao visual e similaridade vetorial.
10. O agente decide entre pedir pista, desambiguar ate 3 opcoes, apresentar imovel, agendar visita ou acionar corretor.
11. Resposta e enviada pelo provedor WhatsApp.
12. Eventos e falhas sao auditados.

## Segurança

Secrets ficam apenas em credenciais do n8n, variaveis de ambiente ou cofres. O repositorio contem apenas placeholders. RLS e habilitado em todas as tabelas publicas. O uso de `service_role` deve ficar restrito a automacoes servidor-servidor e nao deve ser exposto ao cliente.
