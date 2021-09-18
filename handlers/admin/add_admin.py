from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from states import AddAdmin
from utils.admin_utils import is_user_valid, is_chat_valid
from loader import dp, bot, adminsDB
from markups.admin_markups import cancel_adding_admin, confirm_adding_admin


@dp.callback_query_handler(text="add_admin")
async def add_administrator(query: CallbackQuery):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await bot.send_message(query.from_user.id,
                           "Отправьте id человека, которого нужно сделать админом."
                           " User-id можно узнать здесь @get_any_telegram_id_bot",
                           reply_markup=cancel_adding_admin)
    await AddAdmin.id.set()


@dp.message_handler(state=AddAdmin.id)
async def add_admin_id(message: types.Message, state: FSMContext):
    if is_user_valid(message.text):
        if await is_chat_valid(message.text, dp):
            text = "Введите имя администратора " \
                   "(будет отображаться в списке администраторов)"

            await state.update_data(user_id=message.text)
            await AddAdmin.name.set()
        else:
            text = "Пользователь ни разу не писал боту!"
    else:
        text = "Такого пользователя не существует!"

    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=cancel_adding_admin
    )


@dp.message_handler(state=AddAdmin.name)
async def add_admin_name(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    data = await state.get_data()
    await bot.send_message(message.from_user.id,
                           "Имя администратора: {0}\n\n"
                           "ID администратора: {1}".format(
                               data['user_name'], data['user_id']
                           ), reply_markup=confirm_adding_admin
                           )
    await AddAdmin.confirm.set()


@dp.callback_query_handler(text="confirm_adding_admin", state=AddAdmin.confirm)
async def confirm_adding_administrator(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if await adminsDB.admin_exists(data["user_id"]) is not None:
        text = "Этот администратор уже есть в базе!"
    else:
        await adminsDB.add_admin(data["user_id"], data["user_name"])
        text = "Администратор успешно добавлен!"
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await bot.send_message(query.from_user.id, text)
    await state.reset_state()


@dp.callback_query_handler(text="cancel_adding_admin", state=AddAdmin.states)
async def cancel_adding_administrator(query: CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await bot.send_message(query.from_user.id, 'Действие отменено!')
    await state.reset_state()

