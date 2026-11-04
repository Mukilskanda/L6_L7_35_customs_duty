PROHIBITED = {"weapons", "narcotics"}


def duty_rate(category, origin):
    if category in PROHIBITED:
        raise ValueError("prohibited item")
    if category == "electronics":
        if origin == "FTA":
            return 0.10
        return 0.20
    if category == "clothing":
        if origin == "FTA":
            return 0.05
        return 0.12
    if category == "books":
        return 0
    return 0.15


def total_duty(category, value, origin, is_gift):
    if value < 0:
        raise ValueError("negative value")
    if is_gift:
        if value <= 5000:
            return 0
        value -= 5000
    elif value <= 1000:
        return 0
    duty = value * duty_rate(category, origin)
    if 0 < duty < 50:
        duty = 50
    return duty


def clearance_channel(value, category, has_documents):
    if category in PROHIBITED:
        return "refuse"
    if value > 100000:
        return "inspect"
    if value > 20000 and not has_documents:
        return "inspect"
    return "green"
