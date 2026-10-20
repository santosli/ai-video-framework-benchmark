使用 hyperframes 和它的官方技能，把 input 制作为一条完整视频。
官方技能入口：official-skills/skills/hyperframes/SKILL.md
先通过 python3 read_skill.py 读取官方入口及按需参考（每次读取记录路径/hash），然后读取 input/brief.md、events.json、expected.json 和 input-manifest.json。
只使用给定素材、字体、文字、数据和声音；不改只读 input、official-skills、node_modules、package.json、package-lock.json、read_skill.py；禁止安装/更新依赖、技能或从外部补素材和模板。不得查看其他样本/框架工程。
输入数字/画幅/音轨/时长/验收以本版本 expected.json 和 events.json 为准；brief 中旧版概述不能覆盖它们。
必要内容、时间窗口和验收不变，排版、运动、镜头与转场可自行设计；浅底 #f4f7fb、深色正文 #172b45、蓝色强调 #2563eb。按本版本原生画幅设计，30 fps；有声任务使用给定音轨，不变速、不另配音，T06 按给定混音要求。
写码/自查/技术纠错总预算见 task-config.json，超时保留工程不重抽。保持技术检查与美术判断分开。本任务已授权自动预览和完整导出，官方技能中采访/人工批准环节由共用实验 brief 与本授权取代，不扩大任务范围。
沙箱内不启动 Chrome 或自行完整渲染。用同一文件接口向 .render-requests/ 原子写入 JSON，请求预览抽帧或完整导出；等待 .render-results/<id>/result.json，读取日志与 PNG。接口见 RENDER-API.md。只请求必要自查，不无限重试。技术纠错由执行器统一模板反馈。
最终写 submission.json，格式为 {"outputs":[{"name":"final.mp4","entry":"相对入口路径","composition":"组合 ID（适用时）","props":{}}],"timing_entry":"相对路径","editable_data_entry":"相对路径","notes":"交接说明"}。
outputs 名称须逐项对应 expected.json.outputs；多版本完整提交全部 5 份，V03 是固定主票。使用官方工程格式；预览与导出命令由外部服务执行，统一软件 H.264/libx264、CRF18、medium、yuv420p、有声 AAC48k/192k、捕获并发上限4。
首次实现交回后执行器保存 attempt-1；纠错版本与可交付版分别保存。不能完成时保留原始错误，不删步骤或更换输入。
工程与画面不得显示框架名、模型名或本地路径。输出依赖锁、素材/事件/可改数据入口和交接说明；不依赖隐藏会话动作。

任务阶段：revision
对应初版副本已放在当前工程；v1 保留在 baseline-input。统一修改指令：换给定 props：4 行变 5 行，活动项目/数字更新；供参考；布局需适配，信息不丢，时间不变。
