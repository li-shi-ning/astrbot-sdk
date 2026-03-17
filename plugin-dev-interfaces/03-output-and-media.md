# 03 消息输出与媒体接口

## 输出模式

在 Handler 中常见两种回复方式：

- `yield event.xxx_result(...)`：声明式返回。
- `await event.send(...)`：主动发送（常用于会话控制内部）。

## 常见消息类型

- 纯文本：`plain_result`
- 图片：`image_result`
- 组合消息链：`event.make_result()` + `message_components`

## 文转图（Text / HTML -> Image）

AstrBot 提供两种常见能力：

- `text_to_image(text)`：快速文本转图片。
- `html_render(template, data, options=...)`：Jinja2 模板渲染图像。

适用于：

- 排版较复杂的榜单、卡片、日报。
- 需要避免纯文本超长刷屏的场景。

## 参考

- `docs/zh/dev/star/guides/send-message.md`
- `docs/zh/dev/star/guides/html-to-pic.md`
