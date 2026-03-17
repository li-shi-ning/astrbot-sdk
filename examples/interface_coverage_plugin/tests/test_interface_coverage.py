from __future__ import annotations

from pathlib import Path

import pytest

from astrbot_sdk.testing import PluginHarness


@pytest.mark.asyncio
async def test_cover_command_exercises_common_clients() -> None:
    plugin_dir = Path(__file__).resolve().parents[1]

    async with PluginHarness.from_plugin_dir(plugin_dir) as harness:
        records = await harness.dispatch_text("cover")

    texts = [record.text or "" for record in records if record.kind == "text"]
    assert any("platform.send ok" in text for text in texts)
    assert any("llm=Echo: coverage" in text for text in texts)
    assert any("plugin=interface_coverage_plugin" in text for text in texts)
    assert any("apis=1" in text for text in texts)


@pytest.mark.asyncio
async def test_message_event_and_custom_capability() -> None:
    plugin_dir = Path(__file__).resolve().parents[1]

    async with PluginHarness.from_plugin_dir(plugin_dir) as harness:
        ping_records = await harness.dispatch_text("ping")
        capability = await harness.invoke_capability("coverage.echo", {"text": "abc"})

    assert any(record.text == "pong" for record in ping_records)
    assert capability == {"echoed": "abc", "plugin_id": "interface_coverage_plugin"}
