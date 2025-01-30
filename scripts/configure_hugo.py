#!/usr/bin/env python3
import os
import sys

def main():
    print("\n⚙️ 配置Hugo设置...")
    
    try:
        # 获取域名设置
        domain = os.environ.get("CUSTOM_DOMAIN") or f"{os.environ.get('GITHUB_REPOSITORY_OWNER')}.github.io/{os.environ.get('GITHUB_REPOSITORY').split('/')[-1]}"
        owner = os.environ.get("GITHUB_REPOSITORY_OWNER")
        
        if not owner:
            raise ValueError("未找到GITHUB_REPOSITORY_OWNER环境变量")
        
        print(f"🌐 使用域名: {domain}")
        print(f"👤 站点所有者: {owner}")

        if os.path.exists(".github/hugo.toml"):
            with open(".github/hugo.toml", "r", encoding="utf-8") as f:
                content = f.read()
                print(f"📖 当前配置文件内容:\n{content}")
            print("✅ hugo.toml已存在，跳过创建")
            return
            
        print("\n📝 创建hugo.toml配置文件...")
        
        config_content = f"""baseURL = "https://{domain}"
languageCode = "zh-cn"
title = "{owner}'s Space"
theme = "PaperMod"

[params]
mainSections = ["post"]
defaultTheme = "auto"
ShowReadingTime = true
ShowShareButtons = false
ShowPostNavLinks = true
ShowBreadCrumbs = true
ShowCodeCopyButtons = true
ShowToc = true

[params.homeInfoParams]
Title = "欢迎来到 {owner} 的文档站"
Content = "在喧嚣时代中静心思考，用文字传递理性与希望。"

[[params.socialIcons]]
name = "github"
url = "https://github.com/{owner}"

[outputs]
home = ["HTML", "RSS", "JSON"]

[taxonomies]
category = "categories"
tag = "tags"

[menu]
main = [
    {{identifier = "archives", name = "Archives", url = "/archives/", weight = 10}},
    {{identifier = "categories", name = "Categories", url = "/categories/", weight = 20}},
    {{identifier = "search", name = "Search", url = "/search/", weight = 30}},
    {{identifier = "tags", name = "Tags", url = "/tags/", weight = 40}}
]"""
        
        print("📁 创建.github目录...")
        os.makedirs(".github", exist_ok=True)
        
        print("💾 写入配置文件...")
        with open(".github/hugo.toml", "w", encoding="utf-8") as f:
            f.write(config_content)
        print("✅ hugo.toml配置文件创建成功")

        with open(".github/hugo.toml", "r", encoding="utf-8") as f:
                content = f.read()
                print(f"📖 当前配置文件内容:\n{content}")

        print("📤 提交更改到Git...")
        git_add = os.system("git add .github/hugo.toml")
        if git_add == 0:
            print("✅ Git add成功")
        else:
            raise Exception("Git add失败")
            
        git_commit = os.system('git commit -m "feat: add hugo configuration"')
        if git_commit == 0:
            print("✅ Git commit成功")
        else:
            raise Exception("Git commit失败")
            
        print("\n✅ Hugo配置完成")
        
    except Exception as e:
        print(f"\n❌ 配置Hugo时出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
