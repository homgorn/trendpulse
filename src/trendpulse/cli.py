import asyncio

import typer

from trendpulse.core.llm.gateway import LLMGateway
from trendpulse.schemas import GenerateRequest
from trendpulse.service import TrendPulseService

app = typer.Typer(help="TrendPulse CLI")


def _run_generate(
    theme: str,
    platform: str,
    region: str,
    budget_mode: str,
    task_type: str,
) -> None:
    req = GenerateRequest(
        theme=theme,
        platform=platform,
        region=region,
        budget_mode=budget_mode,
        task_type=task_type,
    )
    service = TrendPulseService(gateway=LLMGateway())
    result = asyncio.run(service.generate(req))
    typer.echo(result.model_dump_json(indent=2))


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    theme: str = typer.Option(None, help="Theme/niche (legacy single-command mode)"),
    platform: str = typer.Option("tiktok", help="Target platform"),
    region: str = typer.Option("global", help="Target region"),
    budget_mode: str = typer.Option("balanced", help="balanced|low_cost"),
    task_type: str = typer.Option("creative", help="creative|analysis|reasoning"),
):
    if ctx.invoked_subcommand is not None:
        return

    if theme is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()

    _run_generate(
        theme=theme,
        platform=platform,
        region=region,
        budget_mode=budget_mode,
        task_type=task_type,
    )


@app.command("generate")
def generate(
    theme: str = typer.Option(..., help="Theme/niche"),
    platform: str = typer.Option("tiktok", help="Target platform"),
    region: str = typer.Option("global", help="Target region"),
    budget_mode: str = typer.Option("balanced", help="balanced|low_cost"),
    task_type: str = typer.Option("creative", help="creative|analysis|reasoning"),
):
    _run_generate(
        theme=theme,
        platform=platform,
        region=region,
        budget_mode=budget_mode,
        task_type=task_type,
    )


if __name__ == "__main__":
    app()
