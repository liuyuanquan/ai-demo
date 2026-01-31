import argparse
from .scraper import get_person_links, extract_person_info
from .processor import save_temp_data, process_data

# 存储采集的数据
data = []


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="网页爬虫工具")
    parser.add_argument("--link", type=str, help="单独测试的链接")
    args = parser.parse_args()

    # 如果提供了单独的链接，只测试该链接
    if args.link:
        print(f"开始测试单个链接: {args.link}")
        info = extract_person_info(args.link)
        info['链接'] = args.link
        print(f"测试结果: {info}")
        return

    # 否则执行完整流程
    print("开始采集人员链接...")
    person_links, page_title = get_person_links()
    print(f"共采集到 {len(person_links)} 个人员链接")

    print("开始提取人员信息...")
    for i, link in enumerate(person_links, 1):
        print(f"处理第 {i} 个链接: {link}")
        info = extract_person_info(link)
        # 添加链接到数据中以便调试
        info['链接'] = link
        data.append(info)
        
        # 每次处理完都保存
        print(f"已处理 {i} 个链接，保存结果...")
        save_temp_data(data)

    # 处理最终数据
    process_data(data, page_title)


if __name__ == "__main__":
    main()
