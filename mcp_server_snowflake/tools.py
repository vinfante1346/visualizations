import requests
from typing import Optional
from collections import OrderedDict

import mcp.types as types
from bs4 import BeautifulSoup
from snowflake.connector import DictCursor
from snowflake.connector import connect

from mcp_server_snowflake.utils import SnowflakeResponse, SnowflakeException

import logging

logger = logging.getLogger(__name__)

sfse = SnowflakeResponse()  # For parsing Snowflake responses


# Cortex Search Service
@sfse.snowflake_response(api="search")
async def query_cortex_search(
    account_identifier: str,
    service_name: str,
    database_name: str,
    schema_name: str,
    query: str,
    PAT: str,
    columns: Optional[list[str]] = None,
    filter_query: Optional[dict] = {},
) -> dict:
    """
    Query a Cortex Search Service using the REST API.
    https://docs.snowflake.com/developer-guide/snowflake-rest-api/reference/cortex-search-service

    Args:
        account_identifier (str): Your Snowflake account_identifier.
        service_name (str): Name of the Cortex Search Service.
        database_name (str): Target database.
        schschema_nameema (str): Target schema.
        query (str): The query string to submit to Cortex Search.
        PAT (str): Personal Access Token token for authentication.
        columns (list[str], optional): A list of columns to return for each relevant result in the response. Defaults to None.
        filter_query (dict, optional): A filter query to apply to the search results. Defaults to an empty dict.

    Returns:
        dict: JSON response from the Cortex Search API.
    """
    base_url = f"https://{account_identifier}.snowflakecomputing.com/api/v2/databases/{database_name}/schemas/{schema_name}/cortex-search-services/{service_name}:query"

    headers = {
        "X-Snowflake-Authorization-Token-Type": "PROGRAMMATIC_ACCESS_TOKEN",
        "Authorization": f"Bearer {PAT}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }

    payload = {
        "query": query,
        "filter": filter_query,
    }

    if isinstance(columns, list) and len(columns) > 0:
        payload["columns"] = columns

    logging.warning(payload)

    response = requests.post(base_url, headers=headers, json=payload)

    if response.status_code == 200:
        return response
    else:
        raise SnowflakeException(
            tool="Cortex Search",
            status_code=response.status_code,
            message=response.text,
        )


def get_cortex_search_tool_types(search_services: list[dict]) -> list[types.Tool]:
    """
    Get the tool parameter inputs for each search services.

    Args:
        search_services (list[dict]): List of search service specifications.

    Returns:
        list[types.Tool]: List of tool parameters.
    """

    return [
        types.Tool(
            name=x.get("service_name"),
            description=x.get("description"),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "User query to search in search service",
                    },
                    "columns": {
                        "type": "array",
                        "description": "Optional list of columns to return for each relevant result in the response.",
                    },
                    "filter_query": {
                        "type": "object",
                        "description": """Cortex Search supports filtering on the ATTRIBUTES columns specified in the CREATE CORTEX SEARCH SERVICE command.

Cortex Search supports four matching operators:

1. TEXT or NUMERIC equality: @eq
2. ARRAY contains: @contains
3. NUMERIC or DATE/TIMESTAMP greater than or equal to: @gte
4. NUMERIC or DATE/TIMESTAMP less than or equal to: @lte

These matching operators can be composed with various logical operators:

- @and
- @or
- @not

The following usage notes apply:

Matching against NaN ('not a number') values in the source query are handled as
described in Special values. Fixed-point numeric values with more than 19 digits (not
including leading zeroes) do not work with @eq, @gte, or @lte and will not be returned
by these operators (although they could still be returned by the overall query with the
use of @not).

TIMESTAMP and DATE filters accept values of the form: YYYY-MM-DD and, for timezone
aware dates: YYYY-MM-DD+HH:MM. If the timezone offset is not specified, the date is
interpreted in UTC.

These operators can be combined into a single filter object.

Example:
Filtering on rows where NUMERIC column numeric_col is between 10.5 and 12.5 (inclusive):

{ "@and": [
  { "@gte": { "numeric_col": 10.5 } },
  { "@lte": { "numeric_col": 12.5 } }
]}""",
                    },
                },
                "required": ["query"],
            },
        )
        for x in search_services
    ]


# Cortex Complete Service
@sfse.snowflake_response(api="complete")
async def cortex_complete(
    prompt: str,
    model: str,
    account_identifier: str,
    PAT: str,
    response_format: Optional[dict] = None,
) -> dict:
    base_url = f"https://{account_identifier}.snowflakecomputing.com/api/v2/cortex/inference:complete"

    headers = {
        "X-Snowflake-Authorization-Token-Type": "PROGRAMMATIC_ACCESS_TOKEN",
        "Authorization": f"Bearer {PAT}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
    }

    # Add response_format to payload if provided
    if response_format is not None:
        payload["response_format"] = response_format

    response = requests.post(base_url, headers=headers, json=payload)

    if response.status_code == 200:
        return response
    else:
        raise SnowflakeException(
            tool="Cortex Complete",
            status_code=response.status_code,
            message=response.text,
        )


