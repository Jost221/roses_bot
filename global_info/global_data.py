new_user_data = {
    'user_view': [
        'ФИО',
        "номер телефона", 
        "ответ в формате Да\Нет. Вы готовы купить розы на свои кровные?"
        ],
    'column_name': [
        'username',
        'phone',
        'purchase_consent'
        ],
}

bank_data = {
    'user_view': ['название банка', 'данные данные для первода'],
    'column_name': ['bank_name', 'bank_data']
}


def contains_onli_alph(data: str):
    if any(char in "1234567890.,:;!_*-+()/#¤%&)" for char in data):
        raise Exception('Строка не должна содержать цифр или спец символов')
    return data


def have_3_words(data: str):
    if len(data.strip().split(" ")) != 3:
        raise Exception(
            'Необзодимо указать ФИО полностью (слова должны быть разделены одинарным пробелом)')
    return data


def onli_number(data: str):
    new_data = data.replace('+7', '8').replace(' ', '').replace('(', '') \
        .replace(')', '').replace('-', '')
    if not new_data.isdigit():
        raise Exception('Строка содержит буквы или спец символы')
    return int(new_data)


def len_number(data):
    if len(str(data)) == 11:
        return data
    raise Exception("Строка не соответствует номеру телефона")


def start_with_nine(data):
    if str(data)[1] == '9':
        return data
    raise Exception('Необходимо указать мобильный номер телефона')


def yes_no_to_int(data):
    if data.lower() == 'да':
        return 1
    if data.lower() == 'нет':
        return 0
    raise Exception(
        'Убедитесь что вы написали ответ в соответствии с форматом Да/Нет')


CHECKS = {
    'username': [contains_onli_alph, have_3_words],
    'phone': [onli_number, len_number, start_with_nine],
    'purchase_consent': [yes_no_to_int],
    'bank_name': [contains_onli_alph],
    'bank_data': [onli_number]
}

list_data = [
    {
        'addres': 'г. Кострома ул. Комсомольская д.1',
        'count_roses': 58
    },
    {
        'addres': 'г. Моосква ул. Ленинградская д.6',
        'count_roses': 20
    },
    {
        'addres': 'г. Москва ул. Пушкина д.53',
        'count_roses': 10
    },
    {
        'addres': 'г. Москва ул. Каллантай д.45',
        'count_roses': 32
    }
]

roses_cell = 100