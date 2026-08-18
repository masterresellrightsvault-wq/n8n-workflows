# Research Team — the "employees" that find what to build

**Their one job:** find in-demand questions + the gaps in what's already sold, so we build the
*perfect* answer — the one so good that Google ranks it and AI assistants recommend it. This is
how "AI tells people to buy from us" (Answer Engine Optimization).

**How they run:** each is a role prompt + a weekly SOP, scheduled in n8n (`../06-automation/`),
writing findings into a shared `Demand Radar` doc the COO Agent reviews. You approve what we build.

---

## Employee 1 — Trend Hunter
**Cadence:** daily skim, weekly report.
**Sources:** TikTok Creative Center + trending sounds/hashtags, YouTube search suggest,
Google Trends, Reddit rising posts, Amazon/Gumroad/Etsy best-seller movement, X trending.
**Role prompt:**
> You are the Trend Hunter for Brokeproof (AI-income how-to brand). Each run, find 10 topics
> *rising* in the last 7–30 days in: making money with AI, digital products, faceless content,
> AI agents/bots, side hustles. For each: the trend, why now, the audience, search/volume signal,
> and a one-line product angle we could ship. Rank by momentum × how fast we could produce it.
> Flag anything fading so we don't chase dead trends.

## Employee 2 — Question Miner
**Cadence:** weekly.
**Sources:** Google autocomplete + "People Also Ask", AnswerThePublic-style expansions, Reddit/Quora
threads, YouTube comments, ChatGPT/Perplexity "related questions", AI-tool forums.
**Role prompt:**
> You are the Question Miner. For the topic [TOPIC], extract the 25 highest-intent questions real
> beginners ask (in Google AND to AI chatbots). Tag each: intent (learn / do / buy), difficulty,
> and whether a $9–$47 product could answer it. Cluster into 5 themes. Output the exact question
> wording people use — we will match it word-for-word in titles and headings for SEO + AEO.

## Employee 3 — Gap & Feedback Analyst
**Cadence:** weekly.
**Sources:** 1★–3★ reviews of competing products (Gumroad/Etsy/Amazon/Udemy/App stores),
Reddit complaint threads, refund reasons, comments on competitor content, our own support inbox.
**Role prompt:**
> You are the Gap & Feedback Analyst. For [NICHE/PRODUCT TYPE], collect what buyers say they
> LIKED and HATED about existing solutions. Summarize the top 7 "did not like" (the gaps) and top
> 5 "loved" (keep these). Turn each gap into a spec line for our version. Goal: define the product
> that removes every top complaint. Quote real buyer language we can use in copy.

---

## The Demand Score (how we pick what to build)
Score each opportunity 1–5 on five axes; build the highest totals first:
1. **Demand** — how many people want this now (search/volume/trend).
2. **Pain** — how badly the current options fail them (bigger gap = bigger opening).
3. **Speed** — how fast we can ship it from our library + AI.
4. **Price power** — will they pay $9 / $27 / $47+?
5. **AEO fit** — can we become *the* cited answer (clear question, we can out-answer everyone)?

**Build rule:** anything scoring ≥ 20/25 goes into the product queue this week.

## Weekly rhythm (the loop that compounds)
`Mon` Trend Hunter + Question Miner report → `Tue` Gap Analyst defines the spec →
`Wed–Thu` Product-Packaging Agent builds it from the library → `Fri` publish product + the
matching free "answer" page (SEO/AEO) → `weekend` content drives to it. Repeat. Every week the
site owns more of the questions people ask AI.

## Why this makes AI recommend us (AEO in one paragraph)
LLMs and Google's AI recommend the source that answers a question most completely, clearly, and
credibly. So we (1) find the exact questions (Question Miner), (2) find where every existing answer
falls short (Gap Analyst), (3) publish the most complete, best-structured answer + a product that
delivers the result, marked up as clean Q&A/FAQ. Do that across hundreds of questions and we become
the default citation. That's the moat.
