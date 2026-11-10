# Repository guidance

## Project boundaries
- This fork turns `dnsmasq-china-list` domain rules into AdGuard Home upstream DNS files. It does not provide ad-blocking rules; describe that distinction accurately in docs.
- Keep the README for Simplified Chinese readers. Write pull request titles in English; PR descriptions may be in Chinese.

## Source and generated files
- `convert.py` generates `converted/`. Do not hand-edit generated files; regenerate them when converter behavior or source lists change, and review the diff.
- `CN_DNS` and `THE_DNS` are GitHub Actions repository variables. Users enter one DNS server per line; preserve support for space-separated `CN_DNS` values.
- Keep upstream-list sync (`sync.yml`) separate from rule generation (`convert.yml`). Avoid changing schedules, DNS defaults, or published file paths without checking the user-facing effect.

## Verification
- For converter changes, run it with representative DNS values and check valid, missing, and malformed input; inspect generated output for unexpected churn.
- For workflow changes, run the affected workflow on a branch and check its GitHub Actions result before merging. For README-only changes, check links and examples; code tests are not needed.
