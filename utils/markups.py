from telebot import types

def category_markup(portal_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
    btn1 = types.KeyboardButton(f'/news {portal_id}')
    btn2 = types.KeyboardButton(f'/entertainment {portal_id}')
    btn3 = types.KeyboardButton(f'/sports {portal_id}')
    btn4 = types.KeyboardButton(f'/business {portal_id}')
    btn5 = types.KeyboardButton(f'/opinion {portal_id}')
    btn6 = types.KeyboardButton('/close')
    btn7 = types.KeyboardButton('/portals')

    if portal_id == '(G)':
        markup.row(btn1, btn2)
        markup.row(btn3, btn4, btn6)
        markup.row(btn7)
    else:
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.row(btn5, btn6)
        markup.row(btn7)
    return markup