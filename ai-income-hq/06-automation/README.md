# Automation (n8n) — AI Income HQ

Two workflows do 90% of the ops work. Both use connectors already in this repo (`../../workflows/`).

## 1) Order → Deliver + Tag (`order-delivery.json` starter included)
**Trigger:** storefront/Stripe webhook on new purchase.
**Steps:** parse order → email the buyer their download link → add/tag them in MailerLite by
product → (optional) post the sale to a private Slack/Telegram for you.
**Why:** instant fulfillment + builds the email list (your real asset) automatically.

## 2) Content → Schedule-Post
**Trigger:** new finished asset lands in a Drive/folder (or a row in a content sheet).
**Steps:** read asset + caption → schedule/post to TikTok, IG, YouTube, Pinterest → log to a
metrics sheet the COO Agent reads.
**Why:** turns the 30-day calendar into hands-off distribution.

## Build order
Start with #1 (fulfillment can't be manual once ads run). Add #2 when you're posting daily.
`order-delivery.json` is a minimal, importable starter — swap in your real credentials in n8n
and point the email/tag nodes at MailerLite.
