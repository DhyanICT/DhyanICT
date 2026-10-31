<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/hero-mobile-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/hero-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <img alt="Dhyan Patel. Applied AI and full-stack engineer. I build AI systems that show their work." src="assets/hero-light.svg" width="100%">
</picture>

Currently shipping SportX1 at [Next Play Games](https://github.com/Next-Play-Games).

[Projects](#user-content-selected-work) &nbsp; / &nbsp; [Experience](#user-content-production-experience) &nbsp; / &nbsp; [LinkedIn](https://www.linkedin.com/in/dhyan-patel-94101b22a/)

<br>

# <picture><img src="assets/section-mark.svg" width="24" height="24" alt=""></picture> Selected work

## TrustMed AI

Health questions, answered with cited evidence.

<a href="https://github.com/DhyanICT/Trusted_Medical_AI">
  <img src="assets/trustmed-flow.png" width="100%" alt="TrustMed AI workflow: a question retrieves medical evidence, which grounds an answer with citations.">
</a>

A medical Q&A assistant combining Neo4j, FAISS, and Llama 3.1 to generate cited answers while keeping trusted medical information separate from patient experiences.

Python &nbsp; · &nbsp; Neo4j &nbsp; · &nbsp; FAISS &nbsp; · &nbsp; Llama 3.1

[Code](https://github.com/DhyanICT/Trusted_Medical_AI) &nbsp; / &nbsp; [Evaluation](https://github.com/DhyanICT/Trusted_Medical_AI/tree/main/evaluations)

## Computer-Use Automation

Learn a browser task once. Replay it without an LLM.

<a href="https://github.com/DhyanICT/Computer-Use-Automation">
  <img src="assets/automation-flow.png" width="100%" alt="Computer-Use Automation workflow: discover a browser task, save a reusable artifact, and replay it deterministically.">
</a>

A Python system that learns browser tasks once and replays reusable workflows without an LLM, with policy checks, data redaction, and human handoff.

Python &nbsp; · &nbsp; Chrome DevTools Protocol

[Code](https://github.com/DhyanICT/Computer-Use-Automation) &nbsp; / &nbsp; [Design report](https://github.com/DhyanICT/Computer-Use-Automation/blob/main/REPORT.md)

# <picture><img src="assets/section-mark.svg" width="24" height="24" alt=""></picture> Production experience

## <picture><img src="assets/american-football.svg" width="36" height="36" alt=""></picture> [Next Play Games / SportX1](https://github.com/Next-Play-Games)

**Software Development Intern** &nbsp; · &nbsp; June 2026–present

Payments, team management and coach messaging across mobile, web and PostgreSQL.

<br>

# <picture><img src="assets/section-mark.svg" width="24" height="24" alt=""></picture> Core tools

TypeScript &nbsp; · &nbsp; Python &nbsp; · &nbsp; React<br>
React Native &nbsp; · &nbsp; PostgreSQL &nbsp; · &nbsp; Supabase

<br>

<details>
<summary><b>More projects and architecture</b></summary>

### More shipped work

**[Proofboard](https://github.com/DhyanICT/deepspace_proofboard)**. Real-time group decisions with a visible rationale: server-enforced one-vote-per-person in a Durable Object, live presence, and a two-browser Playwright suite. [Live](https://proofboard-dhyan.app.space)

**[Rules Quiz API](https://github.com/DhyanICT/nextplay-rules-fullstack)**. A TypeScript and Express API with Zod-validated endpoints and attempt scoring, tested with Jest and Supertest, plus a React (Vite) client and a React Native screen.

**[Task Board](https://github.com/DhyanICT/Task_Board_NextPlay)**. A Next.js 14 and Supabase Kanban board where anonymous sessions and row-level security keep each guest's tasks private, with drag and drop, search and priority filters. [Live](https://taskboard-gamma-ten.vercel.app/)

**[SparkScope](https://github.com/DhyanICT/Spark_Homes_Developer)**. An offline-first PWA for estimating repair costs during property walkthroughs. ZIP and Excel export are implemented in plain JavaScript with no dependencies, so exports work without a connection.

**[CycleSync](https://github.com/DhyanICT/CycleSync)**. A native Android (Java) cycle tracker with an offline chatbot that answers in English and Gujarati.

**[NYC taxi trip graph](https://github.com/DhyanICT/DPS1)**. A pipeline that cleans a month of NYC taxi trips from Parquet with pandas and loads them into Neo4j as a location graph using Cypher, uniqueness constraints and startup retries.

### Architecture and evaluation

- **TrustMed AI:** [System architecture and setup](https://github.com/DhyanICT/Trusted_Medical_AI#readme) · [Retrieval evaluation](https://github.com/DhyanICT/Trusted_Medical_AI/tree/main/evaluations)
- **Computer-Use Automation:** [Design report and tradeoffs](https://github.com/DhyanICT/Computer-Use-Automation/blob/main/REPORT.md)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/trustmed-retrieval-dark.svg">
  <img alt="TrustMed retrieval results on a 7-query ground-truth set: Precision at 5 is 74.3%, Recall at 15 is 87.5%, and F1 at 15 is 70.6%." src="assets/trustmed-retrieval-light.svg" width="100%">
</picture>

### More about my production work

**Software Development Intern**, full-time, June 2026 – present

SportX1 is a sports coaching and team-management platform. I work across its React Native app, React dashboard and Supabase/PostgreSQL backend, with **88 merged pull requests across five repositories** as of October 2026.

- **Registration and payments.** Square payments, installment plans, recurring invoices, coupons and audited cash and check payments. 142 targeted tests.
- **Organizations and teams.** Organization, group and team hierarchy with reassignment, multi-team membership, parent notifications and admin permissions.
- **AI personal trainer.** Training plans, habit tracking, progress, privacy-conscious sharing and server-validated XP. 74 focused tests.
- **Coach communication.** AI-assisted messaging, scheduled and recurring announcements, reply threads and reliable email delivery. 161 tests.
- **Reliability.** Database permissions, concurrency, migration ordering, and deploys that retry only on confirmed HTTP 409 conflicts.

**Stack.** TypeScript, React, React Native and Expo, Supabase, PostgreSQL, Square, GitHub Actions

### Capabilities

**Languages.** TypeScript, Python, JavaScript, SQL, Java, Cypher

**AI and retrieval.** RAG over knowledge graphs, embeddings (sentence-transformers), FAISS vector search, LLM agents and planners, retrieval evaluation (precision, recall, F1 at k)

**Backend.** Supabase (PostgreSQL, Auth, row-level security), FastAPI, Node.js, Express, REST API design, Zod validation, Square payments, Cloudflare Workers and Durable Objects

**Frontend and mobile.** React, React Native and Expo, Next.js, Vite, Tailwind CSS, Streamlit, Progressive Web Apps, Android (Java)

**Data.** PostgreSQL (schema design, migrations, permissions), Neo4j, pandas, Parquet, web scraping and ETL

**Testing and delivery.** Playwright, Jest, Supertest, Vitest, unittest, GitHub Actions deployment workflows, Chrome DevTools Protocol

### Recent GitHub activity

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/activity-dark.svg">
  <img alt="Recent GitHub contributions and top languages, refreshed weekly." src="assets/activity-light.svg" width="100%">
</picture>

<sub>Refreshed weekly by [a small script](scripts/generate_activity.py) in this repository.</sub>

</details>

<br>

[Connect on LinkedIn](https://www.linkedin.com/in/dhyan-patel-94101b22a/)
