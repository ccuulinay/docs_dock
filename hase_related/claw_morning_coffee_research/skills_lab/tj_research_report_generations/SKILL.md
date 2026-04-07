---
name: "research-report-generations"
version: "1.0.0"
description: "Conduct comprehensive web research on any topic, analyze market reactions and social commentary, and produce detailed analysis reports in markdown and professional HTML formats. Optionally converts reports to mobile-responsive HTML emails and sends them via the configured nanobot-ai email channel."
tags: ["research", "web-search", "reporting", "html", "email"]
---

# Research Report Generations Skill

This skill drives nanobot-ai to conduct comprehensive web research on any topic, analyze market reactions and social commentary, synthesize findings into a structured markdown report, and then produce a professional HTML presentation. If the user requests email delivery, the skill formats the HTML into a mobile-responsive email and sends it via the `sending_email` skill, attaching the markdown report.

## When to Use

Use this skill when the user wants to:
- Research a topic and produce a written analysis
- Generate a professional research report with web-sourced data
- Create an HTML presentation from research findings
- Send research reports via email with both HTML body and markdown attachment
- Analyze market reactions, news, or social commentary on a specific subject
- Compile executive briefings or deep-dive reports on emerging trends

## Prerequisites

- Internet access for web research
- For email sending: configured nanobot-ai email channel (`~/.nanobot/config.json`) with `enabled` and `consentGranted` set to `true`

## Workflow

The skill follows a 3-to-5 step pipeline depending on user needs:

1. **Research Phase** — Web search, source evaluation, and synthesis
2. **Markdown Report Generation** — Structured, citation-rich markdown document
3. **HTML Report Generation** — Professional HTML based on `DESIGN.md` (The Academic Editorial / Modern Archivist)
4. **Optional: HTML Email Conversion** — Mobile-responsive inline-CSS email format
5. **Optional: Email Distribution** — Send via `sending_email` skill with markdown attachment

---

## Step 1 — Research Phase

### Understanding the Topic

Begin by clarifying the user's research request:
- What is the core topic or question?
- What depth is expected? (executive summary vs. deep dive)
- What time period or geography is relevant?
- Are there specific aspects to emphasize? (market reaction, social commentary, financial, technical)

### Web Search Strategy

Use multiple targeted search queries to gather diverse perspectives:
- Search for recent news and developments
- Search for expert analysis or industry reports
- Search for social/media commentary and public reaction
- Search for opposing viewpoints or critical analysis

For each query, evaluate sources for:
- **Recency** — prefer sources from the last 6-12 months unless historical context is needed
- **Credibility** — prefer established publications, research institutions, domain experts
- **Diversity** — include multiple viewpoints and geographies
- **Data richness** — favor sources with concrete numbers, quotes, or citations

### Synthesis

As you consume sources:
1. Extract key facts, figures, quotes, and claims
2. Note the source and publication date for every significant piece of information
3. Identify patterns, consensus views, and areas of disagreement
4. Flag uncertainties or conflicting data
5. Summarize market or social reactions in a dedicated section

---

## Step 2 — Markdown Report Generation

Generate a well-structured markdown report. Save it with a descriptive filename (e.g., `ai-market-analysis-2026-04-04.md`).

### Required Sections

| Section | Purpose |
|---------|---------|
| **Title** | Clear, descriptive headline |
| **Executive Summary** | 2-4 paragraph overview of findings and key takeaway |
| **Introduction / Context** | Why this topic matters now |
| **Key Findings** | 3-7 bullet points of the most important discoveries |
| **Detailed Analysis** | Subsections exploring different angles (market, social, technical, etc.) |
| **Market Reactions / Social Commentary** | Specific section for sentiment, quotes, and public/opinion leader reactions |
| **Data & Evidence** | Tables, metrics, timelines |
| **Conclusion / Recommendations** | Synthesis and actionable takeaways |
| **Sources & References** | Numbered list of sources with URLs and dates |

### Writing Guidelines

- Use clear, authoritative prose appropriate for a professional audience
- Attribute all significant claims to sources
- Use markdown tables for structured data
- Use `**bold**` for key terms and metrics
- Keep paragraphs focused (3-5 sentences)
- Include inline citations like `(Source Name, Date)` or superscript reference numbers

---

## Step 3 — HTML Report Generation

Transform the markdown report into a professional HTML document based on `DESIGN.md` in the current directory (The Academic Editorial / Modern Archivist design system).

### Design System Requirements

