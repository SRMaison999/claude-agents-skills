#!/bin/bash
# Dead Code Analysis Script using Knip
# Usage: ./analyze_dead_code.sh [path]

set -e

TARGET_PATH="${1:-.}"

echo "🔍 Analyzing dead code in: $TARGET_PATH"
echo ""

# Check if Knip is installed
if ! command -v npx &> /dev/null; then
    echo "❌ Error: npx not found. Please install Node.js"
    exit 1
fi

# Run Knip analysis
cd "$TARGET_PATH"

echo "📦 Running Knip analysis..."
echo ""

# Run Knip and capture output
npx knip --reporter json > /tmp/knip-report.json 2>&1 || true
npx knip --reporter markdown > /tmp/knip-report.md 2>&1 || true

echo ""
echo "✅ Analysis complete!"
echo ""
echo "📊 Reports generated:"
echo "  - JSON: /tmp/knip-report.json"
echo "  - Markdown: /tmp/knip-report.md"
echo ""
echo "📖 To view the markdown report:"
echo "   cat /tmp/knip-report.md"
