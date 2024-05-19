
def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min(value, max_value), min_value)