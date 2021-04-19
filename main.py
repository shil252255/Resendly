import json
from telethon import TelegramClient, events
from settings import API_ID, API_HASH, SESSION_NAME, FROM_CHAT_NAME, TO_CHAT_NAME

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
client.start()


def save_log(date_of_mess: str, mess: str, chat_name: str):
    """Сохранение сообщений с меткой времени в json файле"""
    save_mes = {'date': date_of_mess, 'message': mess}
    file_name = chat_name + '.log'
    with open(file_name, 'a', encoding='utf-8') as all_mes_file:
        json.dump(save_mes, all_mes_file, ensure_ascii=False, indent=4)


def get_channel_id_dict() -> dict:
    """Возвращает словарь id по названия каналов на которые подписан пользователь"""
    ch_dict = {}
    for dialog in client.iter_dialogs():
        id_dict = dialog.message.peer_id.__dict__
        if 'channel_id' in id_dict:
            ch_dict[dialog.title] = str(id_dict['channel_id'])
    return ch_dict


def get_values(d: dict, k: str) -> str:
    """возвращает имя канала по его id"""
    answer = ''
    for key in d:
        if d[key] == k:
            answer = key
    return answer


def event_data_extractor(event):
    """Извлекает все необходимые данные из события
    :rtype: str: имя канала, str: дата получения сообщения, str: текст сообщения"""
    channel_id = str(event.message.peer_id.channel_id)
    channel_name = get_values(channel_dict, channel_id)
    mess = event.message.message
    date_of_mess = event.message.date.strftime("%d.%m.%Y %H:%M")
    return channel_name, date_of_mess, mess


def resend_channel(ch_name: str):
    """
    :param ch_name: название чата откуда пришло сообщение
    :return ch_name_to_send: чат куда отправить сообщение
    """
    if len(FROM_CHAT_NAME) != len(TO_CHAT_NAME):
        return False
    return TO_CHAT_NAME[FROM_CHAT_NAME.index(ch_name)]


@client.on(events.NewMessage(chats=FROM_CHAT_NAME))
async def normal_handler(event):
    channel_name, date_of_mess, mess = event_data_extractor(event)
    send_mess = date_of_mess + '\n' + mess
    save_log(date_of_mess, mess, channel_name)
    await client.send_message(resend_channel(channel_name), send_mess)


if __name__ == '__main__':
    channel_dict = get_channel_id_dict()
    print('Ready!')
    client.run_until_disconnected()
