from aiogram import executor

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, skip_updates=True)


