#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/terraform"
IP=$(terraform output -raw public_ip)
cd ../ansible
cat > inventory.ini <<EOF
[web]
${IP}
EOF
echo "Wrote ansible/inventory.ini with IP: ${IP}"
