# Design System Specification: The Academic Editorial

## 1. Overview & Creative North Star
**Creative North Star: "The Modern Archivist"**
This design system moves away from the sterile, "template-heavy" feel of traditional corporate dashboards. Instead, it draws inspiration from high-end editorial journals and architectural monographs. The goal is to present complex research data not just as information, but as an authoritative narrative.

We break the "standard UI" mold by embracing **intentional asymmetry** and **tonal depth**. Rather than using rigid boxes and lines to separate thoughts, we use expansive white space and shifting planes of color. The result is a layout that feels curated, quiet, and deeply professional—allowing the research to breathe and the typography to command authority.

---

## 2. Colors & Surface Philosophy
The palette is rooted in a "Deep Blue & Charcoal" foundation, providing a sense of permanence and intellectual rigor.

### The "No-Line" Rule
To achieve a premium editorial feel, **1px solid borders for sectioning are strictly prohibited.** Structural boundaries must be defined exclusively through background color shifts. For example, a research methodology section (`surface-container-low`) should sit directly against the main `surface` without a stroke.

### Surface Hierarchy & Nesting
We treat the UI as a series of physical layers—like fine bond paper stacked on a dark oak desk.
*   **Base Layer:** `surface` (#f9f9ff) for the main document body.
*   **Secondary Context:** `surface-container-low` (#f0f3ff) for sidebars or secondary insights.
*   **Prominent Callouts:** `surface-container-high` (#dee8ff) for key takeaways.
*   **Floating Elements:** `surface-container-lowest` (#ffffff) for interactive cards to create a "lifted" effect.

### The Glass & Gradient Rule
For high-impact areas (e.g., Executive Summaries), use **Glassmorphism**. Apply `surface-tint` at 10% opacity with a `24px` backdrop blur. For primary CTAs or Report Headers, use a subtle linear gradient from `primary` (#002045) to `primary_container` (#1a365d) at a 135-degree angle to add "soul" and dimension.

---

## 3. Typography
The system employs a sophisticated "Serif-on-Sans" pairing to balance academic heritage with modern readability.

*   **Display & Headlines (Noto Serif):** Used to establish an authoritative voice. `display-lg` should be used with tight letter-spacing (-0.02em) to create a striking, masthead-like appearance.
*   **Body (Work Sans):** Chosen for its exceptional legibility in long-form research. Use `body-lg` for the primary narrative to ensure the reader never feels fatigued.
*   **Labels & Metadata (Public Sans):** A more utilitarian sans-serif used for data points, chart labels, and captions.

**Typography Scale:**
- **Display LG:** 3.5rem (Noto Serif) — *Report Titles*
- **Headline MD:** 1.75rem (Noto Serif) — *Chapter Headers*
- **Body LG:** 1rem (Work Sans) — *Primary Narrative*
- **Label MD:** 0.75rem (Public Sans) — *Data Legends / Micro-copy*

---

## 4. Elevation & Depth
Depth is achieved through **Tonal Layering** rather than structural shadows.

*   **The Layering Principle:** To lift a component, place a `surface-container-lowest` card upon a `surface-container-low` background. This creates a soft, natural "step" in the layout.
*   **Ambient Shadows:** If a floating state is required (e.g., a hovering data tooltip), use a highly diffused shadow: `0px 12px 32px rgba(18, 28, 44, 0.06)`. The shadow color must be a tint of `on_surface` to mimic natural light.
*   **The Ghost Border:** If a boundary is required for accessibility in data tables, use `outline_variant` (#c4c6cf) at **15% opacity**. Never use 100% opaque lines.

---

## 5. Components

### Data Tables
*   **Layout:** No vertical lines. Horizontal lines only, using the "Ghost Border" rule.
*   **Header:** `label-md` in `on_surface_variant`, all-caps with 0.05em tracking.
*   **Row Highlight:** On hover, shift the background to `surface-container-highest`.

### Research Callout Boxes
*   **Style:** Use `surface_container` (#e7eeff) with a 4px left-accent border of `tertiary_fixed_dim` (#f8bc4b). 
*   **Typography:** Use `title-md` for the callout header to create a distinct visual break from the body text.

### Charts & Data Visualization
*   **Primary Series:** `primary` (#002045)
*   **Comparison Series:** `secondary` (#545f72)
*   **Highlight/Trend:** `tertiary_fixed_dim` (#f8bc4b)
*   **Note:** All chart backgrounds should be transparent to let the surface hierarchy remain visible.

### Buttons
*   **Primary:** Solid `primary` fill, `on_primary` text. `xl` roundedness (0.75rem).
*   **Secondary:** No fill. "Ghost Border" (20% opacity `outline`) with `primary` text.
*   **Tertiary:** Text-only, using `primary` and `title-sm` weight.

### Input Fields
*   **Style:** Filled style using `surface_container_low`. 
*   **Indicator:** A 2px bottom-only stroke using `primary` that activates on focus. This maintains the "editorial" look while providing clear interaction states.

---

## 6. Do’s and Don’ts

### Do
*   **Do** use asymmetrical margins (e.g., a wider left margin for body text) to create an editorial feel.
*   **Do** use `tertiary_fixed_dim` (#f8bc4b) sparingly as a "highlighter" for the most critical data point in a report.
*   **Do** lean on the `spacing-xl` (48px+) scale to separate major research chapters.

### Don’t
*   **Don't** use pure black (#000000) for text. Use `on_surface` (#121c2c) to maintain a sophisticated, ink-on-paper feel.
*   **Don't** use standard "drop shadows" on cards; use background color shifts to define hierarchy.
*   **Don't** use dividers between list items. Use vertical padding and `body-md` typography to create separation.

---

## 7. Roundedness Scale
To maintain a professional yet modern feel, we use a "Soft-Square" approach:
*   **Cards/Containers:** `lg` (0.5rem)
*   **Buttons/Chips:** `xl` (0.75rem)
*   **Small UI Elements (Checkboxes):** `sm` (0.125rem)