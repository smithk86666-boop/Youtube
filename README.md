# Youtube

Workspace for faceless YouTube channels, built to be automated over time. Start with `CLAUDE.md` for the rules and layout.

- `channels/sleep-stories/`: first channel (working name "Quiet Hours"), narrated sleep content for adults
- `docs/research/`: dated, sourced research notes (niche choice, launch risks)
- `docs/automation-roadmap.md`: path from manual to automated
- `docs/compliance-checklist.md`: pre-publish gate

```
pip install pyyaml
python3 tools/new_channel.py <slug> "<Name>"
python3 tools/validate.py
```
