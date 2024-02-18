from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
from aiogram.filters.callback_data import CallbackData


class PaymentCallbackFactory(CallbackData, prefix="pay"):
    choice: str
    value_gen: Optional[str] = None
    value_price: Optional[str] = None


# По стоимости подписки, просьба поправить 5 генераций-129 руб, 20 генераций-249 руб
def get_kb_fab_prices():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="5 генераций-69 руб", callback_data=PaymentCallbackFactory(choice="payment",
                                                                         value_gen="5",
                                                                         value_price="69")
    )
    builder.button(
        text="10 генераций-99 руб", callback_data=PaymentCallbackFactory(choice="payment",
                                                                          value_gen='10',
                                                                          value_price="99")
    )
    builder.button(
        text="15 генераций-129 руб", callback_data=PaymentCallbackFactory(choice="payment",
                                                                          value_gen='15',
                                                                          value_price="129")
    )
    # Выравниваем кнопки по 1 в ряд
    builder.adjust(1)
    return builder.as_markup()


class ChoiceCallbackFactory(CallbackData, prefix="sex"):
    choice: str
    value: Optional[str] = None


# кноппки возраста
def get_kb_fab_age():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Ребёнок", callback_data=ChoiceCallbackFactory(choice="age", value="kid")
    )
    builder.button(
        text="Взрослый", callback_data=ChoiceCallbackFactory(choice="age", value='adult')
    )
    # Выравниваем кнопки по 1 в ряд
    builder.adjust(1)
    return builder.as_markup()


def get_kb_fab_sex():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Мужской", callback_data=ChoiceCallbackFactory(choice="sex", value="man")
    )
    builder.button(
        text="Женский", callback_data=ChoiceCallbackFactory(choice="sex", value='woman')
    )
    # Выравниваем кнопки по 2 в ряд
    builder.adjust(2)
    return builder.as_markup()


def get_kb_fab_prof_m():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Пожарный", callback_data=ChoiceCallbackFactory(choice="prof", value="Firefighter")
    )
    builder.button(
        text="Врач", callback_data=ChoiceCallbackFactory(choice="prof", value="Doctor")
    )
    builder.button(
        text="Космонавт", callback_data=ChoiceCallbackFactory(choice="prof", value='Astronaut')
    )
    builder.button(
        text="Спортсмен", callback_data=ChoiceCallbackFactory(choice="prof", value='Athlete')
    )
    builder.button(
        text="Ученый", callback_data=ChoiceCallbackFactory(choice="prof", value="Scientist")
    )
    builder.button(
        text="Водитель", callback_data=ChoiceCallbackFactory(choice="prof", value='Driver')
    )
    builder.button(
        text="Строитель", callback_data=ChoiceCallbackFactory(choice="prof", value='Builder')
    )
    builder.button(
        text="Инженер", callback_data=ChoiceCallbackFactory(choice="prof", value="Engineer")
    )
    builder.button(
        text="Блогер", callback_data=ChoiceCallbackFactory(choice="prof", value='Blogger')
    )
    builder.button(
        text="Повар", callback_data=ChoiceCallbackFactory(choice="prof", value='Cook')
    )
    builder.button(
        text="Бухгалтер", callback_data=ChoiceCallbackFactory(choice="prof", value='Accountant')
    )
    builder.button(
        text="Парикмахер", callback_data=ChoiceCallbackFactory(choice="prof", value="Hairdresser")
    )
    builder.button(
        text="Президент", callback_data=ChoiceCallbackFactory(choice="prof", value='President')
    )
    builder.button(
        text="Журналист", callback_data=ChoiceCallbackFactory(choice="prof", value='Journalist')
    )
    builder.button(
        text="Адвокат", callback_data=ChoiceCallbackFactory(choice="prof", value="Advocate")
    )
    builder.button(
        text="Актер", callback_data=ChoiceCallbackFactory(choice="prof", value='Actor')
    )
    builder.button(
        text="Миллионер", callback_data=ChoiceCallbackFactory(choice="prof", value='Millionaire')
    )
    builder.button(
        text="Полицейский", callback_data=ChoiceCallbackFactory(choice="prof", value='Policeman')
    )
    builder.button(
        text="Лев", callback_data=ChoiceCallbackFactory(choice="prof", value='Socialite')
    )
    builder.button(
        text="Принц", callback_data=ChoiceCallbackFactory(choice="prof", value='Prince')
    )
    # Выравниваем кнопки по 3 в ряд
    builder.adjust(3)
    return builder.as_markup()


def get_kb_fab_prof():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Пожарный", callback_data=ChoiceCallbackFactory(choice="prof", value="Firefighter")
    )
    builder.button(
        text="Учитель", callback_data=ChoiceCallbackFactory(choice="prof", value='Teacher')
    )
    builder.button(
        text="Врач", callback_data=ChoiceCallbackFactory(choice="prof", value="Doctor")
    )
    builder.button(
        text="Космонавт", callback_data=ChoiceCallbackFactory(choice="prof", value='Astronaut')
    )
    builder.button(
        text="Спортсмен", callback_data=ChoiceCallbackFactory(choice="prof", value='Athlete')
    )
    builder.button(
        text="Ученый", callback_data=ChoiceCallbackFactory(choice="prof", value="Scientist")
    )
    builder.button(
        text="Водитель", callback_data=ChoiceCallbackFactory(choice="prof", value='Driver')
    )
    builder.button(
        text="Строитель", callback_data=ChoiceCallbackFactory(choice="prof", value='Builder')
    )
    builder.button(
        text="Инженер", callback_data=ChoiceCallbackFactory(choice="prof", value="Engineer")
    )
    builder.button(
        text="Блогер", callback_data=ChoiceCallbackFactory(choice="prof", value='Blogger')
    )
    builder.button(
        text="Повар", callback_data=ChoiceCallbackFactory(choice="prof", value='Cook')
    )
    builder.button(
        text="Бухгалтер", callback_data=ChoiceCallbackFactory(choice="prof", value='Accountant')
    )
    builder.button(
        text="Парикмахер", callback_data=ChoiceCallbackFactory(choice="prof", value="Hairdresser")
    )
    builder.button(
        text="Президент", callback_data=ChoiceCallbackFactory(choice="prof", value='President')
    )
    builder.button(
        text="Журналист", callback_data=ChoiceCallbackFactory(choice="prof", value='Journalist')
    )
    builder.button(
        text="Адвокат", callback_data=ChoiceCallbackFactory(choice="prof", value="Advocate")
    )
    builder.button(
        text="Актер", callback_data=ChoiceCallbackFactory(choice="prof", value='Actor')
    )
    builder.button(
        text="Миллионер", callback_data=ChoiceCallbackFactory(choice="prof", value='Millionaire')
    )
    builder.button(
        text="Полицейский", callback_data=ChoiceCallbackFactory(choice="prof", value='Policeman')
    )
    builder.button(
        text="Принцесса", callback_data=ChoiceCallbackFactory(choice="prof", value='Prince')
    )
    builder.button(
        text="Светская львица", callback_data=ChoiceCallbackFactory(choice="prof", value='Socialite')
    )
    # Выравниваем кнопки по 2 в ряд
    builder.adjust(2)
    return builder.as_markup()


# Создаем объекты инлайн-кнопок
without_watermark = InlineKeyboardButton(
    text='Фото без водяных знаков',
    callback_data='without_watermark'
)

gen_repit = InlineKeyboardButton(
    text='Сгенерировать еще фото',
    callback_data='gen_repit'
)

buy_more = InlineKeyboardButton(
    text='Купить еще генераций',
    callback_data='buy_repit'
)
