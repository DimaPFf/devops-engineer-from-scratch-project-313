def get_range(range_pagination):
    start, end = map(int, range_pagination.strip('[]').split(','))
    if start < 0 or end < 0:
        return None
    if start > end:
        return None
    offset = start
    limit = end - start
    return (offset, limit)