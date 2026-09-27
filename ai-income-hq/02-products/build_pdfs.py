#!/usr/bin/env python3
"""Income HQ — branded PDF product generator (The Anti-PLR Standard)."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Table, TableStyle, ListFlowable, ListItem)
from reportlab.lib.enums import TA_LEFT

OUT = os.path.join(os.path.dirname(__file__), "pdf")
os.makedirs(OUT, exist_ok=True)

ORANGE   = HexColor("#E2601F")
ORANGE_D = HexColor("#C2490D")
INK      = HexColor("#191A1D")
SOFT     = HexColor("#5A5D64")
LINE     = HexColor("#E4E2DD")
WASH     = HexColor("#FBEDE4")   # light orange callout bg
PAPER    = HexColor("#F7F5F1")
WHITE    = HexColor("#FFFFFF")

styles = getSampleStyleSheet()
def S(name, **kw):
    kw.setdefault("parent", styles["Normal"])
    return ParagraphStyle(name, **kw)

H2   = S("H2", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=ORANGE_D,
         spaceBefore=18, spaceAfter=7)
H3   = S("H3", fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=INK,
         spaceBefore=10, spaceAfter=3)
BODY = S("Body", fontName="Helvetica", fontSize=10.5, leading=15.5, textColor=INK,
         spaceAfter=7, alignment=TA_LEFT)
BULL = S("Bull", parent=BODY, spaceAfter=3)
LEDE = S("Lede", fontName="Helvetica-Oblique", fontSize=12, leading=17, textColor=SOFT,
         spaceAfter=10)
ACT  = S("Act", fontName="Helvetica-Bold", fontSize=10.5, leading=15, textColor=INK)
CAP  = S("Cap", fontName="Helvetica", fontSize=8.5, leading=11, textColor=SOFT)

USABLE = letter[0] - 1.5*inch

def cover_fn(title, subtitle, tag):
    def draw(c, doc):
        w, h = letter
        c.setFillColor(PAPER); c.rect(0, 0, w, h, fill=1, stroke=0)
        # top orange band
        c.setFillColor(ORANGE); c.rect(0, h-2.5*inch, w, 2.5*inch, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 20); c.drawString(0.75*inch, h-1.15*inch, "INCOME HQ")
        c.setFont("Helvetica-Bold", 9)
        c.drawString(0.75*inch, h-1.45*inch, "THE ANTI-PLR STANDARD")
        # seal
        c.setStrokeColor(WHITE); c.setLineWidth(1.5)
        c.roundRect(w-1.55*inch, h-1.4*inch, 0.8*inch, 0.8*inch, 8, fill=0, stroke=1)
        c.setFont("Helvetica-Bold", 22); c.drawCentredString(w-1.15*inch, h-1.12*inch, "IH")
        # tag
        c.setFillColor(ORANGE_D); c.setFont("Helvetica-Bold", 9)
        c.drawString(0.75*inch, h-3.15*inch, tag.upper())
        # title
        c.setFillColor(INK)
        tsize = 34 if len(title) < 34 else 27
        c.setFont("Helvetica-Bold", tsize)
        y = h-3.75*inch
        # simple word-wrap
        words, line, lines = title.split(), "", []
        maxw = w-1.5*inch
        for wd in words:
            test = (line+" "+wd).strip()
            if c.stringWidth(test, "Helvetica-Bold", tsize) > maxw:
                lines.append(line); line = wd
            else:
                line = test
        lines.append(line)
        for ln in lines:
            c.drawString(0.75*inch, y, ln); y -= tsize+6
        # subtitle
        c.setFillColor(SOFT); c.setFont("Helvetica", 13)
        y -= 6
        words, line, lines = subtitle.split(), "", []
        for wd in words:
            test = (line+" "+wd).strip()
            if c.stringWidth(test, "Helvetica", 13) > maxw:
                lines.append(line); line = wd
            else:
                line = test
        lines.append(line)
        for ln in lines:
            c.drawString(0.75*inch, y, ln); y -= 18
        # footer
        c.setStrokeColor(LINE); c.setLineWidth(1)
        c.line(0.75*inch, 0.95*inch, w-0.75*inch, 0.95*inch)
        c.setFillColor(SOFT); c.setFont("Helvetica", 9)
        c.drawString(0.75*inch, 0.72*inch, "incomehq  ·  done-for-you products that actually work")
    return draw

def footer(c, doc):
    w, h = letter
    c.setStrokeColor(LINE); c.setLineWidth(0.8)
    c.line(0.75*inch, 0.7*inch, w-0.75*inch, 0.7*inch)
    c.setFillColor(SOFT); c.setFont("Helvetica", 8)
    c.drawString(0.75*inch, 0.52*inch, "INCOME HQ · The Anti-PLR Standard")
    c.drawRightString(w-0.75*inch, 0.52*inch, "%d" % doc.page)

def action(text):
    t = Table([[Paragraph("→  "+text, ACT)]], colWidths=[USABLE])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),WASH),
        ("LINEBEFORE",(0,0),(0,-1),3,ORANGE),
        ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
        ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
    ]))
    return t

def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(i, BULL), leftIndent=6, value="•") for i in items],
        bulletType="bullet", bulletColor=ORANGE, leftIndent=14, spaceAfter=8)

def render(block):
    kind = block[0]
    if kind == "lede":   return [Paragraph(block[1], LEDE)]
    if kind == "h2":     return [Paragraph(block[1], H2)]
    if kind == "h3":     return [Paragraph(block[1], H3)]
    if kind == "body":   return [Paragraph(block[1], BODY)]
    if kind == "bullets":return [bullets(block[1])]
    if kind == "action": return [action(block[1]), Spacer(1, 6)]
    if kind == "break":  return [PageBreak()]
    return []

def build(filename, title, subtitle, tag, blocks):
    path = os.path.join(OUT, filename)
    doc = SimpleDocTemplate(path, pagesize=letter,
                            leftMargin=0.75*inch, rightMargin=0.75*inch,
                            topMargin=0.9*inch, bottomMargin=0.9*inch,
                            title=title, author="Income HQ")
    story = [PageBreak()]
    for b in blocks:
        story += render(b)
    doc.build(story, onFirstPage=cover_fn(title, subtitle, tag), onLaterPages=footer)
    print("built", path)

# ---------------------------------------------------------------- content

P1 = [
 ("lede","The honest, plain-English answer to the five questions every beginner asks — plus the exact 14-day plan to your first sale. No code. No big budget."),
 ("h2","The 5 questions, answered straight"),
 ("h3","1. Where do I even start?"),
 ("body","With ONE thing you can sell. Not a course, not a funnel, not a logo. A simple digital product (a guide, a template, a prompt pack) that solves one specific problem for one specific person. You'll pick it on Day 1 below."),
 ("h3","2. Do I need to be technical or know how to code?"),
 ("body","No. Everything in this guide is copy, paste, and click. The AI does the heavy lifting; free no-code tools handle the rest."),
 ("h3","3. How much can I realistically make, and how fast?"),
 ("body","Be realistic and you'll actually get there. Most beginners see their first $250–$500 within a few weeks. With a small email list of 1,500–2,000 people in a niche, a $37–$67 product can do around $1,000 in a launch week. Slow is normal. Quitting is the only real failure."),
 ("h3","4. Can I start with no money?"),
 ("body","Yes. Free AI tools, a free storefront, and a free email tool are enough to make your first sales. You reinvest profit later — never rent you don't have."),
 ("h3","5. How long until I see results?"),
 ("body","If you ship something in the next 14 days and put it in front of people, weeks — not months. The people who wait for 'perfect' are the ones who never get paid."),
 ("break",),
 ("h2","Your 14-day plan to the first sale"),
 ("h3","Days 1–2 · Pick your lane"),
 ("body","Choose one niche you can speak to and one problem inside it. Write it as: 'I help [who] do [what].' Example: 'I help busy parents plan meals in 20 minutes a week.'"),
 ("action","Finish this sentence today: I help ______ do ______."),
 ("h3","Days 3–5 · Make one simple product"),
 ("body","Use AI to draft a short, genuinely useful guide, planner, checklist, or prompt pack that solves that one problem. Keep it tight — 5 to 20 pages of real value beats 100 pages of filler."),
 ("h3","Days 6–7 · Package it"),
 ("body","Give it a benefit-driven title, a clean cover, and a price. Start with a $9 'tripwire' — cheap enough to be an easy yes, valuable enough to build trust."),
 ("h3","Days 8–10 · Set up the shop"),
 ("body","Create a free Stan Store or Payhip page, connect Stripe/PayPal, and upload your product for instant delivery. Add a short sales description: the problem, the promise, what's inside, and a clear button."),
 ("h3","Days 11–14 · Get it in front of people"),
 ("body","Post 3 short pieces of content a day about the problem you solve, each ending with a link to your $9 offer. Tell your existing contacts. Answer questions where your buyers already hang out."),
 ("action","Ship the product and make it public by Day 14 — even if it feels 80% ready. You'll improve it from real feedback."),
 ("break",),
 ("h2","Pick your income model"),
 ("bullets",[
   "<b>Digital products</b> — sell guides, templates, and packs once, deliver forever. Best first model.",
   "<b>Faceless content</b> — grow an audience with short videos, sell products to it.",
   "<b>Freelance with AI</b> — offer a done-for-you service (content, design, automations) and let AI make you fast.",
   "<b>Affiliate</b> — recommend tools you use and earn a cut; great add-on once you have an audience."]),
 ("h2","Free tools to start (zero budget)"),
 ("bullets",[
   "<b>AI:</b> ChatGPT, Claude, or Gemini — free tiers are plenty to begin.",
   "<b>Store:</b> Stan Store or Payhip — instant digital delivery + checkout.",
   "<b>Email:</b> MailerLite or Beehiiv — build the list that becomes your real asset.",
   "<b>Design:</b> Canva free — covers, mockups, and simple graphics."]),
 ("h2","The 5 mistakes that keep beginners broke"),
 ("bullets",[
   "Learning forever and never shipping. Ship first, learn from sales.",
   "Building for 'everyone.' Narrow it down — one person, one problem.",
   "Pricing from fear. A $9 yes beats a $99 maybe. Start small, climb later.",
   "No email capture. Every visitor should have a way to join your list.",
   "Quitting at week 3. The first sale is the hardest; it gets easier fast."]),
 ("h2","Your next step"),
 ("body","You now have the plan. Pick your lane today, and let the next 14 days do the work. When you're ready to move faster, the Income HQ store has done-for-you products, prompt packs, and AI employees that hand you the shortcuts — the Anti-PLR Standard, always ready to sell."),
 ("action","Do the very first line now: I help ______ do ______. Everything starts there."),
]

P2 = [
 ("lede","The AI skills people are paying to learn right now — what each one is, why it pays, and the fastest way to start. Pick one, get good enough to sell it, then add the next."),
 ("h2","How to use this pack"),
 ("body","You don't need all of these. Pick the ONE that fits your lane, do its 'first practice task,' and you'll be more capable than most people selling these services today. Come back for the next skill when you're ready to expand."),
 ("break",),
 ("h2","1. Prompt engineering"),
 ("body","<b>What it is:</b> getting reliable, high-quality output from AI by writing clear, structured instructions.<br/><b>Why it pays:</b> it's the foundation of every other skill — and businesses pay for prompt libraries and setups that just work."),
 ("action","First task: rewrite a vague prompt into role + task + format + example. Compare the results."),
 ("h2","2. AI content creation"),
 ("body","<b>What it is:</b> using AI to produce posts, scripts, emails, and articles that sound human and convert.<br/><b>Why it pays:</b> every brand needs endless content and hates writing it."),
 ("action","First task: turn one idea into a TikTok script, an email, and a carousel — keeping one consistent message."),
 ("h2","3. AI automation (no-code)"),
 ("body","<b>What it is:</b> connecting apps with tools like n8n, Make, or Zapier so tasks run themselves.<br/><b>Why it pays:</b> you sell businesses back their time — one automation can be worth hundreds a month."),
 ("action","First task: build a flow that emails you whenever a form is filled in."),
 ("h2","4. Building AI agents & 'employees'"),
 ("body","<b>What it is:</b> assembling AI that performs a role — a research agent, a support agent, a content agent.<br/><b>Why it pays:</b> 'AI employees' are the hottest product category; people buy ready-made ones."),
 ("action","First task: write a one-paragraph role prompt for a 'research assistant' and test it on a real question."),
 ("h2","5. AI image & design"),
 ("body","<b>What it is:</b> generating on-brand covers, mockups, thumbnails, and ads with AI image tools.<br/><b>Why it pays:</b> good visuals sell products and content; most beginners have none."),
 ("action","First task: generate three product-cover options in one consistent style."),
 ("h2","6. SEO & AEO (getting found by Google and AI)"),
 ("body","<b>What it is:</b> structuring content so search engines rank it and AI assistants quote it.<br/><b>Why it pays:</b> free, compounding traffic is the cheapest customer acquisition there is."),
 ("action","First task: write one page that answers a real question as a clean Q&A with an FAQ section."),
 ("h2","7. AI video"),
 ("body","<b>What it is:</b> creating short-form and faceless video with AI voice, clips, and captions.<br/><b>Why it pays:</b> video is the #1 way to grow an audience fast."),
 ("action","First task: script and storyboard one 30-second faceless video."),
 ("h2","8. Selling & offers"),
 ("body","<b>What it is:</b> packaging value into an irresistible offer and writing copy that converts.<br/><b>Why it pays:</b> the best product with a weak offer makes nothing; this multiplies everything else."),
 ("action","First task: write a price ladder — free lead magnet, $9, $27, $47 bundle — for your niche."),
 ("h2","Where to go next"),
 ("body","Learn by shipping. Pick a skill, do the task, then sell a small product built on it. Income HQ's store gives you done-for-you templates for each of these so you can deliver before you're an expert — the Anti-PLR way."),
]

P3 = [
 ("lede","Ten plug-in AI 'employees' you can put to work today. Each one comes with what it does and a ready-to-paste role prompt. Copy it into ChatGPT, Claude, or Gemini and fill the [brackets]."),
 ("h2","How to hire an AI employee"),
 ("body","Paste the role prompt into your AI as the first message, replace the [brackets], and give it the task. To make it permanent, save it as a custom GPT / Project so it remembers its job. Start with one; add more as you grow."),
 ("break",),
 ("h2","1. The Content Employee"),
 ("body","Writes your short-form scripts, captions, and carousels on demand."),
 ("action","Prompt: 'You are my Content Employee for [BRAND], a [NICHE] business. Voice: warm, plain-English, one CTA per piece. When I give you a topic, output a TikTok script, an IG carousel, and a caption with 5 hashtags. Never use hype or false claims.'"),
 ("h2","2. The SEO/AEO Employee"),
 ("body","Finds keywords and writes pages Google ranks and AI assistants cite."),
 ("action","Prompt: 'You are my SEO/AEO Employee. For the topic [TOPIC], give 10 long-tail question keywords, then write a page outline (title, H2s, FAQ schema questions, internal links, and the product CTA).'"),
 ("h2","3. The DM Closer"),
 ("body","Turns comments and DMs into sales without being pushy."),
 ("action","Prompt: 'You are my DM Closer. When someone comments [KEYWORD] on my post about [PRODUCT], write a warm, helpful reply that leads with value and ends with a soft link to [OFFER]. No pressure, no spam.'"),
 ("h2","4. The Research Employee"),
 ("body","Digs up trends, questions, and competitor gaps so you build what sells."),
 ("action","Prompt: 'You are my Research Employee. For [NICHE], list the 15 questions beginners ask most, the top 5 complaints about existing products, and 5 product ideas that fix those complaints.'"),
 ("h2","5. The Support Employee"),
 ("body","Answers customer questions and drafts refund replies kindly and fast."),
 ("action","Prompt: 'You are my Support Employee for [BRAND]. Reply to this customer message in a friendly, helpful tone. Resolve simple issues; for refunds, draft a kind reply and flag it for me to approve: [MESSAGE].'"),
 ("h2","6. The Offer Employee"),
 ("body","Builds irresistible offers and price ladders."),
 ("action","Prompt: 'You are my Offer Employee. For [NICHE], build a price ladder (free, $9, $27, $47 bundle, $97/mo) with a name and one-line promise for each rung.'"),
 ("h2","7. The Email Employee"),
 ("body","Writes welcome sequences and promo emails that sell."),
 ("action","Prompt: 'You are my Email Employee. Write a 5-email welcome sequence for [NICHE]: deliver the freebie, build trust with quick wins, then pitch [PRODUCT]. Short, friendly, one CTA each.'"),
 ("h2","8. The Launch Employee"),
 ("body","Plans a simple product launch you can actually execute solo."),
 ("action","Prompt: 'You are my Launch Employee. Give me a 7-day launch plan for [PRODUCT] at $[PRICE]: daily content angle, email, and CTA, building to launch day.'"),
 ("h2","9. The Repurpose Employee"),
 ("body","Turns one idea into a week of content across platforms."),
 ("action","Prompt: 'You are my Repurpose Employee. Turn this idea: [IDEA] into a TikTok, an IG carousel, a Pinterest pin, a tweet, and an email subject line — one consistent message.'"),
 ("h2","10. The COO (oversees the rest)"),
 ("body","Reviews your numbers, flags what's wrong, and tells you the next move."),
 ("action","Prompt: 'You are my COO. Here are today's numbers: [PASTE sales, traffic, email, ads]. Give me a 5-line status, a ranked \\'needs attention\\' list, and for each issue a fix marked SAFE-TO-DO or ASK-ME-FIRST.'"),
 ("h2","Build your team"),
 ("body","Start with the Content and Research employees — they feed everything else. Add the rest as you grow. Want them pre-built and connected so they run on a schedule? That's what the Income HQ membership sets up for you."),
]

P4 = [
 ("lede","Ten automations that quietly run your business while you sleep. Each shows the trigger, the action, the tools, and how to set it up. Start with #1 — you can't fulfil orders by hand once traffic hits."),
 ("h2","Before you start"),
 ("body","You'll use a free no-code tool — n8n, Make, or Zapier — to connect your apps. Each automation below is a simple 'when this happens, do that.' Build one, test it, turn it on, move to the next."),
 ("break",),
 ("h2","1. Instant order delivery"),
 ("body","<b>Trigger:</b> new purchase. <b>Action:</b> email the buyer their download + tag them in your email tool. <b>Tools:</b> Stripe/store webhook → email → MailerLite."),
 ("action","Set up first: fulfilment must be automatic before you run any ads."),
 ("h2","2. Lead capture → welcome"),
 ("body","<b>Trigger:</b> someone grabs your freebie. <b>Action:</b> deliver it and start the 5-email welcome sequence. <b>Tools:</b> form → email automation."),
 ("h2","3. Social scheduler"),
 ("body","<b>Trigger:</b> a finished post lands in a folder or sheet. <b>Action:</b> publish/schedule it to TikTok, IG, YouTube, and Pinterest. <b>Tools:</b> Drive/Sheet → n8n → social APIs."),
 ("h2","4. Abandoned-cart rescue"),
 ("body","<b>Trigger:</b> checkout started, not finished. <b>Action:</b> send a 3-email nudge handling the top objection. <b>Tools:</b> store webhook → email."),
 ("h2","5. Review / testimonial request"),
 ("body","<b>Trigger:</b> 3 days after delivery. <b>Action:</b> ask for a testimonial with 3 easy questions. <b>Tools:</b> delay → email."),
 ("h2","6. Content repurposer"),
 ("body","<b>Trigger:</b> you save a new idea. <b>Action:</b> AI turns it into 5 formats and drops them in your content sheet. <b>Tools:</b> Sheet → AI node → Sheet."),
 ("h2","7. New-sale alert"),
 ("body","<b>Trigger:</b> any sale. <b>Action:</b> ping your phone (Telegram/Slack) with the amount and product. <b>Tools:</b> webhook → messenger. (Great for motivation.)"),
 ("h2","8. Daily metrics digest"),
 ("body","<b>Trigger:</b> every morning. <b>Action:</b> pull sales, traffic, and email stats into one message your COO employee reviews. <b>Tools:</b> schedule → APIs → message."),
 ("h2","9. Affiliate / referral tracker"),
 ("body","<b>Trigger:</b> referred sale. <b>Action:</b> log it and credit the referrer. <b>Tools:</b> store → sheet/CRM."),
 ("h2","10. Weekly demand scan"),
 ("body","<b>Trigger:</b> every Monday. <b>Action:</b> collect trending questions and competitor complaints into a 'build-next' list. <b>Tools:</b> schedule → AI research → sheet."),
 ("h2","Turn it on"),
 ("body","Build #1 today; add one per week. Within two months your store fulfils, follows up, posts, and reports on its own — that's leverage. Want these pre-built and wired to your store? The Income HQ membership installs them for you."),
]

build("01-start-making-money-with-ai.pdf",
      "Start Making Money With AI",
      "No code. No big budget. The exact first 14 days to your first sale.",
      "AI Income · Beginner", P1)
build("02-in-demand-ai-skills-pack.pdf",
      "In-Demand AI Skills Pack",
      "The 8 AI skills people pay to learn — and the fastest way to start each.",
      "Skills · Career", P2)
build("03-ai-employees-plug-in-agents.pdf",
      "AI Employees: Plug-In Agents",
      "10 ready-to-paste AI workers that write, sell, and research for you.",
      "Agents · Automation", P3)
build("04-automations-that-run-your-business.pdf",
      "Automations That Run Your Business",
      "10 set-and-forget systems that fulfil, follow up, and post while you sleep.",
      "Automations · Systems", P4)
print("ALL DONE")
