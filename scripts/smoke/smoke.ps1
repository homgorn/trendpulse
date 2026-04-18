param(
  [string]$BaseUrl = "http://127.0.0.1:8011"
)

$ErrorActionPreference = "Stop"

Write-Host "== TrendPulse smoke: $BaseUrl =="

Write-Host "`n[1/5] GET /health"
$health = Invoke-RestMethod -Uri "$BaseUrl/health" -Method Get
$health | ConvertTo-Json -Depth 10

Write-Host "`n[2/5] GET /ready"
$ready = Invoke-RestMethod -Uri "$BaseUrl/ready" -Method Get
$ready | ConvertTo-Json -Depth 10

Write-Host "`n[3/5] GET /metrics (first lines)"
$metricsRaw = Invoke-WebRequest -Uri "$BaseUrl/metrics" -Method Get
$metricsLines = $metricsRaw.Content -split "`n"
$metricsLines | Select-Object -First 10 | ForEach-Object { $_ }

Write-Host "`n[4/5] POST /v1/generate (may fail if provider keys are missing; this is acceptable smoke behavior)"
$body = @{
  theme       = "ai tools"
  platform    = "tiktok"
  region      = "global"
  budget_mode = "balanced"
  task_type   = "creative"
} | ConvertTo-Json

try {
  $gen = Invoke-RestMethod `
    -Uri "$BaseUrl/v1/generate" `
    -Method Post `
    -ContentType "application/json" `
    -Headers @{ "x-trace-id" = "smoke-ps1" } `
    -Body $body
  $gen | ConvertTo-Json -Depth 10
}
catch {
  if ($_.Exception.Response -and $_.Exception.Response.StatusCode.value__ -eq 400) {
    Write-Host "POST /v1/generate returned 400 (expected when provider keys are absent)."
  } else {
    throw
  }
}

Write-Host "`n[5/5] Smoke completed"
