---
name: story-cards
description: 一站式社媒图文内容创作工作台（适配手机 Qoder、独立账号）。把一个想法变成可发布的图文故事：策划可选张数的卡片稿、多画风选择、逐平台（小红书/抖音/公众号）标题/标签/热点话题/封面文案、流量与点赞评论增长方案；经确认后批量出图、逐张核对中文文字、交付图片+分平台文案包+发布清单。当用户说"做图文/图文故事/社媒内容/小红书抖音公众号图文/给我老婆做内容/内容创作"时使用。
---

# 图文内容工作台（story-cards）

## 概述
面向非技术社媒创作者（含手机端、独立账号）。一个想法 → 策划案（卡片稿+画风+分平台包装+增长方案）→ 确认 → 批量出图 → 核对 → 交付。出图走使用者配置的千问 Token Plan 额度。

## 首次使用配置（每台设备/每个账号一次，之后无感）
配置目录 `~/.story-cards/`：`key`（600 权限）+ `config.json`（默认平台/张数/画风）。
1. 若 `key` 不存在：请用户粘贴一个千问 API Key（千问平台「API Keys」页；可用本人或家人共享的 Key），用 `umask 077; printf '%s' '<key>' > ~/.story-cards/key` 写入。**不打印、不进仓库、不外传**。
2. 若 `config.json` 不存在：用一次问卷（或默认）收齐 默认平台/张数/画风 并写入。
3. 旧版 `~/.qwen_social_key` 若存在可迁移为 `~/.story-cards/key`。

## 主流程（确认前不出图）
1. **采集**：读想法。缺省偏好从 config 读；仅当想法本身有歧义才追问，最多一轮。
2. **策划**：定故事弧线与情绪曲线；按选定张数 N 写卡片稿（每张=画面设定+图上文字 2-4 行）；主角形象跨卡一致。画风从 [styles.md](references/styles.md) 选（默认 healing）。
3. **分平台包装**：对每个目标平台按 [platforms.md](references/platforms.md) 产出：标题 2-3 变体、标签/hashtags、热点话题建议、封面文案、正文、建议发布时段。
4. **增长方案**：按 [growth.md](references/growth.md) 产出：开头钩子、情绪共鸣点、评论引导、点赞/收藏动机、系列化建议、互动回复话术、复盘指标。
5. **确认**：把 策划+包装+增长 一起呈现，问「确认出图 / 改哪里（张数/画风/平台/文案）」。未确认不出图。
6. **出图**：写 cards JSON（name/scene/lines/pos），运行
   `python3 <skill>/scripts/generate_cards.py --cards <json> --outdir <工作区>/outputs --prefix <故事名>卡片 --style <画风>`
   后台运行等完成。无 python3 的环境用 curl 兜底（见下）。
7. **核对**：逐张 Read PNG，核对中文逐字准确+画面符合；错字单张重出（同一问题只自动纠正一次）。
8. **交付**：图片链接+目录；分平台文案包（标题/标签/正文/热点）；增长清单；发布 checklist。分开说已满足/仍不符。

## 张数与画风
- 张数 N 可选（默认 config，常见 6/9/12/16）；短视频图文宜 6-9，长故事宜 12-16。不固定 16。
- 画风 presets：healing 治愈水彩 / flat 扁平插画 / film 胶片摄影 / ink 国风水墨 / line 手绘线条 / 3d 黏土治愈。见 styles.md。

## curl 兜底（无 python3 时，单张）
`curl -s -X POST "$BASE/services/aigc/multimodal-generation/generation" -H "Authorization: Bearer $(cat ~/.story-cards/key)" -H 'Content-Type: application/json' -d '{"model":"qwen-image-3.0-pro","input":{"messages":[{"role":"user","content":[{"text":"<提示词>"}]}]},"parameters":{"size":"1104*1472","n":1}}'`
取 `output.choices[0].message.content[0].image` 的 URL 再下载。**不要用 compatible-mode/images/generations（url error）**。

## 移动端/独立账号注意
- 不依赖任何他人本机路径；配置与密钥都在使用者自己 home 下。
- 技能可打包 `.skill`/zip 导入手机 Qoder（见交付说明）；导入后首次运行走「首次使用配置」。

## Resources
- `scripts/generate_cards.py`：批量出图，`--style` 选画风，`--cards/--outdir/--prefix/--keyfile/--model/--size/--base`。
- `references/styles.md` / `platforms.md` / `growth.md`。