---
name: claw-recruit
description: 发布职位到Claw直聘平台，AI可以自主创建和发布招聘职位
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] }
      }
  }
---

# Claw直聘 - 职位发布Skill

这个skill让AI能够自主在Claw直聘平台发布职位。

## 自动配置功能

**本skill会自动检测：**
- ✅ 本机局域网IP地址
- ✅ 从本地配置文件读取Token

**无需在openclaw.json中配置环境变量！**

## 快速开始

### 1. 首次使用 - 配置Token

运行配置命令：
```bash
python3 {baseDir}/claw_publish.py setup
```

或者直接指定：
```bash
python3 {baseDir}/claw_publish.py setup --token "你的Token"
```

### 2. 查看配置状态

```bash
python3 {baseDir}/claw_publish.py status
```

### 3. 发布职位

告诉AI：
> "帮我发布一个前端开发工程师职位，薪资15-25K，北京"

## 配置文件位置

配置保存在本地（不暴露到服务器）：
- `~/.claw-recruit/config.json`

## 如何获取Token

1. 在Claw直聘App上登录
2. 进入"我的" -> "OpenClaw配置"
3. Token会自动填充
4. 复制Token到配置命令中

## 命令说明

### setup - 配置
```bash
python3 {baseDir}/claw_publish.py setup
python3 {baseDir}/claw_publish.py setup --url "http://192.168.1.100:8000" --token "your_token"
```

### status - 查看状态
```bash
python3 {baseDir}/claw_publish.py status
```

### 发布职位
```bash
python3 {baseDir}/claw_publish.py \
  --title "前端开发工程师" \
  --description "负责公司前端开发工作..." \
  --requirements "3年以上前端开发经验" \
  --salary-min 15000 \
  --salary-max 25000 \
  --experience "3-5年" \
  --education "本科" \
  --industry "互联网" \
  --city "北京" \
  --company "XX科技有限公司"
```

## 安全特性

- 配置保存在本地 `~/.claw-recruit/config.json`
- 文件权限设为仅用户可读写 (0o600)
- 不会上传到任何服务器
- Token只存在你的设备上

## 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| --title | 职位标题 | 是 |
| --description | 职位描述 | 是 |
| --requirements | 任职要求 | 否 |
| --salary-min | 最低薪资（元/月） | 否 |
| --salary-max | 最高薪资（元/月） | 否 |
| --experience | 经验要求 | 否 |
| --education | 学历要求 | 否 |
| --industry | 行业 | 否 |
| --city | 城市 | 否 |
| --company | 公司名称 | 否 |

## 示例对话

用户: "帮我发布一个Python后端职位，北京，20-30K"

AI: 好的，我来帮你发布这个职位...

```bash
python3 /path/to/claw_publish.py \
  --title "Python后端开发工程师" \
  --description "负责后端系统开发和维护..." \
  --requirements "3年以上Python开发经验" \
  --salary-min 20000 \
  --salary-max 30000 \
  --experience "3-5年" \
  --education "本科" \
  --industry "互联网" \
  --city "北京"
```

✅ 职位发布成功！
- ID: 123
- 状态: 已发布
- AI审核分数: 85