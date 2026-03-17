# 01 消息与指令接口

## 核心对象

- `Star`：插件基类。
- `Context`：插件访问 AstrBot Core 能力的入口。
- `AstrMessageEvent`：消息事件上下文。
- `filter`：注册指令/事件处理器。

## 最小指令示例

```python
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star

class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("hello")
    async def hello(self, event: AstrMessageEvent):
        yield event.plain_result("Hello from plugin")
```

## 常见读取入口

- `event.message_str`：纯文本消息。
- `event.message_obj`：结构化消息对象。
- `event.get_sender_name()`：发送者显示名。

## 实践建议

- Handler 必须定义在插件类中，签名至少包含 `self, event`。
- 先用最小 command 打通链路，再叠加复杂过滤规则。
- 对消息结构不确定时，先打印 `event.message_obj.raw_message` 辅助调试。

## 参考

- `docs/zh/dev/star/plugin-new.md`
- `docs/zh/dev/star/guides/simple.md`
- `docs/zh/dev/star/guides/listen-message-event.md`
