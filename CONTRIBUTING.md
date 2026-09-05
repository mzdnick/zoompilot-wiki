# Contributing to the wiki

Thank you for improving the zoompilot wiki. This page explains the
workflow and the writing style.

## Workflow

1. Fork or branch the wiki repository.
2. Edit or add pages under `docs/`.
3. If you add a new page, register it in the `nav` section of
   `mkdocs.yml`. Pages outside `nav` are not reachable.
4. Run a strict build and fix anything it reports:

   ```bash
   .venv/bin/zensical build --strict
   ```

5. Open a pull request.

Every page also has an edit icon beside its title, which opens the right
file on GitHub. The header icon and the edit links are both built from
`repo_url` in `mkdocs.yml`; that is the only place the wiki's own
repository URL is written, so a repo move is a one-line change there.

## Content rules

- **Simple English.** Short sentences, one idea per sentence. Active
  voice. Everyday words.
- **Safety first.** Anything that can affect safe operation belongs in an
  `admonition` block. Use `!!! danger` for the alpha longitudinal radar
  and AEB warnings, `!!! warning` for other risks, `!!! note` and
  `!!! tip` for helpful context.
- **Link user pages to technical pages.** A feature page explains what a
  driver sees. The matching page in `technical/` explains why the code
  does it. Cross-link both ways.
- **Never invent facts.** Write only what you can source from the
  zoompilot site, the repository, or the Discord. If a page needs facts
  you do not have, leave a `TODO(pass-2):` comment that names the source.
- **Keep migrated pages close to their source.** Pages under
  `docs/technical/` and `docs/how-to/` are near-verbatim imports from the
  zoompilot repository. Change structure or links only, and keep the
  author's voice in the body text.

## Page template

```markdown
---
title: Page title
---

# Page title

One short paragraph: what this is and who it is for.

## Section

Content.

## Design details

- [Matching technical page](../technical/<page>.md)
```

## Structure

| Path | Purpose |
| --- | --- |
| `docs/index.md` | Landing page |
| `docs/getting-started/` | Cars, hardware, install, first drive |
| `docs/features/` | One page per user-facing feature |
| `docs/settings/` | Settings reference (pass 2) |
| `docs/safety.md` | Safety, warnings, limitations |
| `docs/technical/` | Engineering notes from the main repository |
| `docs/how-to/` | Task guides |
| `docs/community/` | Contribute, feedback, roadmap, FAQ |
| `docs/releases/` | Changelog |
| `docs/troubleshooting.md` | Common fixes |

## Styling conventions

- Tables for settings and comparisons.
- `admonition` blocks for warnings, never plain bold text.
- Material icons via `:material-...:` shortcodes on the landing page and
  section cards only.
- One `#` heading per page; the page `title` frontmatter matches it.
