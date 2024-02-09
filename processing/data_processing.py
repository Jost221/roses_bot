import global_info.global_data as global_data
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
import hashlib



def check_answer(text, status, column):
    try:
        for check in global_data.CHECKS[column]:
            text = check(text)
        return text, True
    except Exception as e:
        return e.args[0], False
    
def get_list_item(items: list, text: str):
    list_data = global_data.list_data
    items = []
    for i in list_data:
        for j in text.split(' '):
            if not (j in i['addres']):
                break
        else:
            items.append(
                InlineQueryResultArticle(
                    id = hashlib.md5(i['addres'].encode()).hexdigest(),
                    input_message_content=InputTextMessageContent(
                        message_text=i['addres']
                    ),
                    title=i['addres'],
                    description=f"Необходимо доставить роз: {i['count_roses']}"
                )
            )
    return items

def search_item(msg):
    for i in global_data.list_data:
        if msg == i['addres']:
            return i