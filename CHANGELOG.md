# Changelog

## Unreleased

### Security
- Install instructions no longer name packages the maintainers have not
  published. Until the first release, install from a clone (README, "Install").
- New `SECURITY.md` (private vulnerability reporting), `names.json` (the only
  official package names) and a CI check that fails when a document names any
  other package.
- Releases are built and published only by `.github/workflows/release.yml`
  through PyPI trusted publishing, with provenance attestations.

### Changed
- **Renamed (breaking), `sf-` = Smart Family:** repository `SmartTasksOrg/sf-smartpolicytranslator`, PyPI package `sf-smartpolicytranslator`, command `none`, import package `sf_smartpolicytranslator`, MCP server `io.github.smarttasksorg/sf-smartpolicytranslator`. The unprefixed names are not used any more, so nobody can be sent to a look-alike.
- README: "Install" and "Status" sections; the link to a private file is removed.
- `pyproject.toml`: a `[build-system]` (there was none, so the package could not be built reproducibly), `readme`, SPDX licence, `NOTICE` in the wheel, "3 - Alpha" classifier, Source/Issues/Security/Changelog URLs.
- Go port module path `github.com/SmartTasksOrg/sf-smartpolicytranslator/ports/go`.
