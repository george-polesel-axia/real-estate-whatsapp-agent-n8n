# Handoff para Corretor

O handoff e acionado quando:

- cliente pede corretor;
- agente nao consegue resolver com seguranca;
- cliente demonstra urgencia humana;
- falha tecnica impede atendimento automatizado.

Fluxo:

1. Selecionar corretor ativo da agencia, preferencialmente vinculado ao imovel.
2. Registrar `agent_handoffs`.
3. Enviar resumo da conversa e dados do cliente ao corretor.
4. Avisar cliente que o corretor chamara em poucos minutos.
5. Oferecer visita pre-agendada mesmo durante o handoff.

Se o provedor WhatsApp suportar transferencia, o workflow pode executar a transferencia. Caso contrario, usa notificacao externa.
