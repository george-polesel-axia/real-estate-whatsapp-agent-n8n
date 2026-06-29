create index if not exists idx_brokers_agency_active on brokers (agency_id, active);
create index if not exists idx_clients_phone on clients (phone);
create index if not exists idx_clients_agency on clients (agency_id);

create index if not exists idx_properties_agency on properties (agency_id);
create index if not exists idx_properties_neighborhood on properties (neighborhood);
create index if not exists idx_properties_street on properties (street);
create index if not exists idx_properties_type on properties (property_type);
create index if not exists idx_properties_bedrooms on properties (bedrooms);
create index if not exists idx_properties_parking_spaces on properties (parking_spaces);
create index if not exists idx_properties_status on properties (status);
create index if not exists idx_properties_price on properties (price);
create index if not exists idx_properties_listing_type on properties (listing_type);

create index if not exists idx_properties_neighborhood_trgm on properties using gin (neighborhood gin_trgm_ops);
create index if not exists idx_properties_street_trgm on properties using gin (street gin_trgm_ops);
create index if not exists idx_properties_title_trgm on properties using gin (title gin_trgm_ops);
create index if not exists idx_properties_short_description_trgm on properties using gin (short_description gin_trgm_ops);
create index if not exists idx_properties_full_description_trgm on properties using gin (full_description gin_trgm_ops);
create index if not exists idx_properties_visual_description_trgm on properties using gin (visual_description gin_trgm_ops);

create index if not exists idx_property_media_property_id on property_media (property_id);
create index if not exists idx_property_media_visual_tags on property_media using gin (visual_tags);
create index if not exists idx_property_features_property_id on property_features (property_id);
create index if not exists idx_property_embeddings_property_id on property_embeddings (property_id);
create index if not exists idx_property_embeddings_hnsw on property_embeddings using hnsw (embedding extensions.vector_cosine_ops);

create index if not exists idx_conversations_client on client_conversations (client_id);
create index if not exists idx_conversations_agency_status on client_conversations (agency_id, status);
create index if not exists idx_messages_conversation_created on conversation_messages (conversation_id, created_at);
create index if not exists idx_appointments_agency_start on appointments (agency_id, start_time);
create index if not exists idx_handoffs_agency_status on agent_handoffs (agency_id, status);
create index if not exists idx_agent_events_conversation on agent_events (conversation_id);
create index if not exists idx_agent_failures_resolved on agent_failures (resolved);
