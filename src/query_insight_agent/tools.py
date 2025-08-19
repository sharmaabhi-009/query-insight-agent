import mysql.connector
import asyncio
from typing import Optional, Dict,Any
from google.adk.tools import ToolContext
from solace_ai_connector.common.log import log
from query_insight_agent import get_db_connection

def run_sql_query(query: str) -> str:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        # Format results as list of dicts
        results = [dict(zip(headers, row)) for row in rows]
        return str(results)
    except Exception as e:
        return f"Error executing query: {str(e)}"

async def llm_QUERYINSIGHT(
    sql: str,
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Executes the provided SQL query and returns the results.

    Args:
        sql: The SQL query string to execute
        tool_context: SAM framework context (provided automatically)
        tool_config: Tool-specific configuration (from config.yaml)

    Returns:
        A dictionary containing the query execution status and results or error message.
    """
    log_identifier = "[llm_QUERYINSIGHT]"
    log.info(f"{log_identifier} Received SQL query: {sql}")

    try:
        # Run SQL query asynchronously on a thread to avoid blocking event loop
        result = await asyncio.to_thread(run_sql_query, sql)
        log.info(f"{log_identifier} Query executed successfully.")
        return {
            "status": "success",
            "query_result": result,
            "input_sql": sql
        }
    except Exception as e:
        log.error(f"{log_identifier} Query execution failed: {e}")
        return {
            "status": "error",
            "error_message": str(e),
            "input_sql": sql
        }
