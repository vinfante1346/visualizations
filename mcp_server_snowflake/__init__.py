import asyncio
import argparse
import os

from . import server
from mcp_server_snowflake.utils import MissingArgumentsException


def get_var(var_name: str, env_var_name: str, args) -> str | None:
    """
    Get the value of a variable from command line arguments or environment variables.

    Args:
        var_name (str): The name of the variable to check in command line arguments.
        env_var_name (str): The name of the environment variable to check.

    Returns:
        str | None: The value of the variable if found, otherwise None.
    """

    if getattr(args, var_name):
        return getattr(args, var_name)
    elif env_var_name in os.environ:
        return os.environ[env_var_name]
    else:
        return None


def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description="Snowflake MCP Server")

    parser.add_argument(
        "--account-identifier", required=False, help="Snowflake account identifier"
    )
    parser.add_argument(
        "--username", required=False, help="Username for Snowflake account"
    )
    parser.add_argument(
        "--pat", required=False, help="Personal Access Token (PAT) for Snowflake"
    )
    parser.add_argument(
        "--service-config-file",
        required=False,
        help="Path to service specification file",
    )

    args = parser.parse_args()
    account_identifier = get_var("account_identifier", "SNOWFLAKE_ACCOUNT", args)
    username = get_var("username", "SNOWFLAKE_USER", args)
    pat = get_var("pat", "SNOWFLAKE_PAT", args)
    service_config_file = get_var("service_config_file", "SERVICE_CONFIG_FILE", args)

    parameters = dict(
        account_identifier=account_identifier,
        username=username,
        pat=pat,
        service_config_file=service_config_file,
    )

    if not all(parameters.values()):
        raise MissingArgumentsException(
            missing=[k for k, v in parameters.items() if not v]
        ) from None
    asyncio.run(
        server.main(
            account_identifier=account_identifier,
            username=username,
            pat=pat,
            config_path=service_config_file,
        )
    )


# Optionally expose other important items at package level
__all__ = ["main", "server"]
