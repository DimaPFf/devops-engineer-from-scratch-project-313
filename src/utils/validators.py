def validate_data(data):
    error = {}
    if "original_url" not in data:
        error['original_url'] = "Is empty"
    if "short_name" not in data:
        error['short_name'] = "Is empty"
    return error