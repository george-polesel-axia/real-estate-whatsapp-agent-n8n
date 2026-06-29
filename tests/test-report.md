# Relatorio de Testes

Data: 2026-06-29T20:20:24.894Z

## Cenario 1 - desambiguacao e agendamento

- Entrada: Eu vi no site o sobrado no Alto do Ipiranga de 3 dormitorios.
- Saida: No Alto do Ipiranga temos opcoes com 3 dormitorios na Bento Vieira, Ricardo Jafet, Arcipreste Andrade. O senhor lembra se era alguma dessas ruas?
- Esperado: Ricardo Jafet | Arcipreste Andrade | Bento Vieira
- Resultado: PASS

- Entrada: E um com garagem pra 2 carros e portao azul.
- Saida: No Alto do Ipiranga temos opcoes com 3 dormitorios na Bento Vieira, Arcipreste Andrade. O senhor lembra se era alguma dessas ruas?
- Esperado: Bento Vieira | portao azul
- Resultado: PASS

- Entrada: Pode mandar mais detalhes.
- Saida: Para eu localizar sem inventar, voce lembra alguma pista objetiva: rua, bairro, dormitorios, garagem, cor do portao, faixa de preco ou referencia do site?
- Esperado: pista objetiva | detalhes principais | visita
- Resultado: PASS

- Entrada: Pode ser sabado de manha.
- Saida: Perfeito, vou consultar a agenda do corretor e deixar sabado de manha como primeira opcao. Posso confirmar esse horario para voce?
- Esperado: agenda | sabado
- Resultado: PASS

## Cenario 2 - Rua Rui Barbosa

- Entrada: Eu vi uma casa de 3 dormitorios na Rua Rui Barbosa.
- Saida: Na Rua Rui Barbosa temos uma casa de 3 dormitorios perto da padaria. E essa que o senhor viu?
- Esperado: Rua Rui Barbosa | padaria
- Resultado: PASS

## Cenario 3 - handoff

- Entrada: Quero falar com corretor.
- Saida: Claro, vou pedir para um corretor chamar voce em poucos minutos. Enquanto isso, posso deixar uma visita pre-agendada: prefere sabado pela manha ou domingo as 14h?
- Esperado: corretor | visita
- Resultado: PASS

## Cenario 4 - audio/video

- Entrada: Quero ver aquele sobrado com portao azul e duas vagas.
- Saida: Pelo que voce descreveu, parece ser Sobrado na Rua Bento Vieira com portao azul. Sobrado de 3 dormitorios com 2 vagas e portao azul no Alto do Ipiranga. Quer que eu te passe os detalhes principais ou ja veja uma visita?
- Esperado: Bento Vieira | portao azul
- Resultado: PASS

## Cenario 5 - inexistente

- Entrada: Quero um castelo com garagem para helicoptero.
- Saida: Nao encontrei esse imovel com seguranca. Voce lembra alguma pista objetiva: rua, bairro, dormitorios, garagem, cor do portao, faixa de preco ou referencia do site?
- Esperado: pista objetiva
- Resultado: PASS

## Resumo

Todos os cenarios principais passaram.
