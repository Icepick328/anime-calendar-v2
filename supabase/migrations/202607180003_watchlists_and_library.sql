create table if not exists public.library_entries (
    owner_id uuid not null references public.account_identities(user_id) on delete cascade,
    anilist_id bigint not null check (anilist_id > 0),
    status text not null check (status in ('watching','plan_to_watch','completed','on_hold','dropped')),
    progress integer not null default 0 check (progress >= 0),
    score integer check (score between 0 and 100),
    notes text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    primary key (owner_id, anilist_id)
);

alter table public.library_entries enable row level security;

create policy "library owners can read"
on public.library_entries for select
using (auth.uid() = owner_id);

create policy "library owners can insert"
on public.library_entries for insert
with check (auth.uid() = owner_id);

create policy "library owners can update"
on public.library_entries for update
using (auth.uid() = owner_id)
with check (auth.uid() = owner_id);

create policy "library owners can delete"
on public.library_entries for delete
using (auth.uid() = owner_id);

create or replace function public.touch_library_entry_updated_at()
returns trigger language plpgsql as $$
begin
    new.updated_at = now();
    return new;
end;
$$;

create trigger touch_library_entry_updated_at
before update on public.library_entries
for each row execute function public.touch_library_entry_updated_at();
