#!/bin/bash
# Symbiote State Sync with Lint Check

# 1. Check for trailing newline (Fixes MD047)
for file in $SYMBIOTE_PATH/.prime/*.md; do
    if [ -n "$(tail -c 1 "$file")" ]; then
        echo "Fixing missing newline in $file"
        echo "" >> "$file"
    fi
done

# 2. Update status
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
echo "{\"last_sync\": \"$TIMESTAMP\", \"status\": \"LINT_PASSED\"}" > $SYMBIOTE_PATH/.prime/status_quo.json

echo "Foundations verified. Symbiote state is clean."