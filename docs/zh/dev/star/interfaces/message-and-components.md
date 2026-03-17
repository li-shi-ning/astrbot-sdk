---
outline: deep
---

# 消息与消息链接口

本页介绍如何读取消息、构造消息链并发送消息。

## 核心接口

- `event.message_str`：获取纯文本消息。
- `event.message_obj.message`：获取消息链。
- `event.plain_result(...)`：快速返回文本结果。
- `astrbot.api.message_components`：构造复杂消息（图片、@、回复等）。

## 消息链示例

```python
import astrbot.api.message_components as Comp

message_chain = [
    Comp.Plain("你好"),
    Comp.At(qq=123456),
    Comp.Image(file="https://example.com/image.jpg"),
]
```

## 发送建议

- 优先使用 AstrBot 提供的消息组件，避免直接拼平台原始字段。
- 发送前根据平台能力做降级处理（如不支持 `Reply` 时降级为纯文本）。
- 对外链图片、音频等资源做可用性检查，减少发送失败。

## 相关文档

- [监听消息事件](../guides/listen-message-event.md)
- [发送消息](../guides/send-message.md)
