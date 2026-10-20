# M09 · 品牌片头揭示（第二批共用输入）

本批测试：一次生成初版，不做修订。两家拿到完全相同的本目录。

本版任务：
- 只有音乐，没有人声和字幕：用 assets/logo.svg 的图形组合出标志，再出现文字“木子San”和副标题“AI 实践”，最后定格
- 主要动作落在 assets/beats.json 给出的节拍上；音乐 0.3 秒淡入、结尾 1 秒淡出，峰值不超过 −1 dBFS

输出：1920×1080，30 fps，6.000 秒/180 帧；有声；输出 final.mp4。

无人声。

本场景没有人声，不加字幕。

只有音乐：assets/bgm.wav 从 0 秒起，0.3 秒淡入、结尾 1 秒淡出，峰值不超过 −1 dBFS。

读取同目录 events.json、expected.json、input-manifest.json；素材在 assets/。
配色：浅底 #f4f7fb、深色正文 #172b45、蓝色强调 #2563eb；字体用 assets/fonts/ 的 MiSans。版式、动效与转场自行设计。
编码：H.264/libx264/CRF 18/medium/yuv420p，AAC 48 kHz；两家使用相同参数。
