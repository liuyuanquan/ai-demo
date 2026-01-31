import urllib3

# 禁用安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 目标URL
base_url = "https://fzcljs.wtu.edu.cn/rcdw/fjs.htm"

# 选择器配置
PERSON_LINK_SELECTOR = ".zhutids li a"  # 人员链接选择器
NEXT_PAGE_SELECTOR = "td a.Next"  # 下一页选择器
CONTENT_SELECTOR = ".contysdiv"  # 主要内容选择器

# 提示词配置
SYSTEM_PROMPT = "你是一名专业的信息提取助手，擅长从HTML结构中准确提取人员信息。请仔细分析输入的HTML内容，识别主要人员的姓名、职位和邮箱信息。姓名必须提取中文姓名，绝对不要提取英文姓名。如果信息不存在，请返回空字符串。确保返回的JSON格式正确，只包含指定的字段。"

USER_PROMPT = '''请从以下HTML内容中提取主要人员的姓名、职称类职位和邮箱。

要求：
1. 只提取页面中最主要的人员信息，不要提取多个人员
2. 职称类职位仅指：助教、讲师、副教授、教授
3. 绝对不要包含导师类职位，如硕士生导师、博士生导师等任何导师相关职位
4. 不要包含其他职务或头衔，如院长、主任、所长等
5. 如果有多个职称，请只返回最高级别的一个
6. 职称级别从高到低：教授 > 副教授 > 讲师 > 助教
7. 邮箱请确保是有效的邮箱地址，优先选择wtu.edu.cn域名的邮箱
8. 姓名必须提取中文姓名，如朱云海、张三等，绝对不要提取英文姓名
9. 请严格区分教授和副教授，不要将副教授错误识别为教授
10. 如果页面中明确显示为副教授，请确保返回"副教授"，而不是"教授"
11. 如果某个信息不存在，请返回空字符串
12. 严格按照指定的JSON格式返回
13. 只返回纯粹的职称，不要添加任何修饰词

HTML内容：{content}

返回格式：
{{"name": "姓名", "position": "职称类职位", "email": "邮箱"}}'''

# 常量定义
MAX_RETRIES = 5  # 最大重试次数