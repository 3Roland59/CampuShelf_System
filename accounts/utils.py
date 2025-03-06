def normalize_phone(number: str):
    valid_phone = number.replace(" ", "")
    if valid_phone.__len__() == 14:
        return valid_phone.removeprefix("+233")

    elif valid_phone.__len__() == 13:
        return ("0" + "%s") % valid_phone.removeprefix("+233")
