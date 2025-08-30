from ast import Dict
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import json

from typing import AsyncGenerator
from httpx import AsyncClient  # Import for making async HTTP requests


@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!") # 发送一条纯文本消息

    @filter.command("getreq")
    async def get_req(self, event: AstrMessageEvent, user_info: str) -> AsyncGenerator[None, None]:
        """调用FastAPI接口处理请求"""
        user_name = event.get_sender_name()
        message_str = event.message_str
        message_chain = event.get_messages()
        logger.info(message_chain)

        async def process_request(message_str: str, user_info: dict) -> dict:
            """
            Asynchronously sends a request to the FastAPI endpoint and returns the result.

            Args:
                message_str: The message string from the user.
                user_info: The user information dictionary.

            Returns:
                A dictionary containing the response from the FastAPI endpoint.
                Returns an error dictionary if the request fails.
            """
            url = "http://20.127.145.35:6899/process_request"  # FastAPI endpoint URL

            payload = {
                "message_str": message_str,
                "user_info": user_info
            }

            try:
                async with AsyncClient() as client:  # Use an async HTTP client
                    response = await client.post(url, json=payload, timeout=10.0)  # Adjust timeout as needed

                    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                    return response.json()  # Parse the JSON response

            except Exception as e:
                logger.exception(f"Error during request to FastAPI: {e}")
                return {"error": str(e)}  # Return an error message


        try:
            # Call the async function to send the request
            response_data = await process_request(message_str, user_info)

            # Handle the response
            if "error" in response_data:
                yield event.plain_result(f"Error from FastAPI: {response_data['error']}")
            else:
                yield event.plain_result(f"Hello, {user_name}, FastAPI response: {response_data}!")

        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON: {user_info}")
            yield event.plain_result(f"Hello, {user_name}, Invalid JSON parameter: {user_info}!")
        except TypeError as e:
            logger.exception(f"Error processing JSON: {user_info}")
            yield event.plain_result(f"Hello, {user_name}, Error processing JSON parameter: {e}!")


    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""


