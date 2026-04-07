#!/usr/bin/env python3
"""
Convert a markdown research report into a professional HTML report
using the Academic Editorial / Modern Archivist design system.
"""

import argparse
import re
import sys
from pathlib import Path


# Design system colors and fonts from DESIGN.md
COLORS = {
    "primary": "#002045",
    "primary_container": "#1a365d",
    "on_primary": "#ffffff",
    "surface": "#f9f9ff",
    "surface_container_low": "#f0f3ff",
    "surface_container_high": "#dee8ff",
    "surface_container": "#e7eeff",
    "tertiary_fixed_dim": "#f8bc4b",
    "on_surface": "#121c2c",
    "on_surface_variant": "#43474e",
    "outline_variant": "#c4c6cf",
}


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def md_inline_to_html(text: str) -> str:
    # bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def md_table_to_html(table: dict) -> str:
    html = '<div class="data-table-container">\n<table class="data-table">\n<thead>\n<tr>\n'
    for j, col in enumerate(table["header"]):
        align = " text-right" if any(c.lower() in col for c in ["rate", "growth", "return", "value", "%", "$", "vs", "weight"]) and j > 0 else ""
        html += f'<th class="{align.lstrip()}">{escape_html(col)}</th>\n'
    html += "</tr>\n</thead>\n<tbody>\n"
    for row in table["rows"]:
        html += "<tr>\n"
        for j, cell in enumerate(row):
            align = " text-right" if any(c.lower() in table["header"][j] for c in ["rate", "growth", "return", "value", "%", "$", "vs", "weight"]) and j > 0 else ""
            bold = " font-bold" if j == 0 else ""
            html += f'<td class="{align.lstrip()}{bold}">{escape_html(cell)}</td>\n'
        html += "</tr>\n"
    html += "</tbody>\n</table>\n</div>\n"
    return html


def parse_markdown(md_text: str) -> dict:
    """Parse markdown into structured sections."""
    lines = md_text.splitlines()
    result = {
        "title": "Research Report",
        "subtitle": "",
        "sections": [],
    }

    current_section = None
    current_body = []
    in_list = False
    list_items = []
    list_type = None

    def flush_list():
        nonlocal in_list, list_items, list_type, current_body
        if in_list and list_items:
            if list_type == "ul":
                html = '<ul class="bullet-list">\n'
                for item in list_items:
                    html += f'<li>{md_inline_to_html(item)}</li>\n'
                html += '</ul>\n'
            else:
                html = '<ol class="bullet-list">\n'
                for idx, item in enumerate(list_items, 1):
                    html += f'<li value="{idx}">{md_inline_to_html(item)}</li>\n'
                html += '</ol>\n'
            current_body.append(html)
        in_list = False
        list_items = []
        list_type = None

    def flush_section():
        nonlocal current_section, current_body
        if current_section is not None:
            body_text = "\n".join(current_body)
            current_section["body"] = body_text
            result["sections"].append(current_section)
            current_section = None
            current_body = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("# ") and not stripped.startswith("## "):
            flush_list()
            flush_section()
            result["title"] = stripped[2:].strip()
            i += 1
            continue

        if stripped.startswith("## "):
            flush_list()
            flush_section()
            current_section = {"heading": stripped[3:].strip(), "body": ""}
            i += 1
            continue

        if stripped.startswith("### "):
            flush_list()
            if current_section is not None:
                current_body.append(f'<h3 class="insight-header">{md_inline_to_html(stripped[4:])}</h3>\n')
            i += 1
            continue

        # List items
        if re.match(r'^[-*]\s', stripped):
            if not in_list or list_type != "ul":
                flush_list()
                in_list = True
                list_type = "ul"
            list_items.append(re.sub(r'^[-*]\s+', '', stripped))
            i += 1
            continue

        if re.match(r'^\d+\.\s', stripped):
            if not in_list or list_type != "ol":
                flush_list()
                in_list = True
                list_type = "ol"
            list_items.append(re.sub(r'^\d+\.\s+', '', stripped))
            i += 1
            continue

        # Empty line ends a list
        if stripped == "":
            flush_list()
            i += 1
            continue

        # Blockquote / callout
        if stripped.startswith("> "):
            flush_list()
            quote_text = md_inline_to_html(stripped[2:])
            current_body.append(
                f'<div class="callout" style="margin: 16px 0;">\n'
                f'<p>{quote_text}</p>\n'
                f'</div>\n'
            )
            i += 1
            continue

        # Tables - collect all rows for post-processing
        if "|" in stripped and i + 1 < len(lines) and "-" in lines[i + 1] and "|" in lines[i + 1]:
            flush_list()
            table_lines = []
            # Collect all consecutive table rows
            while i < len(lines):
                row = lines[i].strip()
                if "|" in row:
                    table_lines.append(row)
                    i += 1
                else:
                    break
            # Store all table lines for post-processing
            current_body.append("\n".join(table_lines) + "\n")
            continue

        # Plain paragraph
        if current_section is not None:
            current_body.append(f'<p>{md_inline_to_html(stripped)}</p>\n')
        i += 1

    flush_list()
    flush_section()
    return result


