create or replace function match_properties(
  p_agency_id uuid,
  p_query_embedding extensions.vector(1536),
  p_match_count int default 5
)
returns table (
  property_id uuid,
  title text,
  similarity double precision
)
language sql
stable
as $$
  select
    p.id as property_id,
    p.title,
    max(1 - (pe.embedding <=> p_query_embedding))::double precision as similarity
  from properties p
  join property_embeddings pe on pe.property_id = p.id
  where p.agency_id = p_agency_id
    and p.status = 'active'
    and p_query_embedding is not null
    and pe.embedding is not null
  group by p.id, p.title
  order by similarity desc
  limit greatest(coalesce(p_match_count, 5), 1);
$$;

create or replace function search_properties_hybrid(
  p_agency_id uuid,
  p_query text default null,
  p_neighborhood text default null,
  p_street text default null,
  p_property_type text default null,
  p_bedrooms int default null,
  p_parking_spaces int default null,
  p_listing_type text default null,
  p_min_price numeric default null,
  p_max_price numeric default null,
  p_match_count int default 5,
  p_query_embedding extensions.vector(1536) default null
)
returns table (
  property_id uuid,
  external_ref text,
  title text,
  property_type text,
  listing_type text,
  neighborhood text,
  street text,
  bedrooms int,
  parking_spaces int,
  price numeric,
  short_description text,
  visual_description text,
  nearby_references text[],
  media jsonb,
  structured_score numeric,
  text_score numeric,
  vector_score numeric,
  visual_score numeric,
  total_score numeric
)
language sql
stable
as $$
  with candidates as (
    select p.*
    from properties p
    where p.agency_id = p_agency_id
      and p.status = 'active'
      and (p_neighborhood is null or p.neighborhood ilike '%' || p_neighborhood || '%')
      and (p_street is null or p.street ilike '%' || p_street || '%')
      and (p_property_type is null or p.property_type = p_property_type)
      and (p_bedrooms is null or p.bedrooms = p_bedrooms)
      and (p_parking_spaces is null or p.parking_spaces >= p_parking_spaces)
      and (p_listing_type is null or p.listing_type = p_listing_type)
      and (p_min_price is null or p.price >= p_min_price)
      and (p_max_price is null or p.price <= p_max_price)
  ),
  scored as (
    select
      c.*,
      (
        case when p_neighborhood is not null and c.neighborhood ilike '%' || p_neighborhood || '%' then 1 else 0 end +
        case when p_street is not null and c.street ilike '%' || p_street || '%' then 1 else 0 end +
        case when p_property_type is not null and c.property_type = p_property_type then 1 else 0 end +
        case when p_bedrooms is not null and c.bedrooms = p_bedrooms then 1 else 0 end +
        case when p_parking_spaces is not null and c.parking_spaces >= p_parking_spaces then 1 else 0 end +
        case when p_listing_type is not null and c.listing_type = p_listing_type then 1 else 0 end
      )::numeric as structured_score,
      greatest(
        similarity(coalesce(c.title, ''), coalesce(p_query, '')),
        similarity(coalesce(c.neighborhood, ''), coalesce(p_query, '')),
        similarity(coalesce(c.street, ''), coalesce(p_query, '')),
        similarity(coalesce(c.short_description, ''), coalesce(p_query, '')),
        similarity(coalesce(c.full_description, ''), coalesce(p_query, ''))
      )::numeric as text_score,
      greatest(
        similarity(coalesce(c.visual_description, ''), coalesce(p_query, '')),
        coalesce((
          select max(similarity(coalesce(pm.visual_description, '') || ' ' || array_to_string(pm.visual_tags, ' '), coalesce(p_query, '')))
          from property_media pm
          where pm.property_id = c.id
        ), 0)
      )::numeric as visual_score,
      coalesce((
        select max(1 - (pe.embedding <=> p_query_embedding))
        from property_embeddings pe
        where pe.property_id = c.id
          and p_query_embedding is not null
          and pe.embedding is not null
      ), 0)::numeric as vector_score
    from candidates c
  )
  select
    s.id as property_id,
    s.external_ref,
    s.title,
    s.property_type,
    s.listing_type,
    s.neighborhood,
    s.street,
    s.bedrooms,
    s.parking_spaces,
    s.price,
    s.short_description,
    s.visual_description,
    s.nearby_references,
    coalesce((
      select jsonb_agg(jsonb_build_object(
        'id', pm.id,
        'media_type', pm.media_type,
        'url', pm.url,
        'caption', pm.caption,
        'visual_tags', pm.visual_tags,
        'visual_description', pm.visual_description,
        'sort_order', pm.sort_order
      ) order by pm.sort_order)
      from property_media pm
      where pm.property_id = s.id
    ), '[]'::jsonb) as media,
    s.structured_score,
    s.text_score,
    s.vector_score,
    s.visual_score,
    (
      s.structured_score * 1.5 +
      s.text_score * 2.0 +
      s.vector_score * 3.0 +
      s.visual_score * 2.0
    )::numeric as total_score
  from scored s
  order by total_score desc, price asc nulls last
  limit greatest(coalesce(p_match_count, 5), 1);
$$;
