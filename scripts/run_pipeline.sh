#!/bin/bash

cd ~/self-healing-cloud

# Step 1: Collect metrics
METRICS=$(python3 scripts/monitor.py)

# Step 2: Get decision — only last line is JSON
DECISION=$(echo "$METRICS" | python3 scripts/decision.py | tail -1)

# Step 3: Extract actions
ACTIONS=$(echo "$DECISION" | python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read().strip())
    for a in d.get('actions', []):
        print(a)
except Exception as e:
    pass
")

# Step 4: Extract service name
SERVICE=$(echo "$DECISION" | python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read().strip())
    print(d.get('service', 'apache2'))
except:
    print('apache2')
")

# Step 5: Execute healing
if [ -n "$ACTIONS" ]; then
    while IFS= read -r action; do
        bash ~/self-healing-cloud/scripts/heal.sh "$action" "$SERVICE"
    done <<< "$ACTIONS"
fi
