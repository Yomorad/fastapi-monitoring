import requests
from aiogram import types
from aiogram.filters import Command
from aiogram import F
from aiogram.fsm.context import FSMContext
from config import dp, FASTAPI_API_URL
from states import ProductStates

# Команда /start для приветствия
@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Я бот для мониторинга цен. Вот что я умею:\n"
        "/add - Добавить товар на мониторинг\n"
        "/delete - Удалить товар\n"
        "/list - Список товаров на мониторинге\n"
        "/history - История цен на товар"
    )

# Добавление товара на мониторинг
@dp.message(Command('add'))
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Отправьте ссылку на товар для мониторинга или 'Отмена' для выхода:")
    await state.set_state(ProductStates.waiting_for_link)

# Обработка ссылки на товар
@dp.message(ProductStates.waiting_for_link)
async def process_link(message: types.Message, state: FSMContext):
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

# Удаление товара
@dp.message(Command('delete'))
async def delete_product(message: types.Message, state: FSMContext):
    await message.answer("Введите ID товара для удаления или 'Отмена' для выхода:")
    await state.set_state(ProductStates.waiting_product_id_for_delete_product)

# Обработка ID товара для удаления
@dp.message(ProductStates.waiting_product_id_for_delete_product)
async def process_deletion(message: types.Message, state: FSMContext):
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

# Получение списка товаров на мониторинге
@dp.message(Command('list'))
async def list_products(message: types.Message):
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

# Получение истории цен на товар
@dp.message(Command('history'))
async def get_price_history(message: types.Message, state: FSMContext):
    await message.answer("Введите ID товара для получения истории цен или 'Отмена' для выхода:")
    await state.set_state(ProductStates.waiting_product_id_for_getting_history)

# Обработка ID товара для истории цен
@dp.message(ProductStates.waiting_product_id_for_getting_history)
async def process_history_request(message: types.Message, state: FSMContext):
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

# Обработка некорректных команд
@dp.message(F.text)
async def handle_unknown_message(message: types.Message):
    await message.answer("Некорректный ввод. Используйте /start для просмотра доступных команд.")

# Функция для регистрации всех обработчиков
def register_handlers(dp):
    dp.message.register(send_welcome, Command('start'))
    dp.message.register(add_product, Command('add'))
    dp.message.register(process_link, ProductStates.waiting_for_link)
    dp.message.register(delete_product, Command('delete'))
    dp.message.register(process_deletion, ProductStates.waiting_product_id_for_delete_product)
    dp.message.register(list_products, Command('list'))
    dp.message.register(get_price_history, Command('history'))
    dp.message.register(process_history_request, ProductStates.waiting_product_id_for_getting_history)
    dp.message.register(handle_unknown_message, F.text)
