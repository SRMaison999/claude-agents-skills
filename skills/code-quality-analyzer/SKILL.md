---
name: code-quality-analyzer
description: Analyze React/TypeScript components for UX issues, accessibility problems, unused code, and missing error handling. Use when reviewing code quality or investigating user-reported issues. Reports only concrete issues found in the actual code.
---

# Code Quality Analyzer

Perform rigorous code analysis on React/TypeScript components to find real, actionable issues.

## Core Principle

**NEVER HALLUCINATE.** Only report issues that are verifiably present in the code you've read. If you haven't read the file, don't make assumptions about it.

## Analysis Checklist

### 1. Unused State Variables
- Look for `useState`, `useRef`, `useCallback` declarations
- Check if the variable is used anywhere in the component
- **Issue if:** Variable is declared but never referenced

### 2. Non-Functional Buttons
- Find all `<button>` elements and event handlers
- Check if `onClick` handlers actually do something
- **Issue if:** Button has `onClick={() => console.log(...)}` or `onClick={() => { /* TODO */ }}`
- **Issue if:** Button calls a function that doesn't exist

### 3. Missing Error Handling
- Find all async operations, API calls, and state updates
- Check if they're wrapped in try/catch blocks
- **Issue if:** `updateProject()`, `fetch()`, or similar operations have no error handling
- **Issue if:** User gets no feedback when operation fails

### 4. Browser confirm() Dialogs
- Search for `confirm(` usage
- **Issue if:** Using native browser confirm instead of custom modal
- These look unprofessional and can't be styled

### 5. Destructive Actions Without Confirmation
- Find delete/remove operations
- Check if there's a confirmation step
- **Issue if:** Destructive action (delete, clear, reset) has no confirmation

### 6. Loading States
- Find async operations
- Check if there's a loading indicator shown to user
- **Issue if:** Long operation with no visual feedback

### 7. Empty States
- Check if component handles empty data gracefully
- **Issue if:** Shows blank screen when data is empty instead of helpful message

### 8. Accessibility Quick Checks
- Icon-only buttons should have `aria-label` or `title`
- Interactive elements should have accessible names
- **Issue if:** `<button><Icon /></button>` with no label

## How to Verify Issues

For each potential issue:

1. **Read the actual code** - Don't assume, verify
2. **Search the entire file** - Use grep/search to confirm variable usage
3. **Check line numbers** - Provide exact locations
4. **Extract relevant code** - Show the problematic code snippet
5. **Explain the impact** - Why does this matter to the user?

## Report Format

For each issue found:

```
Issue #N: [Brief Title]
File: [path/to/file.tsx]
Line: [line number(s)]

Code:
[exact code snippet from the file]

Problem: [What's wrong and why]

How I verified:
- [Step 1]
- [Step 2]
- [Conclusion]

User Impact: [How this affects the end user]

Fix: [Specific solution]

Effort: [Time estimate]
```

## Example Report

```
Issue #1: Unused State Variable - editingRole
File: src/components/planning/RolesAndTeamsStep.tsx
Lines: 21, 266

Code:
// Line 21
const [editingRole, setEditingRole] = useState<string | null>(null)

// Line 266
<button onClick={() => setEditingRole(role.id)}>
  <Edit2 className="w-3 h-3" />
</button>

Problem: The editingRole state is declared and set when the Edit button is clicked, but this state is never read anywhere in the component.

How I verified:
- Searched the entire file (541 lines) for "editingRole"
- Found only 2 occurrences: declaration (line 21) and setter (line 266)
- No conditional rendering based on editingRole
- No modal component that checks if editingRole !== null

User Impact: The Edit button appears clickable with hover effect, but clicking it does absolutely nothing visible. Users will think it's broken.

Fix: Either implement edit functionality (add modal) or disable/remove the button

Effort: 2-4 hours (implement) or 5 minutes (disable/remove)
```

## What NOT to Report

- Don't report issues in files you haven't read
- Don't report "possible" issues without verification
- Don't suggest improvements that aren't actual bugs
- Don't report style preferences unless they're inconsistencies

## Summary Format

At the end of your report:

```
Summary
Total Issues Found: [number]
- Critical: [count] ([brief description])
- Important: [count] ([brief description])
- Minor: [count] ([brief description])

Estimated Total Fix Time: [time range]

Top Priority:
1. [Most important fix]
2. [Second priority]
3. [Third priority]
```
