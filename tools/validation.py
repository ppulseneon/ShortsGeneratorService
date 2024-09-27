"""
    Метод для валидации списка обязательных полей
"""
def validate_required_fields(data, required_fields):
    for field, field_type in required_fields.items():
        if field not in data or data[field] is None:
            return False, f"Missing required field: {field}"
        try:
            field_type(data[field])
        except ValueError:
            return False, f"Invalid type for field: {field}"
    return True, None
