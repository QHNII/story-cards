# story-cards · 治愈系图文故事创作技能

一个 Qoder 项目级 Skill：把一个想法变成可发布的图文故事（可选张数、多画风、分平台标题/标签/热点、流量与互动增长方案），确认后批量出图、核对中文文字、交付图片+文案包。

## 手机 Qoder 使用（云端任务）
1. 手机 Qoder → 新建任务 → 选择 **Cloud** 环境 → 链接 GitHub → 选择本仓库 `QHNII/story-cards`。
2. 首次使用按技能提示配置一个千问 API Key（存于你设备本地 `~/.story-cards/key`，本仓库不含任何密钥）。
3. 之后直接发一个想法/故事，技能自动走「策划→确认→出图→交付」。

## 目录
- `.qoder/skills/story-cards/SKILL.md` 主流程
- `.qoder/skills/story-cards/scripts/generate_cards.py` 出图脚本
- `.qoder/skills/story-cards/references/` 画风/平台/增长知识库

## 桌面 Qoder 使用
扩展 → Skills → Add Skills → Upload Skill，选择本仓库打包的 `.skill`，或将 `.qoder/skills/story-cards` 放入项目/用户技能目录。