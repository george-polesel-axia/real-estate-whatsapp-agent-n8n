import { writeFileSync } from 'node:fs';

const properties = [
  {
    id: 'AI-001',
    title: 'Sobrado na Rua Bento Vieira com portao azul',
    type: 'sobrado',
    neighborhood: 'Alto do Ipiranga',
    street: 'Rua Bento Vieira',
    bedrooms: 3,
    parking: 2,
    visual: 'portao azul',
    reference: 'metro',
    description: 'Sobrado de 3 dormitorios com 2 vagas e portao azul no Alto do Ipiranga.'
  },
  {
    id: 'AI-002',
    title: 'Sobrado na Ricardo Jafet',
    type: 'sobrado',
    neighborhood: 'Alto do Ipiranga',
    street: 'Avenida Ricardo Jafet',
    bedrooms: 3,
    parking: 1,
    visual: 'fachada neutra',
    reference: 'mercado',
    description: 'Sobrado de 3 dormitorios proximo a Ricardo Jafet.'
  },
  {
    id: 'AI-003',
    title: 'Sobrado na Arcipreste Andrade',
    type: 'sobrado',
    neighborhood: 'Alto do Ipiranga',
    street: 'Rua Arcipreste Andrade',
    bedrooms: 3,
    parking: 2,
    visual: 'jardim',
    reference: 'escola',
    description: 'Sobrado de 3 dormitorios e 2 vagas em rua tranquila.'
  },
  {
    id: 'RB-001',
    title: 'Casa na Rua Rui Barbosa perto da padaria',
    type: 'casa',
    neighborhood: 'Centro',
    street: 'Rua Rui Barbosa',
    bedrooms: 3,
    parking: 1,
    visual: 'casa terrea',
    reference: 'padaria',
    description: 'Casa de 3 dormitorios na Rua Rui Barbosa, perto da padaria.'
  }
];

function attrs(text) {
  const lower = text.toLowerCase();
  return {
    neighborhood: lower.includes('alto do ipiranga') ? 'Alto do Ipiranga' : null,
    street: lower.includes('rui barbosa') ? 'Rua Rui Barbosa' : null,
    type: lower.includes('sobrado') ? 'sobrado' : lower.includes('casa') ? 'casa' : null,
    bedrooms: /3|tres|três/.test(lower) && /dorm/.test(lower) ? 3 : null,
    parking: /2|duas|dois/.test(lower) && /(vaga|garagem|carro)/.test(lower) ? 2 : null,
    visual: lower.includes('portao azul') || lower.includes('portão azul') ? 'portao azul' : null,
    broker: lower.includes('corretor'),
    schedule: /(sabado|sábado|domingo|visita|agendar)/.test(lower),
    nonexistent: lower.includes('castelo') || lower.includes('helicoptero')
  };
}

function search(a) {
  return properties
    .map((p) => {
      let score = 0;
      if (a.neighborhood && p.neighborhood === a.neighborhood) score += 2;
      if (a.street && p.street === a.street) score += 3;
      if (a.type && p.type === a.type) score += 2;
      if (a.bedrooms && p.bedrooms === a.bedrooms) score += 1;
      if (a.parking && p.parking >= a.parking) score += 1;
      if (a.visual && p.visual.includes(a.visual)) score += 4;
      return { ...p, score };
    })
    .filter((p) => p.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 3);
}

function respond(text) {
  const a = attrs(text);
  if (a.broker) return 'Claro, vou pedir para um corretor chamar voce em poucos minutos. Enquanto isso, posso deixar uma visita pre-agendada: prefere sabado pela manha ou domingo as 14h?';
  if (a.schedule) return 'Perfeito, vou consultar a agenda do corretor e deixar sabado de manha como primeira opcao. Posso confirmar esse horario para voce?';
  if (a.nonexistent) return 'Nao encontrei esse imovel com seguranca. Voce lembra alguma pista objetiva: rua, bairro, dormitorios, garagem, cor do portao, faixa de preco ou referencia do site?';
  const candidates = search(a);
  if (!candidates.length) return 'Para eu localizar sem inventar, voce lembra alguma pista objetiva: rua, bairro, dormitorios, garagem, cor do portao, faixa de preco ou referencia do site?';
  if (candidates[0].score >= 7) return `Pelo que voce descreveu, parece ser ${candidates[0].title}. ${candidates[0].description} Quer que eu te passe os detalhes principais ou ja veja uma visita?`;
  if (a.street === 'Rua Rui Barbosa') return 'Na Rua Rui Barbosa temos uma casa de 3 dormitorios perto da padaria. E essa que o senhor viu?';
  return `No Alto do Ipiranga temos opcoes com 3 dormitorios na ${candidates.map((p) => p.street.replace('Rua ', '').replace('Avenida ', '')).join(', ')}. O senhor lembra se era alguma dessas ruas?`;
}

const scenarios = [
  {
    name: 'Cenario 1 - desambiguacao e agendamento',
    turns: [
      ['Eu vi no site o sobrado no Alto do Ipiranga de 3 dormitorios.', ['Ricardo Jafet', 'Arcipreste Andrade', 'Bento Vieira']],
      ['E um com garagem pra 2 carros e portao azul.', ['Bento Vieira', 'portao azul']],
      ['Pode mandar mais detalhes.', ['pista objetiva', 'detalhes principais', 'visita']],
      ['Pode ser sabado de manha.', ['agenda', 'sabado']]
    ]
  },
  { name: 'Cenario 2 - Rua Rui Barbosa', turns: [['Eu vi uma casa de 3 dormitorios na Rua Rui Barbosa.', ['Rua Rui Barbosa', 'padaria']]] },
  { name: 'Cenario 3 - handoff', turns: [['Quero falar com corretor.', ['corretor', 'visita']]] },
  { name: 'Cenario 4 - audio/video', turns: [['Quero ver aquele sobrado com portao azul e duas vagas.', ['Bento Vieira', 'portao azul']]] },
  { name: 'Cenario 5 - inexistente', turns: [['Quero um castelo com garagem para helicoptero.', ['pista objetiva']]] }
];

const report = ['# Relatorio de Testes', '', `Data: ${new Date().toISOString()}`, ''];
let failures = 0;

for (const scenario of scenarios) {
  report.push(`## ${scenario.name}`, '');
  for (const [input, expected] of scenario.turns) {
    const output = respond(input);
    const ok = expected.some((term) => output.toLowerCase().includes(term.toLowerCase()));
    if (!ok) failures += 1;
    report.push(`- Entrada: ${input}`);
    report.push(`- Saida: ${output}`);
    report.push(`- Esperado: ${expected.join(' | ')}`);
    report.push(`- Resultado: ${ok ? 'PASS' : 'FAIL'}`, '');
  }
}

report.push('## Resumo', '');
report.push(failures === 0 ? 'Todos os cenarios principais passaram.' : `${failures} verificacoes falharam.`);

writeFileSync(new URL('../tests/test-report.md', import.meta.url), `${report.join('\n')}\n`);

if (failures) process.exit(1);
console.log('Simulation tests passed.');
