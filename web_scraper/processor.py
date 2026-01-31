import pandas as pd
import re


def save_temp_data(data):
    """保存临时数据到Excel文件"""
    temp_df = pd.DataFrame(data)
    temp_df.to_excel("web_scraper_temp.xlsx", index=False, engine='openpyxl')
    print(f"已保存 {len(data)} 条临时数据")


def process_data(data, page_title):
    """处理数据并生成最终Excel文件"""
    print("整理数据...")
    # 创建DataFrame
    df = pd.DataFrame(data)
    # 移除重复数据
    df = df.drop_duplicates(subset=["姓名", "邮箱"], keep="first")
    # 重新排列列顺序
    df = df[["姓名", "职位", "邮箱", "备注", "链接"]]

    print("生成Excel文件...")
    # 生成Excel文件名
    if page_title:
        # 清理标题中的非法字符，确保可以用作文件名
        safe_title = re.sub(r'[\\/:*?"<>|]', '', page_title)
        # 限制文件名长度
        safe_title = safe_title[:50]
        excel_name = f"{safe_title}.xlsx"
    else:
        excel_name = "web_scraper.xlsx"
    # 保存为Excel文件
    df.to_excel(excel_name, index=False, engine="openpyxl")

    print(f"数据采集完成，已生成文件: {excel_name}")
    print(f"共采集到 {len(df)} 条有效数据")
    
    return excel_name
