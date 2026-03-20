#!/usr/bin/env python3
"""
Claw直聘职位发布工具
用于OpenClaw skill调用
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error

# 从环境变量读取配置（安全）
CLAW_API_URL = os.environ.get("CLAW_API_URL", "")
CLAW_API_TOKEN = os.environ.get("CLAW_API_TOKEN", "")

if not CLAW_API_URL:
    print("错误: 未配置CLAW_API_URL环境变量")
    print("请在 ~/.openclaw/openclaw.json 中配置:")
    print('{ "skills": { "entries": { "claw-recruit": { "env": { "CLAW_API_URL": "你的API地址" } } } } }')
    sys.exit(1)

if not CLAW_API_TOKEN:
    print("错误: 未配置CLAW_API_TOKEN环境变量")
    print("请从App登录后获取Token，然后配置到环境变量")
    sys.exit(1)

def publish_job(
    title: str,
    description: str,
    requirements: str = "",
    salary_min: int = 0,
    salary_max: int = 0,
    experience_required: str = "",
    education_required: str = "",
    industry: str = "",
    city: str = "",
    company_name: str = ""
) -> dict:
    """发布职位到Claw直聘"""
    
    if not CLAW_API_TOKEN:
        return {"error": "未配置CLAW_API_TOKEN，请先登录获取Token"}
    
    url = f"{CLAW_API_URL}/api/jobs"
    
    data = {
        "title": title,
        "description": description,
        "requirements": requirements,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "experience_required": experience_required,
        "education_required": education_required,
        "industry": industry,
        "city": city,
        "company_name": company_name,
        "created_by_agent": True
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CLAW_API_TOKEN}"
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {"error": f"HTTP {e.code}: {error_body}"}
    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="发布职位到Claw直聘")
    parser.add_argument("--title", required=True, help="职位标题")
    parser.add_argument("--description", required=True, help="职位描述")
    parser.add_argument("--requirements", default="", help="任职要求")
    parser.add_argument("--salary-min", type=int, default=0, help="最低薪资")
    parser.add_argument("--salary-max", type=int, default=0, help="最高薪资")
    parser.add_argument("--experience", default="", help="经验要求")
    parser.add_argument("--education", default="", help="学历要求")
    parser.add_argument("--industry", default="", help="行业")
    parser.add_argument("--city", default="", help="城市")
    parser.add_argument("--company", default="", help="公司名称")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    
    args = parser.parse_args()
    
    result = publish_job(
        title=args.title,
        description=args.description,
        requirements=args.requirements,
        salary_min=args.salary_min,
        salary_max=args.salary_max,
        experience_required=args.experience,
        education_required=args.education,
        industry=args.industry,
        city=args.city,
        company_name=args.company
    )
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if "error" in result:
            print(f"错误: {result['error']}")
            sys.exit(1)
        else:
            print(f"职位发布成功!")
            print(f"ID: {result.get('id')}")
            print(f"标题: {result.get('title')}")
            print(f"状态: {result.get('status')}")
            if result.get('ai_score'):
                print(f"AI审核分数: {result.get('ai_score')}")

if __name__ == "__main__":
    main()