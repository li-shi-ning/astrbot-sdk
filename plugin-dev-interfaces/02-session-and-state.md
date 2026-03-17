# 02 会话与状态接口

## 会话控制（多轮交互）

适合问答、表单收集、接龙、确认流程等“需要等待下一条消息”的场景。

典型能力：

- `session_waiter(...)`：创建会话等待器。
- `SessionController.keep(...)`：延长/重置会话超时。
- `SessionController.stop()`：主动结束会话。

## 轻量状态存储（KV）

适合保存插件配置、短期标记、用户状态快照等：

- `put_kv_data(key, value)`
- `get_kv_data(key, default)`
- `delete_kv_data(key)`

## 大文件存储规范

插件数据应存放于：

- `data/plugin_data/{plugin_name}/`

这样可避免升级/重装插件时丢失或污染代码目录。

## 参考

- `docs/zh/dev/star/guides/session-control.md`
- `docs/zh/dev/star/guides/storage.md`
