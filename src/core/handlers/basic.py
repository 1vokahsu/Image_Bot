from aiogram import Bot, F
from aiogram.enums import ChatMemberStatus
from aiogram.types import CallbackQuery, Message, FSInputFile, InlineKeyboardMarkup, PhotoSize, LabeledPrice, \
    PreCheckoutQuery
from aiogram.types.message import ContentType
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from Image_Bot.src.create_dp import dp
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from Image_Bot.src.core.keyboards import kb
from Image_Bot.src.core.config.config import config
from Image_Bot.src.core.database.queries.orm import AsyncORM
from Image_Bot.src.ai_model import ai_gen_photo, ai_swap_photo, watermark_text
import os


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    upload_photo = State()


@dp.callback_query(F.data == "gen_repit")
async def process_start(callback: CallbackQuery, bot: Bot, state: FSMContext):
    print(f"Юзера {callback.from_user.id} нажал на кнопку \"сгенерировать снова\"")
    user_channel_status = await bot.get_chat_member(chat_id=-1001711057486, user_id=callback.from_user.id)
    print(user_channel_status.status)
    if user_channel_status.status != ChatMemberStatus.LEFT:
        gens = await AsyncORM.get_gens(callback.from_user.id)
        print(f"Проверяем, что у юзера {callback.from_user.id} есть хотя бы 1 генерация")
        if gens > 0:
            await callback.message.answer(
                "Загрузите чёткое фото, на котором хорошо видно лицо"
            )
            await state.set_state(FSMFillForm.upload_photo)
        else:
            print(f"У юзера {callback.from_user.id} закончились генерации")
            await callback.answer(text="У вас закончились бесплатные генерации",
                                  show_alert=True)
            print("Предлагаем купить генерации")
            await callback.message.answer(text="Можете приобрести генерации!",
                                          reply_markup=kb.get_kb_fab_prices())
    else:
        await callback.message.answer(
            text="Чтобы ознакомиться с возможностями нашего бота, подпишись на канал @haappymom\n\n"
                 "После подписки нажмите /create_image"
        )


@dp.message(Command("create_image"))
async def create_image(message: Message, bot: Bot, state: FSMContext):
    print(f"Юзер {message.from_user.id} нажал /create_image ")
    print(f"Добавляем юзера {message.from_user.id} в бд")
    await AsyncORM.add_user_id(message.from_user.id, message.from_user.username)
    user_channel_status = await bot.get_chat_member(chat_id=-1001711057486, user_id=message.from_user.id)
    print(user_channel_status.status)
    if user_channel_status.status != ChatMemberStatus.LEFT:
        gens = await AsyncORM.get_gens(message.from_user.id)
        print(f"Проверяем, что у юзера {message.from_user.id} есть хотя бы 1 генерация")
        if gens > 0:
            await message.answer(
                "Загрузите чёткое фото, на котором хорошо видно лицо"
            )
            await state.set_state(FSMFillForm.upload_photo)
        else:
            print(f"У юзера закончились {message.from_user.id} генерации")
            await message.answer(text="У вас закончились бесплатные генерации.\n\nМожете приобрести их!",
                                 reply_markup=kb.get_kb_fab_prices())
    else:
        await message.answer(
            text="Чтобы ознакомиться с возможностями нашего бота, подпишись на канал @haappymom\n\n"
                 "После подписки нажмите /create_image"
        )


@dp.message(CommandStart())
async def process_start_command(message: Message, bot: Bot, state: FSMContext):
    print(f"Юзер {message.from_user.id} нажал /start ")
    await message.answer(
        "<b>Вы когда-нибудь представляли своего ребенка пожарным, ученым, врачом или даже президентом?</b>\n\n"
        "<i>Наш инновационный бот может воплотить это воображение в реальность!</i> ✨\n\n\n"
        "Просто <b>загрузите фотографию</b> 📸 и посмотрите, как бы выглядели Вы или Ваш ребёнок"
        " в роли представителя любой профессии!\n\n"
        "<i>Исследуйте мир современных возможностей – от врача и инженера до ученого,"
        " спортсмена или светской львицы!</i> 👨‍⚕️💃"
    )
    print(f"Добавляем юзера {message.from_user.id} в бд")
    await AsyncORM.add_user_id(message.from_user.id, message.from_user.username)
    user_channel_status = await bot.get_chat_member(chat_id=-1001711057486, user_id=message.from_user.id)
    print(user_channel_status.status)
    if user_channel_status.status == ChatMemberStatus.LEFT:
        await message.answer(
            text="Чтобы ознакомиться с возможностями нашего бота, подпишись на канал @haappymom\n\n"
                 "После подписки нажмите /create_image"
        )
    else:
        gens = await AsyncORM.get_gens(message.from_user.id)
        print(f"Проверяем, что у юзера {message.from_user.id} есть хотя бы 1 генерация")
        if gens > 0:
            await message.answer(
                "Загрузите чёткое фото, на котором хорошо видно лицо"
            )
            await state.set_state(FSMFillForm.upload_photo)
        else:
            print(f"У юзера закончились {message.from_user.id} генерации")
            await message.answer(text="У вас закончились бесплатные генерации.\n\nМожете приобрести их!",
                                 reply_markup=kb.get_kb_fab_prices())


