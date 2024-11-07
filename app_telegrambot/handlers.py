import requests
from aiogram import types
from aiogram.filters import Command
from aiogram import F
from aiogram.fsm.context import FSMContext
from config import dp, FASTAPI_API_URL
from states import ProductStates

@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    """
    Обрабатывает команду /start и отправляет приветственное сообщение
    пользователю с доступными командами.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    await message.answer(
        "Привет! Я бот для мониторинга цен. Вот что я умею:\n"
        "/add - Добавить товар на мониторинг\n"
        "/delete - Удалить товар\n"
        "/list - Список товаров на мониторинге\n"
        "/history - История цен на товар"
    )

@dp.message(Command('add'))
async def add_product(message: types.Message, state: FSMContext):
    """
    Обрабатывает команду /add и запрашивает ссылку на товар для добавления
    его в мониторинг.

    Args:
        message (types.Message): Сообщение от пользователя.
        state (FSMContext): Контекст состояния для управления состояниями.
    """
    await message.answer("Отправьте ссылку на товар для мониторинга или 'Отмена' для выхода:")
    await state.set_state(ProductStates.waiting_for_link)

@dp.message(ProductStates.waiting_for_link)
async def process_link(message: types.Message, state: FSMContext):
    """
    Обрабатывает сообщение с ссылкой на товар и добавляет товар в мониторинг.

    Args:
        message (types.Message): Сообщение от пользователя.
        state (FSMContext): Контекст состояния для управления состояниями.
    """
    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer("Добавление товара отменено.")
        return

    link = message.text
    response = requests.post(f"{FASTAPI_API_URL}/products/", json={"link_product": link})
    if response.status_code == 200:
        await message.answer("Товар успешно добавлен на мониторинг!")
    else:
        await message.answer("Ошибка при добавлении товара.")
    await state.clear()  # Очищаем состояние после обработки

@dp.message(Command('delete'))
async def delete_product(message: types.Message, state: FSMContext):
    """
    Обрабатывает команду /delete и запрашивает ID товара для удаления.

    Args:
        message (types.Message): Сообщение от пользователя.
        state (FSMContext): Контекст состояния для управления состояниями.
    """
    await message.answer("Введите ID товара для удаления или 'Отмена' для выхода:")
    await state.set_state(ProductStates.waiting_product_id_for_delete_product)

@dp.message(ProductStates.waiting_product_id_for_delete_product)
async def process_deletion(message: types.Message, state: FSMContext):
    """
    Обрабатывает сообщение с ID товара и удаляет товар из мониторинга.

    Args:
        message (types.Message): Сообщение от пользователя.
        state (FSMContext): Контекст состояния для управления состояниями.
    """
    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer("Удаление товара отменено.")
        return

    if not message.text.isdigit():
        await message.answer("Некорректный ввод. Пожалуйста, введите ID товара или 'Отмена' для выхода.")
        return

    product_id = message.text
    response = requests.delete(f"{FASTAPI_API_URL}/products/{product_id}")
    if response.status_code == 200:
        await message.answer("Товар успешно удалён!")
    else:
        await message.answer("Ошибка при удалении товара или товар не найден.")
    await state.clear()  # Очищаем состояние после обработки

@dp.message(Command('list'))
async def list_products(message: types.Message):
    """
    Обрабатывает команду /list и возвращает список товаров на мониторинге.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    response = requests.get(f"{FASTAPI_API_URL}/products/")
    if response.status_code == 200:
        products = response.json()
        if products:
            product_list = "\n".join([f"id: {product['id']}\nname: {product['name_product']}\nlink: {product['link_product']}\
                                      \ndescription: {product['description']}\nrate: {product['rate']}\n" for product in products])
            await message.answer(f"Товары на мониторинге:\n{product_list}")
        else:
            await message.answer("Список товаров пуст.")
    else:
        await message.answer("Ошибка при получении списка товаров.")

@dp.message(Command('history'))
async def get_price_history(message: types.Message, state: FSMContext):
    """
    Обрабатывает команду /history и запрашивает ID товара для 
    получения его истории цен.

    Args:
        message (types.Message): Сообщение от пользователя.
        state (FSMContext): Контекст состояния для управления состояниями.
    """
    await message.answer("Введите ID товара для получения истории цен или 'Отмена' для выхода:")
    await state.set_state(ProductStates.waiting_product_id_for_getting_history)

@dp.message(ProductStates.waiting_product_id_for_getting_history)
async def process_history_request(message: types.Message, state: FSMContext):
    """
    Обрабатывает ID товара и возвращает его историю цен.

    Args:
        message (types.Message): Сообщение от пользователя.
        state (FSMContext): Контекст состояния для управления состояниями.
    """
    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer("Запрос истории цен отменён.")
        return

    if not message.text.isdigit():
        await message.answer("Некорректный ввод. Пожалуйста, введите ID товара или 'Отмена' для выхода.")
        return

    product_id = message.text
    response = requests.get(f"{FASTAPI_API_URL}/products/{product_id}/price-history")
    if response.status_code == 200:
        price_history = response.json()
        if price_history:
            history = "\n".join([f"Цена: {entry['price']} Руб. на {entry['price_time']}" for entry in price_history])
            await message.answer(f"История цен для товара {product_id}:\n{history}")
        else:
            await message.answer("История цен для этого товара пуста.")
    else:
        await message.answer("Ошибка при получении истории цен.")
    await state.clear()  # Очищаем состояние после обработки

@dp.message(F.text)
async def handle_unknown_message(message: types.Message):
    """
    Обрабатывает неизвестные команды и отправляет сообщение об ошибке.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    await message.answer("Некорректный ввод. Используйте /start для просмотра доступных команд.")

def register_handlers(dp):
    """
    Регистрирует все обработчики команд в диспетчере.

    Args:
        dp: Экземпляр диспетчера для регистрации обработчиков.
    """
    dp.message.register(send_welcome, Command('start'))
    dp.message.register(add_product, Command('add'))
    dp.message.register(process_link, ProductStates.waiting_for_link)
    dp.message.register(delete_product, Command('delete'))
    dp.message.register(process_deletion, ProductStates.waiting_product_id_for_delete_product)
    dp.message.register(list_products, Command('list'))
    dp.message.register(get_price_history, Command('history'))
    dp.message.register(process_history_request, ProductStates.waiting_product_id_for_getting_history)
    dp.message.register(handle_unknown_message, F.text)
