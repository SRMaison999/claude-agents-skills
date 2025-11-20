#!/bin/bash
# Test Coverage Analyzer
# Runs tests with coverage and generates detailed reports
# Usage: ./analyze_coverage.sh [path]

set -e

TARGET_PATH="${1:-.}"

echo "🧪 Analyzing test coverage in: $TARGET_PATH"
echo ""

# Check if Node.js is installed
if ! command -v npx &> /dev/null; then
    echo "❌ Error: npx not found. Please install Node.js"
    exit 1
fi

cd "$TARGET_PATH"

# Check package.json for test framework
if [ ! -f "package.json" ]; then
    echo "❌ Error: No package.json found"
    exit 1
fi

echo "📦 Detecting test framework..."

# Determine test framework
if grep -q "\"vitest\"" package.json; then
    TEST_RUNNER="vitest"
    echo "✅ Found Vitest"
elif grep -q "\"jest\"" package.json; then
    TEST_RUNNER="jest"
    echo "✅ Found Jest"
else
    echo "⚠️  No test framework found (Vitest or Jest)"
    TEST_RUNNER="unknown"
fi

if [ "$TEST_RUNNER" != "unknown" ]; then
    echo ""
    echo "🏃 Running tests with coverage..."
    echo ""

    if [ "$TEST_RUNNER" = "vitest" ]; then
        npx vitest run --coverage 2>&1 || echo "⚠️  Some tests failed"
    else
        npx jest --coverage 2>&1 || echo "⚠️  Some tests failed"
    fi

    echo ""
    echo "✅ Coverage analysis complete!"
    echo ""
    echo "📊 Coverage reports:"
    echo "  - HTML: coverage/index.html"
    echo "  - JSON: coverage/coverage-final.json"
    echo ""
else
    echo "⚠️  Cannot run coverage without a test framework"
    echo "   Install Vitest or Jest first"
fi

# List all source files
echo "📁 Finding source files..."
find src -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" > /tmp/source-files.txt 2>/dev/null || true

# List all test files
echo "🧪 Finding test files..."
find . -name "*.test.*" -o -name "*.spec.*" > /tmp/test-files.txt 2>/dev/null || true

SOURCE_COUNT=$(wc -l < /tmp/source-files.txt)
TEST_COUNT=$(wc -l < /tmp/test-files.txt)

echo ""
echo "📈 Project stats:"
echo "  - Source files: $SOURCE_COUNT"
echo "  - Test files: $TEST_COUNT"
echo ""
echo "📖 File lists saved:"
echo "  - Source: /tmp/source-files.txt"
echo "  - Tests: /tmp/test-files.txt"