@dp.callback_query(kb.ChoiceCallbackFactory.filter(F.choice == "age"))
async def process_age(callback: CallbackQuery,
                      callback_data: kb.ChoiceCallbackFactory,
                      bot: Bot):
    user_id = callback.from_user.id
    await AsyncORM.add_age(user_id, callback_data.value)
    print(f"Добавляем юзеру {callback.from_user.id} возраст в бд")
    user_channel_status = await bot.get_chat_member(chat_id=-1001711057486, user_id=callback.from_user.id)
    print(user_channel_status.status)
    if user_channel_status.status != ChatMemberStatus.LEFT:
        gens = await AsyncORM.get_gens(callback.from_user.id)
        print(f"Проверяем, что у юзера {callback.from_user.id} есть хотя бы 1 генерация")
        if gens > 0:
            sex = await AsyncORM.get_sex(callback.from_user.id)
            print(f"Предлагаем юзеру {callback.from_user.id} выбрать профессию\nВыбран пол {sex}")
            if sex != "man":
                await callback.message.edit_text(
                    "Выберите профессию",
                    reply_markup=kb.get_kb_fab_prof()
                )
            else:
                await callback.message.reply(
                    "Выберите профессию",
                    reply_markup=kb.get_kb_fab_prof_m()
                )
        else:
            print(f"У юзера {callback.from_user.id} закончились генерации")
            await callback.answer(text="У вас закончились бесплатные генерации",
                                  show_alert=True)
            print("Предлагаем купить генерации")
            await callback.message.answer(text="Можете приобрести генерации!",
                                          reply_markup=kb.get_kb_fab_prices())
    else:
        await callback.message.answer(
            text="Чтобы ознакомиться с возможностями нашего бота, подпишись на канал @haappymom\n\n"
                 "После подписки нажмите /create_image"
        )


# Этот хэндлер будет срабатывать, если отправлено фото
# и переводить в состояние выбора образования
@dp.message(StateFilter(FSMFillForm.upload_photo), F.photo[-1].as_('largest_photo'))
async def process_photo(message: Message,
                        state: FSMContext,
                        largest_photo: PhotoSize,
                        bot: Bot):
    user_id = message.from_user.id
    # Cохраняем данные фото (file_unique_id и file_id) в хранилище
    # по ключам "photo_unique_id" и "photo_id"
    user_channel_status = await bot.get_chat_member(chat_id=-1001711057486, user_id=message.from_user.id)
    print(user_channel_status.status)
    if user_channel_status.status != ChatMemberStatus.LEFT:
        gens = await AsyncORM.get_gens(message.from_user.id)
        print(f"Проверяем, что у юзера {message.from_user.id} есть хотя бы 1 генерация")
        if gens > 0:
            await state.update_data(
                photo_unique_id=largest_photo.file_unique_id,
                photo_id=largest_photo.file_id
            )
            await state.clear()
            print(f"Загружаем фото юзера {message.from_user.id}")
            await bot.download(
                message.photo[-1],
                destination=f"images/{user_id}.jpeg"
            )
            await message.reply(
                text="Выберите пол",
                reply_markup=kb.get_kb_fab_sex()
            )
        else:
            print(f"У юзера закончились {message.from_user.id} генерации")
            await message.answer(text="У вас закончились бесплатные генерации.\n\nМожете приобрести их!",
                                 reply_markup=kb.get_kb_fab_prices())
    else:
        await message.answer(
            text="Чтобы ознакомиться с возможностями нашего бота, подпишись на канал @haappymom\n\n"
                 "После подписки нажмите /create_image"
        )


