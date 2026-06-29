insert into real_estate_agencies (id, name, whatsapp_phone, email)
values ('00000000-0000-0000-0000-000000000001', 'Imobiliaria Exemplo', '+5511999999999', 'contato@imobiliariaexemplo.com.br')
on conflict (id) do nothing;

insert into brokers (id, agency_id, name, phone, email, google_calendar_id, active)
values ('00000000-0000-0000-0000-000000000011', '00000000-0000-0000-0000-000000000001', 'Carla Souza', '+5511988887777', 'carla@imobiliariaexemplo.com.br', 'primary', true)
on conflict (id) do nothing;

insert into properties (
  id, agency_id, external_ref, title, property_type, listing_type, status, neighborhood, street, city, state,
  bedrooms, suites, bathrooms, parking_spaces, price, useful_area, short_description, full_description,
  visual_description, nearby_references, features
) values
(
  '00000000-0000-0000-0000-000000000101', '00000000-0000-0000-0000-000000000001', 'AI-001',
  'Sobrado na Rua Bento Vieira com portao azul', 'sobrado', 'venda', 'active', 'Alto do Ipiranga', 'Rua Bento Vieira', 'Sao Paulo', 'SP',
  3, 1, 3, 2, 980000, 145,
  'Sobrado de 3 dormitorios com 2 vagas e portao azul no Alto do Ipiranga.',
  'Sobrado bem distribuido, com sala ampla, 3 dormitorios, 1 suite, garagem para 2 carros e area externa funcional.',
  'Fachada com portao azul, garagem para dois carros e entrada lateral.',
  array['metro', 'padaria', 'mercado'],
  '{"portao":"azul","garagem":"2 carros","churrasqueira":true}'::jsonb
),
(
  '00000000-0000-0000-0000-000000000102', '00000000-0000-0000-0000-000000000001', 'AI-002',
  'Sobrado na Ricardo Jafet', 'sobrado', 'venda', 'active', 'Alto do Ipiranga', 'Avenida Ricardo Jafet', 'Sao Paulo', 'SP',
  3, 1, 2, 1, 890000, 130,
  'Sobrado de 3 dormitorios proximo a Ricardo Jafet.',
  'Opcao com boa localizacao, 3 dormitorios e facil acesso a servicos.',
  'Fachada neutra com garagem coberta para um carro.',
  array['avenida principal', 'mercado'],
  '{"garagem":"1 carro"}'::jsonb
),
(
  '00000000-0000-0000-0000-000000000103', '00000000-0000-0000-0000-000000000001', 'AI-003',
  'Sobrado na Arcipreste Andrade', 'sobrado', 'venda', 'active', 'Alto do Ipiranga', 'Rua Arcipreste Andrade', 'Sao Paulo', 'SP',
  3, 0, 2, 2, 930000, 138,
  'Sobrado de 3 dormitorios e 2 vagas em rua tranquila.',
  'Casa sobrado em rua residencial, com 3 dormitorios e duas vagas.',
  'Fachada clara, garagem frontal e pequeno jardim.',
  array['escola', 'padaria'],
  '{"jardim":true}'::jsonb
),
(
  '00000000-0000-0000-0000-000000000104', '00000000-0000-0000-0000-000000000001', 'RB-001',
  'Casa na Rua Rui Barbosa perto da padaria', 'casa', 'venda', 'active', 'Centro', 'Rua Rui Barbosa', 'Sao Paulo', 'SP',
  3, 1, 2, 1, 720000, 115,
  'Casa de 3 dormitorios na Rua Rui Barbosa, perto da padaria.',
  'Casa terrea com 3 dormitorios, boa iluminacao e localizacao proxima a padaria do bairro.',
  'Fachada terrea simples, calcada larga e comercio proximo.',
  array['padaria', 'mercado'],
  '{"referencia":"padaria"}'::jsonb
)
on conflict (id) do nothing;

insert into property_media (property_id, media_type, url, caption, visual_tags, visual_description, sort_order)
values
('00000000-0000-0000-0000-000000000101', 'image', 'https://example.com/imoveis/ai-001-fachada.jpg', 'Fachada com portao azul', array['portao azul', 'garagem 2 carros'], 'Fachada com portao azul e garagem para dois carros.', 1),
('00000000-0000-0000-0000-000000000104', 'image', 'https://example.com/imoveis/rb-001-fachada.jpg', 'Casa perto da padaria', array['padaria', 'casa terrea'], 'Casa terrea na Rua Rui Barbosa proxima a padaria.', 1);
