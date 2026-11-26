# Agent notes for Wippersnapper_Protobuf

## Bump `VERSION` with every proto change

The `VERSION` file at the repo root tracks the protocol version. Any PR that
changes a `.proto` or `.options` file under `proto/` must bump it in the same PR.
That includes adding, removing, renaming or renumbering fields, messages or enums,
and changing nanopb options.

- While `api-v2` is pre-release, increment the prerelease number:
  `2.0.0-alpha.1` -> `2.0.0-alpha.2`.
- Docs-only or CI-only changes don't need a bump.
- When two open PRs both bump `VERSION`, whichever merges second re-bumps it on
  rebase. Two different protocol states must never share a version.

### Downstream copies

Firmware keeps a copy of this version next to its generated wrappers. Update
it whenever you pull new wrappers from this repo:

- Arduino firmware: `src/protos/VERSION` in
  `adafruit/Adafruit_Wippersnapper_Arduino` (`migrate-api-v2` branch).

## Other things to keep in sync when changing a proto

- `proto/wippersnapper/*.options`: every `string` field the firmware reads as
  a fixed buffer needs a `max_size` entry. Without one, nanopb silently
  generates a `pb_callback_t` instead of a `char[]`.
- `proto/wippersnapper/docs/*.md`: update examples and field lists for any
  renamed or removed fields.
- Generated wrappers come from CI. Each PR's Build run uploads
  `arduino-wrapper`, `python-wrapper`, `javascript-wrapper` and
  `documentation` artifacts. Copy only the files your change touched into
  downstream repos, and check that every other file differs only in the
  nanopb timestamp line.
