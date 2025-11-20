---
name: test-coverage-analyzer
description: Analyze test coverage for JavaScript and TypeScript projects using Vitest or Jest. Use when users ask to check test coverage, find untested code, identify missing tests, improve test quality, or analyze testing gaps.
---

# Test Coverage Analyzer

Analyze test coverage and identify untested code in JavaScript and TypeScript projects.

## Quick Start

Run coverage analysis on a project:

```bash
scripts/analyze_coverage.sh /path/to/project
```

This runs tests with coverage and generates:
- HTML coverage report: `coverage/index.html`
- JSON data: `coverage/coverage-final.json`
- Source files list: `/tmp/source-files.txt`
- Test files list: `/tmp/test-files.txt`

## Analysis Workflow

### 1. Run Coverage Analysis

Execute the coverage script:

```bash
scripts/analyze_coverage.sh /path/to/project
```

The script:
- Detects test framework (Vitest or Jest)
- Runs tests with coverage enabled
- Generates coverage reports
- Lists all source and test files

### 2. Review Coverage Data

Read the coverage reports:

```bash
cat coverage/coverage-summary.json  # Overall stats
# OR
# Open coverage/index.html in browser for visual report
```

### 3. Identify Gaps

Compare source files with test files to find:
- Files without any tests
- Functions with low coverage
- Critical paths untested
- Edge cases missing

### 4. Create User Report

Provide a comprehensive coverage analysis with:

- **Coverage Summary**
  - Overall coverage percentage (statements, branches, functions, lines)
  - Total files vs tested files
  - Trend (improving/declining)

- **Untested Code**
  - Files with 0% coverage (full path)
  - Files with <50% coverage
  - Critical functions untested
  - Edge cases not covered

- **High Priority Test Gaps**
  - Public API functions without tests
  - Error handling paths untested
  - Business logic missing coverage
  - Complex algorithms under-tested

- **Recommendations**
  - Priority tests to write (ranked by impact)
  - Test templates/patterns to use
  - Coverage targets by file type
  - Continuous testing setup

## Coverage Metrics

Understand the 4 coverage types:

1. **Statement Coverage** - % of code statements executed
2. **Branch Coverage** - % of if/else branches taken
3. **Function Coverage** - % of functions called
4. **Line Coverage** - % of lines executed

Aim for:
- **80%+** for business logic and public APIs
- **60%+** for utility functions
- **100%** for critical paths (auth, payments, data validation)

## Report Format

Structure the coverage analysis like this:

```markdown
# Test Coverage Analysis Report

## Coverage Summary
- 📊 **Overall Coverage**: X% (statements), Y% (branches)
- ✅ **Well Tested**: N files (>80% coverage)
- ⚠️  **Needs Tests**: M files (<50% coverage)
- ❌ **Untested**: P files (0% coverage)

## Detailed Metrics
| Metric | Coverage | Target | Status |
|--------|----------|--------|--------|
| Statements | 75% | 80% | 🟡 Close |
| Branches | 60% | 70% | 🔴 Below |
| Functions | 85% | 80% | 🟢 Good |
| Lines | 78% | 80% | 🟡 Close |

## High Priority Test Gaps

### Critical (Untested Business Logic)
1. **`src/services/payment.ts`** - 0% coverage
   - `processPayment()` - handles transactions, NO TESTS
   - `validateCard()` - critical validation, NO TESTS
   - **Risk**: High - financial transactions
   - **Priority**: Urgent

2. **`src/auth/validate.ts`** - 15% coverage
   - `verifyToken()` - only happy path tested
   - Missing: expired tokens, invalid signatures
   - **Risk**: High - security vulnerability
   - **Priority**: Urgent

### Medium Priority (Low Coverage)
1. **`src/utils/data-transform.ts`** - 45% coverage
   - Complex transformations under-tested
   - Edge cases missing (empty arrays, null values)
   - **Priority**: High

2. **`src/components/DataTable.tsx`** - 30% coverage
   - Sorting/filtering logic untested
   - Pagination edge cases missing
   - **Priority**: Medium

### Low Priority (Utilities)
1. **`src/helpers/format.ts`** - 0% coverage
   - Simple string formatting
   - Low risk but should test
   - **Priority**: Low

## Recommendations

### Immediate Actions
1. **Add tests for payment.ts** (URGENT - financial risk)
2. **Improve auth tests** (HIGH - security risk)
3. **Test data transformations** (MEDIUM - data integrity)

### Test Templates

For untested functions, use this pattern:

\`\`\`typescript
import { describe, it, expect } from 'vitest';
import { processPayment } from './payment';

describe('processPayment', () => {
  it('should process valid payment successfully', () => {
    // Happy path
  });

  it('should reject invalid card', () => {
    // Validation error
  });

  it('should handle network errors', () => {
    // Error handling
  });

  it('should prevent duplicate charges', () => {
    // Edge case
  });
});
\`\`\`

### Coverage Targets
- **Critical code**: 100% (auth, payments, validation)
- **Business logic**: 80%+
- **UI components**: 70%+
- **Utilities**: 60%+

## Next Steps
- [ ] Write X high-priority tests
- [ ] Improve coverage for Y critical files
- [ ] Set up coverage thresholds in CI/CD
- [ ] Re-run analysis to track progress
```

## Finding Untested Code

To identify files needing tests:

1. **Files without test files**:
   Compare `/tmp/source-files.txt` with `/tmp/test-files.txt`

2. **Low coverage from report**:
   Check `coverage/coverage-summary.json` for files below threshold

3. **Manual inspection**:
   Open `coverage/index.html` and look for red (untested) sections

## CI/CD Integration

Add coverage thresholds to prevent regression:

**Vitest** (`vitest.config.ts`):
```typescript
export default {
  test: {
    coverage: {
      statements: 80,
      branches: 70,
      functions: 80,
      lines: 80
    }
  }
};
```

**Jest** (`package.json`):
```json
{
  "jest": {
    "coverageThreshold": {
      "global": {
        "statements": 80,
        "branches": 70,
        "functions": 80,
        "lines": 80
      }
    }
  }
}
```

## Troubleshooting

- **No coverage generated**: Check test framework is installed
- **Incorrect numbers**: Verify test files are not included in coverage
- **Missing files**: Check coverage configuration includes all source dirs
- **Low branch coverage**: Add tests for if/else and error paths

## Tools Used

This skill works with:
- **Vitest** - Modern, fast test framework (free, open source)
- **Jest** - Popular test framework (free, open source)

Both support built-in coverage via c8 (Vitest) or istanbul (Jest).

## Resources

- Vitest coverage: https://vitest.dev/guide/coverage.html
- Jest coverage: https://jestjs.io/docs/configuration#collectcoverage-boolean
- Coverage best practices: https://martinfowler.com/bliki/TestCoverage.html