def post_process_tables(section_body: str) -> str:
    """Replace markdown tables in a body string with HTML tables."""
    lines = section_body.splitlines()
    out_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if "|" in stripped and i + 1 < len(lines) and "-" in lines[i + 1] and "|" in lines[i + 1]:
            table_lines = [stripped]
            i += 1
            table_lines.append(lines[i].strip())  # separator
            i += 1
            while i < len(lines):
                row = lines[i].strip()
                if "|" in row:
                    table_lines.append(row)
                    i += 1
                else:
                    break
            header = [c.strip() for c in table_lines[0].split("|")[1:-1]]
            rows = []
            for row_line in table_lines[2:]:
                cells = [c.strip() for c in row_line.split("|")[1:-1]]
                rows.append(cells)
            table_html = md_table_to_html({"header": header, "rows": rows})
            out_lines.append(table_html)
        else:
            out_lines.append(line)
            i += 1
    return "\n".join(out_lines)


def build_html(parsed: dict, title: str = None, subtitle: str = None, email_mode: bool = False) -> str:
    report_title = title or parsed["title"]
    report_subtitle = subtitle or parsed.get("subtitle", "Research Report")

    # Identify special sections
    summary_section = None
    findings_sections = []
    data_sections = []
    detailed_sections = []
    appendix_sections = []
    other_sections = []

    for sec in parsed["sections"]:
        h_lower = sec["heading"].lower()
        body = post_process_tables(sec["body"])
        sec["body_html"] = body
        if any(k in h_lower for k in ["summary", "executive summary", "tldr", "tl;dr"]):
            summary_section = sec
        elif any(k in h_lower for k in ["finding", "key finding", "highlights", "key highlights"]):
            findings_sections.append(sec)
        elif any(k in h_lower for k in ["data", "figures", "metrics", "breakdown", "sector breakdown"]):
            data_sections.append(sec)
        elif any(k in h_lower for k in ["detailed insight", "analysis", "market reaction", "social commentary", "recommendation", "conclusion"]):
            detailed_sections.append(sec)
        elif any(k in h_lower for k in ["source", "reference", "appendix"]):
            appendix_sections.append(sec)
        else:
            other_sections.append(sec)

    # Build feature list for findings
    feature_list_html = ""
    all_findings = ""
    for sec in findings_sections:
        all_findings += sec["body_html"]
    list_items = re.findall(r'<li>(.+?)</li>', all_findings, re.DOTALL)
    if list_items:
        feature_list_html = '<ul class="feature-list">\n'
        for item in list_items[:5]:
            title_match = re.match(r'<strong>(.+?)</strong>\s*[:\-\u2013]\s*(.*)', item, re.DOTALL)
            if title_match:
                ftitle = title_match.group(1)
                fdesc = title_match.group(2)
            else:
                ftitle = item.split(".", 1)[0] if "." in item else item
                fdesc = item.split(".", 1)[1] if "." in item else ""
            feature_list_html += (
                '<li>\n'
                '  <div class="feature-icon"><span class="feature-icon-circle"></span></div>\n'
                '  <div class="feature-content">\n'
                f'    <div class="feature-title">{ftitle}</div>\n'
                f'    <div class="feature-desc">{fdesc}</div>\n'
                '  </div>\n'
                '</li>\n'
            )
        feature_list_html += '</ul>\n'
    else:
        feature_list_html = f'<div class="callout">{all_findings}</div>'

    # Build content sections
    content_html = ""

    # Summary
    summary_body = summary_section["body_html"] if summary_section else ""
    if summary_body:
        summary_text = re.sub(r'</?p>', '', summary_body).strip()
        content_html += (
            '<div class="section">\n'
            '  <div class="two-col">\n'
            '    <div class="col-left">\n'
            '      <h2 class="section-header">Summary <span class="subtitle">(TL;DR)</span></h2>\n'
            '    </div>\n'
            '    <div class="col-right">\n'
            '      <div class="callout">\n'
            f'        <p>{summary_text}</p>\n'
            '      </div>\n'
            '    </div>\n'
            '  </div>\n'
            '</div>\n'
        )

    # Key Findings
    if findings_sections:
        content_html += (
            '<div class="section section-alt">\n'
            '  <div class="two-col">\n'
            '    <div class="col-left">\n'
            '      <h2 class="section-header">Key Findings</h2>\n'
            '    </div>\n'
            '    <div class="col-right">\n'
            f'{feature_list_html}'
            '    </div>\n'
            '  </div>\n'
            '</div>\n'
        )

    # Key Data & Figures
    for sec in data_sections:
        content_html += (
            '<div class="section">\n'
            '  <h2 class="section-header">Key Data & Figures</h2>\n'
            f'{sec["body_html"]}'
            '</div>\n'
        )

    # Detailed Insights
    for sec in detailed_sections:
        content_html += (
            '<div class="section section-alt">\n'
            '  <div class="two-col">\n'
            '    <div class="col-left">\n'
            f'      <h2 class="section-header">{sec["heading"]}</h2>\n'
            '    </div>\n'
            '    <div class="col-right">\n'
            f'{sec["body_html"]}'
            '    </div>\n'
            '  </div>\n'
            '</div>\n'
        )

    # Other sections
    for sec in other_sections:
        content_html += (
            '<div class="section">\n'
            '  <div class="two-col">\n'
            '    <div class="col-left">\n'
            f'      <h2 class="section-header">{sec["heading"]}</h2>\n'
            '    </div>\n'
            '    <div class="col-right">\n'
            f'{sec["body_html"]}'
            '    </div>\n'
            '  </div>\n'
            '</div>\n'
        )

    # Appendix
    for sec in appendix_sections:
        content_html += (
            '<div class="section">\n'
            '  <div class="two-col">\n'
            '    <div class="col-left">\n'
            '      <h2 class="section-header" style="font-style: italic;">Appendix</h2>\n'
            '    </div>\n'
            '    <div class="col-right">\n'
            f'{sec["body_html"]}'
            '    </div>\n'
            '  </div>\n'
            '</div>\n'
        )

    # CTA
    content_html += (
        '<div class="cta-section">\n'
        '  <div class="cta-meta">Generated by nanobot-ai Research Report Generations Skill</div>\n'
        '</div>\n'
    )

    if email_mode:
        return build_email_html(report_title, report_subtitle, content_html)
    else:
        return build_web_html(report_title, report_subtitle, content_html)


