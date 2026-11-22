---
name: payment-chaser
description: Find overdue invoices and draft the right reminder email for each, following the late payment policy. Use when the user asks "who has not paid", "chase payments" or "check overdue invoices".
---

# Payment chaser

## Inputs
`context/invoices-log.csv`, `context/business.md` (policy), `context/clients.csv`, today's date.

## Steps
1. Get today's date from the computer (`date +%F`). Do not guess it.
2. Find rows with status `unpaid` and a due date before today. Count days overdue with a script, not in your head.
3. Show a table first: invoice, client, amount, due date, days overdue, level (1 friendly, 2 clear, 3 firm) from the policy in `business.md`.
4. For each one, check the client's notes in `clients.csv` and the inbox for a related thread (for example `inbox/email-thread-*.txt`). If the client already gave a reason or a promised date, mention it kindly.
5. Draft one email per invoice in `context/brand-voice.md` style. Always include: invoice number, invoice date, amount, due date, IBAN.
6. Save each as `outputs/<date>-chase-<invoice>.md`.
7. If Google is connected (level draft), offer to save each as a Gmail draft with `./kit google gmail draft ...`. Ask first. Never send.

## Rules
- Never threaten legal steps or extra costs. Sam decides that.
- Do not change any status. Only the user marks an invoice as paid.
- No overdue invoices? Say so and stop.

## Log
Last step: ask the user how many minutes this took them (optional), then run `./kit log add client="<client>" task="<what you did>" skill=payment-chaser minutes=<n> files=<output file> outcome=<done|draft>`.
