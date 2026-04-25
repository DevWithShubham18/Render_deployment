from langchain_core.tools import tool


@tool
def render_chart(config: dict) -> dict:
    """
    Generate a chart configuration for frontend rendering.

    Args:
        config: Chart.js compatible config including type, data, options

    Returns:
        Chart config JSON
    """
    return config
