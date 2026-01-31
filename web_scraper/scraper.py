import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .config import base_url, PERSON_LINK_SELECTOR, NEXT_PAGE_SELECTOR, CONTENT_SELECTOR
from .llm import call_llm, parse_llm_result

# 存储所有人员链接
person_links = []

# 存储网页标题
page_title = ""


def get_person_links():
    """分页遍历提取所有人员链接"""
    global page_title
    current_url = base_url
    session = requests.Session()

    while True:
        try:
            response = session.get(current_url, verify=False, timeout=30)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")

            # 提取网页标题
            if not page_title:
                title_elem = soup.find("title")
                if title_elem:
                    page_title = title_elem.text.strip()
                    print(f"获取到网页标题: {page_title}")

            # 提取人员链接
            zhutids = soup.select(PERSON_LINK_SELECTOR)
            for a in zhutids:
                link = urljoin(current_url, a.get("href"))
                person_links.append(link)

            # 查找下一页
            next_page = soup.select_one(NEXT_PAGE_SELECTOR)
            if next_page:
                next_url = urljoin(current_url, next_page.get("href"))
                current_url = next_url
            else:
                break

        except Exception as e:
            print(f"获取人员链接时出错: {e}")
            break

    return person_links, page_title


def extract_person_info(link):
    """提取单个人员的详细信息"""
    info = {"姓名": "", "职位": "", "邮箱": "", "备注": ""}

    try:
        response = requests.get(link, verify=False, timeout=30)
        response.encoding = "utf-8"

        if response.status_code != 200:
            info["备注"] = "链接失效"
            return info

        soup = BeautifulSoup(response.text, "html.parser")

        # 使用 .contysdiv 选择器获取内容
        try:
            content_elem = soup.select_one(CONTENT_SELECTOR)
            if content_elem:
                content = content_elem.prettify()  # 传递完整的 HTML 结构
                # 使用大语言模型分析内容并提取信息
                llm_result = call_llm(content)
                extracted_info = parse_llm_result(llm_result)
                info["姓名"] = extracted_info["姓名"]
                info["职位"] = extracted_info["职位"]
                info["邮箱"] = extracted_info["邮箱"]
            else:
                info["备注"] = f"未找到 {CONTENT_SELECTOR} 元素"
        except Exception as e:
            info["备注"] = f"内容分析失败: {str(e)}"

        # 移除备注末尾的分号和空格
        info["备注"] = info["备注"].rstrip("; ")
        if not info["备注"]:
            info["备注"] = ""

    except Exception as e:
        info["备注"] = f"访问失败: {str(e)}"

    return info