# Этот хэндлер будет срабатывать, если во время отправки фото
# будет введено/отправлено что-то некорректное
@dp.message(StateFilter(FSMFillForm.upload_photo))
async def warning_not_photo(message: Message):
    print(f"Ловим юзера {message.from_user.id} на невалидных данных")
    await message.answer(
        text='Пожалуйста, загрузите чёткое фото, на котором хорошо видно лицо'
    )


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'man' или 'woman'
@dp.callback_query(kb.ChoiceCallbackFactory.filter(F.choice == "sex"))
async def process_sex_buttons(callback: CallbackQuery,
                              callback_data: kb.ChoiceCallbackFactory,
                              bot: Bot):
    print(f"Добавляем юзеру {callback.from_user.id} пол в бд")
    await AsyncORM.add_sex(callback.from_user.id, callback_data.value)
    user_channel_status = await bot.get_chat_member(chat_id=-1001711057486, user_id=callback.from_user.id)
    print(user_channel_status.status)
    if user_channel_status.status != ChatMemberStatus.LEFT:
        gens = await AsyncORM.get_gens(callback.from_user.id)
        print(f"Проверяем, что у юзера {callback.from_user.id} есть хотя бы 1 генерация")
        if gens > 0:
            print(f"Предлагаем юзеру {callback.from_user.id} выбрать возраст")
            if callback.message.text != "Выберите возраст":
                await callback.message.edit_text(
                    "Выберите возраст",
                    reply_markup=kb.get_kb_fab_age()
                )
            await callback.answer()
        else:
            print(f"У юзера {callback.from_user.id} закончились генерации")
            await callback.answer(text="У вас закончились бесплатные генерации",
                                  show_alert=True)
            print("Предлагаем купить генерации")
            await callback.message.answer(text="Можете приобрести генерации!",
                                          reply_markup=kb.get_kb_fab_prices())
    else:
        await callback.message.answer(
            text="Чтобы ознакомиться с возможностями нашего бота, подпишись на канал @haappymom\n\n"
                 "После подписки нажмите /create_image"
        )


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data профессий
@dp.callback_query(kb.ChoiceCallbackFactory.filter(F.choice == "prof"))
async def process_prof_buttons(callback: CallbackQuery,
                               callback_data: kb.ChoiceCallbackFactory,
                               bot: Bot,
                               state: FSMContext):
    print(f"Добавляем юзеру {callback.from_user.id} профессию в бд")
    await AsyncORM.add_prof(callback.from_user.id, callback_data.value)
    user_channel_status = await bot.get_chat_member(chat_id=-1001711057486, user_id=callback.from_user.id)
    print(user_channel_status.status)
    if user_channel_status.status != ChatMemberStatus.LEFT:
        gens = await AsyncORM.get_gens(callback.from_user.id)
        print(f"Проверяем, что у юзера {callback.from_user.id} есть хотя бы 1 генерация")
        if gens > 0:
            if os.path.exists(f"images/{callback.from_user.id}.jpeg"):
                print(f"Выводим юзеру {callback.from_user.id} сообщение о генерации")
                # меняем сообщение
                await callback.message.edit_text(
                    "Идет генерация..."
                )

                print(f"Выгружаем профессию и пол юзера {callback.from_user.id} из бд")
                users = await AsyncORM.get_sex_prof(callback.from_user.id)

                user_id = str(callback.from_user.id)
                check_rate = await AsyncORM.check_rate(callback.from_user.id)

                print(f"Генерация фото профессии юзера {callback.from_user.id}")
                # генерация фото профессии
                gen_s = await ai_gen_photo(user_id, users[0],
                                           users[1])
                swap_s = False
                if gen_s:
                    print(f"Свап фото для юзера {callback.from_user.id}")
                    # свап лицами
                    swap_s = await ai_swap_photo(user_id, f"images/{user_id}.jpeg",
                                                 f"images/{user_id}_prof.jpeg")
                if swap_s and gen_s:
                    if not check_rate:
                        print(f"Генерация водяного знака для юзера {callback.from_user.id}")
                        # ДОБАВЛЕНИЕ ВОДЯНОГО ЗНАКА
                        await watermark_text(f"images/{user_id}_res.jpeg", f"images/{user_id}_res_w.jpeg",
                                             text='HappyMom')
                        print(f"Отправка фото юзеру {callback.from_user.id}")
                        # отправляем фото
                        image_from_pc = FSInputFile(f"images/{user_id}_res_w.jpeg")

                        kb_ = InlineKeyboardMarkup(
                            inline_keyboard=[[kb.without_watermark],
                                             [kb.gen_repit]]
                        )

                    else:
                        print(f"Отправка фото юзеру {callback.from_user.id} без водяного знака")
                        # отправляем фото
                        image_from_pc = FSInputFile(f"images/{user_id}_res.jpeg")

                        kb_ = InlineKeyboardMarkup(
                            inline_keyboard=[[kb.buy_more],
                                             [kb.gen_repit]]
                        )
                    await callback.message.delete()
                    await callback.message.answer_photo(
                        image_from_pc,
                        caption="Бот создан при поддержке @haappymom",
                        reply_markup=kb_
                    )
                    print(f"Удаление фото")
                    # удаление фото
                    os.remove(f"images/{user_id}_prof.jpeg")
                    os.remove(f"images/{user_id}_res.jpeg")
                    os.remove(f"images/{user_id}.jpeg")
                    if not check_rate:
                        os.remove(f"images/{user_id}_res_w.jpeg")
                    print(f"Вычитаем юзеру {callback.from_user.id} 1 генерацию")
                    # вычитаем кол-во генераций у каждого пользователя
                    await AsyncORM.sub_gens(callback.from_user.id)
                else:
                    print(f"Генерация фото не прозошла")
                    await callback.message.answer(f"Что-то пошло не так с генерацией...\nПопробуйте позже")
            else:
                print(f"Предлагаем юзеру {callback.from_user.id} загрузить фото")
                await callback.message.answer(
                    "Загрузите чёткое фото, на котором хорошо видно лицо"
                )
                await state.set_state(FSMFillForm.upload_photo)
        else:
            print(f"У юзера {callback.from_user.id} закончились генерации")
            await callback.answer(text="У вас закончились бесплатные генерации",
                                  show_alert=True)
            print("Предлагаем купить генерации")
            await callback.message.answer(text="Можете приобрести генерации!",
                                          reply_markup=kb.get_kb_fab_prices())

    else:
        await callback.message.answer(
            text="Чтобы ознакомиться с возможностями нашего бота, подпишись на канал @haappymom\n\n"
                 "После подписки нажмите /create_image"
        )


