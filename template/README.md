# Zoomcamp template package

This directory is the template-facing part of `zoomcamp-ops`.

The repository still exposes the established template paths at its root so
existing course links and reusable workflows continue to work:

- [`../STRUCTURE.md`](../STRUCTURE.md) - canonical course layout and unit rules
- [`../docs/conventions.md`](../docs/conventions.md) - prose and presentation conventions
- [`../docs/curriculum-contract.md`](../docs/curriculum-contract.md) - website ingestion contract
- [`../templates/`](../templates/) - copy-paste course files
- [`../scripts/check-zoomcamp/`](../scripts/check-zoomcamp/) - curriculum checker

New template guidance belongs here. The [illustration rubric](illustration-rubric.md)
defines whether an instructional image earns a place in a unit, and the
[image regeneration workflow](image-regeneration-workflow.md) explains how to
clean up a valuable but blurry workshop frame. The [course-wide screenshot
rollout](coursewide-screenshot-rollout.md) scales that workflow to every
screenshot in a course.

Keep the root paths stable until consuming course repositories and public links
have been migrated deliberately.
