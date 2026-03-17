from __future__ import annotations

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
from astrbot_sdk.decorators import register_llm_tool


class InterfaceCoveragePlugin(Star):
    async def on_start(self, ctx: Context) -> None:
        await ctx.db.set("coverage:lifecycle", {"started": True})

    async def on_stop(self, ctx: Context) -> None:
        await ctx.db.delete("coverage:lifecycle")

    @on_command("cover", description="覆盖常用客户端接口")
    async def cover(self, event: MessageEvent, ctx: Context):
        await ctx.db.set("coverage:user", {"id": event.user_id or "unknown"})
        user_record = await ctx.db.get("coverage:user")
        await ctx.memory.save("coverage:last", {"text": event.text or ""})
        memory_hits = await ctx.memory.search("coverage")
        llm_reply = await ctx.llm.chat(event.text or "cover")
        plugin_meta = await ctx.metadata.get_current_plugin()
        name = plugin_meta.display_name if plugin_meta else ctx.plugin_id
        return event.plain_result(
            f"name={name}|db={user_record is not None}|mem={len(memory_hits)}|llm={llm_reply}"
        )

    @on_message(keywords=["coverage-ping"])
    async def coverage_ping(self, event: MessageEvent) -> None:
        await event.reply("coverage-pong")

    @on_event("group_join")
    async def on_group_join(self, event: MessageEvent, ctx: Context) -> None:
        await ctx.platform.send(event.session_id, f"欢迎 {event.user_id}")

    @provide_capability("coverage.echo", description="回显 capability")
    async def echo_capability(
        self,
        payload: dict[str, object],
        ctx: Context,
        cancel_token: CancelToken,
    ) -> dict[str, str]:
        cancel_token.raise_if_cancelled()
        text = str(payload.get("text", ""))
        await ctx.db.set("coverage:capability", {"text": text})
        return {"echo": text}

    @register_llm_tool("coverage_add", description="两个整数求和")
    async def coverage_add(self, a: int, b: int) -> str:
        return str(a + b)
