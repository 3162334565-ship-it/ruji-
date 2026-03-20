---
name: claw-recruit
description: 发布职位到Claw直聘平台，AI可以自主创建和发布招聘职位
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] },
        "primaryEnv": "CLAW_API_TOKEN"
      }
  }
---

# Claw直聘 - 职位发布Skill

这个skill让AI能够自主在Claw直聘平台发布职位。

## 安全配置

**重要**: 所有敏感配置保存在你本地的OpenClaw配置文件中，不会暴露到公网。

### 环境变量配置

```bash
# Claw直聘API地址（必须）
export CLAW_API_URL="你的API地址"

# 用户认证Token（从App登录后获取）
export CLAW_API_TOKEN="你的Token"
```

### 配置文件方式 (推荐)

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "skills": {
    "entries": {
      "claw-recruit": {
        "enabled": true,
        "env": {
          "CLAW_API_URL": "你的API地址",
          "CLAW_API_TOKEN": "你的Token"
        }
      }
    }
  }
}
```

### 如何获取Token

1. 在Claw直聘App上登录
2. 进入"我的" -> "OpenClaw配置"
3. Token会自动填充，保存即可

## 使用方式

告诉AI你想要发布什么样的职位，例如：

- "帮我发布一个前端开发工程师职位，薪资15-25K，需要3年经验"
- "发布一个产品经理职位，地点北京"
- "我公司需要招一个Java后端，薪资20-35K"

AI会自动：
1. 根据你的描述生成完整的职位信息
2. 调用Claw直聘API发布职位
3. 返回发布结果

## 工具调用

### claw_publish_job

使用Python脚本发布职位：

```bash
python3 {baseDir}/claw_publish.py \
  --title "前端开发工程师" \
  --description "负责公司前端开发工作..." \
  --requirements "3年以上前端开发经验，熟悉React/Vue" \
  --salary-min 15000 \
  --salary-max 25000 \
  --experience "3-5年" \
  --education "本科" \
  --industry "互联网" \
  --city "北京" \
  --company "XX科技有限公司"
```

### 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| title | 职位标题 | 是 |
| description | 职位描述 | 是 |
| requirements | 任职要求 | 否 |
| salary-min | 最低薪资（元/月） | 否 |
| salary-max | 最高薪资（元/月） | 否 |
| experience | 经验要求 | 否 |
| education | 学历要求 | 否 |
| industry | 行业 | 否 |
| city | 城市 | 否 |
| company | 公司名称 | 否 |

## 注意事项

1. **必须配置Token**: 没有有效的Token无法发布职位
2. **AI审核**: 发布的职位会经过AI自动审核
   - 分数>=80: 直接发布
   - 分数60-80: 需要人工复审
   - 分数<60: 自动拒绝
3. **薪资单位**: 为月薪，单位是元

## 示例对话

用户: "帮我发布一个Python后端开发职位，北京，20-30K"

AI: 好的，我来帮你发布这个职位。

```bash
python3 /path/to/claw_publish.py \
  --title "Python后端开发工程师" \
  --description "负责公司后端系统开发和维护，参与系统架构设计..." \
  --requirements "3年以上Python开发经验，熟悉Django/Flask，有大型项目经验优先" \
  --salary-min 20000 \
  --salary-max 30000 \
  --experience "3-5年" \
  --education "本科" \
  --industry "互联网" \
  --city "北京" \
  --company "请提供公司名称"
```

职位发布成功！
- 职位ID: 123
- 状态: 已发布
- AI审核分数: 85