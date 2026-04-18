# TrendPulse TODO

## Sprint-01
- [x] Base API/CLI/service scaffold
- [x] Routing profiles wired
- [x] Provider adapters connected
- [x] Basic tests passing

## Sprint-02 Hardening
- [x] Config-driven timeout/retry/circuit-breaker
- [x] Gateway fallback and resilience updates
- [x] Expanded gateway/api/cli tests
- [x] Full pytest pass

## Sprint-03 (done)
- [x] CLI multi-command UX (`trendpulse generate ...`) with backward compatibility
- [x] API observability endpoint `/metrics` (Prometheus text format)
- [x] Readiness endpoint `/ready` (provider configuration readiness)
- [x] Extend tests for new endpoints and CLI behavior
- [x] Full pytest pass after Sprint-03 changes

## Sprint-04 Delivery/Operations
- [x] Add `README.md` with local/dev/ops runbook
- [x] Add `Dockerfile` for API containerization
- [x] Add `docker-compose.yml` for local service orchestration
- [x] Add smoke scripts (`scripts/smoke/smoke.ps1`, `scripts/smoke/smoke.sh`)
- [ ] Validate tests after ops artifacts added
