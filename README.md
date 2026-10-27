# Youtube

Workspace for a faceless sleep channel ("Quiet Hours", working name), built to be automated over time. Start with `CLAUDE.md` for rules, layout, commands, and skills.

- `channels/sleep/`: the channel (strategy, 90-day calendar, 20-video backlog, script 001 with its fact-check report)
- `docs/research/`: sourced research: niche choice, launch risks, top performers, what the bottom 90% get wrong, ambient sounds
- `docs/runbook-human-steps.md`: the few things only the owner can do
- `docs/experiments/`: series and format tests with fixed decision rules
- `tools/`: lint, narration, bed, thumbnail, render, packaging, validation
- `.claude/skills/`: the workflow as Claude skills

```
pip install pyyaml pillow
python3 tools/validate.py
```
