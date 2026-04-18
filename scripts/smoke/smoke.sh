#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://127.0.0.1:8011}"

echo "== TrendPulse smoke: ${BASE_URL} =="

echo
echo "[1/5] GET /health"
curl -fsS "${BASE_URL}/health"
echo

echo
echo "[2/5] GET /ready"
curl -fsS "${BASE_URL}/ready"
echo

echo
echo "[3/5] GET /metrics (first lines)"
curl -fsS "${BASE_URL}/metrics" | head -n 10

echo
echo "[4/5] POST /v1/generate (400 acceptable if provider keys are missing)"
set +e
RESP="$(curl -sS -w '\n%{http_code}' -X POST "${BASE_URL}/v1/generate" \
  -H 'Content-Type: application/json' \
  -H 'x-trace-id: smoke-sh' \
  -d '{"theme":"ai tools","platform":"tiktok","region":"global","budget_mode":"balanced","task_type":"creative"}')"
STATUS="$(echo "${RESP}" | tail -n1)"
BODY="$(echo "${RESP}" | sed '$d')"
set -e

echo "${BODY}"
if [[ "${STATUS}" != "200" && "${STATUS}" != "400" ]]; then
  echo "Unexpected HTTP status from /v1/generate: ${STATUS}"
  exit 1
fi

echo
echo "[5/5] Smoke completed"
