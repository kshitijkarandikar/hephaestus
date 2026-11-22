# Work log

One JSON file per day in `ROOT/worklog/` (or `KIT_WORKLOG_DIR`), named `YYYY-MM-DD.json`. Entries are append only and linked by a hash chain.

## Day file

```
{
  "date": "2026-11-03",
  "entries": [ <entry>, <entry>, ... ]
}
```

Write with 2-space indentation, UTF-8, a newline at the end. Write to a temporary file in the same folder, then rename it over the real file, so a crash never leaves a half file.

## Entry

Keys, in **this exact order** (skip keys that have no value):

| Key | Type | Notes |
|---|---|---|
| `id` | string | `<date>-<NNN>`: the day's date and a 3-digit counter. The counter is the number of entries already in that day's file, plus one (`001` for the first), for example `2026-11-03-001` |
| `time` | string | local time `HH:MM` |
| `kind` | string | `work`, `approval`, `blocked`, `tool`, `note`. Default `work`. Anything else: error |
| `client` | string | |
| `task` | string | required when kind is `work` |
| `skill` | string | |
| `tool` | string | which AI tool did it |
| `minutes` | number | the freelancer's time. Must be a number of 0 or more. Write whole numbers without a decimal point (`240`, not `240.0`) |
| `billable` | boolean | for kind `work` the default is `true` |
| `files` | list of strings | the input is comma separated: split on commas, trim, drop empty items |
| `outcome` | string | |
| `notes` | string | |
| `corrects` | string | id of an entry this one corrects |
| `sample` | boolean | |
| `prev` | string | hash of the previous entry in the whole log, `""` for the very first. Written last |
| `hash` | string | see below. Written last, after `prev` |

The order above is for **new** entries. The sample files in `worklog/` store a few keys in a slightly different order. That is fine: `verify` always uses the order stored in the file, and never reorders.

Input rules for `kit log add`:
- Each `key=value` word sets that key. Unknown keys are ignored. Empty values are ignored.
- `billable` and `sample`: the text `true` or `yes` means true, anything else false.
- `date` and `time` words on the command line are ignored. The date and time always come from the clock (or `KIT_NOW` in tests).
- `minutes` is digits with an optional decimal part only: no sign, no exponent, no text. Errors print `Error: <reason>` to stderr, exit 1, write nothing. Reasons: `kind must be one of work, approval, blocked, tool, note`, `task is required`, `minutes must be a number`.
- Print `logged <id> (<kind>): <task or notes>` on success.

## Hash chain

```
entry_without_hash = the entry's keys up to and including everything except "prev" and "hash"
canonical(x)       = JSON text of x as defined below
hash = sha256_hex( prev + canonical(entry_without_hash) )     (the text encoded as UTF-8)
```

`prev` is the `hash` of the last entry in the newest earlier position: the last entry of the same day if there is one, otherwise the last entry of the latest earlier day file that has entries, otherwise `""`.

### canonical JSON (must be identical in every language)

- No spaces anywhere (`{"a":1,"b":[2,3]}`).
- Keys in the order stored (the order in the table above). Never sort.
- Strings: UTF-8, non-ASCII characters written as they are (not `\uXXXX`). Escape only `"` as `\"`, `\` as `\\`, and control characters below 0x20: use `\b \t \n \f \r` where they exist, otherwise `\u00xx` with lowercase hex.
- Numbers: whole numbers as digits only. Other numbers in the shortest form that reads back the same.
- `true`, `false`. No `null` ever appears.

### verify

Walk the files named `YYYY-MM-DD.json` in name order (ignore any other file in the folder), entries in order. Keep `prev_seen`, starting at `""`.
1. If the entry's `prev` is not `prev_seen`: fail, reason `link to the previous entry is broken (entry removed or reordered?)`.
2. Recompute the hash from the stored entry without `prev` and `hash`, keeping the stored key order. If it differs from `hash`: fail, reason `entry content was changed after it was written`.
3. `prev_seen = hash`.

Success prints `OK: <n> entries, chain intact`, exit 0. Failure prints `BROKEN at <file> <id>: <reason>` to stderr, exit 1.

## Locking

Before writing, create the folder `worklog/.lock`. If that fails, wait 30 ms and try again, up to 100 times, then fail with `worklog is locked`. A lock older than 10 seconds is stale: remove it. Always remove the lock when done.

## `kit log list [date=YYYY-MM-DD]`

Default date: today. If no entries print `no entries for <date>`. Otherwise one line per entry:

`<id> <time> [<kind>] <client>: <task or notes> (<minutes> min)`

The `<client>: ` part appears only if there is a client. The `(<minutes> min)` part appears only if minutes is set and not 0.

## `kit report`

An invalid `by` or `format` value: print `Error: by must be client, skill or day` or `Error: format must be text, md or json` to stderr, exit 1.

Options (all `key=value`, all optional): `from` (default 0000-01-01), `to` (default 9999-12-31), `client` (case-insensitive exact match), `by` (`client`, `skill` or `day`, default `client`), `billable` (`true` or `false`), `format` (`text`, `md`, `json`, default `text`), `save` (`true` also writes the output to `ROOT/outputs/<today>-hours-report.md`, or `.json` for json, and prints `Saved outputs/<name>`).

Which entries count: kind `work`, date from `from` to `to` inclusive, matching filters. The `billable` filter compares with the entry's billable value, where a missing value counts as `true`.
- Entries without `minutes` are not counted. They are listed at the end.
- Group key: `client` (or `(no client)`), `skill` (or `(none)`), or the date.
- A group has `minutes` (sum of all) and `billable` (sum of entries where billable is not false).
- Hours = minutes / 60, shown with exactly 2 decimals.

`text` format:
```
Hours report <from> to <to>
<blank>
<key padded right to 24 chars> <hours right aligned to 7 chars> h   billable <hours right aligned to 7 chars> h     (one line per group, groups sorted by key, comparing by code point so `(no client)` comes first)
<blank>
Total: <hours> h, billable <hours> h
```
If entries without minutes exist, add: a blank line, `<n> work entries have no minutes and are NOT counted:`, then `- <id>: <task>` per entry.

`md` format: first line `# Hours report <from> to <to>`, blank line, table header `| <by> | Hours | Billable hours |`, separator `|---|---|---|`, one row per group `| key | hours | billable hours |`, blank line, the `Total:` line, then the optional missing list.

`json` format, with 2-space indentation:
```
{ "from": ..., "to": ..., "by": ...,
  "groups": { "<key>": { "hours": <number>, "billable_hours": <number> }, ... },
  "total_hours": <number>, "billable_hours": <number>,
  "entries_without_minutes": [ { "date": ..., "id": ..., "task": ... } ] }
```
Hours in json are numbers rounded to 2 decimals.
