# Design Integration Notes

This skill generates HTML reports using the **Academic Editorial / Modern Archivist** design system defined in the local `DESIGN.md` in the current directory (`research_report_generations/DESIGN.md`).

## Design System Summary

**Creative North Star: "The Modern Archivist"**
- Inspired by high-end editorial journals and architectural monographs
- Presents complex research data as an authoritative narrative
- Uses intentional asymmetry, tonal depth, and expansive white space

## Color Palette (from DESIGN.md)

| Role | Hex | Usage |
|------|-----|-------|
| Primary | `#002045` | Headers, key text, CTAs |
| Primary Container | `#1a365d` | Gradients, hover states |
| On Primary | `#ffffff` | Text on dark backgrounds |
| Surface | `#f9f9ff` | Main document body |
| Surface Container Low | `#f0f3ff` | Secondary sections, sidebars |
| Surface Container High | `#dee8ff` | Callouts, highlighted content |
| Surface Container | `#e7eeff` | Research callout boxes |
| Tertiary Fixed Dim | `#f8bc4b` | Key metrics, accent borders, highlights |
| On Surface | `#121c2c` | Body text (never pure black) |
| On Surface Variant | `#43474e` | Secondary text, metadata |
| Outline Variant | `#c4c6cf` | Subtle borders, ghost borders |

## Typography

- **Headlines/Display**: Noto Serif, tight letter-spacing (-0.02em)
- **Body**: Work Sans, comfortable line-height
- **Labels/Metadata**: Public Sans, all-caps, tracking (0.05em-0.2em)

## Key Layout Rules (from DESIGN.md)

1. **No 1px borders for sectioning** — use background color shifts instead
2. **Asymmetric two-column layout** — 33% left / 67% right for major sections
3. **Metric cards** — 3-up row with primary (navy), secondary (light blue), tertiary (lighter blue)
4. **Data tables** — Ghost borders at 15% opacity (`outline_variant`), no vertical lines
5. **Research callout boxes** — `surface_container` (#e7eeff) with 4px left-accent border of `tertiary_fixed_dim` (#f8bc4b)
6. **Report header** — Gradient from `primary` (#002045) to `primary_container` (#1a365d) at 135 degrees
7. **Responsive** — Stack to single column on mobile (max-width: 620px)

## Template Mapping

The helper script (`scripts/generate_html_report.py`) maps markdown sections to the Premium Editorial template as follows:

| Markdown Section | HTML Section |
|------------------|--------------|
| `# Title` | Report Header (with gradient background) |
| `## Executive Summary` / `## Summary` | Summary (TL;DR) — two-column with research callout |
| `## Key Findings` | Key Findings — two-column with feature list |
| `## Data & Figures` / `## Metrics` | Key Data & Figures — metric cards + tables |
| `## Detailed Analysis` / `## Market Reactions` | Detailed Insights — two-column subsections |
| `## Sources` / `## References` | Appendix — two-column with links |
| Other `##` sections | Rendered as two-column sections |

## Email Compatibility

When `--email` mode is enabled:
- Table-based layout replaces `display: table` structures for older clients
- Critical styles are inlined
- Web-safe font fallbacks are used
- Google Fonts may still be referenced but graceful fallbacks apply
