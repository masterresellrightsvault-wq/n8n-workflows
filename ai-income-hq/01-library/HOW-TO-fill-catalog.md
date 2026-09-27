# How the library catalog works

**You don't fill this by hand.** Drop your packs in the Google Drive folder and I auto-build
the catalog by reading the folder. This file explains the columns and the license rules so you
can sanity-check my output.

## Column guide
- **license_type** — the most important column. One of:
  - `PLR` (Private Label Rights) — usually resell **and** rebrand/edit. Best for us.
  - `MRR` (Master Resell Rights) — resell as-is, often can't edit; sometimes buyer gets resell too.
  - `RR` (Resell Rights) — resell as-is, no edits, can't pass resell rights on.
  - `Personal-use only` — **NEVER sell.** Skip.
  - `Unknown` — treat as **do-not-sell** until you find the license file. I'll flag these.
- **resale_ok / rebrand_ok** — yes/no derived from the license. If unknown → no.
- **curate_decision** — `CURATE` (make it a product) or `SKIP`.
- **bundle_target** — which hero bundle this piece rolls into.

## The license guardrail (protects Stripe + your store)
Selling packs you don't have rights to = chargebacks, DMCA takedowns, and a frozen Stripe
account. Rule: **if the license file isn't in the pack, it doesn't get sold** until you confirm
rights with the original seller. I flag every `Unknown`; you decide.

## The curation rule
We use **~2–3%** of the whole library. A store with 40 sharp, rebranded, outcome-named products
outsells one with 4,000 raw PLR files every single time — and it's the only version Google ranks.

## What I do once your Drive folder is shared
1. List every pack + format + item count → fill `library-catalog.csv`.
2. Best-guess the license from filenames/included docs → you confirm the `Unknown`s.
3. Rank by quality + demand → propose the first 3–5 hero bundles.
4. Build those products in `../02-products/` with new covers + rewritten copy.
