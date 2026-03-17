# 05 工程化与发布接口

## 环境准备

建议从官方模板创建插件仓库，并在本地放入 `AstrBot/data/plugins/<plugin_name>` 下调试。

## 元数据规范（metadata.yaml）

至少应正确填写基础元数据；可选增强包括：

- `display_name`
- `support_platforms`
- `astrbot_version`

## 依赖声明

在插件目录提供 `requirements.txt`，避免安装后缺依赖。

## 热重载调试

通过 WebUI 的“重载插件”进行快速开发迭代。

## 开发原则（建议）

- 功能需要可测试。
- 做好异常处理与日志记录。
- 持久化数据放在 `data` 目录，不要写入插件代码目录。
- 避免使用阻塞式网络库（如 `requests`）。

## 参考

- `docs/zh/dev/star/plugin-new.md`
- `docs/zh/dev/star/guides/env.md`
- `docs/zh/dev/star/plugin-publish.md`
