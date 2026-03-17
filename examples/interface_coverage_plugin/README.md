# Interface Coverage Plugin

这个示例插件用于演示并测试 AstrBot SDK 插件开发常见接口：

- Decorators: `on_command` / `on_message` / `on_event` / `provide_capability`
- Context clients: `llm` / `db` / `memory` / `platform` / `metadata` / `http`
- MessageEvent: `reply` / `plain_result`

## 本地体验

```bash
astrbot-sdk dev --local --plugin-dir . --event-text cover
```

## 测试

```bash
python -m pytest examples/interface_coverage_plugin/tests/test_interface_coverage.py -v
```
