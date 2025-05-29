import logging
from typing import Optional
from pydantic import AnyUrl
import yaml
import json
from pathlib import Path

from mcp.server import Server, NotificationOptions
import mcp.types as types
import mcp.server.stdio
from mcp.server.models import InitializationOptions

import mcp_server_snowflake.tools as tools

config_file_uri = Path(__file__).parent.parent / "services" / "service_config.yaml"
server_name = "mcp-server-snowflake"
server_version = "0.0.1"

logger = logging.getLogger(server_name)


class SnowflakeService:
    def __init__(
        self,
        account_identifier: Optional[str] = None,
        username: Optional[str] = None,
        pat: Optional[str] = None,
        config_path: Optional[str] = None,
    ):
        self.account_identifier = account_identifier
        self.username = username
        self.pat = pat
        self.config_path = config_path
        self.default_complete_model = None
        self.search_services = []
        self.analyst_services = []
        self.agent_services = []
        self.unpack_service_specs()

    def unpack_service_specs(self) -> None:
        # Load the service configuration from a YAML file
        with open(self.config_path, "r") as file:
            service_config = yaml.safe_load(file)

        # Extract the service specifications
        self.search_services = service_config.get("search_services", [])
        self.analyst_services = service_config.get("analyst_services", [])

        self.agent_services = service_config.get(
            "agent_services", []
        )  # Not supported yet
        self.default_complete_model = service_config.get("cortex_complete", {}).get(
            "default_model", None
        )

        if self.default_complete_model is None:
            logger.warning(
                "No default model found in the service specification. Using snowflake-llama-3.3-70b as default."
            )


async def load_service_config_resource(file_path: str):
    with open(file_path, "r") as file:
        service_config = yaml.safe_load(file)

    return json.dumps(service_config)


async def main(account_identifier: str, username: str, pat: str, config_path: str):
    snowflake_service = SnowflakeService(
        account_identifier=account_identifier,
        username=username,
        pat=pat,
        config_path=config_path,
    )  # noqa F841
    server = Server("snowflake")  # noqa F841

    # For DEBUGGING
    logger.info("Starting Snowflake MCP server")

    @server.list_resources()
    async def list_resources() -> list[types.Resource]:
        return [
            types.Resource(
                uri=config_file_uri.as_uri(),
                name="Service Specification Configuration",
                description="Service Specification Configuration",
                mimeType="application/yaml",
            )
        ]

    @server.read_resource()
    async def read_resource(uri: AnyUrl) -> str:
        if str(uri) == config_file_uri.as_uri():
            service_config = await load_service_config_resource(
                snowflake_service.config_path
            )

            return service_config

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        # Define tool types for Cortex Search Service
        search_tools_types = tools.get_cortex_search_tool_types(
            snowflake_service.search_services
        )
        # Define tool types for Cortex Analyst Service
        analyst_tools_types = tools.get_cortex_analyst_tool_types(
            snowflake_service.analyst_services
        )
        # Tools that are not dynamically instantiated based on config file
        base_tools = [
            # Cortex Complete Tool Type
            tools.get_cortex_complete_tool_type(),
            # Get model cards
            tools.get_cortex_models_tool_type(),
            # Get spec config file
            types.Tool(
                name="get-specification-resource",
                description="""Retrieves the service specification resource""",
                inputSchema={"type": "object", "properties": {}, "required": []},
            ),
        ]

        return base_tools + search_tools_types + analyst_tools_types

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name == "get-specification-resource":
            spec = await read_resource(config_file_uri.as_uri())
            return [
                types.EmbeddedResource(
                    type="resource",
                    resource=types.TextResourceContents(
                        text=spec,
                        uri=config_file_uri.as_uri(),
                        mimeType="application/json",
                    ),
                )
            ]

        if name == "get-model-cards":
            # Call the cortex_complete function
            response = await tools.get_cortex_models(
                account_identifier=snowflake_service.account_identifier,
                username=snowflake_service.username,
                PAT=snowflake_service.pat,
            )

            if response:
                return [types.TextContent(type="text", text=json.dumps(response))]
            else:
                raise ValueError("No model cards found.")

        if name == "cortex-complete":
            # Validate required parameters
            prompt = arguments.get("prompt")
            if not prompt:
                raise ValueError("Missing required parameters")

            model = arguments.get("model")
            if not model:
                model = snowflake_service.default_complete_model

            response_format = arguments.get("response_format")

            # Call the cortex_complete function
            response = await tools.cortex_complete(
                prompt=prompt,
                model=model,
                account_identifier=snowflake_service.account_identifier,
                PAT=snowflake_service.pat,
                response_format=response_format,
            )

            return [types.TextContent(type="text", text=str(response))]

        if name in [
            spec.get("service_name") for spec in snowflake_service.search_services
        ]:
            # Find the corresponding service specification
            service_spec = next(
                (
                    spec
                    for spec in snowflake_service.search_services
                    if spec.get("service_name") == name
                ),
                None,
            )
            if not service_spec:
                raise ValueError(f"Service specification for {name} not found")

            # Extract parameters from the service specification
            database_name = service_spec.get("database_name")
            schema_name = service_spec.get("schema_name")

            # Validate required parameters
            query = arguments.get("query")
            columns = arguments.get("columns", [])
            filter_query = arguments.get("filter_query", None)
            if not query:
                raise ValueError("Missing required parameters")

            # Call the query_cortex_search function
            response = await tools.query_cortex_search(
                account_identifier=snowflake_service.account_identifier,
                service_name=name,
                database_name=database_name,
                schema_name=schema_name,
                query=query,
                PAT=snowflake_service.pat,
                columns=columns,
                filter_query=filter_query,
            )

            return [types.TextContent(type="text", text=str(response))]

        if name in [
            spec.get("service_name") for spec in snowflake_service.analyst_services
        ]:
            # Find the corresponding service specification
            service_spec = next(
                (
                    spec
                    for spec in snowflake_service.analyst_services
                    if spec.get("service_name") == name
                ),
                None,
            )
            if not service_spec:
                raise ValueError(f"Service specification for {name} not found")

            # Extract parameters from the service specification
            semantic_model = service_spec.get("semantic_model")

            # Validate required parameters
            query = arguments.get("query")
            if not query:
                raise ValueError("Missing required parameters")

            # Call the query_cortex_search function
            response = await tools.query_cortex_analyst(
                account_identifier=snowflake_service.account_identifier,
                semantic_model=semantic_model,
                query=query,
                username=snowflake_service.username,
                PAT=snowflake_service.pat,
            )

            return [types.TextContent(type="text", text=str(response))]

    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=server_name,
                server_version=server_version,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
