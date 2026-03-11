def get_range(range_pagination):
    start, end = map(int, range_pagination.strip('[]').split(','))
    if start < 0 or end < 0:
        return None
    if start > end:
        return None
    offset = start - 1
    limit = end - start + 1
    return (offset, limit)