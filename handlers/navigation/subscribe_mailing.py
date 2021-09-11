from loader import dp, bot, subscribeDB
from aiogram import types


@dp.callback_query_handler(lambda c: c.data.endswith('sub'))
async def mailing(query: types.CallbackQuery):
    if query.data == 'sub':
        try:
            await subscribeDB.add_user(query.from_user.id)
            await bot.send_message(query.from_user.id, 'Вы успешно подписались на рассылку!')
        except Exception:
            await bot.send_message(query.from_user.id, 'Ошибка. Вы и так подписаны на рассылку!')
        await bot.delete_message(query.from_user.id, query.message.message_id)
    else:
        try:
            await subscribeDB.delete_user(query.from_user.id)
            await bot.send_message(query.from_user.id, 'Вы успешно отписались от рассылки!')
        except Exception:
            await bot.send_message(query.from_user.id, 'Ошибка. Вы не подписаны на рассылку!')
        await bot.delete_message(query.from_user.id, query.message.message_id)
    await query.answer()
