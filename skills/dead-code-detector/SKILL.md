---
name: dead-code-detector
description: Detect unused files, exports, dependencies, and dead code in JavaScript and TypeScript projects using Knip. Use when users ask to find dead code, unused code, clean up codebase, identify unused dependencies, find unused exports, or optimize bundle size.
---

# Dead Code Detector

Detect and report unused files, exports, dependencies, and dead code in JavaScript and TypeScript projects.

## Quick Start

Run the analysis script on a project directory:

```bash
scripts/analyze_dead_code.sh /path/to/project
```

This generates two reports:
- `/tmp/knip-report.json` - Machine-readable results
- `/tmp/knip-report.md` - Human-readable markdown report

## Analysis Workflow

### 1. Run Analysis

Execute the analysis script on the target directory:

```bash
scripts/analyze_dead_code.sh /path/to/project
```

### 2. Read Reports

Read both reports to get comprehensive results:

```bash
cat /tmp/knip-report.md    # Human-readable summary
cat /tmp/knip-report.json  # Detailed data
```

### 3. Generate User Report

Create a detailed report for the user with:

- **Summary Statistics**
  - Total unused files count
  - Total unused exports count
  - Total unused dependencies count
  - Estimated lines of code that can be removed

- **Categorized Findings**
  - Unused files (with full paths)
  - Unused exports (file + export name)
  - Unused dependencies (package names)
  - Unused devDependencies (package names)

- **Impact Analysis**
  - Potential bundle size reduction
  - Maintenance burden reduction
  - Risk assessment for each finding

- **Recommendations**
  - Prioritized cleanup tasks (high/medium/low priority)
  - Safe removal candidates vs items requiring investigation
  - Suggested cleanup order

## What Knip Detects

Knip finds:
- **Unused files** - Files never imported anywhere
- **Unused exports** - Exported functions/components/types never used
- **Unused dependencies** - npm packages in package.json but never imported
- **Unused devDependencies** - Development packages not used
- **Duplicate exports** - Same functionality exported multiple times
- **Circular dependencies** - Files importing each other

## Report Format

Provide results in this structure:

```markdown
# Dead Code Analysis Report

## Summary
- 🗑️ **Unused Files**: X files (estimated Y lines)
- 📦 **Unused Exports**: X exports across Y files
- 📚 **Unused Dependencies**: X packages
- 💾 **Potential Savings**: ~X KB bundle reduction

## Findings

### High Priority (Safe to Remove)
1. **Unused Files**
   - `src/utils/old-helper.ts` (45 lines)
   - `src/components/DeprecatedButton.tsx` (120 lines)

2. **Unused Dependencies**
   - `lodash` (can remove from package.json)
   - `moment` (can remove, using date-fns instead)

### Medium Priority (Requires Review)
1. **Unused Exports**
   - `formatDate` in `src/utils/date.ts:23`
   - `UserType` in `src/types/user.ts:15`

### Low Priority (Further Investigation)
1. **Potential Test Code**
   - Files in `src/__tests__` might be intentionally unused

## Recommendations
1. Start with unused dependencies - safest to remove
2. Review unused exports - some might be part of public API
3. Check unused files for historical/documentation value
4. Run tests after each cleanup step

## Next Steps
- [ ] Remove X unused dependencies
- [ ] Delete X unused files
- [ ] Clean up X unused exports
- [ ] Re-run analysis to verify
```

## Important Notes

- **Always preserve public API exports** even if unused internally
- **Check git history** before deleting files (might contain valuable context)
- **Run tests** after cleanup to ensure nothing breaks
- **Consider library mode** - some exports might be for library consumers
- **Knip configuration** can be customized via `knip.json` for project-specific needs

## Troubleshooting

If Knip reports false positives:
1. Check if project uses dynamic imports
2. Verify entry points are correctly configured
3. Look for string-based imports (e.g., `require(variableName)`)
4. Consider adding exceptions to knip.json configuration

## Resources

- Knip documentation: https://knip.dev/
- This skill uses the official Knip tool (open source, free)
