# Art sourcing for videos and thumbnails

Visuals should be accurate for the period. Anachronistic AI imagery is a known complaint about the AI history channels (see `docs/research/2026-10-top-performers.md`). Every image needs a recorded source and license in the backlog entry under `licenses.visuals`.

## Allowed sources, in order of preference
1. Our own work (photos, drawings, the generated night sky from `tools/make_thumbnail.py`). Record "own work".
2. Public-domain works with a documented source, for example digitized medieval manuscripts and old prints held by museums and libraries, or files on Wikimedia Commons marked public domain. Record the museum or library, the file page URL, the date checked, and the license shown on that page. A reproduction of a public-domain artwork is not always public domain in every jurisdiction; read the file page.
3. Properly licensed stock or commissioned art, with the license saved.

## Not allowed
- Images with unclear rights, scraped from search results.
- Photorealistic AI images of people or events that never happened, passed off as historical. If AI imagery is used for background only, it must be clearly stylized and the synthetic-content toggle decision recorded.

## Candidate subjects for the first videos
- 001 (medieval English village): fourteenth-century manuscript marginalia showing peasant work, held by the British Library, often found on Wikimedia Commons (verify each file's license on its page).
- Later videos: period prints and paintings matching each setting.

## Record format (backlog entry)
```
licenses:
  visuals: "Source: <institution>; <file page URL>; license: <as shown>; checked 2026-MM-DD"
```

## Animating art
`tools/animate_painting.py` turns a still painting or photo of water into a seamless 1080p looping clip (rolling wave displacement, haze shimmer, foam glints, slow push-in). It animates the art as given, so the rights to the still apply to the clip. The loop is 30 s; the narration or ambient audio carries the video. Pass the clip to `render_video.py --video`. Rendering a 30 s loop takes about 80 s on 4 cores; a long video re-encodes at 24 fps, so allow more time than for a still.

A painting found online (for example via a screenshot or image search) is almost certainly someone's copyrighted work. Do not use it in a monetized video without the artist's written permission or a license. The first test used such an image for a private preview only.

## Original generated scenes
`tools/procedural_waves.py` draws an original breaking-surf scene from code (sky, headlands, sea, foam, sand): crests swell, steepen, break into whitewater, throw spray, and wash up the beach, in a 30 s seamless loop. No source artwork is used, so the output is our own work. Record `licenses.visuals: "own work: tools/procedural_waves.py, seed N, palette P"`. Change `--seed` and `--palette` per video so scenes differ.

Restyling or filtering someone else's artwork does not remove their copyright; the result is still a derivative of the original. The way to avoid the problem is to not use their pixels at all: draw something new, or use art you own or have a license for. Subjects (waves, headlands, dusk light) are not protected, only a particular artist's expression of them.

## Status
Automated downloading was attempted and blocked by a rate limit on the shared network connection, so images are fetched by hand or in a later session. Until then the pilot uses the generated night sky.
