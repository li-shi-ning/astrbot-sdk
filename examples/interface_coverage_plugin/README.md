# Interface Coverage Plugin

用于演示 AstrBot SDK 插件开发中常见能力接口：

- `on_command` + `on_message`
- `MessageEvent` 基础方法
- `Context` 的 metadata / db / memory / llm / provider client
- `provide_capability` 对外暴露能力
- `PluginHarness` 的 dispatch 与 capability 调用测试

## 运行

```bash
astrbot-sdk validate examples/interface_coverage_plugin
astrbot-sdk dev --local --plugin-dir examples/interface_coverage_plugin --event-text ping
```

## 测试

```bash
python -m pytest examples/interface_coverage_plugin/tests -v
```
