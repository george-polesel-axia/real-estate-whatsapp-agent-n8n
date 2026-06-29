alter table real_estate_agencies enable row level security;
alter table brokers enable row level security;
alter table clients enable row level security;
alter table properties enable row level security;
alter table property_media enable row level security;
alter table property_features enable row level security;
alter table property_embeddings enable row level security;
alter table client_conversations enable row level security;
alter table conversation_messages enable row level security;
alter table appointments enable row level security;
alter table agent_handoffs enable row level security;
alter table agent_events enable row level security;
alter table agent_failures enable row level security;
alter table agent_settings enable row level security;

grant usage on schema public to anon, authenticated, service_role;
grant select, insert, update on all tables in schema public to service_role;
grant usage, select on all sequences in schema public to service_role;

create policy "service_role_all_real_estate_agencies" on real_estate_agencies for all to service_role using (true) with check (true);
create policy "service_role_all_brokers" on brokers for all to service_role using (true) with check (true);
create policy "service_role_all_clients" on clients for all to service_role using (true) with check (true);
create policy "service_role_all_properties" on properties for all to service_role using (true) with check (true);
create policy "service_role_all_property_media" on property_media for all to service_role using (true) with check (true);
create policy "service_role_all_property_features" on property_features for all to service_role using (true) with check (true);
create policy "service_role_all_property_embeddings" on property_embeddings for all to service_role using (true) with check (true);
create policy "service_role_all_client_conversations" on client_conversations for all to service_role using (true) with check (true);
create policy "service_role_all_conversation_messages" on conversation_messages for all to service_role using (true) with check (true);
create policy "service_role_all_appointments" on appointments for all to service_role using (true) with check (true);
create policy "service_role_all_agent_handoffs" on agent_handoffs for all to service_role using (true) with check (true);
create policy "service_role_all_agent_events" on agent_events for all to service_role using (true) with check (true);
create policy "service_role_all_agent_failures" on agent_failures for all to service_role using (true) with check (true);
create policy "service_role_all_agent_settings" on agent_settings for all to service_role using (true) with check (true);

create policy "authenticated_select_agencies_by_app_metadata" on real_estate_agencies for select to authenticated
using (id::text = ((select auth.jwt()) -> 'app_metadata' ->> 'agency_id'));

create policy "authenticated_select_properties_by_agency" on properties for select to authenticated
using (agency_id::text = ((select auth.jwt()) -> 'app_metadata' ->> 'agency_id'));

create policy "authenticated_select_property_media_by_agency" on property_media for select to authenticated
using (
  exists (
    select 1 from properties p
    where p.id = property_media.property_id
      and p.agency_id::text = ((select auth.jwt()) -> 'app_metadata' ->> 'agency_id')
  )
);

create policy "authenticated_select_brokers_by_agency" on brokers for select to authenticated
using (agency_id::text = ((select auth.jwt()) -> 'app_metadata' ->> 'agency_id'));
