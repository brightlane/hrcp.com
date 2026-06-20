# HRCP Prep Hub — hrcp.com

Independent affiliate SEO site for HRCP HR certification study materials. **1,570 pages in 16 languages**, built and deployed in under 5 seconds.

**Live site:** https://brightlane.github.io/hrcp.com/

---

## Setup (5 minutes)

1. Upload `build.py` to the **root** of the `brightlane/hrcp.com` repo
2. Create `.github/workflows/deploy.yml` from the provided file
3. **Settings → Pages → Source → GitHub Actions**
4. **Settings → Secrets and variables → Actions → New repository secret**
   - Name: `ANTHROPIC_API_KEY`
   - Value: your Anthropic API key (enables daily AI blog post)
5. Push to `main` — first build triggers automatically

> **First run:** The workflow deletes every existing file in the repo — all old JS, HTML, XML, JSON, sitemaps, robots.txt, and any other root files. Only `build.py` and `.github/` are preserved. The repo is rebuilt from scratch on every run. This is intentional.

---

## File Layout

```
repo root/
├── build.py          ← entire site generator (2,969 lines, pure Python 3)
├── README.md         ← this file
└── .github/
    └── workflows/
        └── deploy.yml  ← purges old files, builds, deploys (cron 07:00 UTC)
```

No npm. No pip installs. No dependencies. Runs on any Python 3.11+.

---

## What It Builds

| Category | Pages |
|---|---|
| EN general HR cert keywords | 30 |
| EN exam-specific (8 exams × 10 aspects) | 80 |
| EN career-level pages | 5 |
| EN industry-specific pages | 6 |
| EN US states (50 × 5 geo types) | 250 |
| EN US cities (100 cities × 5 geo types) | 500 |
| Spanish (ES) | 44 |
| Portuguese (PT) | 44 |
| French (FR) | 40 |
| German (DE) | 44 |
| Japanese (JA) | 40 |
| Korean (KO) | 40 |
| Arabic (AR) | 40 |
| Chinese (ZH) | 44 |
| Hindi (HI) | 44 |
| Italian (IT) | 40 |
| Dutch (NL) | 40 |
| Polish (PL) | 40 |
| Turkish (TR) | 42 |
| Indonesian (ID) | 43 |
| Vietnamese (VI) | 42 |
| Blog posts (61 seeds + daily AI) | 61 |
| Essential pages | 5 |
| **TOTAL** | **1,570** |

Build time: ~1–3 seconds. No dependencies.

---

## Languages & URL Structure

| Language | Path | Pages |
|---|---|---|
| English | `/guides/` | 873 |
| Spanish | `/es/guias/` | 44 |
| Portuguese | `/pt/guias/` | 44 |
| French | `/fr/guides/` | 40 |
| German | `/de/anleitungen/` | 44 |
| Japanese | `/ja/guides/` | 40 |
| Korean | `/ko/guides/` | 40 |
| Arabic | `/ar/guides/` | 40 |
| Chinese | `/zh/guides/` | 44 |
| Hindi | `/hi/guides/` | 44 |
| Italian | `/it/guide/` | 40 |
| Dutch | `/nl/gidsen/` | 40 |
| Polish | `/pl/przewodniki/` | 40 |
| Turkish | `/tr/rehberler/` | 42 |
| Indonesian | `/id/panduan/` | 43 |
| Vietnamese | `/vi/huong-dan/` | 42 |

Arabic pages include `dir="rtl"` on `<html>`. Every page carries `hreflang` alternate links for all 16 language variants.

International pages include **native-language content blocks** (42–51% of paragraph text in the target language) covering: why HRCP, main HR certifications, and study strategy. The intro sentence, CTA, and these three sections are fully native-language for all 15 non-English languages.

---

## HR Certifications Covered

