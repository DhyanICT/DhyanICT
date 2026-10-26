<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <img alt="Dhyan Patel, applied AI and full-stack engineer. I build AI systems that show their work." src="assets/hero-light.svg" width="100%">
</picture>

I'm a software engineer working where applied AI meets full-stack product. I build systems whose output can be checked: a GraphRAG medical assistant that cites every source and ships with its own evaluation harness, a computer-use agent that turns one LLM-guided run into a replayable, policy-checked artifact, and real-time web apps deployed with end-to-end tests.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-dhyan--patel-0F1B2D?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/dhyan-patel-94101b22a/)
<!-- TODO: uncomment once filled in
[![Email](https://img.shields.io/badge/Email-you%40example.com-0F1B2D?style=flat-square&logo=maildotru&logoColor=white)](mailto:you@example.com)
[![Portfolio](https://img.shields.io/badge/Portfolio-yourdomain.dev-0F1B2D?style=flat-square&logo=googlechrome&logoColor=white)](https://yourdomain.dev)
[![Resume](https://img.shields.io/badge/Resume-PDF-0F1B2D?style=flat-square&logo=readthedocs&logoColor=white)](https://yourdomain.dev/resume.pdf)
-->

```console
$ whoami
Dhyan Patel
applied AI and full-stack engineer

$ focus --now
agentic automation, RAG,
real-time web apps

$ stack --strongest
Python, TypeScript, React,
FastAPI, Node.js, Neo4j

$ open-to
software, full-stack and
applied AI engineering roles
```

<!-- TODO (recommended): add 2–3 lines of real experience here, e.g.
## Experience
**Role, Company** (Month YYYY – Month YYYY). One line on what you shipped and its result.
-->

## Featured engineering work

<a href="https://github.com/DhyanICT/Trusted_Medical_AI">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/plate-trustmed-dark.svg">
  <img alt="TrustMed AI: medical Q&A grounded in a knowledge graph, with citations. Recall at 15: 87.5%." src="assets/plate-trustmed-light.svg" width="100%">
</picture>
</a>

**Problem.** General-purpose chatbots answer health questions without showing where the answer came from, and blend vetted guidance with anecdote.

**What I built.** An assistant that retrieves from a Neo4j knowledge graph of disease and drug monographs plus semantically indexed patient discussions, then has Llama 3.1 8B write a sectioned answer that cites each source and labels it as trusted or community.

**The hard part.** Keeping anecdote from leaking into medical guidance. A FAISS disease index first detects which conditions the question is about, retrieval is filtered to those conditions, and every chunk carries its provenance into the prompt so the model can separate the two kinds of evidence. Community posts are tagged with recurring themes before indexing.

**Evidence.** An evaluation harness with hand-labelled ground truth, citation-presence checks and end-to-end completeness tests. Warm retrieval averages about 30 ms.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/trustmed-retrieval-dark.svg">
  <img alt="Retrieval quality on a 7-query ground-truth set. Top 5: precision 74.3, recall 77.7, F1 74.4. Top 10: 68.6, 81.3, 68.9. Top 15: 69.5, 87.5, 70.6." src="assets/trustmed-retrieval-light.svg" width="100%">
</picture>

**Stack.** Python, FastAPI, Streamlit, Neo4j and Cypher, FAISS, sentence-transformers, Hugging Face Inference

[Code](https://github.com/DhyanICT/Trusted_Medical_AI) &nbsp;/&nbsp; [Evaluation guide](https://github.com/DhyanICT/Trusted_Medical_AI/blob/main/EVALUATION_GUIDE.md)

<details>
<summary><b>Architecture</b></summary>

```mermaid
flowchart TB
  S[Disease, drug and Reddit scrapers] --> T[Theme tagger]
  T --> KG[(Neo4j graph)]
  KG --> IDX[FAISS indexes]
  Q[Question via Streamlit and FastAPI] --> DD[Disease detection]
  IDX --> DD
  DD --> R[Filtered top-k retrieval]
  IDX --> R
  R --> LLM[Llama 3.1 8B]
  LLM --> A[Sectioned answer with citations]
```

</details>

<br>

<a href="https://github.com/DhyanICT/Computer-Use-Automation">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/plate-cua-dark.svg">
  <img alt="Computer-Use Automation: an agent learns a UI task once; replays run without an LLM." src="assets/plate-cua-light.svg" width="100%">
</picture>
</a>

**Problem.** Legacy back-office software rarely has an API, and letting an LLM decide every click is slow, costly and hard to audit.

**What I built.** A Python system that runs one LLM-guided discovery pass against a UI, saves the successful run as a typed capability artifact (`cua.capability.v1`), and replays it deterministically with new parameters and no model in the loop.

**The hard part.** Making replay robust and safe. Steps target elements semantically (visible text, row label, nearby text) and keep CSS paths only as hints. Business outcomes such as `member_not_found` are reported separately from failures. An origin and action allowlist, log redaction, and a human-handoff seam pause before risky actions and resume in the same browser session.

**Evidence.** The browser controller speaks the Chrome DevTools Protocol directly, with no third-party packages. Every run writes JSONL logs, screenshots and DOM snapshots, and unit tests cover policy, redaction, parameter templating and the artifact schema.

**Stack.** Python, Chrome DevTools Protocol, OpenAI-compatible LLM API, unittest

[Code](https://github.com/DhyanICT/Computer-Use-Automation) &nbsp;/&nbsp; [Design report](https://github.com/DhyanICT/Computer-Use-Automation/blob/main/REPORT.md)

<details>
<summary><b>Architecture</b></summary>

```mermaid
flowchart LR
  G[Goal and typed params] --> P[Planner: LLM or offline scripted]
  P <--> B[CDP browser controller]
  B --> A[(Capability artifact)]
  A --> RP[Deterministic replay]
  RP --> POL{Policy}
  POL -->|allowed| OUT[Structured result and evidence]
  POL -->|risky action| H[Human handoff]
  H -->|resume| RP
```

</details>

<br>

<a href="https://github.com/DhyanICT/deepspace_proofboard">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/plate-proofboard-dark.svg">
  <img alt="Proofboard: real-time group decisions with a visible rationale. 14 tests, deployed." src="assets/plate-proofboard-light.svg" width="100%">
</picture>
</a>

**Problem.** Group decisions get made in chat threads, and the reasoning behind them disappears.

**What it does.** A shared board where a group frames a question, adds options, attaches reasons for and against with source links, votes once (and can change that vote), and records the outcome. Everyone sees options, reasons, vote counts and who is viewing, live.

**The hard part.** Integrity under concurrent edits. One ballot per person per board is enforced server-side in a Durable Object, not in the UI, and the client waits for confirmed writes so it never shows a vote the server rejected. Presence runs in a separate ephemeral room so it can't touch durable data.

**Evidence.** 14 passing tests, including a two-browser collaboration spec covering live options, vote changes, presence and outcomes, plus a Playwright check against the deployed app.

**Stack.** TypeScript, React, Vite, Cloudflare Workers and Durable Objects (DeepSpace), Playwright, Vitest

[Code](https://github.com/DhyanICT/deepspace_proofboard) &nbsp;/&nbsp; [Live app](https://proofboard-dhyan.app.space)

## More shipped work

**[Rules Quiz API](https://github.com/DhyanICT/nextplay-rules-quiz-fullstack-assessment)**. A TypeScript and Express API with Zod-validated endpoints and attempt scoring, tested with Jest and Supertest, plus a React (Vite) client and a React Native screen.

**[Task Board](https://github.com/DhyanICT/Task_Board_NextPlay)**. A Next.js 14 and Supabase Kanban board where anonymous sessions and row-level security keep each guest's tasks private, with drag and drop, search and priority filters. [Live](https://taskboard-gamma-ten.vercel.app/)

**[SparkScope](https://github.com/DhyanICT/Spark_Homes_Developer)**. An offline-first PWA for estimating repair costs during property walkthroughs. ZIP and Excel export are implemented in plain JavaScript with no dependencies, so exports work without a connection.

**[CycleSync](https://github.com/DhyanICT/CycleSync)**. A native Android (Java) cycle tracker with an offline chatbot that answers in English and Gujarati.

**[NYC taxi trip graph](https://github.com/DhyanICT/DPS1)**. A pipeline that cleans a month of NYC taxi trips from Parquet with pandas and loads them into Neo4j as a location graph using Cypher, uniqueness constraints and startup retries.

## What the work shows

| Capability | Where to see it |
| --- | --- |
| LLM systems with measured quality | TrustMed retrieval and citation evals; CUA's split between LLM discovery and LLM-free replay |
| Safety and data integrity | CUA allowlist, redaction and handoff; Proofboard server-enforced voting; Task Board row-level security |
| Testing as part of the build | Playwright two-user specs, Jest and Supertest, Python unit tests |
| End-to-end ownership | Deployed apps with live links, setup guides and documented trade-offs |

## Capabilities

**Languages.** Python, TypeScript, JavaScript, Java, SQL, Cypher

**AI and retrieval.** RAG over knowledge graphs, embeddings (sentence-transformers), FAISS vector search, LLM agents and planners, retrieval evaluation (precision, recall, F1 at k)

**Backend.** FastAPI, Node.js, Express, REST API design, Zod validation, Supabase Auth and row-level security, Cloudflare Workers and Durable Objects

**Frontend and mobile.** React, Next.js, Vite, Tailwind CSS, Streamlit, Progressive Web Apps, Android (Java)

**Data.** Neo4j, PostgreSQL (Supabase), pandas, Parquet, web scraping and ETL

**Testing and automation.** Playwright, Jest, Supertest, Vitest, unittest, Chrome DevTools Protocol

## Activity

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/activity-dark.svg">
  <img alt="Recent GitHub contributions and top languages, refreshed weekly." src="assets/activity-light.svg" width="100%">
</picture>

<sub>Generated weekly by <a href="scripts/generate_activity.py">a small script</a> in this repository, with no third-party stats service.</sub>

---

Reach me on [LinkedIn](https://www.linkedin.com/in/dhyan-patel-94101b22a/). <!-- TODO: add email and portfolio here too -->
