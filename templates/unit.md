<!--
  UNIT TEMPLATE — copy to cohorts/<year>/<NN-module>/<NN-unit-slug>.md.

  The filename is the unit's URL slug: two-digit prefix, kebab-case, .md.
  Once the cohort is published that slug is frozen — renaming the file moves
  a live URL.

  The H1 is the unit's title everywhere, on GitHub and on the website. Do not
  number it: the number comes from the filename prefix.

  Delete this comment and the frontmatter keys you do not need. Full rules:
  STRUCTURE.md §5 in DataTalksClub/zoomcamp-template.

  On video_url: this is where the recording belongs and where the site will
  read it. It is not read yet — today the deployed unit page picks the video up
  from a body line of the form `video: [Recording](https://youtu.be/...)`. For
  a NEW unit use the frontmatter key (and add the body line too if the video
  must show on the site before that ships). Never convert an existing unit's
  video to frontmatter on its own: that removes it from the published page.
-->
---
video_url: {{YOUTUBE_URL}}          # omit the key entirely if there is no video
code:                               # omit if the unit walks through no files
  - label: {{e.g. Notebook}}
    path: {{e.g. code/notebook.ipynb}}
---
# {{UNIT_TITLE}}

{{One or two sentences saying what this unit covers, before any heading.}}

{{Body.

Images live in this module's images/ directory and are linked relatively:
![alt text](images/name.png)

Link a sibling unit by filename:            [the next unit](02-next-unit.md)
Link the homework:                          [homework](homework.md)
Link the module index:                      [module overview](README.md)
Link another module in the same cohort:     [regression](../02-regression/01-linear-regression.md)

Anything outside this cohort — a past cohort, another repository — is an
absolute GitHub URL, not a relative path.

No video links in the body: the recording goes in video_url above.
No prev/next lines and no "## Navigation" block: the site renders navigation
and the module README is the index.}}

## {{Section Heading}}

{{Sections are h2. This file has exactly one h1, the title above.}}

## Notes

{{Optional. Community notes are content and stay. Contributors add theirs here
via a pull request.}}
