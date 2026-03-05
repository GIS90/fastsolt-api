# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    异步HTTP客户端工具类，基于httpx
    支持重试、超时、连接池管理、请求/响应拦截等功能

base_info:
    __author__ = PyGo
    __time__ = 2026/3/5 22:25
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api
    __file_name__ = aiohttp_lib.py

usage:

# 使用示例
async def example_usage1():
    # 创建客户端实例
    async with AsyncHTTPClientLib(
            base_url="https://jsonplaceholder.typicode.com",
            timeout=10.0,
            max_retries=2,
            http2=True,
            log=True
    ) as client:
        # 1. 简单的GET请求
        response = await client.get("/posts/1")
        print(f"GET响应: {response.status_code}")
        print(response.json())

        # 2. POST请求
        new_post = {
            "title": "测试文章",
            "body": "这是文章内容",
            "userId": 1
        }
        response = await client.post("/posts", json_data=new_post)
        print(f"\nPOST响应: {response.status_code}")
        print(response.json())

        # 3. 带查询参数的GET请求
        response = await client.get("/comments", params={"postId": 1})
        comments = response.json()
        print(f"\n评论数量: {len(comments)}")

        # 4. 批量请求
        requests = [
            {"method": "GET", "url": "/posts/1"},
            {"method": "GET", "url": "/posts/2"},
            {"method": "GET", "url": "/posts/3"},
        ]
        responses = await client.batch_request(requests, max_concurrent=3)
        print(f"\n批量请求完成，共 {len(responses)} 个响应")

        # 5. 添加请求拦截器
        async def log_request(request):
            print(f"拦截到请求: {request.method} {request.url}")
            return request

        client.add_request_interceptor(log_request)

        # 6. 添加响应拦截器
        async def log_response(response):
            print(f"拦截到响应: {response.status_code}")
            return response

        client.add_response_interceptor(log_response)

        # 使用拦截器的请求
        response = await client.get("/posts/4")
        print(f"\n带拦截器的请求完成，状态码: {response.status_code}")


# 高级用法示例：自定义重试策略和错误处理
async def example_usage2():
    # 自定义错误处理
    async def error_handler(error, context):
        print(f"自定义错误处理: {context['method']} {context['url']} - {str(error)}")
        # 可以在这里发送告警、记录到数据库等

    # 创建客户端
    client = (AsyncHTTPClientLib(
        base_url="https://api.example.com",
        timeout=5.0,
        max_retries=3,
        retry_status_codes=[408, 429, 500, 502, 503, 504],
        pool_limits={
            'max_connections': 50,
            'max_keepalive_connections': 10
        },
        headers={
            'Authorization': 'Bearer your-token-here',
            'X-Custom-Header': 'custom-value'
        }
    ))

    client.add_error_handler(error_handler)

    try:
        # 发送请求
        response = await client.get("/users/1")
        if response.status_code == 200:
            user_data = response.json()
            print(f"用户数据: {user_data}")
        else:
            print(f"请求失败: {response.status_code}")

    except Exception as e:
        print(f"最终错误: {e}")

    finally:
        await client.close()


# 运行示例
if __name__ == "__main__":
    asyncio.run(example_usage1())
    # asyncio.run(example_usage2())


状态码说明：
408     Request Timeout(请求超时)
429	    Too Many Requests(请求过多)
500	    Internal Server Error(服务器内部错误)
502	    Bad Gateway(错误网关)
503	    Service Unavailable(服务不可用)
504	    Gateway Timeout(网关超时)


design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import asyncio
import httpx
from typing import Optional, Dict, Any, List, Callable
from urllib.parse import urljoin
from httpx import Timeout, Limits, HTTPError, RequestError

from deploy.utils.logger import logger as LOG


