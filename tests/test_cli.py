from typer.testing import CliRunner

from trendpulse import cli as cli_mod


runner = CliRunner()


def test_cli_help_shows_generate():
    result = runner.invoke(cli_mod.app, ["--help"])
    assert result.exit_code == 0
    assert "generate" in result.output.lower()


def test_cli_generate_subcommand(monkeypatch):
    async def _fake_generate(req, trace_id=None):
        from trendpulse.schemas import GenerateResponse

        return GenerateResponse(
            idea="Idea",
            audience="Audience",
            monetization="Subs",
            risks=[],
            sources=[],
            provider="gemini",
            model="gemini-2.0-flash",
            profile="creative",
        )

    class _FakeService:
        async def generate(self, req, trace_id=None):
            return await _fake_generate(req, trace_id)

    monkeypatch.setattr(cli_mod, "TrendPulseService", lambda gateway: _FakeService())
    monkeypatch.setattr(cli_mod, "LLMGateway", lambda: object())

    result = runner.invoke(
        cli_mod.app,
        [
            "generate",
            "--theme",
            "ai tools",
            "--platform",
            "tiktok",
            "--region",
            "global",
            "--budget-mode",
            "balanced",
            "--task-type",
            "creative",
        ],
    )
    assert result.exit_code == 0
    assert '"idea": "Idea"' in result.output


def test_cli_legacy_single_command_mode(monkeypatch):
    async def _fake_generate(req, trace_id=None):
        from trendpulse.schemas import GenerateResponse

        return GenerateResponse(
            idea="Legacy Idea",
            audience="Audience",
            monetization="Subs",
            risks=[],
            sources=[],
            provider="gemini",
            model="gemini-2.0-flash",
            profile="creative",
        )

    class _FakeService:
        async def generate(self, req, trace_id=None):
            return await _fake_generate(req, trace_id)

    monkeypatch.setattr(cli_mod, "TrendPulseService", lambda gateway: _FakeService())
    monkeypatch.setattr(cli_mod, "LLMGateway", lambda: object())

    result = runner.invoke(
        cli_mod.app,
        [
            "--theme",
            "ai tools",
            "--platform",
            "tiktok",
            "--region",
            "global",
            "--budget-mode",
            "balanced",
            "--task-type",
            "creative",
        ],
    )
    assert result.exit_code == 0
    assert '"idea": "Legacy Idea"' in result.output
