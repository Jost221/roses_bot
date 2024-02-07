first_data = {
    0: ['ФИО', 'username', 'Users'],
    1: ['номер телефона', 'telephone', 'Users'],
    2: ['готовность самостоятельно купить розы (Да/Нет)', 'purchase_consent', 'Users'],
    3: ['название банка', 'bank_name', 'bank'],
    4: ['данные данные для первода', 'bank_data', 'bank']
}


# Заделки на будущее
checks = {
    0: []
}

def correct_full_name(data: str):
    if any(char in "1234567890.,:;!_*-+()/#¤%&)" for char in data):
        raise 'Строка не должна содержать цифр или спец символов'
    if len(data.split(" ")):
        raise 'Необзодимо указать ФИО полностью (слова должны быть разделены одинарным пробелом)'