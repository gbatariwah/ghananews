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
    btn8 = types.KeyboardButton(f'/politics {portal_id}')
    btn9 = types.KeyboardButton(f'/showbiz {portal_id}')
    btn10 = types.KeyboardButton(f'/local {portal_id}')

    if portal_id == '(G)':
        markup.row(btn1, btn2)
        markup.row(btn3, btn4, btn6)
        markup.row(btn7)
    elif portal_id == '(M)':
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.row(btn5, btn6)
        markup.row(btn7)
    else:
        markup.row(btn10, btn8)
        markup.row(btn9, btn4, btn3)
        markup.row(btn5, btn7, btn6)
    return markup


def portals_markup():
    markup = types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True, selective=False)
    btn1 = types.KeyboardButton('/ghanaweb')
    btn2 = types.KeyboardButton('/myjoyonline')
    btn3 = types.KeyboardButton('/peacefmonline')
    btn4 = types.KeyboardButton('/close')

    markup.row(btn1, btn2)
    markup.row(btn3, btn4)

    return markup