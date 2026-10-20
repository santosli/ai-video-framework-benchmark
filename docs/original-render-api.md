# 文件式渲染接口（两家同一契约）
将 UTF-8 JSON 先写临时文件，再 rename 为 .render-requests/<唯一id>.json。
请求结构：{"kind":"preview|export","entry":"相对入口路径","composition":"组合ID（适用时）","props":{},"frames":[0,75,149]}
preview 的 frames 是 30 fps 下帧号（1–12 个）；export 忽略 frames。
本框架官方入口/组合语法按冻结技能填写，不传任意命令。默认入口适用时用 index.html 或 src/index.tsx。
外部服务按官方固定浏览器串行渲染；PNG、render.log、退出码、耗时和文件 hash 写到 .render-results/<id>/；最后原子写 result.json。
preview 输出 frames/ 下 PNG；export 输出 output.mp4。先读 result.json，再看 PNG/log。预览等待计入自查预算；完整导出等待计入独立导出预算；返回超时/错误照实记录，不自行降参数。
请求 ID 只能字母数字、下划线、短横线；不能覆盖已有 ID。不要修改服务响应。
最终 submission.json 各 output 的 name 由 expected.json.outputs 决定；entry/组合/props 使用同一请求格式。