def build_web_html(title: str, subtitle: str, content: str) -> str:
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape_html(title)}</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif:wght@400;700&family=Work+Sans:wght@300;400;500;600&family=Public+Sans:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body, table, td, p, h1, h2, h3, h4, h5, h6 {{margin: 0; padding: 0;}}
    body {{width: 100% !important; -webkit-text-size-adjust: 100%;}}
    body {{
      font-family: 'Work Sans', Arial, sans-serif;
      background-color: {COLORS["surface"]};
      color: {COLORS["on_surface"]};
      line-height: 1.6;
    }}
    h1, h2, h3, h4 {{
      font-family: 'Noto Serif', Georgia, serif;
      color: {COLORS["primary"]};
    }}
    .email-container {{
      max-width: 800px;
      margin: 0 auto;
      background-color: {COLORS["surface"]};
    }}
    .top-nav {{
      background-color: {COLORS["surface_container_low"]};
      padding: 16px 40px;
      text-align: center;
    }}
    .top-nav-brand {{
      font-family: 'Noto Serif', Georgia, serif;
      font-size: 20px;
      font-weight: 700;
      color: {COLORS["primary"]};
      letter-spacing: -0.02em;
    }}
    .report-header {{
      padding: 48px 40px 32px;
      text-align: center;
      background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["primary_container"]} 100%);
    }}
    .report-header .subtitle {{
      font-family: 'Public Sans', Arial, sans-serif;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      color: rgba(255,255,255,0.7);
      margin-bottom: 8px;
    }}
    .report-header h1 {{
      font-size: 48px;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: {COLORS["on_primary"]};
      margin: 0 0 16px 0;
      line-height: 1.1;
    }}
    .report-header .accent-line {{
      width: 96px;
      height: 6px;
      background-color: {COLORS["tertiary_fixed_dim"]};
      border-radius: 3px;
      margin: 0 auto;
    }}
    .section {{padding: 32px 40px;}}
    .section-alt {{background-color: {COLORS["surface_container_low"]};}}
    .two-col {{display: table; width: 100%;}}
    .col-left {{
      display: table-cell;
      width: 33%;
      vertical-align: top;
      padding-right: 24px;
    }}
    .col-right {{
      display: table-cell;
      width: 67%;
      vertical-align: top;
    }}
    .section-header {{
      font-size: 28px;
      font-weight: 700;
      color: {COLORS["primary"]};
      margin-bottom: 24px;
    }}
    .section-header .subtitle {{
      font-family: 'Work Sans', Arial, sans-serif;
      font-size: 16px;
      font-weight: 400;
      color: {COLORS["on_surface_variant"]};
      opacity: 0.5;
      display: block;
      margin-top: 4px;
    }}
    .callout {{
      background-color: {COLORS["surface_container"]};
      border-left: 4px solid {COLORS["tertiary_fixed_dim"]};
      padding: 24px;
      margin: 0;
      border-radius: 0 8px 8px 0;
    }}
    .callout p {{
      font-size: 18px;
      line-height: 1.6;
      color: {COLORS["on_surface"]};
      margin: 0;
    }}
    .metrics-row {{
      display: table;
      width: 100%;
      margin: 24px 0;
      border-spacing: 16px 0;
      margin-left: -16px;
      margin-right: -16px;
    }}
    .metric-card {{
      display: table-cell;
      width: 33.33%;
      padding: 24px;
      border-radius: 8px;
      vertical-align: top;
    }}
    .metric-card-primary {{
      background-color: {COLORS["primary"]};
      color: {COLORS["on_primary"]};
      border-bottom: 4px solid {COLORS["tertiary_fixed_dim"]};
    }}
    .metric-card-secondary {{
      background-color: {COLORS["surface_container_high"]};
      border-left: 4px solid {COLORS["primary"]};
    }}
    .metric-card-tertiary {{
      background-color: {COLORS["surface_container"]};
      border-left: 4px solid {COLORS["tertiary_fixed_dim"]};
    }}
    .metric-label {{
      font-family: 'Public Sans', Arial, sans-serif;
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      opacity: 0.7;
      margin-bottom: 8px;
    }}
    .metric-card-secondary .metric-label,
    .metric-card-tertiary .metric-label {{
      color: {COLORS["on_surface_variant"]};
    }}
    .metric-value {{
      font-family: 'Noto Serif', Georgia, serif;
      font-size: 36px;
      font-weight: 700;
      line-height: 1.2;
    }}
    .metric-card-secondary .metric-value,
    .metric-card-tertiary .metric-value {{
      color: {COLORS["primary"]};
    }}
    .metric-desc {{
      font-size: 12px;
      opacity: 0.8;
      margin-top: 4px;
    }}
    .metric-card-secondary .metric-desc,
    .metric-card-tertiary .metric-desc {{
      color: {COLORS["on_surface_variant"]};
    }}
    .data-table-container {{
      background-color: #ffffff;
      border-radius: 8px;
      overflow: hidden;
      margin: 24px 0;
    }}
    .data-table {{
      width: 100%;
      border-collapse: collapse;
    }}
    .data-table th {{
      font-family: 'Public Sans', Arial, sans-serif;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: {COLORS["primary"]};
      background-color: {COLORS["surface_container_low"]};
      padding: 16px;
      text-align: left;
      font-weight: 600;
    }}
    .data-table td {{
      padding: 16px;
      font-size: 14px;
      border-bottom: 1px solid rgba(196, 198, 207, 0.15);
    }}
    .data-table tr:last-child td {{
      border-bottom: none;
    }}
    .data-table .text-right {{text-align: right;}}
    .data-table .font-bold {{
      font-weight: 600;
      color: {COLORS["primary"]};
    }}
    .feature-list {{
      list-style: none;
      padding: 0;
      margin: 0;
    }}
    .feature-list li {{
      padding: 16px 0;
      border-bottom: 1px solid rgba(196, 198, 207, 0.15);
      display: table;
      width: 100%;
    }}
    .feature-list li:last-child {{
      border-bottom: none;
    }}
    .feature-icon {{
      display: table-cell;
      width: 24px;
      padding-right: 16px;
      vertical-align: top;
    }}
    .feature-icon-circle {{
      width: 24px;
      height: 24px;
      background-color: {COLORS["tertiary_fixed_dim"]};
      border-radius: 50%;
      display: block;
    }}
    .feature-content {{
      display: table-cell;
      vertical-align: top;
    }}
    .feature-title {{
      font-weight: 600;
      color: {COLORS["primary"]};
      margin-bottom: 4px;
      font-size: 16px;
    }}
    .feature-desc {{
      color: {COLORS["on_surface_variant"]};
      font-size: 14px;
      line-height: 1.5;
    }}
    .insight-subsection {{margin-bottom: 24px;}}
    .insight-subsection:last-child {{margin-bottom: 0;}}
    .insight-header {{
      font-size: 18px;
      font-weight: 700;
      color: {COLORS["primary"]};
      margin-bottom: 12px;
      padding-bottom: 8px;
    }}
    .bullet-list {{
      margin: 0;
      padding-left: 20px;
    }}
    .bullet-list li {{
      color: {COLORS["on_surface_variant"]};
      font-size: 14px;
      line-height: 1.6;
      margin-bottom: 8px;
    }}
    .cta-section {{
      padding: 48px 40px;
      text-align: center;
      background-color: {COLORS["surface_container_low"]};
    }}
    .cta-meta {{
      margin-top: 16px;
      font-family: 'Public Sans', Arial, sans-serif;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: {COLORS["on_surface_variant"]};
    }}
    .footer {{
      background-color: {COLORS["surface_container"]};
      padding: 48px 40px;
      text-align: center;
    }}
    .footer-brand {{
      font-family: 'Noto Serif', Georgia, serif;
      font-size: 20px;
      font-weight: 700;
      color: {COLORS["primary"]};
      margin-bottom: 24px;
    }}
    .footer-text {{
      font-size: 12px;
      color: {COLORS["on_surface_variant"]};
      line-height: 1.6;
      opacity: 0.7;
    }}
    @media only screen and (max-width: 620px) {{
      .section, .report-header, .footer, .cta-section {{padding-left: 20px !important; padding-right: 20px !important;}}
      .report-header h1 {{font-size: 36px !important;}}
      .col-left, .col-right {{
        display: block !important;
        width: 100% !important;
        padding-right: 0 !important;
        margin-bottom: 24px;
      }}
      .metric-card {{
        display: block !important;
        width: 100% !important;
        margin-bottom: 16px !important;
      }}
      .metrics-row {{
        display: block !important;
        border-spacing: 0 !important;
      }}
      .two-col {{display: block !important;}}
    }}
  </style>
