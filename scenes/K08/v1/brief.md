# K08 · 章节进度条（第二批共用输入）

本批测试：一次生成初版，不做修订。两家拿到完全相同的本目录。

本版任务：
- 3 段人物片段按顺序首尾相接，对应 3 个章节：“测试条件”“测试方法”“测试结果”
- 画面顶部常驻章节导航条：当前章高亮、进度随时间推进，进入下一段时切到下一章；导航条不挡人脸

输出：1920×1080，30 fps，16.367 秒/491 帧；有声；输出 final.mp4。

人物与口播：assets/host-1.mp4 + assets/voice-1.wav、assets/host-2.mp4 + assets/voice-2.wav、assets/host-3.mp4 + assets/voice-3.wav，按顺序首尾相接，从 0 秒开始，不留空隙。

字幕：按 events.json 的 lines 原文逐条烧录进画面（不增删改字），每条在对应语音说出时出现、说完后消失；本输入不提供逐字或逐句时间，时间由你自己从音轨确定。

背景音乐用 assets/bgm.wav，从 0 秒起截取；无人声处相对原文件 −18 dB，人声期间再压低 8 dB（即 −26 dB），升降渐变约 0.3 秒；开头 0.5 秒淡入，结尾 1 秒淡出。人声按原样 0 dB 放置，不变速、不剪改。成片峰值不超过 −1 dBFS。

读取同目录 events.json、expected.json、input-manifest.json；素材在 assets/。
配色：浅底 #f4f7fb、深色正文 #172b45、蓝色强调 #2563eb；字体用 assets/fonts/ 的 MiSans。版式、动效与转场自行设计。
编码：H.264/libx264/CRF 18/medium/yuv420p，AAC 48 kHz；两家使用相同参数。
