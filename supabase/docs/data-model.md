# Modelo de Dados

O modelo separa agencias, corretores, clientes, imoveis, conversas, mensagens, agendamentos e auditoria.

`properties` guarda dados estruturados do imovel. `property_media` guarda URLs e descricoes visuais. `property_embeddings` permite busca semantica por conteudo textual e visual.

`client_conversations` representa uma conversa por cliente/canal. `conversation_messages` armazena entradas e saidas, incluindo transcricoes e intencao extraida.

`appointments`, `agent_handoffs`, `agent_events` e `agent_failures` sustentam operacao, auditoria e melhoria continua.
