# Interface Coverage Plugin

这个示例插件用于本地测试，目标是覆盖 AstrBot SDK 的常用接口：

- 生命周期：`on_start` / `on_stop`
- 装饰器：`@on_command`、`@on_message`、`@on_event`
- Context 客户端：`ctx.llm`、`ctx.db`、`ctx.memory`、`ctx.platform`、`ctx.metadata`
- Capability 导出：`@provide_capability`
- LLM Tool 注册：`@register_llm_tool`

## 本地验证

```bash
python run_tests.py -k "interface_coverage_plugin"
```
