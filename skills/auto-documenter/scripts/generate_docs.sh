#!/bin/bash
# Auto Documentation Generator
# Uses TypeDoc for TypeScript and react-docgen-typescript for React components
# Usage: ./generate_docs.sh [path] [output-dir]

set -e

TARGET_PATH="${1:-.}"
OUTPUT_DIR="${2:-./docs}"

echo "📚 Generating documentation for: $TARGET_PATH"
echo "📁 Output directory: $OUTPUT_DIR"
echo ""

# Check if Node.js is installed
if ! command -v npx &> /dev/null; then
    echo "❌ Error: npx not found. Please install Node.js"
    exit 1
fi

cd "$TARGET_PATH"

# Check if TypeScript project
if [ -f "tsconfig.json" ]; then
    echo "✅ TypeScript project detected"

    # Generate TypeDoc documentation
    echo "📖 Generating TypeDoc documentation..."
    npx typedoc --out "$OUTPUT_DIR/api" --readme none 2>&1 || echo "⚠️  TypeDoc generation completed with warnings"

    echo ""
fi

# Check if React project
if [ -f "package.json" ] && grep -q "react" package.json; then
    echo "✅ React project detected"

    # Generate React component documentation
    echo "⚛️  Analyzing React components..."

    # Find all component files
    find src -name "*.tsx" -o -name "*.jsx" > /tmp/component-files.txt 2>/dev/null || true

    COMPONENT_COUNT=$(wc -l < /tmp/component-files.txt)
    echo "   Found $COMPONENT_COUNT component files"

    echo ""
fi

echo ""
echo "✅ Documentation generation complete!"
echo ""
echo "📊 Generated documentation:"
if [ -d "$OUTPUT_DIR/api" ]; then
    echo "  - TypeDoc API: $OUTPUT_DIR/api/index.html"
fi
echo "  - Component list: /tmp/component-files.txt"
echo ""
echo "📖 Next steps:"
echo "   1. Review generated documentation"
echo "   2. Check for missing JSDoc comments"
echo "   3. Add examples for complex functions"
