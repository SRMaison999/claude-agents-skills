---
name: visual-consistency-checker
description: Analyze multiple React/TypeScript components to detect visual and style inconsistencies. Compares UI patterns like tabs, buttons, cards, spacing, and typography across different sections. Reports only concrete inconsistencies found by comparing actual code.
---

# Visual Consistency Checker

Analyze multiple components to find visual inconsistencies where the same UI element type has different styles across the application.

## Core Principle

**NEVER HALLUCINATE.** Only report issues that are verifiably present in the code you've read. This skill REQUIRES reading multiple files to compare styles. If you haven't read and compared at least 2 files, don't make assumptions.

## When to Use This Skill

Use this skill when:
- Analyzing multiple related components (e.g., different section views)
- User reports that "this page looks different from that page"
- Reviewing UI consistency across the application
- Creating design system documentation

## Analysis Checklist

### 1. Tab Styles

- Find components using tabs (navigation between views)
- Extract the tab styling: variant, colors, borders, spacing
- **Issue if:** Same UI pattern (tabs) uses different styles in different places

Example inconsistency:
```tsx
// File A - using "pill" variant
<Tabs variant="pill" className="bg-gray-100">

// File B - using "underline" variant
<Tabs variant="underline" className="border-b">
```

### 2. Button Styles

- Find all button types: primary, secondary, danger, ghost
- Compare `className` patterns across components
- **Issue if:** Similar buttons have different sizing, padding, or hover effects

Check:
- Primary action buttons
- Secondary/cancel buttons
- Icon buttons
- Danger/destructive action buttons

### 3. Card/Container Styles

- Find card/container components
- Compare: borders, shadows, padding, border-radius
- **Issue if:** Content cards use different shadows or spacing

Example:
```tsx
// File A
<div className="bg-white rounded-lg shadow-sm p-6">

// File B
<div className="bg-white rounded-md shadow-md p-4">
// Different: radius (lg vs md), shadow (sm vs md), padding (6 vs 4)
```

### 4. Spacing Patterns

- Look at spacing between elements (gap, margin, padding)
- **Issue if:** Similar layouts use different spacing scales
- Tailwind scale should be consistent: `gap-2`, `gap-4`, `gap-6`, etc.

Common patterns to check:
- Gap between form fields
- Padding inside sections
- Margin between major sections

### 5. Typography

- Compare heading styles: sizes, weights, colors
- Compare body text styles
- **Issue if:** H2 headings have different sizes in different pages

Example:
```tsx
// File A
<h2 className="text-2xl font-bold text-gray-900">

// File B
<h2 className="text-xl font-semibold text-gray-800">
// Inconsistent: size, weight, and color
```

### 6. Empty States

- Find empty state messages
- **Issue if:** Different styling or tone for similar situations

### 7. Loading Indicators

- Find loading spinners/skeletons
- **Issue if:** Different components use different loading patterns

### 8. Icons

- Check icon sizes and positioning
- **Issue if:** Similar contexts use different icon sizes
- Standard sizes: `w-4 h-4`, `w-5 h-5`, `w-6 h-6`

### 9. Form Elements

- Compare input field styling
- Compare label styling
- **Issue if:** Forms in different sections look different

### 10. Modal/Dialog Styles

- Compare modal header, body, footer styling
- **Issue if:** Modals have inconsistent padding or button placement

## How to Verify Inconsistencies

1. **Read at least 2 files** - You must compare actual code
2. **Extract exact className values** - Don't paraphrase
3. **Identify the pattern** - What UI element type is it?
4. **Compare line by line** - Show the actual differences
5. **Assess impact** - Does this confuse users?

## Report Format

```
Inconsistency #N: [UI Element Type] Style Mismatch
Files:
- [path/to/fileA.tsx:line]
- [path/to/fileB.tsx:line]

Pattern: [What UI pattern this is - tabs, buttons, etc.]

File A Code:
[exact code snippet from File A]

File B Code:
[exact code snippet from File B]

Differences:
- [Specific difference 1]
- [Specific difference 2]
- [Specific difference 3]

User Impact: [How this affects user experience]

Recommendation: [Which style to standardize on and why]

Effort: [Time to fix]
```

## Example Report

```
Inconsistency #1: Tab Component Style Mismatch
Files:
- src/components/logistics/LogisticsView.tsx:89
- src/components/planning/PlanningView.tsx:67

Pattern: Tab navigation between sections

File A Code (Logistics):
<Tabs value={activeTab} variant="pill" className="mb-6">
  <TabsList className="grid grid-cols-3 bg-gray-100">
    <TabsTrigger value="transport">Transport</TabsTrigger>

File B Code (Planning):
<Tabs value={activeSection} variant="underline">
  <TabsList className="border-b border-gray-200">
    <TabsTrigger value="roles">Équipes</TabsTrigger>

Differences:
- Variant: "pill" vs "underline"
- Background: gray-100 vs border-b
- Visual appearance: rounded pills vs underlined text

How I verified:
- Read both files completely
- Extracted exact className values
- Both serve same purpose (section navigation)

User Impact: Users see different navigation styles in different sections, making the app feel inconsistent and less professional

Recommendation: Standardize on "underline" variant:
- More modern appearance
- Cleaner, less visual weight
- Better for professional applications
- Already used in Planning section

Effort: 15 minutes (change variant + test)
```

## Comparison Strategy

To effectively find inconsistencies:

1. **Identify component types** first (tabs, cards, buttons)
2. **Read multiple files** with same component type
3. **Extract styling patterns** side by side
4. **Document differences** with exact code
5. **Recommend standard** based on best example

## What NOT to Report

- Minor differences that don't affect UX (e.g., `px-4` vs `px-3.5`)
- Intentional variations (e.g., primary vs secondary buttons)
- Different contexts requiring different styles
- Single-file issues (this skill is for cross-file comparison)

## Summary Format

```
Summary
Total Inconsistencies Found: [number]

By Category:
- Tabs/Navigation: [count]
- Buttons: [count]
- Cards/Containers: [count]
- Typography: [count]
- Spacing: [count]
- Other: [count]

Recommendations:
1. [Most important standardization]
2. [Second priority]
3. [Third priority]

Total Effort to Fix: [time estimate]

Next Steps:
1. Create design system documentation
2. Standardize components
3. Update all instances
```
