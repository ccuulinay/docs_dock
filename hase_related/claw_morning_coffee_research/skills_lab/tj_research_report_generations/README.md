# Research Report Generations Skill for nanobot-ai

A nanobot-ai skill that conducts comprehensive web research on any topic, analyzes market reactions and social commentary, and produces detailed analysis reports in both markdown and professional HTML formats. Optionally converts reports to mobile-responsive HTML emails and distributes them via the configured email channel.

## Overview

This skill orchestrates a complete research-to-report pipeline:

1. **Research** — Multi-query web search across news, analysis, and social commentary
2. **Markdown Report** — Structured, citation-rich document with findings and analysis
3. **HTML Report** — Professional "Modern Archivist" presentation using the Academic Editorial design system
4. **HTML Email** *(optional)* — Mobile-responsive inline-CSS email format
5. **Email Distribution** *(optional)* — Sends HTML body + markdown attachment via `sending_email`

## Installation

1. Copy this skill directory to your nanobot skills folder:
   ```bash
   cp -r research_report_generations ~/.nanobot/skills/
   ```

2. Or use the skill-creator skill:
   ```
   @skill-creator Create a new skill from /path/to/research_report_generations
   ```

## Usage

### Basic Research Report

```
Research the current state of quantum computing in 2026 and write a report.
```

**Outputs:**
- `quantum-computing-2026-report.md`
- `quantum-computing-2026-report.html`

### Research + Email Delivery

```
Research the latest developments in renewable energy and send the report to team@example.com.
```

**Outputs + Actions:**
- `renewable-energy-report-2026-04-04.md`
- `renewable-energy-report-2026-04-04.html`
- `renewable-energy-report-2026-04-04-email.html`
- Email sent to `team@example.com` with HTML body and markdown attachment

### Market Reaction Analysis

```
Analyze how markets and social media reacted to the Fed's latest decision.
```

**Outputs:**
- `fed-decision-market-reaction.md`
- `fed-decision-market-reaction.html`

## Skill Structure

```
research_report_generations/
├── SKILL.md                           # Main skill definition and AI instructions
├── README.md                          # This file
├── scripts/
│   └── generate_html_report.py        # Helper script: markdown → professional HTML
└── references/
    └── design_integration.md          # Notes on DESIGN.md integration
```

## Helper Script

The included Python script converts a markdown research report into a styled HTML file.

### Generate a web HTML report

```bash
python research_report_generations/scripts/generate_html_report.py \
  --markdown report.md \
  --output report.html \
  --title "AI Market Analysis" \
  --subtitle "Research Report • April 2026"
```

### Generate an email-compatible HTML report

```bash
python research_report_generations/scripts/generate_html_report.py \
  --markdown report.md \
  --output report-email.html \
  --email \
  --title "AI Market Analysis" \
  --subtitle "Research Report • April 2026"
```

## Report Structure

Generated markdown reports include these sections:

| Section | Purpose |
|---------|---------|
| **Title** | Clear, descriptive headline |
| **Executive Summary** | 2-4 paragraph overview |
| **Introduction / Context** | Why this topic matters now |
| **Key Findings** | 3-7 most important discoveries |
| **Detailed Analysis** | Subsections by angle (market, social, technical) |
| **Market Reactions / Social Commentary** | Sentiment, quotes, reactions |
| **Data & Evidence** | Tables, metrics, timelines |
| **Conclusion / Recommendations** | Synthesis and takeaways |
| **Sources & References** | Numbered list with URLs and dates |

## Design System

HTML reports follow the **Academic Editorial / Modern Archivist** design system (defined in the local `DESIGN.md`):

- **Deep navy** (#002045) and **charcoal** (#121c2c) foundation
- **Primary container** (#1a365d) for gradients and secondary darks
- **Off-white** (#f9f9ff) surface with blue-tinted containers
- **Surface container** (#e7eeff) for research callout boxes
- **Gold accent** (#f8bc4b) for critical highlights
- **Typography**: Noto Serif (headlines) + Work Sans (body) + Public Sans (labels)
- **Layout**: Asymmetric two-column sections, metric cards, data tables, feature lists

## Email Prerequisites

To send reports via email, ensure the nanobot email channel is configured in `~/.nanobot/config.json`:

```json
{
  "channels": {
    "email": {
      "enabled": true,
      "consentGranted": true,
      "smtpHost": "smtp.gmail.com",
      "smtpPort": 587,
      "smtpUsername": "my-nanobot@gmail.com",
      "smtpPassword": "your-app-password",
      "fromAddress": "my-nanobot@gmail.com"
    }
  }
}
```

**Important**: For Gmail, use an App Password, not your regular password.

## Requirements

- Python 3.7+ (for the helper script)
- Internet access (for web research)
- Configured nanobot email channel (optional, for sending)

## Security Notes

- Never expose email credentials in chat responses
- Store credentials in `~/.nanobot/config.json` with restricted permissions:
  ```bash
  chmod 600 ~/.nanobot/config.json
  ```
- Verify `enabled` and `consentGranted` before sending emails

## License

Part of the nanobot-ai skill ecosystem.

## See Also

- [SKILL.md](SKILL.md) — Detailed skill instructions for the AI agent
- `professional_html_email_report_generator/SKILL.md` — HTML/email design templates
- `sending_email/SKILL.md` — Email sending configuration and workflow
