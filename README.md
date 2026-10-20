# AI 写代码做视频：Remotion × HyperFrames，36 场景复现包

这套材料公开了木子San这轮视频制作对比使用的**测试方法、108 份原始任务提示词、36 个场景及 54 份初版／修改版输入规格**。你可以挑一个场景，让同一个 AI 分别用 Remotion 和 HyperFrames 做，再按同一张表检查成片。

> **先看复现边界：**这是源码与提示词包，不包含原始人像视频、配音、BGM、字体文件和二进制媒体，也不包含原实验的私有渲染服务。缺少的文件逐项列在各场景清单中；你需要准备有权使用的素材。更换素材、模型或渲染执行方式后属于“按同一方法复测”，不能据此宣称逐字节重现原成绩。

**English:** A source-only, Chinese-language reproduction kit for a 36-scene AI video authoring comparison. Includes original prompts, revision instructions, input contracts, pinned framework/skill versions, and review templates. Bring your own lawful media; no private runtime or credentials are included.

## 从一个场景开始

要求 Python 3.10+；实际制作另需 Node.js 22+、npm、Git、FFmpeg 和可用的 AI 编程工具。准备工具只使用 Python 标准库，不会调用模型或花费 API 额度。

```bash
git clone https://github.com/santosli/ai-video-framework-benchmark.git
cd ai-video-framework-benchmark
python3 tools/benchmark.py validate
python3 tools/benchmark.py list

# P03 是静音的 React 任务列表案例，所需组件和数据已包含；字体和参考 PNG 仍需准备。
python3 tools/benchmark.py prepare P03 remotion --out /tmp/video-bench-p03-remotion
python3 tools/benchmark.py prepare P03 hyperframes --out /tmp/video-bench-p03-hyperframes
```

接着按 [完整复现步骤](docs/reproduce.md) 补齐素材、安装固定依赖及官方技能，再分别用**全新对话、独立目录**打开两份 `TASK.md`。两边使用同一份共用输入，禁止互相参考生成代码或结果。

只想看提示词，可以直接打开 [原始提示词目录](prompts/original)，或运行：

```bash
# 默认输出适合普通本地环境的适配版；已替换原实验的专用渲染服务接口。
python3 tools/benchmark.py prompt M04 remotion
# 原样查看当时下发的提示词（含原实验专用接口要求）。
python3 tools/benchmark.py prompt M04 remotion --original
# 第一批还有同一个任务的指定修改。
python3 tools/benchmark.py prompt P03 remotion --phase revision
```

**提示词必须和对应 `brief.md`、`events.json`、`expected.json` 一起使用。**原始提示词引用原实验的 `read_skill.py`、任务配置与文件式渲染服务，单独粘贴不会自动建立这些环境；工具生成的适配版和原文分开保存。

## 这轮怎么测

- 图表／动画 15 组、口播 15 组、产品演示 6 组，共 36 对。
- 第一批 18 组：初版制作 + 指定修改，盲评看修订版。第二批 18 组：只做初版。因此每家计入 54 次有效运行，共 108 次。
- 同一个模型：Codex `gpt-6.1-sol`，推理强度 `high`；分别使用两家冻结的官方 Skill。每个任务使用独立上下文和独立工作目录，修改阶段从本框架对应初版副本开始。
- 原输出为 30 fps；默认 1920 × 1080，指定竖屏场景例外。固定软件 H.264、CRF 18、medium、yuv420p，有声 AAC 48 kHz / 192 kbps，捕获并发上限 4。
- 第一批提供共用时间轴；**第二批字幕只给文本，不给逐句／逐词时间**，由参赛方从音轨确定。
- 先隐藏工具名做个人偏好盲评，再单独做技术检查；好看与合格分别记录。

完整边界、重跑处理与评审差异见 [测试方法](docs/methodology.md)；锁定配置见 [环境清单](environments/lock.json)。本包已经核对 108 份提示词哈希，以及双方 54 份输入版本的一致性；发布本包时没有重跑 108 次 AI 制作。

## 场景索引

第一批每项有 `v1` 初版和 `v2` 修改版；第二批只有 `v1`。每项的完整修改指令可查 [场景定义](scenes/index.json) 与原始修订提示词。

