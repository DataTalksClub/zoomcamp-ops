# New Zoomcamp Checklist

Step-by-step to spin up a new camp from this template.

## 1. Create the repo

- [ ] Create `<course>-zoomcamp` under the DataTalksClub org.
- [ ] Add `.github/FUNDING.yml` (copy from this template).
- [ ] Add `images/` with a banner (`width="80%"`, see conventions). This
      directory is repo branding only — unit images live in their module.

## 2. Landing page

- [ ] Copy `templates/root-README.md` to `README.md`.
- [ ] Replace every `{{PLACEHOLDER}}`.
- [ ] Keep the section order from `STRUCTURE.md` §2.
- [ ] Set the title to `<Course> Zoomcamp: A Free <N>-Week Course on <topic>`.
- [ ] Point the syllabus links at `cohorts/<year>/NN-module/`.

## 3. Course identity

- [ ] Mint a course `content_id`: `uuidgen | tr 'A-Z' 'a-z'`.
- [ ] Write `course.yaml` at the root — fields in `docs/curriculum-contract.md` §3.
      The `slug` is the published URL segment and is frozen once anything ships.
- [ ] Write `SITE.md`: the website's course description. Prose, no banner
      markup, no badges. It is not the README.

## 4. First cohort

- [ ] Copy `templates/cohorts-README.md` to `cohorts/README.md`.
- [ ] Create `cohorts/<year>/` and write `cohort.yaml`
      (`docs/curriculum-contract.md` §4). The directory name is the cohort
      identifier — do not restate it anywhere else.
- [ ] Copy `templates/cohort-README.md` to `cohorts/<year>/README.md` and fill
      in the schedule, deadlines and office hours.

## 5. Modules and units

- [ ] Create `cohorts/<year>/NN-kebab-name/` directories, two-digit zero-padded.
- [ ] In each, write `module.yaml` with a fresh `content_id` and the module title.
- [ ] Copy `templates/module-README.md` into each module's `README.md`. It is
      the GitHub index; the lessons are separate files it links.
- [ ] Write units as `NN-kebab.md` siblings, from `templates/unit.md`. One H1,
      unnumbered; the video in frontmatter; images in the module's `images/`.
- [ ] Add `homework.md` + `homework.yaml` in the module directory. Never commit
      a plaintext answer key.
- [ ] Add a final project / capstone.

## 6. Shared docs

- [ ] Copy `templates/after-sign-up.md` and adapt.
- [ ] Copy `templates/learning-in-public.md` and adapt.
- [ ] Add `certificate.md`.
- [ ] Optionally add `awesome-<topic>.md`.

## 7. Tooling

- [ ] Copy `templates/workflows/curriculum-check.yml` to
      `.github/workflows/curriculum-check.yml` and pin the zoomcamp-template SHA.
- [ ] Run `check-zoomcamp` locally until it is clean:
      `uv run https://raw.githubusercontent.com/DataTalksClub/zoomcamp-template/main/scripts/check-zoomcamp/check_zoomcamp.py .`
- [ ] Copy `scripts/generate-thumbnails` if the camp uses self-hosted thumbnails.
- [ ] Copy `scripts/youtube-upload` + `scripts/chop-specs` if you run the video
      pipeline.
- [ ] Run scripts with `uv run`.

## 8. Final pass

- [ ] `check-zoomcamp` reports zero errors.
- [ ] No emoji in `##`/`###` headings; no bold formatting.
- [ ] No hand-maintained table of contents, and no per-unit prev/next lines.
- [ ] Standardized heading names (see `docs/conventions.md`).
- [ ] Every syllabus entry links into the current cohort's module directory.
- [ ] Ask the website team to register the repository's webhook, and confirm the
      first import run is green.
