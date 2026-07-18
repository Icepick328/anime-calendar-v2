-- v0.6.3 Personal Calendar Engine

create table if not exists public.personal_calendars (
    calendar_id uuid primary key default gen_random_uuid(),
    owner_id uuid not null references public.account_identities(user_id) on delete cascade,
    name text not null check (char_length(trim(name)) between 1 and 120),
    visibility text not null default 'private' check (visibility in ('private', 'unlisted')),
    enabled boolean not null default true,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.personal_calendar_tokens (
    calendar_id uuid primary key references public.personal_calendars(calendar_id) on delete cascade,
    token_hash text not null unique check (char_length(token_hash) = 64),
    created_at timestamptz not null default now(),
    rotated_at timestamptz
);

alter table public.personal_calendars enable row level security;
alter table public.personal_calendar_tokens enable row level security;

create policy "owners manage personal calendars" on public.personal_calendars
for all using (auth.uid() = owner_id) with check (auth.uid() = owner_id);

create policy "owners manage calendar tokens" on public.personal_calendar_tokens
for all using (
    exists (
        select 1 from public.personal_calendars c
        where c.calendar_id = personal_calendar_tokens.calendar_id
          and c.owner_id = auth.uid()
    )
) with check (
    exists (
        select 1 from public.personal_calendars c
        where c.calendar_id = personal_calendar_tokens.calendar_id
          and c.owner_id = auth.uid()
    )
);

create or replace function public.resolve_personal_calendar(presented_token_hash text)
returns setof public.personal_calendars
language sql
security definer
set search_path = public
as $$
    select c.*
    from public.personal_calendars c
    join public.personal_calendar_tokens t using (calendar_id)
    where t.token_hash = presented_token_hash
      and c.enabled = true
      and c.visibility = 'unlisted'
    limit 1;
$$;

revoke all on function public.resolve_personal_calendar(text) from public;
grant execute on function public.resolve_personal_calendar(text) to anon, authenticated;
