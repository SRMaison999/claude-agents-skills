---
name: accessibility-checker
description: Analyze React/TypeScript components for accessibility issues including ARIA labels, keyboard navigation, color contrast, focus management, and semantic HTML. Reports only concrete accessibility violations found in the actual code.
---

# Accessibility Checker

Perform rigorous accessibility (a11y) analysis on React/TypeScript components to find real, actionable issues that affect users with disabilities.

## Core Principle

**NEVER HALLUCINATE.** Only report issues that are verifiably present in the code you've read. If you haven't read the file, don't make assumptions about it.

## Analysis Checklist

### 1. Missing ARIA Labels

- Find interactive elements: `<button>`, `<input>`, `<select>`, `<textarea>`, icon-only buttons
- Check if they have accessible names via:
  - Text content (e.g., `<button>Save</button>`)
  - `aria-label` attribute
  - `aria-labelledby` attribute
  - `title` attribute (less preferred but acceptable)
- **Issue if:** Icon-only button with no label: `<button><XIcon /></button>`

### 2. Non-Semantic HTML

- Find clickable `<div>` or `<span>` elements
- **Issue if:** `<div onClick={...}>` instead of `<button>`
- **Issue if:** `<div>` used for interactive elements that should be buttons/links
- Semantic HTML provides keyboard navigation and screen reader support automatically

### 3. Keyboard Navigation

- Check if interactive elements are keyboard accessible
- **Issue if:** `onClick` on non-focusable element without `tabIndex={0}`
- **Issue if:** Custom dropdowns/modals without keyboard support (Escape to close, Arrow keys to navigate)

### 4. Focus Management

- Check if modals/dialogs manage focus properly
- **Issue if:** Modal opens but focus stays on background
- **Issue if:** No visual focus indicator (`:focus` styles removed)
- **Issue if:** Focus trap not implemented in modals

### 5. Form Labels

- Find all form inputs
- **Issue if:** `<input>` without associated `<label>`
- **Issue if:** Placeholder used as label (placeholders disappear when typing)
- Labels should be visible and associated via `htmlFor`/`id` or by wrapping

### 6. Image Alt Text

- Find all `<img>` tags and icon components
- **Issue if:** `<img>` without `alt` attribute
- **Issue if:** Decorative images with descriptive alt (should be `alt=""`)
- **Issue if:** Important icons without text alternative

### 7. Color as Only Indicator

- Look for error states, status indicators, warnings
- **Issue if:** Error shown only by red color without text/icon
- **Issue if:** Required fields indicated only by color
- Users with color blindness need additional indicators

### 8. Dynamic Content Announcements

- Find dynamic updates (toasts, alerts, live regions)
- **Issue if:** Important updates not announced to screen readers
- Should use `role="alert"`, `role="status"`, or `aria-live`

### 9. Disabled Elements Without Explanation

- Find `disabled` buttons/inputs
- **Issue if:** Button disabled with no explanation why
- Should have tooltip or nearby text explaining how to enable it

### 10. Modal/Dialog Accessibility

- Check modal implementations
- **Issue if:** Missing `role="dialog"` or `role="alertdialog"`
- **Issue if:** No `aria-labelledby` or `aria-label` on modal
- **Issue if:** Can't close with Escape key

## WCAG References

- **WCAG 2.1 Level A**: Minimum accessibility (legal requirement in many countries)
- **WCAG 2.1 Level AA**: Target for most websites (includes color contrast)
- **WCAG 2.1 Level AAA**: Enhanced accessibility

Common criteria:
- **1.1.1** Non-text Content (images need alt text)
- **1.3.1** Info and Relationships (semantic HTML)
- **2.1.1** Keyboard accessible
- **2.4.7** Focus Visible
- **3.3.2** Labels or Instructions (form labels)
- **4.1.2** Name, Role, Value (ARIA for custom components)

## How to Verify Issues

1. **Read the actual code** - Don't assume
2. **Check each interactive element** - Buttons, links, inputs
3. **Look for ARIA attributes** - Search for `aria-`
4. **Check semantic HTML** - Are divs used as buttons?
5. **Verify focus management** - Modal focus, keyboard nav

## Report Format

```
Issue #N: [Brief Title]
File: [path/to/file.tsx]
Line: [line number]

Code:
[exact code snippet]

Problem: [Accessibility violation]

WCAG Criterion: [e.g., 4.1.2 Name, Role, Value (Level A)]

User Impact: [How this affects users with disabilities]

How I verified:
- [Verification steps]

Fix:
[Specific accessible solution with code example]

Effort: [Time estimate]
```

## Example Report

```
Issue #1: Icon-only button without accessible label
File: src/components/Header.tsx
Line: 45

Code:
<button onClick={toggleMenu} className="p-2">
  <Menu className="w-5 h-5" />
</button>

Problem: Button contains only an icon with no accessible name for screen readers

WCAG Criterion: 4.1.2 Name, Role, Value (Level A)

User Impact: Screen reader users hear "button" with no indication of what it does

How I verified:
- Searched for aria-label, aria-labelledby, and title attributes
- Button contains only <Menu /> icon component
- No accessible name provided

Fix:
<button
  onClick={toggleMenu}
  className="p-2"
  aria-label="Toggle navigation menu"
>
  <Menu className="w-5 h-5" />
</button>

Effort: 2 minutes per button
```

## What NOT to Report

- Don't report contrast issues without actual color values
- Don't assume keyboard behavior without checking implementation
- Don't report theoretical issues - only verified problems
- Don't report styling preferences that don't affect accessibility

## Testing Recommendations

After fixing issues, recommend testing with:
- Keyboard only (Tab, Enter, Escape, Arrow keys)
- Screen reader (NVDA, JAWS, VoiceOver)
- Browser devtools accessibility inspector
- axe DevTools browser extension

## Summary Format

```
Summary
Total Accessibility Issues: [number]
- Critical (WCAG Level A): [count]
- Important (WCAG Level AA): [count]
- Enhancement (WCAG Level AAA): [count]

Top Priority:
1. [Most important issue]
2. [Second priority]
3. [Third priority]

Estimated Fix Time: [time range]
```
