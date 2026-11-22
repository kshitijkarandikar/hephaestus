# Small tools

## `kit calc "<expression>"`

Money math without trusting anyone's head.

- Allowed characters: digits, `+ - * /`, parentheses, `.`, spaces. Anything else: print `Use only numbers and + - * / ( ). Example: calc "(4+5+3)*95"` to stderr, exit 1.
- Not allowed: `**`, `//`. Same error.
- Do **not** use a general `eval` on the text. Write a small parser (numbers, unary minus, `* /` before `+ -`, parentheses), or evaluate only after the character check with a mechanism that cannot call anything.
- Accepted: unary plus and minus, numbers like `5.` and `.5`. A lone operator, empty parentheses or an empty expression are invalid.
- A result that rounds to zero prints `0.00`, never `-0.00`.
- Division by zero or an invalid expression: `That is not a valid calculation.` to stderr, exit 1.
- Output: the result rounded **half up to 2 decimals**, always with 2 decimals (`1140.00`). Round using decimal arithmetic, so `1.005` becomes `1.01`, not `1.00`.

## `kit pdf <html file> [pdf file]`

Print an HTML file to PDF with the Chrome, Edge or Brave browser on this laptop.

- The HTML file must be inside `ROOT/outputs/` or `ROOT/context/templates/` after resolving symbolic links. Otherwise: `Only files in outputs/ or context/templates/ can be printed.` exit 1.
- The PDF defaults to `ROOT/outputs/<html name without extension>.pdf`. It must be inside `ROOT/outputs/`. Otherwise: `The PDF must go in outputs/.` exit 1.
- File missing: `File not found: <path>`, exit 1.
- Find a browser, first match wins:
  - macOS: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`, `/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge`, `/Applications/Brave Browser.app/Contents/MacOS/Brave Browser`, `/Applications/Chromium.app/Contents/MacOS/Chromium`
  - Windows: Edge in `%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe` and `%ProgramFiles%\...`, Chrome in `%ProgramFiles%\Google\Chrome\Application\chrome.exe` and `%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe`
  - Linux: `/usr/bin/google-chrome`, `/usr/bin/chromium`, `/usr/bin/chromium-browser`, `/usr/bin/microsoft-edge`
- None found: `No Chrome or Edge found. Open the HTML file and use Print, Save as PDF.` to stderr, exit 2.
- Run the browser with these arguments, with a time limit of 45 seconds and its output discarded:
  `--headless=new --disable-gpu --no-pdf-header-footer --user-data-dir=<temp folder>/kit-pdf-profile --print-to-pdf=<pdf path> <file:// URL of the html file>`
- Success: print the absolute PDF path, exit 0. If no PDF file exists afterwards: `No PDF was made.` exit 1.

## `kit doctor`

Print a title, then one line per check, then a verdict. Prefix `  [ok]   `, `  [warn] ` or `  [FAIL] `.

1. Runtime: the language and version running the kit. `[ok]`.
2. Security rules: run the same tests as `kit check selftest`. `[ok]` with the summary line, else `[FAIL]`.
3. Work log: run the same check as `kit log verify`. `[ok]` or `[FAIL]` with the reason.
4. Integrity seal: as `kit check integrity`. Missing seal is `[warn]`. A mismatch is `[FAIL]`.
5. Browser for PDF: found is `[ok]`, otherwise `[warn]` that PDF will not work.
6. AI tools on the PATH: `claude`, `codex`, `gemini`. List the ones found, `[warn]` if none.

The exact text after the prefix is free, except that the lines must say what was checked and the result.

Verdict: `All good.` and exit 0 if there is no `[FAIL]`, otherwise `Fix the problems above.` and exit 1.
