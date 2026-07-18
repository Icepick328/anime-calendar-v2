-- v0.6.2 Identity and Persistence
-- Apply with the Supabase CLI or SQL editor after reviewing for your environment.

create extension if not exists pgcrypto;

create table if not exists public.account_identities (
    user_id uuid primary key references auth.users(id) on delete cascade,
    email text,
    status text not null default 'active' check (status in ('active', 'disabled', 'pending')),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.profiles (
    user_id uuid primary key references public.account_identities(user_id) on delete cascade,
    display_name text not null check (char_length(trim(display_name)) between 1 and 80),
    timezone text not null default 'UTC',
    locale text not null default 'en-US',
    updated_at timestamptz not null default now()
);

create table if not exists public.user_preferences (
    user_id uuid primary key references public.account_identities(user_id) on delete cascade,
    favorite_genres text[] not null default '{}',
    excluded_genres text[] not null default '{}',
    favorite_studios text[] not null default '{}',
    preferred_provider_ids text[] not null default '{}',
    preferred_release_types text[] not null default '{}',
    preferred_variants text[] not null default '{}',
    favorite_anilist_ids bigint[] not null default '{}',
    include_unmatched_releases boolean not null default true,
    updated_at timestamptz not null default now(),
    constraint no_genre_overlap check (
        not (favorite_genres && excluded_genres)
    )
);

alter table public.account_identities enable row level security;
alter table public.profiles enable row level security;
alter table public.user_preferences enable row level security;

create policy "owners read identity" on public.account_identities
for select using (auth.uid() = user_id);
create policy "owners update identity" on public.account_identities
for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "owners read profile" on public.profiles
for select using (auth.uid() = user_id);
create policy "owners insert profile" on public.profiles
for insert with check (auth.uid() = user_id);
create policy "owners update profile" on public.profiles
for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "owners read preferences" on public.user_preferences
for select using (auth.uid() = user_id);
create policy "owners insert preferences" on public.user_preferences
for insert with check (auth.uid() = user_id);
create policy "owners update preferences" on public.user_preferences
for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

create or replace function public.handle_new_auth_user()
returns trigger
language plpgsql
security definer set search_path = ''
as $$
begin
    insert into public.account_identities (user_id, email, status)
    values (new.id, new.email, 'active');
    insert into public.profiles (user_id, display_name)
    values (new.id, coalesce(nullif(split_part(new.email, '@', 1), ''), 'Anime Fan'));
    insert into public.user_preferences (user_id) values (new.id);
    return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
after insert on auth.users
for each row execute procedure public.handle_new_auth_user();

create or replace function public.delete_my_account_data(requested_user_id uuid)
returns void
language plpgsql
security invoker
set search_path = public
as $$
begin
    if auth.uid() is null or auth.uid() <> requested_user_id then
        raise exception 'not authorized';
    end if;
    -- Deleting auth.users must be completed by a trusted server-side function.
    -- Cascades remove these private application records immediately.
    delete from public.account_identities where user_id = requested_user_id;
end;
$$;

grant execute on function public.delete_my_account_data(uuid) to authenticated;
