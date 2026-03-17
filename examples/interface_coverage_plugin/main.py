from __future__ import annotations

from pydantic import BaseModel

from astrbot_sdk import (
    Context,
    MessageEvent,
    Star,
    on_command,
    on_event,
    on_message,
    provide_capability,
)
from astrbot_sdk.context import CancelToken


class EchoIn(BaseModel):
    text: str


class EchoOut(BaseModel):
    echoed: str
    plugin_id: str


class InterfaceCoveragePlugin(Star):
    @on_command("cover", description="覆盖常用客户端接口")
    async def cover(self, event: MessageEvent, ctx: Context):
        llm_text = await ctx.llm.chat("coverage")

        await ctx.db.set("coverage:key", {"value": 1})
        db_value = await ctx.db.get("coverage:key")
        db_keys = await ctx.db.list("coverage:")
        await ctx.db.delete("coverage:key")

        await ctx.memory.save(
            "coverage:memory", {"text": event.text}, tags=["coverage"]
        )
        memory_found = await ctx.memory.search("coverage")
        await ctx.memory.delete("coverage:memory")

        plugin = await ctx.metadata.get_current_plugin()
        await ctx.http.register_api(
            route="/coverage/echo",
            handler=self.http_echo,
            methods=["GET", "POST"],
            description="coverage demo api",
        )
        api_count = len(await ctx.http.list_apis())
        await ctx.http.unregister_api("/coverage/echo")

        await ctx.platform.send(event.session_id, "platform.send ok")

        return event.plain_result(
            f"llm={llm_text}|db={db_value}|keys={len(db_keys)}|memory={len(memory_found)}"
            f"|plugin={plugin.name if plugin else ctx.plugin_id}|apis={api_count}"
        )

    @on_message(keywords=["ping"])
    async def ping(self, event: MessageEvent) -> None:
        await event.reply("pong")

    @on_event("group_join")
    async def on_group_join(self, event: MessageEvent, ctx: Context) -> None:
        await ctx.platform.send(event.session_id, f"welcome {event.user_id}")

    @provide_capability(
        "coverage.echo",
        description="echo capability for tests",
        input_model=EchoIn,
        output_model=EchoOut,
    )
    async def echo_capability(
        self,
        payload: dict[str, object],
        ctx: Context,
        cancel_token: CancelToken,
    ) -> dict[str, str]:
        cancel_token.raise_if_cancelled()
        text = str(payload.get("text", ""))
        return {"echoed": text, "plugin_id": ctx.plugin_id}

    @provide_capability("coverage.http", description="http handler")
    async def http_echo(
        self,
        payload: dict[str, object],
        ctx: Context,
        cancel_token: CancelToken,
    ) -> dict[str, object]:
        cancel_token.raise_if_cancelled()
        return {"status": 200, "body": {"payload": payload, "plugin": ctx.plugin_id}}