| Credential | Issuer | Level | Exam Cost | HRCP Materials |
|---|---|---|---|---|
| aPHR | HRCI | Entry — no experience req. | $400 | $175 online / $195 print |
| PHR | HRCI | Mid-level | $495 | $295 online / $375 print |
| SPHR | HRCI | Senior | $495 | Same as PHR |
| SHRM-CP | SHRM | Mid-level | $300–$475 | $295 online |
| SHRM-SCP | SHRM | Senior | $300–$475 | Same as SHRM-CP |
| PHRi | HRCI | International | $495 | $295 online |
| SPHRi | HRCI | International Senior | $495 | Same as PHRi |
| GPHR | HRCI | Global | $495 | Included in PHR/SPHR program |

---

## SEO Features

### Schemas (per page where applicable)
- `Article` + `BreadcrumbList` + `FAQPage` + `WebPage` (Speakable) — all pages
- `SpeakableSpecification` — all pages (voice / AI assistant signal)
- `HowTo` with 5 named steps — how-to, study guide, and exam prep pages
- `VideoObject` — how-to and study guide pages
- `Review` with rating (4.8★) — review and HRCP-named pages
- `ItemList` — comparison and best-of pages
- `SoftwareApplication` (HRCP product) — all pages via entities schema
- `Organization` with `knowsAbout` (8 exam types) — homepage
- `SearchAction` (SiteLinksSearchBox) — homepage
- Named entity `mentions` for HRCI, SHRM, and HRCP on every Article schema

### Content quality
- **12 EN body variants** — prevents template fingerprinting across 873 pages
- **10 geo state body variants** — 10-way hash using `sh(slug + loc)` for true per-location distribution
- **6 geo city body variants** — city-specific content for 100 US cities
- **3 comparison body variants** — data, pros/cons, research framing
- **Niche body** — industry-specific content for healthcare, tech, nonprofit, government, manufacturing, finance
- **10 intl body variants** — per language, with 3 native-language content blocks per page
- **8 FAQ questions per page** — 8 category-specific pools × 8 questions (General, Exam Guide, Comparison, Products, How-To, Informational, Geo-State, Default)
- **6 blog post templates** — analysis, strategy, concise tips, long deep-dive, Q&A, numbered list — routed by post category
- **6 rotating EXTRA_SECTIONS** — requirements table, salary table, study tips, career path guide, exam day guide, empty (for shorter pages)
- **50 internal link anchors** — rotated per page; targets spread across guides AND blog posts
- **Category-specific meta description templates** — 4–6 distinct templates per category (Geo-State, Exam Guide, Comparison, How-To, etc.)
- **Pass rate stat (72% PHR)** visible on every page — E-E-A-T signal
- **Official sources citation box** — hrci.org, shrm.org, hrcp.com linked on every EN page
- **Author bar** with "Sources: HRCI, SHRM, PayScale" — freshness + authority signal
- **Word count displayed** in update badge on every page

### Technical SEO
- **Zero duplicate titles** across all 873 EN pages (unique_title dedup registry)
- **Google + Bing verification tags** in `hd()` — on every one of the 1,570 pages
- **Hreflang** on every page for all 16 languages
- **Category-specific meta descriptions** — no two pages use the same template
- **Canonical tags** — every page
- **OG + Twitter card** — every page
- **12 AI crawlers** explicitly allowed in robots.txt (GPTBot, ChatGPT-User, Claude-Web, anthropic-ai, PerplexityBot, Google-Extended, Googlebot, Bingbot, Applebot, Twitterbot, LinkedInBot, FacebookBot)
- **llms.txt** — machine-readable site catalog for AI indexing (includes all 8 certs, pricing, study tips)
- **RSS feed** — `/blog/rss.xml`
- **XML sitemap** — 1,586 URLs with priority and changefreq

---

## Affiliate

All CTAs link to:
```
https://www.linkconnector.com/ta.php?lc=007949120619007379&atid=HRCPWebs
```

---

## Verification Tags

Appear in `hd()` — fired on every one of the 1,570 pages:

```
Google: eWVDN3vbam9nnaZQu7wAQKyfmJJdM7zjI80l4DGeUrQ
Bing:   574044E39556B8B8DAAF1D1F233C87B0
```

---

## Geo Coverage

**US States:** All 50 × 5 keyword types = 250 pages

