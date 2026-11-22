---
name: html-to-pdf
description: Turn an HTML file into a PDF with the Chrome or Edge browser on this computer. Use when the user wants a PDF of an invoice, quote, report or letter.
---

# HTML to PDF

## Steps
1. Write one complete HTML page into `outputs/<name>.html`. Use `context/templates/invoice.html` as a style reference for invoices. Rules: A4 page, print-safe fonts, no web images or web fonts.
2. Run the script from the kit folder:
   ```
   ./kit pdf outputs/<name>.html
   ```
3. It prints the PDF path, `outputs/<name>.pdf`. Tell the user.
4. If it says no browser was found, tell the user to open the HTML file and use Print, Save as PDF.

## Rules
- Only files inside `outputs/` or `context/templates/`.
- Never put real client data into practice files.

## Log
Last step: ask the user how many minutes this took them (optional), then run `./kit log add client="<client>" task="<what you did>" skill=html-to-pdf minutes=<n> files=<output file> outcome=<done|draft>`.