| ID | 场景 | 批次 |
| --- | --- | --- |
| [T01](scenes/T01/v1/brief.md) | 字幕、关键词与换行 | 1 |
| [T02](scenes/T02/v1/brief.md) | B-roll、画中画与同步 | 1 |
| [T03](scenes/T03/v1/brief.md) | 双人对话与说话人标签 | 1 |
| [T04](scenes/T04/v1/brief.md) | 横竖屏重排与安全区 | 1 |
| [T05](scenes/T05/v1/brief.md) | 真实整期长时间轴、5 章与局部返工 | 1 |
| [T06](scenes/T06/v1/brief.md) | 多轨声音、停顿与音量联动 | 1 |
| [S01](scenes/S01/v1/brief.md) | 准确数值、柱图与总量 | 1 |
| [S02](scenes/S02/v1/brief.md) | 拓扑关系与数量联动 | 1 |
| [S03](scenes/S03/v1/brief.md) | SVG 变形与状态表达 | 1 |
| [S04](scenes/S04/v1/brief.md) | 公式排版与分步推导 | 1 |
| [S05](scenes/S05/v1/brief.md) | 3D、粒子与确定性时间 | 1 |
| [S06](scenes/S06/v1/brief.md) | SVG、视频与多层组合 | 1 |
| [P01](scenes/P01/v1/brief.md) | 截图状态、指针与操作路径 | 1 |
| [P02](scenes/P02/v1/brief.md) | 已有 HTML/CSS 页面复用 | 1 |
| [P03](scenes/P03/v1/brief.md) | 已有 React 组件与数据复用 | 1 |
| [P04](scenes/P04/v1/brief.md) | 长页滚动、缩放与目标定位 | 1 |
| [P05](scenes/P05/v1/brief.md) | 3D 设备与动态屏幕纹理 | 1 |
| [P06](scenes/P06/v1/brief.md) | 参数化批量版本与局部更新 | 1 |
| [K01](scenes/K01/v1/brief.md) | 口播景别切换 | 2 |
| [K02](scenes/K02/v1/brief.md) | 圆形小窗出镜 | 2 |
| [K03](scenes/K03/v1/brief.md) | 推近强调 | 2 |
| [K04](scenes/K04/v1/brief.md) | 花字弹出 | 2 |
| [K05](scenes/K05/v1/brief.md) | 左右分屏 | 2 |
| [K06](scenes/K06/v1/brief.md) | 名牌条与金句卡 | 2 |
| [K07](scenes/K07/v1/brief.md) | 开场快剪 | 2 |
| [K08](scenes/K08/v1/brief.md) | 章节进度条 | 2 |
| [K09](scenes/K09/v1/brief.md) | 评论卡弹出 | 2 |
| [M01](scenes/M01/v1/brief.md) | 数据卡片数字滚动 | 2 |
| [M02](scenes/M02/v1/brief.md) | 折线图逐点绘制 | 2 |
| [M03](scenes/M03/v1/brief.md) | 时间轴里程碑 | 2 |
| [M04](scenes/M04/v1/brief.md) | 代码逐行高亮 | 2 |
| [M05](scenes/M05/v1/brief.md) | 表格排序变化 | 2 |
| [M06](scenes/M06/v1/brief.md) | 前后对比擦除 | 2 |
| [M07](scenes/M07/v1/brief.md) | 路线图描边 | 2 |
| [M08](scenes/M08/v1/brief.md) | 卡片 3D 翻转 | 2 |
| [M09](scenes/M09/v1/brief.md) | 品牌片头揭示 | 2 |

## 公开了什么

| 目录 | 内容 |
| --- | --- |
| `prompts/original/` | 108 份运行前任务提示词，SHA-256 与运行记录核对 |
| `scenes/<ID>/v1/`、`v2/` | 场景说明、事件、验收条件、可编辑数据及自制网页／React／SVG 等文本输入 |
| `input-manifest.json` | 已包含文件的哈希，以及需要自行提供的媒体／字体文件路径、原始哈希与大小 |
| `environments/` | 固定版本、官方技能提交号、两家依赖锁文件 |
| `tools/` | 列出场景、输出提示词、准备独立工作区、检查输入和包完整性 |
| `results/` | 原轮汇总数据与空白评审表，供记录自己的结果 |

素材准备和替换规则见 [输入与素材](docs/assets.md)。本包不分发官方 Skill、框架源码、浏览器二进制、API 密钥、账号会话或私人原始日志。

## 怎么理解原轮结果

本轮个人盲评：图表和动画 15 组里选 Remotion 9 组、两家都好 6 组；口播各选 4 组、两家都好 7 组；产品演示选 Remotion 3 组、HyperFrames 1 组、两家都没选 2 组。

这不是工具能力上限榜。每个场景只取一轮有效样本，评委只有作者一人；两家曾在同一台机器并行运行，导出时间不用于严谨的速度排名；缓存输入 Token 的差异也不等于实际账单差异。原轮数据在 [汇总 JSON](results/reference-summary.json)，请把自己的运行结果另存，勿覆盖原轮数据。

## 许可与反馈

自行编写的工具、提示词、说明文档使用 [MIT](LICENSE)；`scenes/` 中的输入素材源码与数据按 [CC BY-SA 4.0](LICENSE.scenes) 发布，来源说明见 [第三方声明](THIRD_PARTY_NOTICES.md)。框架、官方 Skill、字体与读者自备媒体各自遵守其原许可，本仓库许可不替代它们。

欢迎通过 Issues 反馈缺少的输入条件，或附上模型、版本、素材替换、完整提示词和检查结果分享复测。不要提交密钥、私人会话、人脸素材或无权再分发的媒体。
