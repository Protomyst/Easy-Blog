#!/usr/bin/env python3
import os

def create_page(path, content, page_type):
    try:
        print(f"\n📝 创建{page_type}页面...")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ {page_type}页面创建成功: {path}")
    except Exception as e:
        print(f"❌ 创建{page_type}页面失败: {e}")
        raise

def main():
    print("\n⚙️ 开始创建必要页面...")
    
    try:
        search_content = """---
title: "Search"
layout: "search"
summary: "search"
placeholder: "搜索文章..."
---
"""

        archives_content = """---
title: "Archives"
layout: "archives"
url: "/archives/"
summary: "archives"
---
"""

        create_page("build/content/search.md", search_content, "搜索")
        create_page("build/content/archives.md", archives_content, "归档")
        
        print("\n✅ 所有必要页面创建完成")
        
    except Exception as e:
        print(f"\n❌ 创建页面时出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
