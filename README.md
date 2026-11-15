<p align="center">
  <a href="assets/readme/hero.png"><img src="assets/readme/hero.png" width="100%" alt="README Atelier：One project. Three ways to tell it. 同一个 Fieldnotes 概念项目，展示编辑式、技术型和活泼插画三种 README 方向。"></a>
</p>

<p align="center">
  <img src="assets/readme/markdown.svg" alt="Markdown：技能指引">
  <img src="assets/readme/python.svg" alt="Python 3.11+：检查脚本">
  <img src="assets/readme/node.svg" alt="Node.js 22.20+：安装工具">
</p>

# README Atelier

**一个项目，可以有不同的讲述方式。**

README Atelier 帮助开发者把 README 做得好看、清晰，也更容易上手。它先阅读真实仓库，再提出 2–3 个明显不同的视觉方向；你选定后，才制作封面、正文和使用示例。

上面的 Fieldnotes 是概念示例，展示同一内容的三种视觉表达，并非真实项目效果或可点击界面。每次设计都从目标项目出发，方向不限于封面中的三种风格。

[安装与使用](#安装与使用) · [工作流程](#工作流程) · [使用示例](#使用示例) · [本地检查](#本地检查) · [MIT 许可证](LICENSE)

## 安装与使用

需要 **Node.js 22.20+**、npm / npx，以及支持本地 Skills 的编程工具。Python 只在运行附带的检查脚本时需要。

安装到本机，跨项目使用：

```bash
npx skills add Annabelle0726/Readme-Atelier --skill readme-atelier -g
```

按照提示选择你使用的工具。`-g` 表示用户级安装；省略它，则安装到当前项目。使用的是 `npx skills add`，不需要安装一个同名 npm 应用。

打开想改善 README 的项目，在对话中输入：

```text
使用 $readme-atelier 改善这个仓库的 README。
先阅读真实项目，给我 2–3 个不同的视觉方向，等我选择后再制作完整版本。
正文保留中文，加入可以复制的安装命令和最小使用示例。
```

第一轮会得到项目分析和可见的方向草图。选定方向后，继续制作并检查最终 README。

检查是否已安装：

```bash
npx skills list -g
```

列表中应出现 `readme-atelier`。如果编程工具未立即识别，开启新会话或重新加载技能目录。更多安装方式见[完整安装指南](docs/installation.md)，包括本地源码安装、项目级安装和更新命令。

## 从项目本身，找到表达方式

一个 CLI 的真实命令输出、一个产品的实际界面、一套工具的最小使用示例，都可以成为 README 的主角。先找到最有说服力的内容，再决定怎么设计。

| 你想改善的地方 | README Atelier 的做法 |
| --- | --- |
| 看起来像套了同一个模板 | 从项目内容、受众和真实产物中提取视觉线索，比较不同构图与信息重点 |
| 图片好看，但看不懂项目 | 用可读的 Markdown 说明价值、能力与限制，重要信息不只放在图片里 |
| 内容很多，却不知道怎么开始 | 优先给出环境要求、安装命令和一个能走通的最小示例 |
| 需要封面、插图或真实演示 | 按项目选择 SVG、图像生成、截图或组合方式；需要动态演示时提供 GIF 和静态备用图 |
| 桌面还好，手机上太挤 | 在桌面和手机宽度下检查裁切、字重、换行、图片尺寸与阅读顺序 |

## 工作流程

1. **读懂仓库。** 查看现有 README、结构、源码、配置、截图、示例和许可证，确定哪些内容有证据支持。
2. **比较方向。** 展示 2–3 个可见的草图，让构图、信息重点或视觉语言产生实质区别；等你选择后继续。
3. **制作封面与素材。** 沿用选定方向，展示准确的技术栈；概念图说明身份，真实产物证明能力。
4. **写清楚第一次使用。** 组织正文、安装步骤、配置和示例，保留可复制的命令与可搜索的文字。
5. **预览、检查、迭代。** 检查常见桌面宽度、360–390px 手机宽度及明暗背景，展示结果并按反馈调整。

已经选定视觉方向时会直接沿用，不必重复选择。已有授权会继续有效，提交与发布遵循你的要求。

## 使用示例

**完整改版**

```text
使用 $readme-atelier 重做这个项目的 README。
面向第一次接触项目的开发者，先展示真实效果，再说明怎么开始使用。
先给我几个视觉草图，不要编造功能、数据或成果。
```

**只制作封面**

```text
使用 $readme-atelier 为这个项目设计 README 封面。
先提供视觉方向，只交付图片和嵌入代码，不修改 README 正文。
```

**只做审阅**

```text
使用 $readme-atelier 检查 README 的可读性和首次使用路径。
指出哪些内容缺少证据、哪些步骤不完整；只给建议，不修改文件。
```

## 本地检查

附带的 `audit_readme.py` 使用 Python 3.11+ 标准库，无需安装第三方包。它只读检查常见本地链接和图片引用、文件名大小写、空替代文本及图片体积。

在本仓库根目录运行：

```bash
python skills/readme-atelier/scripts/audit_readme.py README.md --repo-root .
```

检查其他项目时，将 `README.md` 和 `--repo-root` 改为目标路径；使用安装副本时，将脚本路径改为已安装技能目录中的 `scripts/audit_readme.py`。

例如，对本仓库安装指南执行：

```bash
python skills/readme-atelier/scripts/audit_readme.py docs/installation.md --repo-root . --strict
```

本次实际运行结果节选：

```json
{
  "errors": [],
  "warnings": [],
  "assets": [],
  "external_links": [
    "https://github.com/vercel-labs/skills"
  ]
}
```

`--strict` 会把警告也视为失败。脚本不会联网检查外部链接或验证锚点，也不会证明命令能成功运行、封面足够清晰或 GIF 播放正常；这些需要单独验证。

## 文件结构

```text
skills/readme-atelier/
├── SKILL.md                         # 工作流程与范围边界
├── LICENSE                          # 随技能分发的 MIT 协议
├── agents/                          # 显示名称与调用提示
├── references/
│   ├── discovery-and-content.md     # 仓库分析与内容组织
│   ├── visual-directions.md         # 方向草图与选择
│   ├── assets-and-demos.md          # 封面、图标与真实演示
│   └── preview-and-review.md        # 预览与验收
└── scripts/
    └── audit_readme.py              # 只读检查脚本
```

技能主体是 Markdown 指引，不附带生图模型、浏览器或独立的应用界面。图像生成、录屏和实际预览依赖你所用环境的能力；工具不可用或项目无法运行时，应说明限制，并使用能够核实的素材。

## 参与改进

欢迎通过 [Issue](https://github.com/Annabelle0726/Readme-Atelier/issues) 提供问题与使用反馈，或提交 Pull Request。提供目标场景、预期行为和实际结果，有助于定位需要改进的指引。

修改检查脚本后，在仓库根目录运行现有测试：

```bash
python -m unittest discover -s tests -v
```

## 许可证与素材

本技能采用 [MIT 许可证](LICENSE)。目标项目的许可证仍由其维护者决定，第三方图标和素材遵循各自的授权要求。

封面使用选定的概念视觉；素材来源与编辑说明见[视觉说明](docs/visuals.md)。
