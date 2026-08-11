def evaluate_metric_success(
                            value: float,
                            operator: str,
                            target: float
                            ) -> bool:
    
    if operator == ">=" and value >= target:
        return True
    elif operator == "<=" and value <= target:
        return True
    elif operator == "==" and value == target:
        return True
    return False