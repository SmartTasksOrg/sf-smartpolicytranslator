# Changelog

## Unreleased

### Added
- `sf-smartpolicytranslator` command (`[project.scripts]`), like every other Smart* tool, and
  `python -m sf_smartpolicytranslator`.
- `--demo`: translates a bundled sample regulation (`sf_smartpolicytranslator/data/sample_regulation.txt`,
  the same synthetic text as `examples/sample_regulation.txt`) with no input file, and saves nothing.
  `--version`.
- `tests/test_cli.py` (6 tests); CI also installs the wheel and runs `sf-smartpolicytranslator --demo`
  from an empty folder.

### Changed
- The command line exits 1 when the policy fails validation, and exits 2 with a usage message when it is
  given no input (it used to fail with an argparse error naming `source` only).

### Removed
- `.venv-iaiso/`: a local Windows virtual environment (two executables and a `pyvenv.cfg` with a local
  path) that had been committed by mistake. `.gitignore` now excludes `.venv-*/`, `spt.db` and
  `tests/_t.db`.

### Documentation
- README "Install": `pip install sf-smartpolicytranslator` now that the first release is on PyPI, with how to check its provenance;
  "Status" says where it is published. `names.json` marks `sf-smartpolicytranslator` as registered.
- Release check: the wheel installed in a clean environment now runs the README's demo command from an empty folder, not only `--version`.

## 1.0.0 — first PyPI release as `sf-smartpolicytranslator` (2026-10-09)

Published to PyPI on 2026-10-09 from tag `v1.0.0` by `.github/workflows/release.yml`, with provenance attestations.

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