</head>
<body>
  <div class="email-container">
    <div class="top-nav">
      <div class="top-nav-brand">nanobot-ai Research</div>
    </div>
    <div class="report-header">
      <div class="subtitle">{escape_html(subtitle)}</div>
      <h1>{escape_html(title)}</h1>
      <div class="accent-line"></div>
    </div>
{content}
    <div class="footer">
      <div class="footer-brand">nanobot-ai</div>
      <div class="footer-text">
        Generated by nanobot-ai Research Report Generations Skill.<br/>
        For informational purposes only.
      </div>
    </div>
  </div>
</body>
</html>
'''


def build_email_html(title: str, subtitle: str, content: str) -> str:
    return f'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape_html(title)}</title>
  <!--[if mso]>
  <style type="text/css">
    table {{border-collapse: collapse;}}
    .fallback-font {{font-family: Arial, sans-serif;}}
  </style>
  <![endif]-->
  <style type="text/css">
    body, table, td, p, h1, h2, h3, h4, h5, h6 {{margin: 0; padding: 0;}}
    body {{width: 100% !important; -webkit-text-size-adjust: 100%; ms-text-size-adjust: 100%;}}
    /* Email content styles */
    .data-table-container {{background-color: #ffffff; border-radius: 8px; overflow: hidden; margin: 24px 0;}}
    table.data-table {{width: 100%; border-collapse: collapse;}}
    table.data-table th {{font-family: Arial, sans-serif; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #002045; background-color: #f0f3ff; padding: 12px 16px; text-align: left; font-weight: 600;}}
    table.data-table td {{padding: 12px 16px; font-size: 14px; border-bottom: 1px solid rgba(196, 198, 207, 0.15); font-family: Arial, sans-serif; color: #121c2c;}}
    table.data-table tr:last-child td {{border-bottom: none;}}
    table.data-table .text-right {{text-align: right;}}
    table.data-table .font-bold {{font-weight: 600; color: #002045;}}
    .insight-header {{font-family: Georgia, serif; font-size: 18px; font-weight: 700; color: #002045; margin: 24px 0 12px 0;}}
    .bullet-list {{margin: 0; padding-left: 20px; font-family: Arial, sans-serif; font-size: 14px; color: #121c2c; line-height: 1.6;}}
    .bullet-list li {{margin-bottom: 8px;}}
    .section-header {{font-family: Georgia, serif; font-size: 20px; font-weight: 700; color: #002045; margin: 32px 0 16px 0;}}
    .callout {{background-color: #e7eeff; border-left: 4px solid #f8bc4b; padding: 16px 20px; margin: 16px 0; border-radius: 0 8px 8px 0;}}
    .callout p {{font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6; color: #121c2c; margin: 0;}}
    .two-col {{display: table; width: 100%;}}
    .col-left {{display: table-cell; width: 33%; vertical-align: top; padding-right: 24px;}}
    .col-right {{display: table-cell; width: 67%; vertical-align: top;}}
    .feature-list {{list-style: none; padding: 0; margin: 0;}}
    .feature-list li {{padding: 12px 0; border-bottom: 1px solid rgba(196, 198, 207, 0.15); display: table; width: 100%;}}
    .feature-list li:last-child {{border-bottom: none;}}
    .feature-icon {{display: table-cell; width: 24px; padding-right: 12px; vertical-align: top;}}
    .feature-icon-circle {{width: 24px; height: 24px; background-color: #f8bc4b; border-radius: 50%; display: block;}}
    .feature-content {{display: table-cell; vertical-align: top;}}
    .feature-title {{font-weight: 600; color: #002045; margin-bottom: 4px; font-size: 15px; font-family: Arial, sans-serif;}}
    .feature-desc {{color: #43474e; font-size: 13px; line-height: 1.5; font-family: Arial, sans-serif;}}
    .cta-section {{padding: 32px 40px; text-align: center; background-color: #f0f3ff;}}
    .cta-meta {{margin-top: 12px; font-family: Arial, sans-serif; font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; color: #43474e;}}
    @media only screen and (max-width: 620px) {{
      .email-container {{width: 100% !important; max-width: 100% !important;}}
      .mobile-padding {{padding-left: 15px !important; padding-right: 15px !important;}}
      .data-table-container {{overflow-x: auto; display: block;}}
      table.data-table {{min-width: 100%;}}
      .two-col {{display: block !important;}}
      .col-left, .col-right {{display: block !important; width: 100% !important; padding-right: 0 !important; margin-bottom: 16px;}}
    }}
  </style>
</head>
<body style="margin: 0; padding: 0; background-color: {COLORS['surface']}; font-family: Arial, Helvetica, sans-serif;">
  <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: {COLORS['surface']};">
    <tr>
      <td align="center" valign="top" style="padding: 20px 0;">
        <table role="presentation" class="email-container" border="0" cellpadding="0" cellspacing="0" width="600" style="max-width: 600px; background-color: {COLORS['surface']};">
          <!-- Top Nav -->
          <tr>
            <td style="background-color: {COLORS['surface_container_low']}; padding: 16px 40px; text-align: center;">
              <p style="font-family: Georgia, serif; font-size: 20px; font-weight: 700; color: {COLORS['primary']}; margin: 0; letter-spacing: -0.02em;">nanobot-ai Research</p>
            </td>
          </tr>
          <!-- Header -->
          <tr>
            <td style="padding: 48px 40px 32px; text-align: center; background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_container']} 100%);">
              <p style="font-family: Arial, sans-serif; font-size: 11px; text-transform: uppercase; letter-spacing: 0.2em; color: rgba(255,255,255,0.7); margin: 0 0 8px 0;">{escape_html(subtitle)}</p>
              <h1 style="font-family: Georgia, serif; font-size: 36px; font-weight: 700; color: {COLORS['on_primary']}; margin: 0 0 16px 0; line-height: 1.1; letter-spacing: -0.02em;">{escape_html(title)}</h1>
              <table role="presentation" border="0" cellpadding="0" cellspacing="0" style="margin: 0 auto;">
                <tr><td style="width: 96px; height: 6px; background-color: {COLORS['tertiary_fixed_dim']}; border-radius: 3px; font-size: 0; line-height: 0;">&nbsp;</td></tr>
              </table>
            </td>
          </tr>
          <!-- Content -->
          <tr>
            <td class="mobile-padding" style="padding: 0;">
{content}
            </td>
          </tr>
          <!-- Footer -->
          <tr>
            <td style="background-color: {COLORS['surface_container']}; padding: 48px 40px; text-align: center;">
              <p style="font-family: Georgia, serif; font-size: 20px; font-weight: 700; color: {COLORS['primary']}; margin: 0 0 24px 0;">nanobot-ai</p>
              <p style="font-size: 12px; color: {COLORS['on_surface_variant']}; line-height: 1.6; opacity: 0.7; margin: 0;">
                Generated by nanobot-ai Research Report Generations Skill.<br/>
                For informational purposes only.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
'''


def main():
    parser = argparse.ArgumentParser(description="Convert markdown research report to professional HTML")
    parser.add_argument("--markdown", "-m", required=True, help="Path to input markdown file")
    parser.add_argument("--output", "-o", required=True, help="Path to output HTML file")
    parser.add_argument("--title", "-t", help="Override report title")
    parser.add_argument("--subtitle", "-s", default="Research Report", help="Report subtitle")
    parser.add_argument("--email", action="store_true", help="Generate email-compatible HTML")
    args = parser.parse_args()

    md_path = Path(args.markdown)
    if not md_path.exists():
        print(f"Error: Markdown file not found: {md_path}", file=sys.stderr)
        sys.exit(1)

    md_text = md_path.read_text(encoding="utf-8")
    parsed = parse_markdown(md_text)

    html = build_html(parsed, title=args.title, subtitle=args.subtitle, email_mode=args.email)

    out_path = Path(args.output)
    out_path.write_text(html, encoding="utf-8")
    print(f"Generated {'email ' if args.email else ''}HTML report: {out_path.absolute()}")


if __name__ == "__main__":
    main()
