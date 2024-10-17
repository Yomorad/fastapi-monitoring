from aiogram.fsm.state import State, StatesGroup

# Определение состояний для FSM
class ProductStates(StatesGroup):
    waiting_for_link = State()
    waiting_product_id_for_delete_product = State()
    waiting_product_id_for_getting_history = State()
