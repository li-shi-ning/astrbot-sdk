from astrbot_sdk import (
    Context,
    MessageEvent,
    Star,
    on_command,
    on_message,
    provide_capability,
)


class InterfaceCoveragePlugin(Star):
    @on_command("ping", description="基础消息事件信息")
    async def ping(self, event: MessageEvent, ctx: Context) -> None:
        chat_type = "group" if event.is_group_chat() else "private"
        await event.reply(f"pong:{chat_type}:{event.get_session_id()}")

    @on_command("meta", description="元数据接口示例")
    async def meta(self, event: MessageEvent, ctx: Context) -> None:
        plugin = await ctx.metadata.get_current_plugin()
        plugins = await ctx.metadata.list_plugins()
        await event.reply(
            f"meta:{plugin.display_name if plugin else ctx.plugin_id}:{len(plugins)}"
        )

    @on_command("dbmem", description="DB + Memory 接口示例")
    async def dbmem(self, event: MessageEvent, ctx: Context) -> None:
        await ctx.db.set("demo:key", {"value": 1})
        db_value = await ctx.db.get("demo:key")
        await ctx.memory.save("memory:key", {"topic": "sdk", "ok": True})
        memory = await ctx.memory.get("memory:key")
        matches = await ctx.memory.search("sdk")
        await event.reply(f"dbmem:{db_value['value']}:{memory['topic']}:{len(matches)}")

    @on_command("llm", description="LLM 接口示例")
    async def llm(self, event: MessageEvent, ctx: Context) -> None:
        plain = await ctx.llm.chat("hello")
        raw = await ctx.llm.chat_raw("hello")
        chunks: list[str] = []
        async for chunk in ctx.llm.stream_chat("hello"):
            chunks.append(chunk)
        await event.reply(f"llm:{plain}:{raw.finish_reason}:{''.join(chunks)}")

    @on_message(keywords=["sdk-keyword"])
    async def keyword_echo(self, event: MessageEvent, ctx: Context) -> None:
        await event.reply("keyword:ok")

    @provide_capability(
        "interface_coverage.capabilities.summary", description="返回摘要"
    )
    async def capability_summary(self, payload: dict, ctx: Context) -> dict:
        prefix = str(payload.get("prefix", "cap"))
        providers = await ctx.providers.list_all()
        return {
            "message": f"{prefix}:{ctx.plugin_id}",
            "provider_count": len(providers),
        }
