#!/usr/bin/env python3
"""
Claw直聘职位发布工具
用于OpenClaw skill调用
自动检测本机IP和读取本地Token
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import socket
import platform

def get_local_ip():
    """获取本机局域网IP地址"""
    try:
        # 创建一个UDP socket连接外部地址来获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def get_default_api_url():
    """获取默认的API URL（本机IP）"""
    ip = get_local_ip()
    return f"http://{ip}:8000"

def get_config_dir():
    """获取配置目录"""
    home = os.path.expanduser("~")
    config_dir = os.path.join(home, ".claw-recruit")
    os.makedirs(config_dir, exist_ok=True)
    return config_dir

def get_config_file():
    """获取配置文件路径"""
    return os.path.join(get_config_dir(), "config.json")

def load_config():
    """加载本地配置"""
    config_file = get_config_file()
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_config(api_url=None, token=None):
    """保存配置到本地"""
    config = load_config()
    if api_url:
        config["api_url"] = api_url
    if token:
        config["token"] = token
    
    config_file = get_config_file()
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    # 设置文件权限为仅用户可读写
    os.chmod(config_file, 0o600)
    print(f"配置已保存到: {config_file}")

def get_api_url():
    """获取API URL（优先级：环境变量 > 本地配置 > 自动检测）"""
    # 1. 环境变量
    url = os.environ.get("CLAW_API_URL", "")
    if url:
        return url
    
    # 2. 本地配置
    config = load_config()
    if config.get("api_url"):
        return config["api_url"]
    
    # 3. 自动检测本机IP
    return get_default_api_url()

def get_token():
    """获取Token（优先级：环境变量 > 本地配置）"""
    # 1. 环境变量
    token = os.environ.get("CLAW_API_TOKEN", "")
    if token:
        return token
    
    # 2. 本地配置
    config = load_config()
    return config.get("token", "")

def show_status():
    """显示当前配置状态"""
    print("=" * 50)
    print("Claw直聘配置状态")
    print("=" * 50)
    print(f"本机IP: {get_local_ip()}")
    print(f"API地址: {get_api_url()}")
    token = get_token()
    if token:
        print(f"Token: {token[:20]}... (已配置)")
    else:
        print("Token: 未配置")
    print(f"配置文件: {get_config_file()}")
    print("=" * 50)

def setup_config(api_url=None, token=None):
    """交互式配置"""
    print("\n🦞 Claw直聘配置向导")
    print("-" * 30)
    
    # 自动检测IP
    local_ip = get_local_ip()
    print(f"检测到本机IP: {local_ip}")
    
    # API URL
    if not api_url:
        default_url = f"http://{local_ip}:8000"
        user_input = input(f"API地址 [{default_url}]: ").strip()
        api_url = user_input if user_input else default_url
    
    # Token
    if not token:
        token = input("请输入Token (从App登录后获取): ").strip()
    
    if not token:
        print("错误: Token不能为空")
        return False
    
    save_config(api_url, token)
    print("\n✅ 配置完成！")
    show_status()
    return True

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
    
    api_url = get_api_url()
    token = get_token()
    
    if not token:
        return {"error": "未配置Token，请先运行: python3 claw_publish.py --setup"}
    
    url = f"{api_url}/api/jobs"
    
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
        "Authorization": f"Bearer {token}"
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
    
    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # setup命令
    setup_parser = subparsers.add_parser("setup", help="配置API地址和Token")
    setup_parser.add_argument("--url", help="API地址")
    setup_parser.add_argument("--token", help="认证Token")
    
    # status命令
    subparsers.add_parser("status", help="查看配置状态")
    
    # publish命令 (默认)
    parser.add_argument("--title", help="职位标题")
    parser.add_argument("--description", help="职位描述")
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
    
    if args.command == "setup":
        success = setup_config(args.url, args.token)
        sys.exit(0 if success else 1)
    
    elif args.command == "status":
        show_status()
        sys.exit(0)
    
    elif args.command is None and args.title:
        # 发布职位
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
                print(f"❌ 错误: {result['error']}")
                sys.exit(1)
            else:
                print(f"✅ 职位发布成功!")
                print(f"ID: {result.get('id')}")
                print(f"标题: {result.get('title')}")
                print(f"状态: {result.get('status')}")
                if result.get('ai_score'):
                    print(f"AI审核分数: {result.get('ai_score')}")
    
    else:
        # 无参数时显示帮助
        parser.print_help()
        print("\n快速开始:")
        print("  1. 配置: python3 claw_publish.py setup")
        print("  2. 发布: python3 claw_publish.py --title '前端工程师' --description '...'")

if __name__ == "__main__":
    main()