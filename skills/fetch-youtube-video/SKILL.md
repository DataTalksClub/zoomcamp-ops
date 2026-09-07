---
name: fetch-youtube-video
description: Download a YouTube workshop recording for local Zoomcamp production work. Use when a video file is needed for chopping, review, or frame extraction; do not use for transcript-only requests.
---

# Fetch a YouTube video

Download the source recording into the repository's gitignored `.tmp/videos/`
directory. Never commit the downloaded video to a course repository.

## Workflow

1. Resolve the video URL or ID and choose a stable, descriptive slug.
2. Check `.tmp/videos/` for an existing source before downloading again.
3. Download the best available video at or below 720p with a separate audio
   stream when available:

   ```bash
   mkdir -p .tmp/videos
   uvx yt-dlp \
     -f 'bv*[height<=720]+ba/b[height<=720]' \
     -S 'res:720,br' \
     --merge-output-format mkv \
     -o '.tmp/videos/<slug>.%(ext)s' \
     '<youtube-url-or-id>'
   ```

4. Verify that the file exists, has a usable duration, and can be opened by
   `ffprobe` or `ffmpeg` before handing it to another workflow.
5. Report the local path, source URL, duration, resolution, and any download
   limitation. Keep the source file in `.tmp/` for chopping or frame review.

## Constraints

- Do not bypass access controls or download private videos without access.
- Do not place large media files in tracked directories.
- Do not re-download an unchanged source just to inspect metadata.
- Use the original recording when a higher-quality local source is available;
  YouTube tops out at the quality it exposes.
- Keep timestamps and source metadata with any later chop plan or illustration
  manifest so extracted frames can be traced back to the recording.

This skill fetches the video only. Use a transcript workflow for captions, and
use `extract-youtube-illustrations` for candidate images.
