# 安装与使用 README Atelier

README Atelier 是一套供支持 Skills 的编程工具读取的指引，帮助你基于真实仓库内容设计 README、封面和使用说明。它包含 Markdown 指引、参考文件、Python 检查脚本和可选的素材渲染脚本；不附带生图模型或独立的桌面应用。

## 环境要求

- 使用下面的安装命令需要 Node.js 22.20 或更高版本，以及随 Node.js 提供的 npm / npx。版本要求来自 [Skills CLI 官方文档](https://github.com/vercel-labs/skills)。
- 使用支持本地 Skills 的编程工具，并允许它读取目标仓库。
- 运行附带的检查脚本需要 Python 3.11 或更高版本，无需安装第三方 Python 包。
- 生图、真实界面录制和浏览器预览使用当前环境提供的能力；安装此技能不会额外提供这些服务。

## 安装到本机，跨项目使用

```bash
npx skills add Annabelle0726/Readme-Atelier --skill readme-atelier -g
```

按照安装器提示选择你使用的工具。`--skill` 指定只安装本技能，`-g` 表示用户级安装，可供多个项目使用。需要跳过交互时可以追加 `-y`，或使用 `--agent <工具标识>` 指定目标工具。

检查用户级安装结果：

```bash
npx skills list -g
```

在列表中找到 `readme-atelier`。如果工具没有立即识别，开启新会话或重新加载技能目录。

## 只安装到当前项目

在希望使用本技能的项目根目录执行：

```bash
npx skills add Annabelle0726/Readme-Atelier --skill readme-atelier
```

省略 `-g` 后使用项目级安装。安装器可能在当前仓库生成技能目录和锁文件，是否提交这些文件由项目自行决定。

## 从本地源码安装

已经下载或克隆本仓库时，在 **Readme-Atelier 仓库根目录** 执行：

```bash
npx skills add . --skill readme-atelier -g
```

检查仓库里可发现的技能，无需安装：

```bash
npx skills add . --list
```

本地源码修改后，重新执行本地安装命令以同步安装副本。

## 第一次使用

打开要改善 README 的项目，在对话中输入：

```text
使用 $readme-atelier 改善这个仓库的 README。
先阅读项目，再给我 2–3 个明显不同的视觉方向，等我选好后再制作完整版。
保留中文，补充能复制使用的安装命令和最小使用示例。
```

技能会先核实项目内容、技术栈、真实效果和许可证，再展示可比较的草图；选定方向后制作封面与正文，并检查桌面、手机宽度下的展示效果。

只需要素材或审阅时，可以明确缩小范围：

```text
使用 $readme-atelier 只设计这个项目的 README 封面，不修改 README 正文。
```

```text
使用 $readme-atelier 审阅 README 的可读性和首次使用路径，只给建议，不修改文件。
```

## 运行本地检查

以下命令在本仓库根目录运行，`/path/to/project` 换成你的目标项目路径；Windows 路径包含空格时保留引号：

```bash
python skills/readme-atelier/scripts/audit_readme.py "/path/to/project/README.md" --repo-root "/path/to/project"
```

如果使用已安装的副本，将脚本位置换成安装器显示的技能目录中的 `scripts/audit_readme.py`。

脚本输出 JSON，只读检查常见本地链接、图片路径、文件名大小写、空替代文本和图片体积。`--strict` 会将警告也视为失败。它不会联网验证外部链接，不检查锚点是否存在，也不能代替实际运行安装命令、视觉预览或 GIF 播放检查。

维护技能时可执行现有脚本测试：

```bash
python -m unittest discover -s tests -v
```

## 可选：渲染流程图与动效

需要可播放的流程图时，可使用随技能提供的渲染器。HTML 场景负责视觉设计，渲染器按指定时间截图，GIF 合成器保留帧间时长。两者不会为项目自动套用固定模板。

在仓库根目录安装可选依赖；仅阅读技能或运行 README 检查不需要这些依赖：

```bash
npm install --prefix .work/render-runtime playwright
node .work/render-runtime/node_modules/playwright/cli.js install chromium
python -m pip install Pillow
```

场景页面需要提供 `window.readmeAtelier.ready`、`duration` 和 `renderAt(seconds)`，以及默认的 `#scene` 元素。完整约定见 [正文叙事与渲染指南](../skills/readme-atelier/references/page-story-and-rendering.md)。

将下面的 `scene.html` 换成实际场景文件；每次选择新的输出目录与 GIF 文件名，脚本不会覆盖已有文件：

```bash
node skills/readme-atelier/scripts/render_scene.mjs --input scene.html --out .work/frames-v1 --runtime .work/render-runtime --width 940 --height 540 --fps 12
python skills/readme-atelier/scripts/assemble_gif.py .work/frames-v1 .work/workflow-v1.gif
node skills/readme-atelier/scripts/render_scene.mjs --input scene.html --out .work/still-v1 --runtime .work/render-runtime --time 9.8
```

安装副本使用其 `scripts/` 下的相同脚本。浏览器预览中的暂停、时间轴等控件由场景页面实现；GitHub README 使用导出的 GIF、静态图、链接与原生折叠内容。GIF 本身没有这些播放控件，重要信息应同时保留为文字与静态图。

维护渲染器时，安装上述依赖后可运行 `node tests/test_render_scene.mjs .work/render-runtime`，验证时间戳、静态图与序列帧的一致性、越界时间和防覆盖行为。GIF 合成检查已包含在 `python -m unittest discover -s tests -v` 中。

## 更新

从远端安装后，可更新指定技能：

```bash
npx skills update readme-atelier -g
```

本地路径安装请重新运行 `npx skills add . --skill readme-atelier -g`；项目级安装更新时将 `-g` 换成 `-p`。

## 许可证

本技能按 [MIT 协议](../LICENSE) 发布。技能不会替你的目标项目选择许可证，第三方图标、截图和其他素材也保留各自的授权要求。
