# Illustration rubric

Use this rubric for instructional images in unit pages: diagrams,
plots, screenshots, terminal output, and application states. It does not
replace the separate rules for repository branding, banners, certificates,
or video thumbnails.

## The primary question

> Does this image contribute something to the lesson that the learner would
> lose if the image were removed?

If the answer is no, remove it. Do not keep an image merely because it was
captured during the workshop or because it documents that a command was run.

## Score each image

Give each criterion 0, 1, or 2 points. Judge the image together with the
paragraphs and code immediately around it, not in isolation.

| Criterion | 0 points | 1 point | 2 points |
| --- | --- | --- | --- |
| Instructional contribution | Adds no new understanding | Reinforces nearby material | Shows a unique fact, relationship, result, or state change |
| Relevance to the lesson | Tangential or navigational | Provides general context | Directly supports the concept or action being taught |
| Readability and focus | Important content is unreadable or buried | Understandable with effort | Relevant content is clear at normal display size |
| Complementarity | Duplicates the prose, code, or another image | Adds a small amount of extra evidence | Shows evidence that text or code does not convey as well |
| Durability | Depends on a live page, personal session, or transient state | Useful but likely to age or require context | Remains useful and understandable as the course evolves |
| Caption and accessibility | Caption is generic, wrong, or missing | Caption identifies the subject | Caption says what the learner should notice; alt text is meaningful |

The maximum score is 12. Use the score as guidance, not as a substitute for
the primary question:

- 0-3: remove.
- 4-6: review; crop, annotate, or replace if the underlying idea matters.
- 7-12: keep if no hard-gate rule below is violated.

## Hard gates

These override the total score:

- If instructional contribution is 0, remove the image.
- If the relevant content cannot be made readable by cropping or replacing
  it, remove the image.
- If the image exposes personal information, credentials, tokens, or private
  chat content, redact it or remove it.
- If the image and its caption do not match, fix the pair before keeping it.
- If the image is one of several near-identical captures, keep only the
  smallest set needed to explain the idea.

## Typical decisions

Keep an image when it shows a meaningful dashboard result, a user-visible
state transition, an architecture or data relationship, a plot that supports
an argument, or a configuration screen whose choices are difficult to explain
in text.

Remove an image when it shows a workshop page, repository navigation, a
presenter or chat panel, an empty application, code already printed clearly in
the lesson, or a command with no meaningful output.

Crop or replace an image when the underlying evidence matters but the capture
contains video-call chrome, browser tabs, unrelated panels, tiny text, or a
partial/incomplete final state. A clean diagram or a short code/output block
is usually better than a video frame.

## Review procedure

For each image:

1. Read the caption and the surrounding lesson text.
2. Complete the sentence: “This image teaches …”. If the sentence cannot be
   completed with a specific learning point, remove the image.
3. Check whether that learning point already appears in prose, code, or a
   previous image.
4. Score the six criteria and apply the hard gates.
5. Record one decision: `keep`, `crop/replace`, or `remove`, with a short
   reason.

The goal is not to remove all screenshots. The goal is to retain the minimum
set of clear images that add instructional value to the written lesson.
