# Roses_bot

Данный бот был разработан на основе блок схемы работы программы. (Красные блоки не реализованны)

bs_orm - личная orm которая предоставляет для меня комфортную работу с БД SQLite (Загружалась в корень проекта, а не через pip, по скольку pypi в корне отказывается причитать вложенные модули к проекту)

Command for start on Linux
```bash
python -m venv env
source ./env/bin/activate
python main.py
```


P.S. Поиск реализован с помощью 
```python
@dp.inline_query()
async def inline_echo(inline_query: InlineQuery) -> None:
```
Последняя строка отвечает на вывод информации пользователю. В ```items``` должны находиться экземпляры класса ```InlineQueryResultArticle``` (Так же можно вставлять картинки ссылки и пр. в элементы)

Над структурой данных не особо задумывался.