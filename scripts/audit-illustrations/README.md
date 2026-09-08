# Illustration audit report generator

`audit_illustrations.py` creates the two lists required by the image workflow:

1. every unit in the selected current scope, with instructional illustration
   present or missing; and
2. every active local or remote image-reference occurrence, with reference,
   decode/dimension checks, and an explicit quality/review status.

The script is read-only with respect to course repositories. It uses the
published 2026 cohort manifests for ML and LLM, the current root module pages
for MLOps, and the current (but explicitly unpublished) 2027 draft cohort for
DE. Edit `DEFAULT_SCOPE_SPECS` when a course changes its authoritative current
scope; do not silently include historical cohorts.

Run from `zoomcamp-ops`:

```bash
python scripts/audit-illustrations/audit_illustrations.py \
  --workspace-root /home/alexey/git \
  --output docs/current-illustration-audit.md
```

The output records each source repository's `HEAD`, worktree state, active
selection, unit coverage, and every image-reference occurrence. `PASS` only
means that a local target resolves and its basic image dimensions can be read.
The `review required` statuses are intentional: crispness, crop direction and
order, text/semantic fidelity, overlays, and lesson-size readability require an
independent visual reviewer and cannot be established by this scanner.
