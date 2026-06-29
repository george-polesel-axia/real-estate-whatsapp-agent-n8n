create table if not exists real_estate_agencies (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  whatsapp_phone text,
  email text,
  created_at timestamptz not null default now()
);

create table if not exists brokers (
  id uuid primary key default gen_random_uuid(),
  agency_id uuid not null references real_estate_agencies(id),
  name text not null,
  phone text,
  email text,
  google_calendar_id text,
  active boolean not null default true,
  created_at timestamptz not null default now()
);

create table if not exists clients (
  id uuid primary key default gen_random_uuid(),
  agency_id uuid not null references real_estate_agencies(id),
  name text,
  phone text not null unique,
  email text,
  lead_status text not null default 'new',
  preferences jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists properties (
  id uuid primary key default gen_random_uuid(),
  agency_id uuid not null references real_estate_agencies(id),
  external_ref text,
  title text not null,
  property_type text not null,
  listing_type text not null,
  status text not null default 'active',
  neighborhood text,
  street text,
  number text,
  city text,
  state text,
  bedrooms int,
  suites int,
  bathrooms int,
  parking_spaces int,
  price numeric,
  condo_fee numeric,
  iptu numeric,
  useful_area numeric,
  total_area numeric,
  short_description text,
  full_description text,
  visual_description text,
  nearby_references text[] not null default '{}',
  features jsonb not null default '{}'::jsonb,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists property_media (
  id uuid primary key default gen_random_uuid(),
  property_id uuid not null references properties(id),
  media_type text not null,
  url text not null,
  caption text,
  visual_tags text[] not null default '{}',
  visual_description text,
  sort_order int not null default 0,
  created_at timestamptz not null default now()
);

create table if not exists property_features (
  id uuid primary key default gen_random_uuid(),
  property_id uuid not null references properties(id),
  feature_key text not null,
  feature_value text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists property_embeddings (
  id uuid primary key default gen_random_uuid(),
  property_id uuid not null references properties(id),
  content_type text not null,
  content text not null,
  embedding extensions.vector(1536),
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists client_conversations (
  id uuid primary key default gen_random_uuid(),
  agency_id uuid not null references real_estate_agencies(id),
  client_id uuid not null references clients(id),
  channel text not null default 'whatsapp',
  provider_conversation_id text,
  status text not null default 'open',
  current_intent text,
  selected_property_id uuid references properties(id),
  last_message_at timestamptz,
  created_at timestamptz not null default now()
);

create table if not exists conversation_messages (
  id uuid primary key default gen_random_uuid(),
  conversation_id uuid not null references client_conversations(id),
  sender_type text not null,
  message_type text not null,
  content text,
  media_url text,
  transcription text,
  parsed_intent jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists appointments (
  id uuid primary key default gen_random_uuid(),
  agency_id uuid not null references real_estate_agencies(id),
  broker_id uuid references brokers(id),
  client_id uuid not null references clients(id),
  property_id uuid references properties(id),
  conversation_id uuid references client_conversations(id),
  start_time timestamptz not null,
  end_time timestamptz not null,
  status text not null default 'pending',
  google_event_id text,
  confirmation_sent boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists agent_handoffs (
  id uuid primary key default gen_random_uuid(),
  agency_id uuid not null references real_estate_agencies(id),
  client_id uuid not null references clients(id),
  broker_id uuid references brokers(id),
  conversation_id uuid references client_conversations(id),
  reason text not null,
  status text not null default 'open',
  created_at timestamptz not null default now(),
  resolved_at timestamptz
);

create table if not exists agent_events (
  id uuid primary key default gen_random_uuid(),
  conversation_id uuid references client_conversations(id),
  event_type text not null,
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists agent_failures (
  id uuid primary key default gen_random_uuid(),
  conversation_id uuid references client_conversations(id),
  failure_type text not null,
  error_message text,
  payload jsonb not null default '{}'::jsonb,
  resolved boolean not null default false,
  created_at timestamptz not null default now()
);

create table if not exists agent_settings (
  id uuid primary key default gen_random_uuid(),
  agency_id uuid not null references real_estate_agencies(id),
  key text not null,
  value jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (agency_id, key)
);

create or replace function set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger set_clients_updated_at
before update on clients
for each row execute function set_updated_at();

create trigger set_properties_updated_at
before update on properties
for each row execute function set_updated_at();

create trigger set_appointments_updated_at
before update on appointments
for each row execute function set_updated_at();

create trigger set_agent_settings_updated_at
before update on agent_settings
for each row execute function set_updated_at();
