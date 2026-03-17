from pathlib import Path

import pytest

from astrbot_sdk.testing import LocalRuntimeConfig, PluginHarness


def _plugin_dir() -> Path:
    return (
        Path(__file__).resolve().parents[1] / "examples" / "interface_coverage_plugin"
    )


@pytest.mark.asyncio
async def test_interface_coverage_command_and_message() -> None:
    async with PluginHarness(LocalRuntimeConfig(plugin_dir=_plugin_dir())) as harness:
        cover_records = await harness.dispatch_text("cover")
        ping_records = await harness.dispatch_text("coverage-ping")

    assert any(
        "name=Interface Coverage Plugin" in (record.text or "")
        for record in cover_records
    )
    assert any(record.text == "coverage-pong" for record in ping_records)


@pytest.mark.asyncio
async def test_interface_coverage_event_and_capability() -> None:
    async with PluginHarness(LocalRuntimeConfig(plugin_dir=_plugin_dir())) as harness:
        event_records = await harness.dispatch_event(
            harness.build_event_payload(
                text="",
                event_type="group_join",
                user_id="tester",
                session_id="group-1",
                group_id="group-1",
            )
        )
        capability_result = await harness.invoke_capability(
            "coverage.echo",
            {"text": "abc"},
        )

    assert any(record.text == "欢迎 tester" for record in event_records)
    assert capability_result == {"echo": "abc"}
