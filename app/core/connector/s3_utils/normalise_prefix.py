def normalise_prefix(prefix: str, start_slash: bool = False, end_slash: bool = False) -> str:
    """
    Normalizes an S3 prefix:
    - Optionally adds/removes a leading slash.
    - Optionally adds/removes a trailing slash.

    Args:
        prefix (str): The prefix to normalize.
        start_slash (bool): If True, ensure prefix starts with '/'. If False, remove leading '/'.
        end_slash (bool): If True, ensure prefix ends with '/'. If False, remove trailing '/'.

    Returns:
        str: The normalized prefix.
    """
    if not prefix:
        return "/" if start_slash or end_slash else ""

    # Normalize starting slash
    if start_slash:
        prefix = prefix if prefix.startswith("/") else f"/{prefix}"
    else:
        prefix = prefix.lstrip("/")

    # Normalize ending slash
    if end_slash:
        prefix = prefix if prefix.endswith("/") else f"{prefix}/"
    else:
        prefix = prefix.rstrip("/")

    return prefix
