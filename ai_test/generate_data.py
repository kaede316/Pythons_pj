#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time : 2025/6/26 22:34 
# @Author : Kaede
# """
#     1、数据数量要多少
#     2、数据格式要什么样子
#     3、数据在生成之后能够直接被应用，还是需要做复杂的数据处理行为
# """
# # 基于提示次定义满足大模型生成直接有效的数据
# from langchain_deepseek import ChatDeepSeek
# from langchain_core.messages import SystemMessage, HumanMessage
# from langchain.output_parsers import PydanticOutputParser  # 导入 PydanticOutputParser
# from langchain.prompts import PromptTemplate  # 导入 PromptTemplate
# from pydantic import BaseModel, Field
# from typing import Literal  # 修正导入方式
#
# # 初始化模型
# model = ChatDeepSeek(
#     model="deepseek-chat",
#     api_key="sk-3653ff11a9bf47a99b5380730193947d",  # 替换成你的真实 API Key
#     temperature=0.7,
#     max_tokens=1000  # 限制最大长度
# )
#
# # 定义模板
# """
#     需要一组json格式的数据，要求数据格式形态为{"name":"alic", "age":"18", "gender":"male"}
# """
#
# # 如果想要有效生成批量有效数据，则需要提前定义好数据格式，然后通过模板生成数据，可以基于pydantic
# # 定义数据模板
# class Person(BaseModel):
#     name:str = Field(description="两到四个字中文名字"),
#     age:int  = Field(description="年龄", ge=0, le=100),
#     gender: Literal["男", "女", "保密"] = Field(description="性别")
#
# # 关联大模型生成数据
# # 1、要求json格式输出
# parser = PydanticOutputParser(pydantic_object=Person)
#
# # 2、定义与大模型交互提示词模板
# prompt = PromptTemplate(
#     template="生成一组用户数据，要求以json格式输出。格式要求为{format_instructions}\n文本信息为{person}",
#     input_variables=['person'],
#     partia_variables={'format_instructions':parser.get_format_instructions()}
# )
# messages = prompt.invoke('人员信息')
# result = model.invoke(messages)
#
# res = parser.invoke(result)
# # 最终数据运行
# print(res)
#
import json

from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import Literal

# 初始化模型
model = ChatDeepSeek(
    model="deepseek-chat",
    api_key="sk-3653ff11a9bf47a99b5380730193947d",  # 替换成你的真实 API Key
    temperature=0.7,
    max_tokens=1000
)

# 定义数据模板（修正了字段定义中的逗号问题）
class Person(BaseModel):
    name: str = Field(description="两到四个字中文名字")
    age: int = Field(description="年龄", ge=0, le=100)
    gender: Literal["男", "女", "保密"] = Field(description="性别")

# 创建输出解析器
parser = PydanticOutputParser(pydantic_object=Person)

# 修正提示词模板（使用正确的输入变量和拼写）
prompt = PromptTemplate(
    template="生成5组用户数据，要求以json格式输出。不使用markdown格式，直接输出纯json格式。格式要求如下：\n{format_instructions}\n信息为{person}\n请生成符合要求的数据。",
    input_variables=['person'],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# 生成提示（使用正确的方式调用）
# formatted_prompt = prompt.format("人员信息")
formatted_prompt = prompt.invoke("人员信息")
# 调用模型
result = model.invoke(formatted_prompt)
print(f"result is {result.content}")
data = json.loads(result.content)
# print(data)


# try:
#     # 解析结果
#     parsed_result = parser.parse(result.content)
#     print("成功生成并解析数据：")
#     print(parsed_result)
# except Exception as e:
#     print(f"解析失败: {e}")
#     print("原始输出内容：")
#     print(result.content)