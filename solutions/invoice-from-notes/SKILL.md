---
name: invoice-from-notes
description: Make an invoice (HTML and PDF) from messy work notes and log it. Use when the user says "invoice this", "bill the client" or points to job notes.
---

# Invoice from notes

## Inputs
Work notes (`inbox/` file or pasted) and the client name.

## Steps
1. Read `context/business.md`, `context/rates.csv`, the client's row in `context/clients.csv`.
2. Read the notes. Make one line per kind of work: description, quantity (hours), rate from `rates.csv`. Match each note to a service in `rates.csv`. If none matches, ask. Never guess a rate.
3. Find the next invoice number: last row of `context/invoices-log.csv`, plus one.
4. Compute amounts with the calculator, never in your head. Example: `./kit calc "(4+5+3)*95"` for the subtotal, `./kit calc "1140*0.21"` for the BTW, `./kit calc "1140*1.21"` for the total. Show the calculation lines to the user.
5. Today is the invoice date. Due date = invoice date + payment term from `business.md`.
6. Write `outputs/invoice-<number>-<client>.html`, copying the layout of `context/templates/invoice.html`.
7. Run the `html-to-pdf` skill to make the PDF.
8. **Show the user the lines and totals. Wait for "ok".** Only then add a row to `context/invoices-log.csv` with status `unpaid`. Then log the task in the work log (see the Log section).
9. If Google is connected (level draft), offer to upload the PDF to Drive with `./kit google drive upload file=outputs/<pdf>`, and a Gmail draft with `./kit google gmail draft`. Ask first. Never send. (A Gmail draft cannot attach the PDF in this kit: tell the user to attach it by hand.)

## Rules
- No row in the log before the user says ok.
- Amounts have 2 decimals. Dates like 2026-12-08 in the log, 8 December 2026 on the invoice.
- Unclear note? Ask. Do not round hours up.

## Log
Last step: ask the user how many minutes this took them (optional), then run `./kit log add client="<client>" task="<what you did>" skill=invoice-from-notes minutes=<n> files=<output file> outcome=<done|draft>`.
