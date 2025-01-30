#!/usr/bin/env python3
import os
import frontmatter
import subprocess
from datetime import datetime
from pathlib import Path

def get_file_date(file_path):
    try:
        result = subprocess.run(
            ["git", "log", "--reverse", "--format=%ai", "--", file_path],
            capture_output=True,
            text=True
        )
        dates = result.stdout.strip().split("\n")
        if dates and dates[0]:
            return dates[0].split()[0]
    except Exception:
        pass
    return datetime.now().strftime("%Y-%m-%d")

def configure_git():
    print("\n🔧 配置Git信息...")
    os.system('git config --local user.email "action@github.com"')
    os.system('git config --local user.name "GitHub Action"')

def commit_changes():
    print("\n📤 提交更改到Git...")
    os.system("git add -A")
    
    # 检查是否有更改需要提交
    if os.system("git diff --quiet && git diff --staged --quiet") != 0:
        if os.system('git commit -m "chore: add front matter to posts"') == 0:
            print("✅ 更改已提交")
        else:
            print("❌ 提交失败")
    else:
        print("✅ 没有需要提交的更改")

def main():
    print("\n📝 开始处理Markdown文件的Front Matter...")
    
    processed_count = 0
    skipped_count = 0
    error_count = 0
    has_changes = False
    
    configure_git()
    
    for file_path in Path(".").rglob("*.md"):
        # 跳过隐藏目录和README文件
        if any(part.startswith(".") for part in file_path.parts) or file_path.name == "README.md":
            print(f"⏭️  跳过文件: {file_path}")
            continue
            
        try:
            print(f"\n处理文件: {file_path}")
            
            # 尝试解析front matter
            post = frontmatter.load(file_path)
            # 如果已经有front matter，跳过
            if post.metadata:
                print(f"✅ 已存在Front Matter，跳过处理")
                skipped_count += 1
                continue
                
            # 获取标题和日期
            title = file_path.stem
            date = get_file_date(str(file_path))
            print(f"📅 获取文章日期: {date}")
            
            # 获取文件所在目录作为分类
            parent_dir = file_path.parent.name
            category = "uncategorized" if parent_dir == "." else parent_dir
            print(f"📂 设置文章分类: {category}")
            
            # 创建新的front matter
            new_content = f"""---
title: "{title}"
date: {date}
categories: ["{category}"]
type: "post"
---

{post.content}"""
            
            # 写入文件
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            
            print(f"✅ 成功添加Front Matter")
            processed_count += 1
            has_changes = True
                
        except Exception as e:
            print(f"❌ 处理文件 {file_path} 时出错: {e}")
            error_count += 1
    
    print(f"\n📊 处理完成:")
    print(f"- 成功处理: {processed_count} 个文件")
    print(f"- 已有Front Matter: {skipped_count} 个文件")
    print(f"- 处理失败: {error_count} 个文件")
    
    if has_changes:
        commit_changes()

if __name__ == "__main__":
    main()
