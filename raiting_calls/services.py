def get_language_id_by_name(name):
    if name == "Каз":
        return 44
    if name == "Рус":
        return 46


def get_list_variation_phone(phone):
    phones = [
        phone,
        f"%2B7{phone}",
        f"7{phone}",
        f"8{phone}",
    ]

    return phones
