---
name: refactoring-analyzer
description: Analyze React/TypeScript code to identify refactoring opportunities including code duplication, complex functions, components with too many responsibilities, and opportunities to extract hooks or components. Use when evaluating code maintainability or planning technical improvements.
---

# Refactoring Analyzer

Perform systematic analysis of React/TypeScript code to identify concrete refactoring opportunities that will improve code maintainability, readability, and reusability.

## Core Principle

**NEVER HALLUCINATE.** Only report refactoring opportunities based on actual code patterns you've verified in the files you've read. Every suggestion must include:
- Exact line numbers
- Real code snippets from the file
- Measurable metrics (lines of code, cyclomatic complexity, duplication count)
- Concrete refactoring steps

## Analysis Checklist

### 1. Code Duplication
- Search for repeated code blocks (3+ lines that appear multiple times)
- Look for similar JSX patterns across components
- Check for duplicated logic in event handlers
- **Issue if:** Same code appears in 2+ places with minimal variation
- **Opportunity:** Extract to shared function, custom hook, or component

### 2. Function/Component Length
- Count lines of code in each function/component
- **Issue if:** Function > 50 lines (excluding comments)
- **Issue if:** Component > 300 lines
- **Opportunity:** Split into smaller, focused functions/components

### 3. Cyclomatic Complexity
- Count conditional branches (if, else, switch, ternary, &&, ||)
- Count loops (for, while, map, filter, etc.)
- **Issue if:** Function has 5+ decision points
- **Opportunity:** Extract complex logic into separate functions

### 4. Too Many Responsibilities (Single Responsibility Principle)
- Identify if component handles multiple concerns
- **Issue if:** Component handles:
  - Data fetching AND UI rendering AND business logic
  - Multiple unrelated features
  - Both presentation AND container logic
- **Opportunity:** Split into container/presentation or separate components

### 5. Custom Hook Opportunities
- Look for stateful logic that's duplicated
- Find useEffect + useState patterns that could be reusable
- **Issue if:** Same state management pattern appears in multiple components
- **Opportunity:** Extract to custom hook (useLocalStorage, useDebounce, etc.)

### 6. Component Extraction Opportunities
- Find JSX blocks that are self-contained and reused
- Look for logical UI sections that could be independent
- **Issue if:** Large JSX block (20+ lines) appears multiple times or handles distinct concern
- **Opportunity:** Extract to separate component

### 7. Props Drilling
- Trace props being passed through multiple component levels
- **Issue if:** Prop passes through 3+ levels without being used in intermediaries
- **Opportunity:** Use Context API or state management library

### 8. Magic Numbers/Strings
- Find hardcoded values used multiple times
- **Issue if:** Same literal value appears 3+ times
- **Opportunity:** Extract to named constant

### 9. Long Parameter Lists
- Count function parameters
- **Issue if:** Function has 5+ parameters
- **Opportunity:** Group related parameters into object

### 10. Complex Conditional Logic
- Find nested ternaries or complex boolean expressions
- **Issue if:** Ternary nested 2+ levels or boolean with 4+ operators
- **Opportunity:** Extract to well-named variable or function

### 11. Dead Code
- Search for unused imports, variables, functions
- **Issue if:** Code defined but never called/referenced
- **Opportunity:** Remove to reduce maintenance burden

### 12. Inconsistent Patterns
- Compare similar components for different approaches
- **Issue if:** Same problem solved differently in different places
- **Opportunity:** Standardize on one approach

## How to Verify Issues

For each potential refactoring:

1. **Read the actual code** - Don't assume, verify the pattern exists
2. **Measure objectively** - Count lines, occurrences, parameters
3. **Check usage** - Search entire codebase to confirm duplication
4. **Provide exact locations** - Line numbers for all instances
5. **Extract relevant code** - Show the actual code that needs refactoring
6. **Quantify impact** - Lines saved, complexity reduced, reusability gained

## Report Format

For each refactoring opportunity:

```
Refactoring Opportunity #N: [Brief Title]
Type: [Code Duplication | Long Function | Too Many Responsibilities | etc.]
Priority: [High | Medium | Low]
Files Affected: [list of files]

Current State:
File: [path/to/file.tsx]
Lines: [line numbers]

Code:
[exact code snippet showing the problem]

Metrics:
- [e.g., "Function length: 87 lines"]
- [e.g., "Duplicated in 3 locations"]
- [e.g., "Cyclomatic complexity: 12"]

Problem: [What makes this code hard to maintain/understand]

How I verified:
- [Step 1: e.g., "Counted 87 lines in function"]
- [Step 2: e.g., "Found identical pattern in ComponentB.tsx:45 and ComponentC.tsx:123"]
- [Conclusion]

Refactoring Steps:
1. [Specific step with code example]
2. [Next step]
3. [Final step]

After Refactoring:
[Show what the improved code would look like]

Benefits:
- [e.g., "Reduces duplication by 45 lines"]
- [e.g., "Makes logic reusable across 3 components"]
- [e.g., "Improves testability"]

Effort: [Time estimate: 30 min | 1-2 hours | 4-6 hours]

Risk: [Low | Medium | High] - [Explanation of risk level]
```

