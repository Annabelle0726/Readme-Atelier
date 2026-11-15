# README 视觉说明

## 选定方向

使用项目维护者提供并选定的 `README-Atelier-C-Hero`：奶油纸纹背景、酒红衬线标题、细金线，以及同一个 Fieldnotes 概念项目的三种并排表达。

封面由原始概念图进行局部文字编辑，副标题为 **Design thoughtful GitHub READMEs.**，主标题保留 **One project. Three ways to tell it.**。图中书页、示意界面和 Fieldnotes 内容用于表达设计方向，并非真实项目或已验证产品输出。

最终封面位于 [hero.png](../assets/readme/hero.png)。收到的是栅格素材，没有原始字体、图层或矢量源；可复制的项目说明、概念解释、流程与命令均保留在 README 正文中。后续调整封面可使用当前成品作为编辑输入。

封面尺寸为 1672 × 941，体积约 2.20 MiB。为保留细密纸纹和三栏文字，此版本保留 PNG 成品，略高于检查脚本默认的 2 MiB 单图提醒阈值；无需依赖图片阅读正文或复制命令。

## 技术标签

封面下方三个本地 SVG 标签分别说明真实的文件格式与运行要求：

- Markdown：技能指引和参考文档。
- Python 3.11+：附带检查脚本的运行环境。
- Node.js 22.20+：当前 Skills CLI 安装工具的要求。

标签由 [Shields.io](https://shields.io/) 生成，图标来自其使用的 [Simple Icons](https://github.com/simple-icons/simple-icons)。SVG 已保存到本仓库，README 展示无需请求外部标签服务。图标不代表官方背书。

## 演示与预览

正文展示两个已有 README 成果：

- [Agency Bloom](cases/agency-bloom.md)：山景晨光封面与植物风格系统图，展示从品牌表达延伸到系统解释的安排。
- [Taste Studio](cases/taste-studio.md)：设计概念封面、页面案例与流程素材，展示整页的视觉连续性。

案例图位于 `assets/readme/cases/`，排版源文件位于 `assets/readme/source/`。手机使用单列排版。原有素材直接来自两个项目的 README，本轮只重新编排展示；不将原有成果归为本次技能运行制作，不将概念配图视为产品运行截图。

新版流程动画为 20 秒，以 Taste Studio 既有素材讲解「读懂、选择、编排、交付」。它保留已选封面的纸色、酒红与细金线，使用纸页叠放、简报形成、正文展开和双端检查说明过程。它是解释动画，不是实际操作录屏；画面中的 README 为讲解排版，具体命令以各项目正式 README 为准。

本地打开 `assets/readme/source/workflow.html` 可播放、暂停、重播、跳转章节和用键盘调整进度；减少动态效果时不自动播放，页面隐藏时暂停。GIF 仅播放，静态 PNG 和文字步骤同时保留。导出使用 15 FPS、300 个采样时刻；GIF 会合并完全相同的静止帧，实际帧数和文件大小见下方导出记录。

本地 Markdown 预览是 GitHub 样式近似，最终展示以 GitHub 渲染为准。GitHub README 使用图片、GIF、链接和原生 `details`；图片中的构图示例不充当可点击的应用控件。

## 从源码重新渲染

先按[可选渲染依赖](installation.md#可选渲染流程图与动效)准备 Playwright、Chromium 与 Pillow。在仓库根目录执行，输出目录和 GIF 文件使用新名称：

```bash
# 案例排版；手机把 width 改为 480，并选择新的输出目录
node skills/readme-atelier/scripts/render_scene.mjs --input assets/readme/source/agency-bloom-case.html --out .work/agency-case-v3 --runtime .work/render-runtime --width 1040 --height 900 --time 0
node skills/readme-atelier/scripts/render_scene.mjs --input assets/readme/source/taste-studio-case.html --out .work/taste-case-v3 --runtime .work/render-runtime --width 1040 --height 900 --time 0

# 静态流程画面；手机使用 width 390
node skills/readme-atelier/scripts/render_scene.mjs --input assets/readme/source/workflow.html --out .work/workflow-still-v3 --runtime .work/render-runtime --width 1040 --height 650 --time 2

# 流程动画；手机使用 width 390
node skills/readme-atelier/scripts/render_scene.mjs --input assets/readme/source/workflow.html --out .work/workflow-frames-v3 --runtime .work/render-runtime --width 1040 --height 650 --fps 15
python skills/readme-atelier/scripts/assemble_gif.py .work/workflow-frames-v3 .work/workflow-v3.gif
```

检查导出结果后，再更新 README 引用的素材。渲染器从真实 PNG 读取导出尺寸；同一时间的状态不依赖此前播放或跳转顺序。

## 案例素材权属

本仓库的技能指引与脚本按 MIT 发布。Agency Bloom 与 Taste Studio 的作品、界面、品牌及第三方素材保留原有权属；本页的展示和排版不会改变它们的许可条件。原有素材不被归功于本次技能运行。

## 本轮导出记录

| 版本 | 尺寸 | 实际帧数 | 时长 | 文件体积 |
| --- | --- | --- | --- | --- |
| 桌面 GIF | 1040 × 650 | 300 | 20 秒 | 4,120,974 字节（约 3.93 MiB） |
| 手机 GIF | 390 × 650 | 300 | 20 秒 | 2,014,347 字节（约 1.92 MiB） |

为保留正文素材的色彩与平滑转场，桌面 GIF 高于 2 MiB 的建议预算；它是正文唯一默认播放的流程动画。使用全局调色板与差异帧优化，未降低导出分辨率。静态图始终可单独查看。

已检查桌面与手机版本、播放 / 暂停 / 重播、键盘进度、章节跳转、减少动态效果，以及同一时间重复渲染和循环首尾状态。包含 GIF 合成与 README 审计的 20 项 Python 检查通过；优化前后抽查 9 个时刻的解码像素保持一致。
