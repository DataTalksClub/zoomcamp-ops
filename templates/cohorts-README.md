<!--
  COHORTS INDEX TEMPLATE — copy to <course>-zoomcamp/cohorts/README.md.
  Twenty lines telling a contributor where to edit. See ../STRUCTURE.md §1, §6.
-->
# Cohorts

The curriculum lives here, one directory per cohort year. The directory name is
the cohort identifier, and it is the year segment of the published URL.

```
cohorts/
├── {{CURRENT_YEAR}}/            # the live cohort — edit here
│   ├── cohort.yaml
│   ├── README.md                # schedule and deadlines
│   └── 01-intro/                # directory name = module slug = URL segment
│       ├── module.yaml
│       ├── README.md            # module index for GitHub readers
│       ├── 01-what-is-ml.md     # a unit; the filename stem is its URL slug
│       ├── homework.md
│       ├── homework.yaml
│       ├── images/              # every image these units use
│       └── code/                # notebooks and scripts these units link
└── {{PREVIOUS_YEAR}}/           # frozen archive of what was taught then
```

## Which cohort do I edit?

`{{CURRENT_YEAR}}`. That is where content pull requests are accepted.

Earlier years are frozen archives. The drift between them is the record of what
each cohort was actually taught, so we do not sync them. Only factual or
breaking errors — a wrong command, a dead dataset URL — get backported, by a
maintainer, one cohort at a time. The trees are congruent, so the same file sits
at the same cohort-relative path in every year and `grep -rl` finds them all.

## The rules in one screen

- A unit is one `NN-kebab.md` file sitting next to `module.yaml`. Its H1 is its
  title; its number comes from the filename prefix.
- Everything a unit needs — images, notebooks, data — lives inside that module
  directory. No `../` reaching into another module for a figure.
- The homework is `homework.md` plus `homework.yaml`, in the module directory.
- Directory and file names are URLs. Renaming a file in a published cohort moves
  a live link, so we do not rename them.

New unit? Start from
[`templates/unit.md`](https://github.com/DataTalksClub/zoomcamp-template/blob/main/templates/unit.md).
Full spec:
[`STRUCTURE.md`](https://github.com/DataTalksClub/zoomcamp-template/blob/main/STRUCTURE.md).
A check runs on every pull request and reports what is wrong before a reviewer
has to.
