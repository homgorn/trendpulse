# SECURITY.md — Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| 0.2.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please send an email to refertur.net@gmail.com with the following details:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Any suggested fixes (optional)

We aim to respond within 48 hours and will keep you updated on our progress.

---

## Security Checklist (OWASP Top 10:2025)

- [ ] Never commit `.env` files
- [ ] Rotate API keys every 30 days
- [ ] Use separate Read-Only keys for public frontend
- [ ] Enable rate limiting in production
- [ ] Configure CORS for your specific domain
- [ ] Use HTTPS (Let's Encrypt / Cloudflare)
- [ ] Enable WAF (Cloudflare / AWS WAF)
- [ ] Set up alerting on anomalies (Prometheus + Alertmanager)
- [ ] Regularly update dependencies (`uv update --dry-run`)
- [ ] Conduct quarterly penetration testing
- [ ] Check supply chain (`uv pip audit`, Dependabot alerts)

---

## Architecture Security Measures

### A01 — Broken Access Control
- API Key authentication (planned)
- Strict CORS configuration
- JWT token support (planned)

### A02 — Cryptographic Failures
- API keys stored hashed in production
- HTTPS everywhere
- No hardcoded secrets

### A03 — Software Supply Chain
- `uv.lock` for reproducible builds
- `uv pip audit` in CI
- Dependabot for dependency updates

### A04 — Insecure Design
- Rate limiting (30 req/min default)
- Input validation via Pydantic
- Circuit breaker pattern

### A05 — Security Misconfiguration
- Security headers (X-Content-Type-Options, X-Frame-Options, CSP)
- No debug mode in production
- Minimal container footprint

### A06 — Vulnerable Components
- Regular `uv update --dry-run` checks
- GitHub Security alerts enabled
- Container scanning in CI

### A07 — Authentication Failures
- JWT access tokens (15min expiry)
- Refresh token rotation (planned)
- API key management (planned)

### A08 — Data Integrity
- Parameterized queries (via ORM)
- Input sanitization
- JSON validation

### A09 — Logging Failures
- Structured logging with trace_id
- No secrets in logs
- Error context preserved

### A10 — Mishandling of Exceptional Conditions
- Global exception handler
- No stack trace leaks to clients
- Graceful degradation

---

## API Security Best Practices

### For Users

1. **Never share your API keys** — They grant access to your account
2. **Use environment variables** — Never hardcode keys in code
3. **Monitor usage** — Check `/metrics` endpoint regularly
4. **Set up alerts** — Configure Prometheus alerts for anomalies

### For Developers

1. **Validate all inputs** — Use Pydantic schemas
2. **Sanitize outputs** — Prevent XSS in responses
3. **Log securely** — No PII in logs
4. **Handle errors gracefully** — Return generic messages to clients

---

## Data Handling

- **API Keys**: Stored encrypted at rest (production)
- **Request Data**: Not persisted in MVP (stateless)
- **Logs**: Retained 30 days, no sensitive data
- **Metrics**: Aggregated, no PII

---

## Compliance

This project follows security best practices. For enterprise deployments:

1. Enable API key authentication
2. Configure VPC/private networking
3. Enable audit logging
4. Set up WAF rules
5. Configure data retention policies
6. Conduct annual security audits

---

## Contact

For security-related questions, contact: refertur.net@gmail.com

For general issues, use GitHub Issues: https://github.com/homgorn/trendpulse/issues