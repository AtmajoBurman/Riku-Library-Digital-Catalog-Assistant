def transform_pg_url(original_url: str) -> str:
    """
    Transforms a PostgreSQL connection URL by:
    1. Replacing 'postgresql+asyncpg' with 'postgresql'.
    2. Replacing '?ssl=require' with '?sslmode=require&channel_binding=require'.

    Args:
        original_url (str): The original PostgreSQL connection URL.

    Returns:
        str: The transformed PostgreSQL connection URL.
    """
    transformed_url = original_url.replace("postgresql+asyncpg", "postgresql")
    transformed_url = transformed_url.replace("?ssl=require", "?sslmode=require&channel_binding=require")
    return transformed_url

