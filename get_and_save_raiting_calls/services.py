FIELD_LANGUAGE_KAZ = 44
FIELD_LANGUAGE_RUS = 46

# Получение ID значения языка в Битрикс по его текстовому представлению
def get_language_id_by_name(name):
    if name == "Каз":
        return FIELD_LANGUAGE_KAZ
    if name == "Рус":
        return FIELD_LANGUAGE_RUS


# получение списка всех вариаций номера телефона
def get_list_variation_phone(phone):
    phones = [
        phone,
        f"%2B7{phone}",
        f"7{phone}",
        f"8{phone}",
    ]

    return phones
