from pathlib import Path

import pytest

from astrbot_sdk.testing import PluginHarness


@pytest.mark.asyncio
async def test_dispatch_commands_and_message_trigger() -> None:
    plugin_dir = Path(__file__).resolve().parents[1]

    async with PluginHarness.from_plugin_dir(plugin_dir) as harness:
        for text in ["ping", "meta", "dbmem", "llm", "sdk-keyword"]:
            await harness.dispatch_text(text)

        records = harness.sent_messages

    sent_texts = [record.text for record in records if record.text is not None]
    assert any(item.startswith("pong:") for item in sent_texts)
    assert any(item.startswith("meta:") for item in sent_texts)
    assert any(item.startswith("dbmem:") for item in sent_texts)
    assert any(item.startswith("llm:") for item in sent_texts)
    assert "keyword:ok" in sent_texts


@pytest.mark.asyncio
async def test_invoke_provided_capability_via_harness() -> None:
    plugin_dir = Path(__file__).resolve().parents[1]

    async with PluginHarness.from_plugin_dir(plugin_dir) as harness:
        output = await harness.invoke_capability(
            "interface_coverage.capabilities.summary",
            {"prefix": "harness"},
        )

    assert output["message"] == "harness:interface_coverage_plugin"
    assert isinstance(output["provider_count"], int)
