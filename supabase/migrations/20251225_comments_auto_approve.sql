-- Migration: Auto-approve comments on insert
-- Description: Sets the default value for is_approved to true and updates the insert policy
-- to allow public insertion of pre-approved comments with validation rules.
alter table public.comments
  alter column is_approved set default true;

drop policy if exists "public insert comments (unapproved)" on public.comments;
drop policy if exists "public insert comments (auto-approved)" on public.comments;
create policy "public insert comments (auto-approved)"
  on public.comments
  for insert
  to anon, authenticated
  with check (
    is_approved = true
    and char_length(author_name) between 1 and 80
    and char_length(body) between 1 and 5000
    and char_length(thread_id) between 1 and 300
  );
