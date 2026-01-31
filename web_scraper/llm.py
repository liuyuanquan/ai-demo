import json
import time
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from .config import SYSTEM_PROMPT, USER_PROMPT, MAX_RETRIES

# 初始化大语言模型
llm = ChatOpenAI(
    model="hunyuan-lite",
    api_key="sk-s4XJBFr7kCFhMvuqxI8EDCR1SboUAxJkXipB66tcV8atDxOk",
    base_url="https://www.dmxapi.cn/v1",
    temperature=0.5,
)


def call_llm(content):
    """调用大语言模型分析内容并提取信息"""
    try:
        # 构建提示模板
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    SYSTEM_PROMPT,
                ),
                (
                    "user",
                    USER_PROMPT,
                ),
            ]
        )

        # 构建输出解析器
        output_parser = JsonOutputParser()

        # 构建链式调用
        chain = prompt | llm | output_parser

        # 添加重试机制
        for retry in range(MAX_RETRIES):
            try:
                print(f"正在调用大语言模型 (尝试 {retry+1}/{MAX_RETRIES})...")
                result = chain.invoke({"content": content})
                return json.dumps(result)
            except Exception as e:
                print(f"调用失败，正在重试: {str(e)}")
                time.sleep(1)  # 等待1秒后重试
        
        print(f"已重试 {MAX_RETRIES} 次，调用大语言模型失败")
        return '{"name": "", "position": "", "email": ""}'
    except Exception as e:
        print(f"调用大语言模型失败: {str(e)}")
        return '{"name": "", "position": "", "email": ""}'


def parse_llm_result(llm_result):
    """解析大语言模型返回的 JSON 结果"""
    try:
        result = json.loads(llm_result)
        
        # 处理返回列表的情况
        if isinstance(result, list) and len(result) > 0:
            result = result[0]  # 取第一个元素
        
        return {
            "姓名": result.get("name", ""),
            "职位": result.get("position", ""),
            "邮箱": result.get("email", ""),
        }
    except Exception as e:
        print(f"解析大语言模型结果失败: {str(e)}")
        return {"姓名": "", "职位": "", "邮箱": ""}
