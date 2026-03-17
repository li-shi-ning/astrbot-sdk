---
outline: deep
---

# 指令与事件接口

本页聚焦插件中“接收输入并触发逻辑”的接口。

## 核心接口

- `@filter.command("...")`：注册命令。
- `@filter.event_message_type(...)`：按消息类型监听。
- `AstrMessageEvent`：统一事件对象。

## 最小命令示例

```python
from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star

class HelloPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("hello")
    async def hello(self, event: AstrMessageEvent):
        """回复一条问候消息"""
        logger.info("/hello triggered")
        yield event.plain_result("Hello from AstrBot plugin!")
```

## 设计建议

- `Handler` 建议在插件类中定义，参数保持 `self, event`。
- 命令名尽量语义化，避免过短或冲突。
- 复杂逻辑抽离到独立模块，`Handler` 保持薄层。

## 相关文档

- [🌠 插件开发指南](../plugin-new.md)
- [监听消息事件](../guides/listen-message-event.md)
- [简单插件开发](../guides/simple.md)
