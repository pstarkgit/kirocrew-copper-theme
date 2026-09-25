# Copper for KiroCrew

![Copper theme preview](.github/preview.svg)

Copper is a high-contrast KiroCrew theme with a near-black canvas, warm copper chrome, and clear semantic colors. Copper is reserved for brand and interaction, while green, amber, red, and slate blue communicate application state.

## Design

- **Near-black field:** neutral surfaces from `#080808` to `#161616`
- **Copper interaction:** `#D06A32` for accent, focus, hover, and chrome
- **Clear state vocabulary:** zombie green for success, amber-gold for warning, punchy red for danger, and slate blue for information
- **Readable secondary text:** high-contrast muted foregrounds in both modes
- **Dark and light palettes:** complete 54-token KiroCrew theme contract

## Install

Kiro Crew's installer is the validator. Extra files at the pack root are rejected, so this repo keeps only the installable files (`theme.json`, `variables.json`, `README.md`, `LICENSE`) plus ignored VCS/meta (`.git`, `.github`, `.gitignore`).

1. Open Kiro Crew.
2. Go to **Settings → Display → Install theme**.
3. Paste this GitHub URL:

   `https://github.com/pstarkgit/kirocrew-copper-theme`

   Or select the local folder that contains `theme.json` and `variables.json`.
4. Choose **Copper**. Re-install overwrites; that is the update path.

## Validate

Optional local check (Python stdlib only; lives under `.github/` so it is not part of the installed pack):

```sh
python3 .github/validate.py
```

It checks the manifest, exact variable contract, safe CSS value forms, matching dark and light keys, and foreground contrast. A successful **Install theme** run is the authoritative check.

## Files

- `theme.json`: KiroCrew theme manifest (level 0, colors only)
- `variables.json`: dark and light CSS variable maps
- `README.md`: this file (allowed in a level-0 pack)
- `LICENSE`: MIT; ignored by the installer as metadata
- `.github/preview.svg`: palette preview for GitHub (ignored by the installer)
- `.github/validate.py`: optional local validator (ignored by the installer)

## Notes

This is an unofficial community theme for KiroCrew. It changes colors only and does not include CSS overrides or executable code.


## Related

- Hermes Agent skins + dashboard themes: https://github.com/pstarkgit/hermes-themes
## License

[MIT](LICENSE)
