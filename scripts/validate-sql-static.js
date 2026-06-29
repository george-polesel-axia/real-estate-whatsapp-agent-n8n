import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const dir = new URL('../supabase/migrations/', import.meta.url);
const files = readdirSync(dir).filter((file) => file.endsWith('.sql')).sort();
const all = files.map((file) => readFileSync(join(dir.pathname, file), 'utf8')).join('\n').toLowerCase();

const required = [
  'create extension if not exists vector',
  'create extension if not exists pg_trgm',
  'create table if not exists real_estate_agencies',
  'create table if not exists brokers',
  'create table if not exists clients',
  'create table if not exists properties',
  'create table if not exists property_media',
  'create table if not exists property_features',
  'create table if not exists property_embeddings',
  'create table if not exists client_conversations',
  'create table if not exists conversation_messages',
  'create table if not exists appointments',
  'create table if not exists agent_handoffs',
  'create table if not exists agent_events',
  'create table if not exists agent_failures',
  'create table if not exists agent_settings',
  'enable row level security',
  'create or replace function match_properties',
  'create or replace function search_properties_hybrid',
  'using hnsw'
];

const forbidden = ['drop table', 'truncate ', 'delete from ', 'alter table disable row level security'];
const errors = [];

for (const phrase of required) {
  if (!all.includes(phrase)) errors.push(`Missing required SQL phrase: ${phrase}`);
}

for (const phrase of forbidden) {
  if (all.includes(phrase)) errors.push(`Forbidden SQL phrase found: ${phrase}`);
}

if (errors.length) {
  console.error(errors.join('\n'));
  process.exit(1);
}

console.log(`Static SQL validation passed for ${files.length} migration files.`);