## Example Report

```
Refactoring Opportunity #1: Extract Repeated Data Fetching Logic
Type: Code Duplication + Custom Hook Opportunity
Priority: High
Files Affected: UserProfile.tsx, ProjectList.tsx, TeamDashboard.tsx

Current State:
File: src/components/UserProfile.tsx
Lines: 23-45

Code:
const [data, setData] = useState<User | null>(null)
const [loading, setLoading] = useState(true)
const [error, setError] = useState<string | null>(null)

useEffect(() => {
  const fetchData = async () => {
    try {
      setLoading(true)
      const response = await fetch(`/api/users/${userId}`)
      if (!response.ok) throw new Error('Failed to fetch')
      const result = await response.json()
      setData(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }
  fetchData()
}, [userId])

Metrics:
- Duplicated in 3 locations (UserProfile.tsx:23, ProjectList.tsx:34, TeamDashboard.tsx:67)
- Total duplicated lines: 23 × 3 = 69 lines
- Pattern is identical except for URL

Problem: Same data fetching pattern repeated in multiple components. Any change to error handling or loading logic must be duplicated 3 times, increasing maintenance burden and bug risk.

How I verified:
- Searched codebase for "useState.*loading.*true"
- Found 3 exact matches with identical pattern
- Confirmed all use fetch + try/catch + loading/error states
- Verified only difference is the API endpoint URL

Refactoring Steps:
1. Create custom hook `useFetch`:

```typescript
// src/hooks/useFetch.ts
export function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const response = await fetch(url)
        if (!response.ok) throw new Error('Failed to fetch')
        const result = await response.json()
        setData(result)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [url])

  return { data, loading, error }
}
```

2. Replace in UserProfile.tsx:

```typescript
const { data, loading, error } = useFetch<User>(`/api/users/${userId}`)
```

3. Repeat for ProjectList.tsx and TeamDashboard.tsx

After Refactoring:
Each component reduced from 23 lines of fetching logic to 1 line hook call.

Benefits:
- Eliminates 69 lines of duplicated code
- Centralizes data fetching logic in one testable hook
- Future improvements (caching, retry logic) only need to be added once
- Makes components more focused on presentation

Effort: 1-2 hours (create hook + update 3 components + write tests)

Risk: Low - Pure extraction, no behavior change, easy to test
```

## Priority Guidelines

**High Priority:**
- Code duplicated 3+ times (high maintenance cost)
- Functions > 100 lines or complexity > 10 (hard to understand/test)
- Components handling 3+ unrelated concerns (violates SRP)
- Props drilling > 3 levels (indicates architectural issue)

**Medium Priority:**
- Code duplicated 2 times
- Functions 50-100 lines or complexity 5-10
- Components 200-300 lines
- Long parameter lists (5+ params)

**Low Priority:**
- Magic numbers/strings (2-4 occurrences)
- Minor inconsistencies in patterns
- Opportunities for slight simplification

## What NOT to Report

- Don't suggest refactoring working code that's already clear and simple
- Don't report style preferences without measurable benefit
- Don't suggest patterns that would increase complexity
- Don't recommend frameworks/libraries without clear justification
- Don't report "possible" issues - only verified patterns

## Risk Assessment

For each refactoring, assess risk:

**Low Risk:**
- Pure extractions (no behavior change)
- Dead code removal
- Renaming variables/constants

**Medium Risk:**
- Changing component structure
- Introducing new abstractions
- Refactoring with moderate test coverage

**High Risk:**
- Major architectural changes
- Refactoring critical business logic
- Areas with no test coverage

## Summary Format

At the end of your report:

```
Refactoring Summary
Total Opportunities Found: [number]

By Priority:
- High: [count] ([brief description])
- Medium: [count] ([brief description])
- Low: [count] ([brief description])

By Type:
- Code Duplication: [count]
- Long Functions/Components: [count]
- Too Many Responsibilities: [count]
- Custom Hook Opportunities: [count]
- Other: [count]

Potential Impact:
- Lines of code reduced: ~[number]
- Files affected: [count]
- Estimated total effort: [time range]

Recommended Order:
1. [Highest value, lowest risk refactoring]
2. [Next priority]
3. [Third priority]

Quick Wins (< 1 hour, high impact):
- [List of easy but valuable refactorings]
```

## Analysis Process

When analyzing files:

1. **Start with overview** - Read entire file, note structure
2. **Measure systematically** - Count lines, complexity, duplication
3. **Search for patterns** - Use grep to find similar code across codebase
4. **Verify each issue** - Confirm with exact line numbers and code
5. **Prioritize by impact** - Focus on high-value, low-risk improvements
6. **Provide actionable steps** - Give concrete refactoring instructions

## Testing Considerations

For each refactoring, consider:
- Is there existing test coverage?
- Will tests need to be updated?
- Should new tests be added after refactoring?
- How can we verify behavior hasn't changed?

Remember: The goal is to make code more maintainable WITHOUT changing behavior. Every refactoring should be incremental, testable, and reversible.
