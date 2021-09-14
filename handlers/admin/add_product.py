from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from markups import admin_markups
from states import AddProduct
from loader import dp, bot, shopDB
from aiogram import types
from utils.admin_utils import notify_subs


@dp.callback_query_handler(text='add_product')
async def add_product(query: types.CallbackQuery):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await bot.send_message(query.from_user.id,
                           text='Укажите название товара.',
                           reply_markup=admin_markups.cancel_adding_product
                           )
    await AddProduct.name.set()


@dp.message_handler(state=AddProduct.name)
async def set_name(message: types.Message, state: FSMContext):
    await message.answer(
        text='<b>Название товара:</b> "{0}"\n\n'
             'Теперь введите описание товара.'.format(message.text),
        reply_markup=admin_markups.cancel_adding_product
    )
    await AddProduct.description.set()
    await state.update_data(name=message.text)


@dp.message_handler(state=AddProduct.description)
async def set_description(message: types.Message, state: FSMContext):
    await message.answer(text='<b>Описание товара:</b>\n\n{0}\n\n'
                              'Введите кол-во товара на складе.'.format(message.text),
                         reply_markup=admin_markups.cancel_adding_product
                         )
    await AddProduct.count.set()
    await state.update_data(description=message.text)


@dp.message_handler(state=AddProduct.count)
async def set_count(message: types.Message, state: FSMContext):
    await message.answer(text='<b>Кол-во товара: </b>{0}\n\n'
                              'Цена за единицу товара?'.format(message.text),
                         reply_markup=admin_markups.cancel_adding_product
                         )
    await AddProduct.price.set()
    await state.update_data(count=message.text)


@dp.message_handler(state=AddProduct.price)
async def set_price(message: types.Message, state: FSMContext):
    await message.answer(text='<b>Цена за единицу товара</b>: {0}\n\n'
                              'Отправьте фото товара документом.'.format(message.text),
                         reply_markup=admin_markups.cancel_adding_product
                         )
    await AddProduct.photo.set()
    await state.update_data(price=message.text)


@dp.message_handler(content_types='document', state=AddProduct.photo)
async def set_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = (
        "<b>{0}</b>\n\n{1}\n\n<b>На складе, ед: </b>{2}\n\n<b>Цена "
        "товара, ₽: </b>{3}".format(
            data['name'], data['description'], data['count'], data['price']))
    await bot.send_document(
        chat_id=message.from_user.id,
        document=message.document.file_id,
        caption=text,
        reply_markup=admin_markups.confirm_adding_product
    )
    await AddProduct.confirm_product.set()
    await state.update_data(photo_id=message.document.file_id)


@dp.callback_query_handler(text="confirm_adding_product",
                           state=AddProduct.confirm_product)
async def confirm_product(query: CallbackQuery, state: FSMContext):
    if query.data.startswith('confirm'):
        data = await state.get_data()
        await shopDB.add_product(
            product_name=data['name'],
            product_description=data['description'],
            product_count=data['count'],
            product_price=data['price'],
            product_photo=data['photo_id']
        )
        await bot.send_message(query.from_user.id,
                               "Товар успешно добавлен!",
                               reply_markup=admin_markups.notify_about_product
                               )
        await AddProduct.notify_about_product.set()

    await bot.delete_message(query.message.chat.id, query.message.message_id)


@dp.callback_query_handler(text="cancel_adding_product", state = AddProduct.states)
async def cancel_adding_product(query: CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await bot.send_message(query.from_user.id, 'Действие отменено!')
    await state.reset_state()


@dp.callback_query_handler(lambda call: 'notify' in call.data, state=AddProduct.notify_about_product)
async def notify_about_product(query: CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    if query.data.startswith('notify'):
        data = await state.get_data()
        await notify_subs(dp, data)
        await bot.send_message(query.from_user.id, "Информация о новом товаре успешно отправлена подписчикам!")
    else:
        await bot.send_message(query.from_user.id, 'Информация о новом товаре не была отправлена подписчикам!')

    await state.reset_state()