class AsyncHTTPClientLib:
    def __init__(
            self,
            base_url: str = "",
            timeout: float = 30.0,
            max_retries: int = 3,
            retry_delay: float = 1.0,
            retry_status_codes: List[int] = None,
            pool_limits: Dict[str, int] = None,
            headers: Dict[str, str] = None,
            cookies: Dict[str, str] = None,
            verify_ssl: bool = True,
            http2: bool = False,
            log: bool = False
    ):
        """
        Args:
            base_url: 基础URL，用于构建完整URL
            timeout: 超时时间（秒）
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）
            retry_status_codes: 重试的HTTP状态码
            pool_limits: 连接池限制 {'max_connections': 100, 'max_keepalive_connections': 20}
            headers: 默认请求头
            cookies: 默认cookies
            verify_ssl: 是否验证SSL证书
            http2: 是否启用HTTP/2
            log: 是否开启日志
        """
        self.base_url = base_url.rstrip('/')
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_status_codes = retry_status_codes or [408, 429, 500, 502, 503, 504]
        self.log = log

        # 设置默认请求头
        default_headers: Dict = {
            'User-Agent': 'Mozilla/5.0 (compatible; AsyncHTTPClient/1.0)',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        if headers:
            default_headers.update(headers)

        # 配置连接池限制
        pool_limits = pool_limits or {
            'max_connections': 100,
            'max_keepalive_connections': 20
        }

        # 创建客户端实例
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers=default_headers,
            cookies=cookies or {},
            verify=verify_ssl,
            http2=http2,
            timeout=Timeout(timeout),
            limits=Limits(
                max_connections=pool_limits.get('max_connections', 100),
                max_keepalive_connections=pool_limits.get('max_keepalive_connections', 20)
            ),
            follow_redirects=True
        )

        # 请求/响应拦截器
        self.request_interceptors: List[Callable] = []
        self.response_interceptors: List[Callable] = []
        self.error_handlers: List[Callable] = []

    def __str__(self) -> str:
        return f"AsyncHTTPClientLib Class: [base-url: {self.base_url}]"

    def __repr__(self) -> str:
        return self.__str__()

    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出，确保资源释放"""
        await self.close()

    async def close(self):
        """关闭客户端连接"""
        if self.client:
            await self.client.aclose()
            if self.log: LOG.info("HTTPX客户端连接已关闭")

    def add_request_interceptor(self, interceptor: Callable):
        """添加请求拦截器"""
        self.request_interceptors.append(interceptor)

    def add_response_interceptor(self, interceptor: Callable):
        """添加响应拦截器"""
        self.response_interceptors.append(interceptor)

    def add_error_handler(self, handler: Callable):
        """添加错误处理器"""
        self.error_handlers.append(handler)

    async def _apply_request_interceptors(self, request):
        """应用请求拦截器"""
        for interceptor in self.request_interceptors:
            request = await interceptor(request) or request
        return request

    async def _apply_response_interceptors(self, response):
        """应用响应拦截器"""
        for interceptor in self.response_interceptors:
            response = await interceptor(response) or response
        return response

    async def _handle_error(self, error: Exception, context: Dict[str, Any]):
        """处理错误"""
        for handler in self.error_handlers:
            try:
                await handler(error, context)
            except Exception as e:
                if self.log: LOG.error(f"错误处理器执行失败: {e}")

    def __build_url(self, url: str) -> str:
        """构建完整URL"""
        if url.startswith(('http://', 'https://')):
            return url
        return urljoin(self.base_url, url.lstrip('/'))

    async def __request(
            self,
            method: str,
            url: str,
            *,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            cookies: Optional[Dict[str, str]] = None,
            files: Optional[Dict[str, Any]] = None,
            timeout: Optional[float] = None,
            retries: Optional[int] = None,
            retry_delay: Optional[float] = None,
            **kwargs
    ) -> httpx.Response:
        """
        发送HTTP请求的核心方法

        Returns:
            httpx.Response: 响应对象

        Raises:
            Exception: 请求失败且超过重试次数
        """
        full_url = self.__build_url(url)
        retries = retries if retries is not None else self.max_retries
        delay = retry_delay if retry_delay is not None else self.retry_delay

        # 合并请求头
        request_headers = dict(self.client.headers)
        if headers:
            request_headers.update(headers)

        # 准备请求参数
        request_kwargs = {
            'params': params,
            'headers': request_headers,
            'cookies': cookies,
            'files': files,
            **kwargs
        }

        if json_data is not None:
            request_kwargs['json'] = json_data
        elif data is not None:
            request_kwargs['data'] = data
        if timeout:
            request_kwargs['timeout'] = timeout

        last_error = None

        for attempt in range(retries + 1):
            try:
                # 创建请求对象（用于拦截器）
                request = self.client.build_request(
                    method=method,
                    url=full_url,
                    **request_kwargs
                )

                # 应用请求拦截器
                request = await self._apply_request_interceptors(request)

                # 记录请求日志
                if self.log:
                    LOG.debug(f"请求 [{attempt + 1}/{retries + 1}]: {method} {full_url}")

                # 发送请求
                response = await self.client.send(request)

                # 应用响应拦截器
                response = await self._apply_response_interceptors(response)

                # 检查是否需要重试
                if response.status_code in self.retry_status_codes and attempt < retries:
                    wait_time = delay * (2 ** attempt)  # 指数退避
                    if self.log:
                        LOG.warning(f"请求返回状态码 {response.status_code}，将在 {wait_time:.2f} 秒后重试")
                    await asyncio.sleep(wait_time)
                    continue

                # 记录响应日志
                if self.log:
                    LOG.debug(f"响应: {method} {full_url} - 状态码: {response.status_code}")

                return response

            except (RequestError, HTTPError) as e:
                last_error = e
                if attempt < retries:
                    wait_time = delay * (2 ** attempt)
                    if self.log:
                        LOG.warning(f"请求失败 ({str(e)})，将在 {wait_time:.2f} 秒后重试")
                    await asyncio.sleep(wait_time)
                else:
                    if self.log:
                        LOG.error(f"请求失败，已达到最大重试次数: {str(e)}")

                    # 处理错误
                    context = {
                        'method': method,
                        'url': full_url,
                        'attempt': attempt + 1,
                        'error': e
                    }
                    await self._handle_error(e, context)

        # 所有重试都失败
        raise last_error or Exception("未知错误")

    async def get(
            self,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> httpx.Response:
        """发送GET请求"""
        return await self.__request('GET', url=url, params=params, **kwargs)

    async def post(
            self,
            url: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> httpx.Response:
        """发送POST请求"""
        return await self.__request('POST', url=url, data=data, json_data=json_data, **kwargs)

    async def put(
            self,
            url: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> httpx.Response:
        """发送PUT请求"""
        return await self.__request('PUT', url=url, data=data, json_data=json_data, **kwargs)

    async def patch(
            self,
            url: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> httpx.Response:
        """发送PATCH请求"""
        return await self.__request('PATCH', url=url, data=data, json_data=json_data, **kwargs)

    async def delete(
            self,
            url: str,
            **kwargs
    ) -> httpx.Response:
        """发送DELETE请求"""
        return await self.__request('DELETE', url=url, **kwargs)

    async def head(
            self,
            url: str,
            **kwargs
    ) -> httpx.Response:
        """发送HEAD请求"""
        return await self.__request('HEAD', url=url, **kwargs)

    async def options(
            self,
            url: str,
            **kwargs
    ) -> httpx.Response:
        """发送OPTIONS请求"""
        return await self.__request('OPTIONS', url=url, **kwargs)

    # 便捷方法：自动解析JSON
    async def get_json(
            self,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> Any:
        """发送GET请求并返回JSON响应"""
        response = await self.get(url=url, params=params, **kwargs)
        return response.json()

    async def post_json(
            self,
            url: str,
            json_data: Optional[Dict[str, Any]] = None,
            **kwargs
    ) -> Any:
        """发送POST请求并返回JSON响应"""
        response = await self.post(url=url, json_data=json_data, **kwargs)
        return response.json()

    # 批量请求
    async def batch_request(
            self,
            requests: List[Dict[str, Any]],
            max_concurrent: int = 10
    ) -> List[httpx.Response]:
        """
        批量发送请求（并发控制）

        Args:
            requests: 请求参数列表，每个元素包含method、url等参数
            max_concurrent: 最大并发数

        Returns:
            List[httpx.Response]: 响应列表
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def _limited_request(req_kwargs):
            async with semaphore:
                method = req_kwargs.pop('method', 'GET')
                url = req_kwargs.pop('url')
                return await self.__request(method, url, **req_kwargs)

        tasks = [_limited_request(req.copy()) for req in requests]
        return await asyncio.gather(*tasks, return_exceptions=True)