**US Cities:** 100 major HR markets × 5 keyword types = 500 pages

**5 geo keyword types per location:**
`hr-certification-prep` · `phr-study-guide` · `shrm-certification` · `hr-certification-classes` · `aphr-certification`

Each geo page includes: local exam location info (Pearson VUE / Prometric / remote proctoring), cost breakdown, which credentials are right for that career stage, and the HRCP pass-or-money-back guarantee.

**International keyword extras by language:**
- Chinese (ZH): HR certification in China, SHRM China, GPHR for Chinese HR professionals
- Hindi (HI): HR certification in India, SHRM India, PHRi for Indian HR professionals
- Spanish (ES): GPHR for LATAM, PHRi internacional, SHRM en español
- Portuguese (PT): Certificação RH Brasil, PHRi Brasil, SHRM-CP Brasil
- German (DE): HR Zertifizierung Deutschland, GPHR/SHRM Zertifizierung
- Indonesian (ID): Sertifikasi HR Indonesia, PHRi Indonesia
- Vietnamese (VI): Chứng Chỉ HR Việt Nam, PHRi Việt Nam
- Turkish (TR): HR Sertifikası Türkiye, GPHR uluslararası

---

## Content Architecture

### Exam Guide Pages (80 pages)
8 exams × 10 aspects:

**Exams:** aPHR, PHR, SPHR, SHRM-CP, SHRM-SCP, PHRi, SPHRi, GPHR

**Aspects:** study-guide, practice-test, study-materials, exam-prep, pass-rate, requirements, vs (comparison), review, cost, flashcards

### Career-Level Pages
- HR Coordinator Certification
- HR Manager Certification
- HR Director Certification
- HR Business Partner Certification
- Entry Level HR Certification

### Industry Pages
Healthcare, Technology, Nonprofit, Government, Manufacturing, Finance

### Blog (61 posts)
**6 templates** routed by category:
- Comparison/Review → long deep-dive (~1,600 words) or Q&A format
- Study Guide → numbered action list or deep-dive
- Study Tips → concise tips (~700 words) or numbered list
- Analysis → data-driven or Q&A
- Informational → rotating formats

**61 topics** covering: aPHR vs PHR, PHR study guide, HRCP review, SHRM-CP vs PHR, pass rates, study schedules, exam day tips, salary impact, recertification, and more.

---

## Daily Rebuild

GitHub Actions rebuilds the entire 1,570-page site daily at **07:00 UTC**. The workflow:

1. Deletes all old files (preserves only `build.py` and `.github/`)
2. Commits the clean state
3. Runs `python build.py` (~2 seconds)
4. Deploys fresh `output/` to GitHub Pages

`ANTHROPIC_API_KEY` enables a fresh daily AI blog post via `claude-sonnet-4-6`. Falls back to 61 rotating seed topics if API is unavailable — the site always deploys successfully.

---

## Audit Results (last build)

| Metric | Result |
|---|---|
| Total pages | 1,570 |
| EN keyword pages | 873 |
| Duplicate titles | 0 |
| Title max length | 68 chars |
| Body variant top (max %) | 11.2% |
| Distinct H2 openings | 553 |
| HowTo schema on prep pages | ✓ all |
| Review schema on review pages | ✓ all |
| SpeakableSpec on all pages | 100% |
| FAQPage on all pages | 100% |
| FAQ per page | 8 questions |
| 14 schema types on 100% pages | ✓ |
| Tables per page | 0.86 avg |
| Pages with comparison table | 71% |
| WC range | 4,353–5,062 |
| WC spread | 709 words |
| Blog H2 distinct templates | 6 |
| Blog WC spread | 498 words |
| Intl native language content | 42–51% |
| hrci.org cited | 50/50 |
| shrm.org cited | 50/50 |
| Affiliate link on all pages | 100% |
| Google verification all pages | 100% |
| Bing verification all pages | 100% |
| Internal link distinct targets | 45+ |
| Sitemap URLs | 1,586 |
| robots.txt AI crawlers | 12 agents |
| Build time | ~2 seconds |
