import importlib.util
from pathlib import Path

import pytest

from astrbot_sdk.testing import MockContext, MockMessageEvent

PLUGIN_DIR = Path(__file__).resolve().parents[1]


def _load_plugin_class():
    module_path = PLUGIN_DIR / "main.py"
    spec = importlib.util.spec_from_file_location(
        "examples_interface_coverage_plugin_main",
        module_path,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.InterfaceCoveragePlugin


InterfaceCoveragePlugin = _load_plugin_class()


@pytest.mark.asyncio
async def test_direct_handlers_cover_major_clients() -> None:
    plugin = InterfaceCoveragePlugin()
    ctx = MockContext(
        plugin_id="interface_coverage_plugin",
        plugin_metadata={"display_name": "Interface Coverage Plugin"},
    )
    event = MockMessageEvent(text="/ping", context=ctx)

    await plugin.ping(event, ctx)
    await plugin.meta(event, ctx)
    await plugin.dbmem(event, ctx)
    await plugin.llm(event, ctx)
    await plugin.keyword_echo(event, ctx)

    assert any(reply.startswith("pong:") for reply in event.replies)
    assert any(reply.startswith("meta:") for reply in event.replies)
    assert any(reply.startswith("dbmem:") for reply in event.replies)
    assert any(reply.startswith("llm:") for reply in event.replies)
    assert "keyword:ok" in event.replies


@pytest.mark.asyncio
async def test_provided_capability_direct_call() -> None:
    plugin = InterfaceCoveragePlugin()
    ctx = MockContext(plugin_id="interface_coverage_plugin")

    result = await plugin.capability_summary({"prefix": "demo"}, ctx)

    assert result["message"] == "demo:interface_coverage_plugin"
    assert isinstance(result["provider_count"], int)