@dp.callback_query(F.data == "without_watermark")
async def process_without_watermark(callback: CallbackQuery):
    print(f"Вывод информации для приобритения генераций")
    await callback.message.answer(text="Можете приобрести генерации!",
                                  reply_markup=kb.get_kb_fab_prices())


@dp.callback_query(F.data == "buy_repit")
async def process_without_watermark(callback: CallbackQuery):
    print(f"Вывод информации для приобритения генераций")
    await callback.message.answer(text="Можете приобрести генерации!",
                                  reply_markup=kb.get_kb_fab_prices())


@dp.callback_query(kb.PaymentCallbackFactory.filter(F.choice == "payment"))
async def confirm(callback: CallbackQuery, callback_data: kb.PaymentCallbackFactory):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Подтверждаю", callback_data=kb.PaymentCallbackFactory(choice="confirm",
                                                                    value_gen=callback_data.value_gen,
                                                                    value_price=callback_data.value_price)
    )
    builder.adjust(1)
    await callback.message.edit_text(
        text="Приобретая продукт, Вы соглашаетесь с тем, что разработчик не несет ответственности за результат "
             "сгенерированной фотографии. Ответственность за фотогенерацию лежит исключительно "
             "на искусственном интеллекте, и конечный результат зависит от его функциональных возможностей и процессов,"
             " на которые разработчик не имеет влияния.",
        reply_markup=builder.as_markup()
    )


