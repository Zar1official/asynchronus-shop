from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from utils.admin_utils import send_products, send_product_back, send_product
from states.admin_states import EditProduct
from loader import dp, bot, shopDB


@dp.callback_query_handler(text="update_product")
async def update_product(query: CallbackQuery):
    await send_products(dp, query.from_user.id)
    await bot.delete_message(query.from_user.id, query.message.message_id)


@dp.callback_query_handler(lambda call: call.data.startswith("remove_product"))
async def remove_product(query: CallbackQuery):
    await shopDB.remove_product(query.data.split('remove_product_')[1])
    await bot.delete_message(query.message.chat.id, query.message.message_id)


@dp.callback_query_handler(lambda call: call.data.startswith("edit_product"))
async def edit_product(query: CallbackQuery):
    product_id = query.data.split('edit_product_')[1]
    await bot.edit_message_caption(query.message.chat.id,
                                   query.message.message_id,
                                   caption="Что нужно изменить?"
                                   )
    await bot.edit_message_reply_markup(
        message_id=query.message.message_id,
        chat_id=query.message.chat.id,
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Название", callback_data="edit_name_" + product_id)
        ).add(
            InlineKeyboardButton("Описание", callback_data="edit_description_" + product_id)
        ).add(
            InlineKeyboardButton("Кол-во товара", callback_data="edit_count_" + product_id)
        ).add(
            InlineKeyboardButton("Цена товара", callback_data="edit_price_" + product_id)
        ).add(
            InlineKeyboardButton("Фото товара", callback_data="edit_photo_" + product_id)
        ).add(
            InlineKeyboardButton("Отмена", callback_data="edit_cancel_" + product_id)
        )
    )
    await EditProduct.edit.set()
    await query.answer()


@dp.callback_query_handler(state=EditProduct.edit)
async def edit_product_choice(query: CallbackQuery, state: FSMContext):
    callback_data = query.data
    product_id = callback_data.split('_')[2]
    await state.update_data(product_id=product_id,
                            message_id=query.message.message_id,
                            chat_id=query.message.chat.id)
    if 'name' in callback_data:
        await bot.edit_message_caption(chat_id=query.message.chat.id,
                                       message_id=query.message.message_id,
                                       caption="Введите новое название."
                                       )
        await EditProduct.name.set()
    elif 'description' in callback_data:
        await bot.edit_message_caption(chat_id=query.message.chat.id,
                                       message_id=query.message.message_id,
                                       caption="Введите новое описание."
                                       )
        await EditProduct.description.set()
    elif 'count' in callback_data:
        await bot.edit_message_caption(chat_id=query.message.chat.id,
                                       message_id=query.message.message_id,
                                       caption="Введите новое кол-во товара на складе."
                                       )
        await EditProduct.count.set()
    elif 'price' in callback_data:
        await bot.edit_message_caption(chat_id=query.message.chat.id,
                                       message_id=query.message.message_id,
                                       caption="Введите новую цену товара."
                                       )
        await EditProduct.price.set()
    elif 'photo' in callback_data:
        await bot.edit_message_caption(chat_id=query.message.chat.id,
                                       message_id=query.message.message_id,
                                       caption="Отправьте новое фото товара документом."
                                       )
        await EditProduct.photo.set()
    else:
        await send_product_back(dp, query.message.chat.id, query.message.message_id, product_id)
        await state.reset_state()
        await query.answer()


@dp.message_handler(state=EditProduct.name)
async def edit_product_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await shopDB.edit_product(data['product_id'], "name", message.text)
    await bot.delete_message(data['chat_id'], data['message_id'])
    await send_product(dp, data['product_id'], message.from_user.id)
    await state.reset_state()


@dp.message_handler(state=EditProduct.description)
async def edit_product_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await shopDB.edit_product(data['product_id'], "description", message.text)
    await bot.delete_message(data['chat_id'], data['message_id'])
    await send_product(dp, data['product_id'], message.from_user.id)
    await state.reset_state()


@dp.message_handler(state=EditProduct.count)
async def edit_product_count(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await shopDB.edit_product(data['product_id'], "count", message.text)
    await bot.delete_message(data['chat_id'], data['message_id'])
    await send_product(dp, data['product_id'], message.from_user.id)
    await state.reset_state()


@dp.message_handler(state=EditProduct.price)
async def edit_product_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await shopDB.edit_product(data['product_id'], "price", message.text)
    await bot.delete_message(data['chat_id'], data['message_id'])
    await send_product(dp, data['product_id'], message.from_user.id)
    await state.reset_state()


@dp.message_handler(state=EditProduct.photo, content_types='document')
async def edit_product_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await shopDB.edit_product(data['product_id'], "photo", message.document.file_id)
    await bot.delete_message(data['chat_id'], data['message_id'])
    await send_product(dp, data['product_id'], message.from_user.id)
    await state.reset_state()
