def hash_input(data: dict) -> str:
    """Generate hash for caching purposes"""
    import hashlib
    import json

    serialized = json.dumps(data, sort_keys=True)
    return hashlib.md5(serialized.encode()).hexdigest()


def format_timestamp(dt=None) -> str:
    """Format timestamp for logs"""
    from datetime import datetime

    if dt is None:
        dt = datetime.utcnow()
    return dt.isoformat()