@dp.callback_query(kb.PaymentCallbackFactory.filter(F.choice == "confirm"))
async def order(callback: CallbackQuery, callback_data: kb.PaymentCallbackFactory, bot: Bot):
    print(f"Вывод информации для оплаты генераций")
    await callback.message.edit_text("Отличный выбор!\n"
                                     "Приобретайте генерации прямо сейчас.\n"
                                     f"Цена: <b>{callback_data.value_price}₽ за {callback_data.value_gen} генераций!</b>\n"
                                     )
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title='Телеграм бот для генерации фото',
        description='Оплата дополнительных генераций',
        payload='Оплата генераций через бота',
        provider_token=config.payments_token.get_secret_value(),
        currency='RUB',
        prices=[
            LabeledPrice(
                label='Оплатить генерации',
                amount=int(callback_data.value_price) * 100
            ),
        ],
        start_parameter='oswyndel',
        provider_data=None,
        photo_url=None,
        photo_size=None,
        photo_width=None,
        photo_height=None,
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        protect_content=True,
        request_timeout=5
    )


@dp.pre_checkout_query()
async def checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message, state: FSMContext, bot: Bot):
    print(f"Оплата прошла успешно")
    print(f"Устанвливаем у юзера {message.from_user.id} флаг оплачено")
    await AsyncORM.update_rate(message.chat.id, True)
    if message.successful_payment.total_amount == 9900:
        gens = 5
    elif message.successful_payment.total_amount == 19900:
        gens = 12
    else:
        gens = 20
    print(f"Добавляем юзеру {message.from_user.id} +{gens} генераций")
    await AsyncORM.add_gens(message.from_user.id, gens)
    await message.answer("Спасибо за оплату! С Вашего счёта было списано "
                         f"{message.successful_payment.total_amount // 100} {message.successful_payment.currency}.\n\n"
                         f"Вам добавлено {gens} генераций")
    user_channel_status = await bot.get_chat_member(chat_id=-1001711057486, user_id=message.from_user.id)
    print(user_channel_status.status)
    if user_channel_status.status == ChatMemberStatus.LEFT:
        await message.answer(
            text="Чтобы ознакомиться с возможностями нашего бота, подпишись на канал @haappymom\n\n"
                 "После подписки нажмите /create_image"
        )
    else:
        gens = await AsyncORM.get_gens(message.from_user.id)
        print(f"Проверяем, что у юзера {message.from_user.id} есть хотя бы 1 генерация")
        if gens > 0:
            await message.answer(
                "Загрузите чёткое фото, на котором хорошо видно лицо"
            )
            await state.set_state(FSMFillForm.upload_photo)
        else:
            print(f"У юзера закончились {message.from_user.id} генерации")
            await message.answer(text="У вас закончились бесплатные генерации.\n\nМожете приобрести их!",
                                 reply_markup=kb.get_kb_fab_prices())


@dp.message(Command(commands='help'))
async def process_help_command(message: Message, state: FSMContext, bot: Bot):
    print(f"Юзер {message.from_user.id} нажал /help ")
    await message.answer(
        "<b>Вы когда-нибудь представляли своего ребенка пожарным, ученым, врачом или даже президентом?</b>\n\n"
        "<i>Наш инновационный бот может воплотить это воображение в реальность!</i> ✨\n\n\n"
        "Просто <b>загрузите фотографию</b> 📸 и посмотрите, как бы выглядели Вы или Ваш ребёнок"
        " в роли представителя любой профессии!\n\n"
        "<i>Исследуйте мир современных возможностей – от врача и инженера до ученого,"
        " спортсмена или светской львицы!</i> 👨‍⚕️💃"
    )
    print(f"Добавляем юзера {message.from_user.id} в бд")
    await AsyncORM.add_user_id(message.from_user.id, message.from_user.username)
    user_channel_status = await bot.get_chat_member(chat_id=-1001711057486, user_id=message.from_user.id)
    print(user_channel_status.status)
    if user_channel_status.status == ChatMemberStatus.LEFT:
        await message.answer(
            text="Чтобы ознакомиться с возможностями нашего бота, подпишись на канал @haappymom\n\n"
                 "После подписки нажмите /create_image"
        )
    else:
        gens = await AsyncORM.get_gens(message.from_user.id)
        print(f"Проверяем, что у юзера {message.from_user.id} есть хотя бы 1 генерация")
        if gens > 0:
            await message.answer(
                "Загрузите чёткое фото, на котором хорошо видно лицо"
            )
            await state.set_state(FSMFillForm.upload_photo)
        else:
            print(f"У юзера закончились {message.from_user.id} генерации")
            await message.answer(text="У вас закончились бесплатные генерации.\n\nМожете приобрести их!",
                                 reply_markup=kb.get_kb_fab_prices())
