import requests
from functools import wraps
from typing import Awaitable, Callable, TypeVar, Optional, Union
from typing_extensions import ParamSpec
import json
from snowflake.connector import DictCursor
from snowflake.connector import connect
from pydantic import BaseModel
import ast

P = ParamSpec("P")
R = TypeVar("R")


class AnalystResponse(BaseModel):
    text: str
    sql: Optional[str] = None
    results: Optional[Union[dict, list]] = None


class SearchResponse(BaseModel):
    results: Union[str, dict, list]


class CompleteResponse(BaseModel):
    results: Union[str, dict, list]


class CompleteResponseStructured(BaseModel):
    results: Union[dict, list]


class SnowflakeResponse:
    """
    Decorator class to parse Snowflake Tool responses from Snowflake RestAPIs services.

    **Usage**
    ```python
    from utils import SnowflakeResponse

    sfse = SnowflakeResponse()

    @sfse.snowflake_sse(api="complete")
    def function_name():
        pass
    ```
    """

    def fetch_results(self, statement: str, **kwargs):
        with (
            connect(**kwargs) as con,
            con.cursor(DictCursor) as cur,
        ):
            cur.execute(statement)
            return cur.fetchall()

    def parse_analyst_response(
        self, response: requests.Response | dict, **kwargs
    ) -> str:
        content = response.json().get("message", {"content": []}).get("content", [])
        res = {}
        for item in content:
            if item.get("type") == "text":
                res["text"] = item.get("text", "")

            elif item.get("type") == "sql":
                res["sql"] = item.get("statement", "")
                if item.get("statement"):
                    res["results"] = self.fetch_results(statement=res["sql"], **kwargs)
        response = AnalystResponse(**res)
        return response.model_dump_json()

    def parse_search_response(self, response: requests.Response | dict) -> str:
        """
        Parses SSE response from Cortex Search Rest API into Plain Text
        """
        content = response.json()
        ret = SearchResponse(results=content.get("results", []))
        return ret.model_dump_json()

    def parse_llm_response(
        self, response: requests.models.Response | dict, structured: bool = False
    ) -> str | list | dict:
        """
        Parses SSE response from Cortex Complete LLM Rest API into Plain Text
        """
        sse_events = dict(events=[])
        content_text = []
        for event in response.iter_lines():
            if bool(event.strip()):
                if event.decode("utf-8").startswith("data: "):
                    event_row = event.decode("utf-8").removeprefix("data: ")
                    try:
                        sse_events["events"].append(json.loads(event_row))
                    except json.JSONDecodeError as JDE:
                        raise (JDE)

        for event in sse_events["events"]:
            delta = event.get("choices")[0].get("delta", {})
            if delta.get("type") == "text":
                if content := delta.get("content"):
                    content_text.append(content)

        if structured:
            ret = CompleteResponseStructured(
                results=ast.literal_eval("".join(content_text))
            )
        else:
            ret = CompleteResponse(results="".join(content_text))

        return ret.model_dump_json()

    def snowflake_response(
        self,
        api: str,
    ) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
        def cortex_wrapper(
            func: Callable[P, Awaitable[R]],
        ) -> Callable[P, Awaitable[R]]:
            @wraps(func)
            async def response_parsers(*args: P.args, **kwargs: P.kwargs) -> R:
                raw_sse = await func(*args, **kwargs)
                conn_kwargs = dict(
                    account=kwargs.get("account_identifier", ""),
                    user=kwargs.get("username", ""),
                    password=kwargs.get("PAT", ""),
                )
                match api:
                    case "complete":
                        structured = kwargs.get("response_format", {})
                        parsed = self.parse_llm_response(
                            response=raw_sse, structured=bool(structured)
                        )
                    case "analyst":
                        parsed = self.parse_analyst_response(
                            response=raw_sse, **conn_kwargs
                        )
                    case "search":
                        parsed = self.parse_search_response(response=raw_sse)
                return parsed

            return response_parsers

        return cortex_wrapper


class SnowflakeException(Exception):
    """Handles Snowflake Tool exceptions"""

    def __init__(self, tool: str, message, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
        self.tool = tool

    def __str__(self):
        """Generic Exeptions"""
        if self.status_code == 400:
            if "unknown model" in self.message:
                return f"{self.tool} Error: Selected model not available or invalid.\n\nError Message: {self.message} "
            else:
                return f"{self.tool} Error: The resource cannot be found.\n\nError Message: {self.message} "

        elif self.status_code == 401:
            return f"{self.tool} Error: An authorization error ocurred.\n\nError Message: {self.message} "
        else:
            return f"{self.tool} Error: An error has ocurred.\n\nError Message: {self.message} \n Code: {self.status_code}"
