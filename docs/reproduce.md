# 复现步骤

## 1. 选场景，先准备一份共用输入

先读 `scenes/index.json` 和场景 `v1/brief.md`，再读 `expected.json` 和 `events.json`。后两者是本版本数据、尺寸、时长和事件的依据，旧版 brief 概述不能覆盖它们。

每个 `input-manifest.json` 都列出文件、哈希、大小和 `included`。所有 `included: false` 的文件需自行准备。不要给两家分别选素材：先补齐并冻结一份共用输入，再复制给双方。用 `ffprobe` 核实每个文件的尺寸、fps、时长、声道与采样率，记录替换及由此调整的事件。见 [素材规则](assets.md)。

## 2. 分别准备工作区

以下以 P03 为例；两个输出目录必须不存在。`prepare` 不会运行模型、安装依赖或联网。

```bash
python3 tools/benchmark.py prepare P03 remotion --out /tmp/video-bench-p03-remotion
python3 tools/benchmark.py prepare P03 hyperframes --out /tmp/video-bench-p03-hyperframes
```

把共用的补齐素材放入两个工作区的 `input/`，逐项确认双方输入 SHA-256 一样。检查缺失项：

```bash
python3 tools/benchmark.py check-input /tmp/video-bench-p03-remotion/input
python3 tools/benchmark.py check-input /tmp/video-bench-p03-hyperframes/input
```

缺少输入或包含的源码被修改时返回非零。默认对外部素材只检查存在，不证明其符合尺寸、时间、许可或内容要求；`--exact` 还会核对历史原素材哈希。自己替换过媒体不可能通过历史原哈希核对，应记录为适配复测，另存新哈希，不要伪造原清单。

## 3. 在开测前装依赖和官方 Skill

两个工作区分别 `npm ci`，读取各自 `package-lock.json`，不要用最新版替代固定版本。网络安装放在计时开始之前。需要 Node.js 22+；若锁定旧依赖不兼容你的环境，先记录差异，完成中性冒烟后再开测。

Remotion 工作区：

```bash
cd /tmp/video-bench-p03-remotion
npm ci
git clone https://github.com/remotion-dev/skills.git official-skills
git -C official-skills checkout --detach 7ba4dcf8ebe1626b00baa41e1f2478113719b60b
python3 read_skill.py skills/remotion-best-practices/SKILL.md
```

HyperFrames 工作区：

```bash
cd /tmp/video-bench-p03-hyperframes
npm ci
git clone https://github.com/heygen-com/hyperframes.git official-skills
git -C official-skills checkout --detach e8eb358fe21d6f1a611e04f8df27ca366b337ce9
python3 read_skill.py skills/hyperframes/SKILL.md
```

原实验暴露给参赛者的技能文件范围是官方仓库 `skills/**`；完整 clone 是获取方式，复测时也只向模型提供这些技能文件，不把完整框架源码变成额外参考资料。官方原文按原许可获取，本仓库不重新分发。`read_skill.py` 记录读取的文件与 SHA-256，不能把这份自愿记录当成系统级文件访问审计。

浏览器原版本记录在 `environments/lock.json`，不同框架使用各自官方浏览器；不要擅自换浏览器来声称精确重现。本文没有自动安装浏览器或模拟原来的渲染服务。

## 4. 新对话制作初版

对两个框架各开全新对话、各自进入工作区，把本地 `TASK.md` 交给 AI。模型与推理强度在计时前回读；原轮为 `gpt-6.1-sol` / `high`。如果你无法使用该模型，可以复测方法，但必须披露模型和推理设置差异。

`TASK.md` 是**便携适配版**：允许使用官方命令在本机预览和导出，替代原实验的专用文件式渲染服务。其余任务、输入和编码要求沿用。不要把 `--original` 的输出直接放进没有渲染服务的工程等待响应。原接口仅作历史说明，见 `original-render-api.md`。

初版写码、自查与技术纠错总预算 20 分钟、最多 2 次统一技术反馈；修订版 10 分钟、最多 1 次。完整导出等待另记，累计上限 15 分钟。不同等待如何计入预算见方法说明。反馈用“验收项 X 未通过，实际 Y，目标 Z”，不给单边额外美术建议。不无限重抽，不只保存最满意的一版。

运行后保存源码、依赖锁、实际完整提示词、技术反馈、预览、MP4、命令、开始／结束时间、Token 原日志和输出哈希。个人私有日志可自行保存，上传时先去掉账号、密钥及私人内容。

## 5. 第一批继续做指定修改

先归档双方各自初版；修改也新开对话，加载**本框架对应初版副本**，不接触另一家工程。例：

```bash
python3 tools/benchmark.py prepare P03 remotion --phase revision \
  --baseline-dir /tmp/video-bench-p03-remotion \
  --out /tmp/video-bench-p03-remotion-revision
```

工具保留初版代码副本，把初版已补齐的 `input/` 存为 `baseline-input/`，把本版本 `v2/` 放到 `input/`。**v2 的外部素材仍要补齐并检查，依赖和官方技能也需重新按第 3 步准备。**修改时不应重新从零自由创作；照统一修订提示词检查新增内容，以及没要求修改的内容是否保住。

第二批 K01–K09、M01–M09 没有修订阶段。

## 6. 盲评与技术检查分别记录

把视频匿名成 A、B，先打乱对应关系。隐藏工具名称及代码，记录偏好 A／B／两家都好／两家都不好，再检查技术要求。第一批比较修订版，第二批比较初版。用 `results/review-template.csv` 记录结果，别把原轮汇总当成自己的复测成绩。

本仓库的 `validate` 只验证公开材料的完整性；`check-input` 只做文件和哈希检查。它们**不是成片技术验收器**，也不能替代看视频、听声音、字幕对齐、裁切检查和修改保留检查。
