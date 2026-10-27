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

## Status
Automated downloading was attempted and blocked by a rate limit on the shared network connection, so images are fetched by hand or in a later session. Until then the pilot uses the generated night sky.