**Creative North Star: "The Modern Archivist"**
- Deep navy (#1A365D) and charcoal (#121c2c) foundation
- Off-white surface (#f9f9ff) with blue-tinted container layers
- Gold accent (#f8bc4b) for critical data points and highlights
- Typography pairing: Noto Serif (headlines) + Work Sans (body) + Public Sans (labels)

### HTML Structure

Use the Premium Editorial template structure defined in the local `DESIGN.md`:

1. **Top Navigation** — Organization/series name
2. **Report Header** — Subtitle, title, gold accent line
3. **Summary (TL;DR)** — Two-column: header left, callout right
4. **Key Findings** — Two-column with feature list (gold circle icons)
5. **Key Data & Figures** — Metric cards + data tables
6. **Detailed Insights** — Two-column with subsections
7. **Appendix** — Sources and links
8. **CTA Section** — Optional call-to-action
9. **Footer** — Copyright and disclaimer

### Output

Save as a standalone `.html` file (e.g., `ai-market-analysis-2026-04-04.html`). The file must:
- Be fully self-contained (no external CSS/JS dependencies)
- Use the design system colors, typography, and spacing
- Include responsive media queries
- Be under ~150KB

You may use the helper script `scripts/generate_html_report.py` to automate this conversion:

```bash
python research_report_generations/scripts/generate_html_report.py \
  --markdown ai-market-analysis-2026-04-04.md \
  --output ai-market-analysis-2026-04-04.html \
  --title "AI Market Analysis" \
  --subtitle "Research Report • April 2026"
```

---

## Step 4 — Optional: HTML Email Conversion

If the user requests email delivery, create an HTML email version of the report. There are two template options:

### Premium Editorial Email
Use when:
- Recipients use modern email clients (Gmail, Apple Mail, Outlook 365)
- The report is for executive/stakeholder consumption
- A distinctive, publication-quality look is desired

Follow the `professional_html_email_report_generator/SKILL.md` Premium Editorial template:
- Web fonts via Google Fonts CDN
- `display: table` layouts for email compatibility
- All critical styles inlined; additional styles in `<style>` block with media queries
- Keep width ≤ 600px

### Standard Email
Use when:
- Maximum email client compatibility is required
- Recipients may use older Outlook versions or corporate filters

Follow `professional_html_email_report_generator/SKILL.md` Standard template:
- Table-based layout only
- Web-safe fonts (Arial, Georgia)
- All styles inline
- No external dependencies

Save the email HTML to a file (e.g., `ai-market-analysis-2026-04-04-email.html`) before sending.

---

## Step 5 — Optional: Email Distribution

If the user explicitly requests email delivery:

1. **Confirm recipients** — Ask for or verify email addresses if not provided
2. **Prepare the email**:
   - Subject line: clear and descriptive (e.g., "Research Report: AI Market Analysis — April 2026")
   - Body: the HTML email version of the report
   - Attachment: the markdown `.md` report file
3. **Send via `sending_email` skill** using the helper script or skill delegation

Example using the script:

```bash
python sending_email/scripts/send_email.py \
  --to "recipient@example.com" \
  --subject "Research Report: AI Market Analysis — April 2026" \
  --body-file ai-market-analysis-2026-04-04-email.html \
  --body-type html \
  --attachment ai-market-analysis-2026-04-04.md
```

If sending to multiple recipients, use comma-separated `--to` addresses or CC fields.

### Security & Consent Checks

Before sending, verify:
- `~/.nanobot/config.json` has `channels.email.enabled: true`
- `channels.email.consentGranted: true`
- Do not expose credentials in chat responses

---

## Report Quality Checklist

Before finalizing, ensure:

- [ ] Research covers multiple credible sources
- [ ] Key findings are supported by evidence
- [ ] Market/social reactions are explicitly addressed
- [ ] Markdown report has all required sections
- [ ] HTML report follows the design system correctly
- [ ] HTML email is mobile-responsive
- [ ] Sources are cited with URLs and dates
- [ ] No unsupported claims or speculation presented as fact
- [ ] Email sending respects consent and configuration

---

## Example Usage

### Basic Research Report
> "Research the current state of quantum computing in 2026 and write a report."

**Actions:**
1. Search web for quantum computing news, breakthroughs, and market data
2. Synthesize findings into `quantum-computing-2026-report.md`
3. Generate `quantum-computing-2026-report.html` using the Premium Editorial design

### Research + Email Delivery
> "Research the latest developments in renewable energy and send the report to team@example.com."

**Actions:**
1. Search web for renewable energy developments
2. Synthesize into `renewable-energy-report-2026-04-04.md`
3. Generate `renewable-energy-report-2026-04-04.html`
4. Create email version `renewable-energy-report-2026-04-04-email.html`
5. Send email to `team@example.com` with HTML body and markdown attachment

### Market Reaction Analysis
> "Analyze how markets and social media reacted to the Fed's latest decision."

**Actions:**
1. Search for financial news coverage, analyst commentary, and social media reactions
2. Synthesize into `fed-decision-market-reaction.md`
3. Generate `fed-decision-market-reaction.html`
4. Present both files to the user

---

## Integration with Other Skills

| Skill | How This Skill Uses It |
|-------|------------------------|
| `sending-email` | For distributing reports via email with attachments |