def get_cortex_complete_tool_type():
    return types.Tool(
        name="cortex-complete",
        description="""Simple LLM chat completion API using Cortex Complete""",
        inputSchema={
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "User prompt message to send to the LLM",
                },
                "model": {
                    "type": "string",
                    "description": "Optional Snowflake Cortex LLM Model name to use.",
                },
                "response_format": {
                    "type": "object",
                    "description": """Optional JSON response format to use for the LLM response.
                            Type must be 'json' and schema must be a valid JSON schema.
                            Example:
                            {
                                "type": "json",
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                    "people": {
                                        "type": "array",
                                        "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {
                                            "type": "string"
                                            },
                                            "age": {
                                            "type": "number"
                                            }
                                        },
                                        "required": ["name", "age"]
                                        }
                                    }
                                    },
                                    "required": ["people"]
                                }
                            }
                            """,
                },
            },
            "required": ["prompt"],
        },
    )


def get_region(
    account_identifier: str,
    username: str,
    PAT: str,
) -> str:
    """
    Get the region of the Snowflake account.
    """

    statement = "SELECT CURRENT_REGION()"
    with (
        connect(
            account=account_identifier,
            user=username,
            password=PAT,
        ) as con,
        con.cursor(DictCursor) as cur,
    ):
        cur.execute(statement)
        return cur.fetchone().get("CURRENT_REGION()")


async def get_cortex_models(
    account_identifier: str,
    username: str,
    PAT: str,
    url: str = "https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-llm-rest-api#model-availability",
) -> str | dict[str, list[dict[str, str]] | str]:
    """
    Get available model cards in Snowflake Cortex COMPLETE REST API.
    """

    # Send HTTP request
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to retrieve the page {url} with {response.status_code}"

    # Parse HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the model availability section (could be a table or other format)
    section = soup.find(id="model-availability") or soup.find(
        string="Model availability"
    ).find_parent("section")

    if not section:
        return (
            f"Failed to retrieve model availability from the docs. Please visit {url}."
        )

    else:
        # Process the specific section if found
        tables = section.find_all("table")
        if tables:
            model_data = []
            table = tables[0]

            # Get headers
            headers = []
            for th in table.find_all("th"):
                headers.append(th.text.strip())

            # Extract rows
            for row in table.find_all("tr")[1:]:  # Skip header row
                cells = row.find_all(["td", "th"])
                if cells:
                    row_data = {}
                    for i, cell in enumerate(cells):
                        if i < len(headers):
                            row_data[headers[i]] = cell.text.strip()
                    model_data.append(row_data)

            return OrderedDict(
                [
                    ("current_region", get_region(account_identifier, username, PAT)),
                    ("model_availability", model_data),
                ]
            )
        else:
            return f"No model availability table found at {url}."


def get_cortex_models_tool_type():
    return types.Tool(
        name="get-model-cards",
        description="""Retrieves available model cards in Snowflake Cortex REST API""",
        inputSchema={"type": "object", "properties": {}, "required": []},
    )


# Cortex Analyst Service
@sfse.snowflake_response(api="analyst")
async def query_cortex_analyst(
    account_identifier: str,
    semantic_model: str,
    query: str,
    username: str,
    PAT: str,
) -> dict:
    """
    Query the Snowflake Cortex Analyst Service using the REST API.

    Args:
        account_identifier (str): Your Snowflake account_identifier.
        semantic_model (str): Fully qualified path to YAML semantic file or Snowflake Semantic View.
                              Examples:
                              - "@my_db.my_schema.my_stage/my_semantic_model.yaml"
                              - "MY_DB.MY_SCH.MY_SEMANTIC_VIEW"
        query (str): The query string to submit to Cortex Analyst.
        PAT (str): Personal Access Token token for authentication.

    Returns:
        dict: JSON response from the Cortex Analyst API.
    """
    base_url = f"https://{account_identifier}.snowflakecomputing.com/api/v2/cortex/analyst/message"

    headers = {
        "X-Snowflake-Authorization-Token-Type": "PROGRAMMATIC_ACCESS_TOKEN",
        "Authorization": f"Bearer {PAT}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }

    if semantic_model.startswith("@") and semantic_model.endswith(".yaml"):
        semantic_type = "semantic_model_file"
    else:
        semantic_type = "semantic_model_view"

    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": query,
                    }
                ],
            }
        ],
        semantic_type: semantic_model,
        "stream": False,  # TO DO: Will need to set to True and handle SSE events
    }

    response = requests.post(base_url, headers=headers, json=payload)

    if response.status_code == 200:
        return response

    else:
        raise SnowflakeException(
            tool="Cortex Analyst",
            status_code=response.status_code,
            message=response.text,
        )


def get_cortex_analyst_tool_types(analyst_services: list[dict]) -> list[types.Tool]:
    """
    Get the tool parameter inputs for each analyst services.

    Args:
        analyst_services (list[dict]): List of analyst service specifications.

    Returns:
        list[types.Tool]: List of tool parameters.
    """

    return [
        types.Tool(
            name=x.get("service_name"),
            description=x.get("description"),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A rephrased natural language prompt from the user.",
                    },
                },
                "required": ["query"],
            },
        )
        for x in analyst_services
    ]
