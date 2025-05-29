"""
Snowflake MCP Server Package.

This package provides a Model Context Protocol (MCP) server implementation for
interacting with Snowflake's Cortex AI services. The server enables seamless
integration with Snowflake's machine learning and AI capabilities through a
standardized protocol interface.

The package supports:
- Cortex Complete: Large language model completions and chat
- Cortex Search: Semantic search across Snowflake data
- Cortex Analyst: Natural language to SQL query generation
- Model management: Discovery and information about available models

The server can be configured through command-line arguments or environment
variables and uses a YAML configuration file to define service specifications.

Environment Variables
---------------------
SNOWFLAKE_ACCOUNT : str
    Snowflake account identifier (alternative to --account-identifier)
SNOWFLAKE_USER : str
    Snowflake username (alternative to --username)
SNOWFLAKE_PAT : str
    Personal Access Token (alternative to --pat)

Examples
--------
Run the server with command-line arguments:

    python -m mcp_server_snowflake --account-identifier myaccount --username myuser --pat mytoken

Run the server with environment variables:

    export SNOWFLAKE_ACCOUNT=myaccount
    export SNOWFLAKE_USER=myuser
    export SNOWFLAKE_PAT=mytoken
    python -m mcp_server_snowflake

Notes
-----
The server requires at minimum an account identifier and Personal Access Token
to authenticate with Snowflake.
"""

import asyncio
import argparse
import os
from pathlib import Path

from . import server


def get_var(var_name: str, env_var_name: str, args) -> str | None:
    """
    Retrieve variable value from command line arguments or environment variables.

    Checks for a variable value first in command line arguments, then falls back
    to environment variables. This provides flexible configuration options for
    the MCP server.

    Parameters
    ----------
    var_name : str
        The attribute name to check in the command line arguments object
    env_var_name : str
        The environment variable name to check if command line arg is not provided
    args : argparse.Namespace
        Parsed command line arguments object

    Returns
    -------
    str | None
        The variable value if found in either source, None otherwise

    Examples
    --------
    Get account identifier from args or environment:

    >>> args = parser.parse_args(['--account-identifier', 'myaccount'])
    >>> get_var('account_identifier', 'SNOWFLAKE_ACCOUNT', args)
    'myaccount'

    >>> os.environ['SNOWFLAKE_ACCOUNT'] = 'myaccount'
    >>> args = parser.parse_args([])
    >>> get_var('account_identifier', 'SNOWFLAKE_ACCOUNT', args)
    'myaccount'
    """

    if getattr(args, var_name):
        return getattr(args, var_name)
    elif env_var_name in os.environ:
        return os.environ[env_var_name]
    else:
        return None


def main():
    """
    Main entry point for the Snowflake MCP server package.

    Parses command line arguments, retrieves configuration from arguments or
    environment variables, validates required parameters, and starts the
    asyncio-based MCP server. The server handles Model Context Protocol
    communications over stdin/stdout streams.

    The function sets up argument parsing for Snowflake connection parameters
    and service configuration, then delegates to the main server implementation.

    Raises
    ------
    ValueError
        If required parameters (account_identifier and pat) are not provided
        through either command line arguments or environment variables
    SystemExit
        If argument parsing fails or help is requested

    Notes
    -----
    The server requires these minimum parameters:
    - account_identifier: Snowflake account identifier
    - pat: Personal Access Token for authentication

    Optional parameters:
    - username: Snowflake username (recommended for full functionality)
    - service-config-file: Path to YAML service configuration

    The service configuration file defaults to '../services/service_config.yaml'
    relative to the package directory if not specified.

    Examples
    --------
    Run with command line arguments:

    >>> main()  # Uses sys.argv for argument parsing

    The function is typically called when the package is run as a module:

    $ python -m mcp_server_snowflake --account-identifier myaccount --pat mytoken
    """
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
        default=Path(__file__).parent.parent / "services" / "service_config.yaml",
    )

    args = parser.parse_args()
    account_identifier = get_var("account_identifier", "SNOWFLAKE_ACCOUNT", args)
    username = get_var("username", "SNOWFLAKE_USER", args)
    pat = get_var("pat", "SNOWFLAKE_PAT", args)
    service_config_file = args.service_config_file

    if not account_identifier or not pat:
        raise ValueError(
            "Both account_identifier and pat must be provided either as command line arguments or environment variables."
        )
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
