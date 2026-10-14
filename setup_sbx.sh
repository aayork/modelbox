#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

[[ -f "$ENV_FILE" ]] || { echo "error: $ENV_FILE not found (copy .env.example to .env)" >&2; exit 1; }

set -a; source "$ENV_FILE"; set +a

: "${MODEL_API_URL:?MODEL_API_URL must be set in .env}"
PROVIDER_NAME="${PROVIDER_NAME:-myllm}"

for cmd in sbx jq; do
  command -v "$cmd" >/dev/null || { echo "error: $cmd is not installed" >&2; exit 1; }
done

# Accept the URL with or without /v1 or a trailing slash
url="${MODEL_API_URL%/}"
[[ "$url" == */v1 ]] || url="$url/v1"

# Build the JSON with jq so special characters can't break it
providers="$(jq -cn --arg name "$PROVIDER_NAME" --arg url "$url" \
  '{($name): {url: $url, wire: "openai"}}')"

sbx settings set platform.allowExperimentalFeatures true
sbx settings set feature.model true
sbx settings set model.providers "$providers"

echo "New provider set '$PROVIDER_NAME' -> $url"
