---
name: auto-documenter
description: Automatically generate documentation for TypeScript and React projects using TypeDoc and react-docgen-typescript. Use when users ask to generate documentation, create API docs, document components, find undocumented code, or improve code documentation.
---

# Auto Documenter

Automatically generate comprehensive documentation for TypeScript and React projects.

## Quick Start

Generate documentation for a project:

```bash
scripts/generate_docs.sh /path/to/project ./docs
```

This creates:
- API documentation (HTML) in `./docs/api/`
- Component analysis in `/tmp/component-files.txt`

## Documentation Workflow

### 1. Generate Documentation

Run the generation script:

```bash
scripts/generate_docs.sh /path/to/project ./output-dir
```

### 2. Analyze Results

Check for:
- Generated HTML documentation
- Component files discovered
- Missing documentation warnings

### 3. Identify Gaps

Read the generated docs and source files to find:
- Functions without JSDoc comments
- Components without prop descriptions
- Complex logic without explanations
- Missing examples for public APIs

### 4. Create User Report

Provide a comprehensive documentation report with:

- **Documentation Coverage**
  - Total files analyzed
  - Files with documentation vs without
  - Documentation coverage percentage

- **Missing Documentation**
  - Functions without JSDoc (file:line)
  - React components without prop descriptions
  - Types/interfaces without descriptions
  - Complex functions needing examples

- **Quality Issues**
  - Incomplete JSDoc (missing @param, @returns)
  - Vague descriptions ("does stuff")
  - Missing type information
  - No usage examples for complex APIs

- **Recommendations**
  - Priority files to document (based on public API, complexity)
  - Documentation templates to use
  - Suggested improvements

## Documentation Standards

### TypeScript Functions

Expected format:
```typescript
/**
 * Calculate the total price including tax
 * @param price - Base price before tax
 * @param taxRate - Tax rate as decimal (e.g., 0.15 for 15%)
 * @returns Total price including tax
 * @example
 * calculateTotal(100, 0.15) // Returns 115
 */
function calculateTotal(price: number, taxRate: number): number {
  return price * (1 + taxRate);
}
```

### React Components

Expected format:
```typescript
interface ButtonProps {
  /** Button label text */
  label: string;
  /** Click handler function */
  onClick: () => void;
  /** Visual style variant */
  variant?: 'primary' | 'secondary';
}

/**
 * Reusable button component with multiple variants
 * @example
 * <Button label="Click me" onClick={handleClick} variant="primary" />
 */
export function Button({ label, onClick, variant = 'primary' }: ButtonProps) {
  // ...
}
```

## Report Format

Structure the documentation analysis like this:

```markdown
# Documentation Analysis Report

## Coverage Summary
- 📊 **Files Analyzed**: X files
- ✅ **Documented**: Y files (Z%)
- ❌ **Undocumented**: N files
- ⚠️  **Partially Documented**: M files

## Generated Documentation
- 📖 API Documentation: `docs/api/index.html`
- ⚛️  React Components: X components analyzed

## Missing Documentation

### High Priority (Public API)
1. **`src/api/client.ts`** - Main API client
   - `fetchData()` at line 45 - no JSDoc
   - `handleError()` at line 78 - missing @param

2. **`src/components/DataTable.tsx`** - Core component
   - Component missing description
   - `columns` prop missing description
   - `onRowClick` prop missing description

### Medium Priority (Internal but Complex)
1. **`src/utils/transform.ts`**
   - `processData()` at line 23 - complex logic, needs explanation
   - Missing usage examples

### Low Priority
1. **`src/helpers/format.ts`**
   - Simple utility functions, but missing JSDoc

## Quality Issues

### Incomplete JSDoc
- `src/services/auth.ts:34` - Missing @returns
- `src/hooks/useData.ts:12` - Missing @example

### Vague Descriptions
- `src/utils/helpers.ts:56` - "Helper function" (not descriptive)

## Recommendations

1. **Start with Public API** (high priority items)
2. **Add JSDoc templates** for common patterns
3. **Include examples** for complex functions
4. **Document props** for all exported React components
5. **Generate docs site** with TypeDoc for team reference

## Next Steps
- [ ] Document X high-priority functions
- [ ] Add prop descriptions to Y components
- [ ] Create usage examples for Z APIs
- [ ] Re-generate docs to verify improvements
```

## Tools Used

This skill uses:
- **TypeDoc** - TypeScript documentation generator (free, open source)
- **react-docgen-typescript** - React props documentation (free, open source)

Both tools parse JSDoc comments and TypeScript types to generate documentation.

## Finding Undocumented Code

To find code needing documentation:

1. **Search for exported functions without JSDoc**:
   ```bash
   grep -B 1 "export function" src/**/*.ts | grep -v "/**"
   ```

2. **Find React components without descriptions**:
   Look for `interface Props` without JSDoc above

3. **Check for missing @param or @returns**:
   Review generated TypeDoc output for "Missing" warnings

## Configuration

TypeDoc can be configured via `typedoc.json`:

```json
{
  "entryPoints": ["src/index.ts"],
  "out": "docs",
  "exclude": ["**/*.test.ts", "**/*.spec.ts"],
  "includeVersion": true
}
```

## Troubleshooting

- **TypeDoc errors**: Check tsconfig.json is valid
- **No docs generated**: Verify entry points exist
- **Missing components**: Ensure .tsx files use proper exports
- **Incomplete docs**: Add more JSDoc comments to source

## Resources

- TypeDoc: https://typedoc.org/
- JSDoc tags: https://jsdoc.app/
- TSDoc standard: https://tsdoc.org/
