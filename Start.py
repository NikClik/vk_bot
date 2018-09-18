from vk_api import *
import time
from bs4 import BeautifulSoup
import urllib.request
import json


def search_in_google(search_info):
    query_string = search_info
    url_string = "https://www.google.co.in/search?q={0}&source=lnms&tbm=isch".format(query_string)
    print(url_string)
    browses = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/43.0.2357.134 Safari/537.36"
    }
    return BeautifulSoup(
            urllib.request.urlopen(
                urllib.request.Request(url_string, browses)), 'html.parser')


def links_list(search_info):
    soup = search_in_google(search_info)
    actual_images = []
    for imgs in soup.find_all("div", {"class": "rg_meta"}):
        img_link = json.loads(imgs.text)["ou"]
        actual_images.append(img_link)
    return actual_images


def send_message(user_login, user_password, send_to, sending_message):
    vk = vk_api.VkApi(login=str(user_login), password=str(user_password), scope='messages')
    vk.auth()
    vk.method('messages.send', {'user_id': int(send_to), 'message': str(sending_message)})


def sender_bot():
    user_login = '375445837705'
    user_password = 'VCXZfdsarewq12'
    target_user_id = 88690770
    vk = vk_api.VkApi(login=str(user_login), password=str(user_password), scope='messages')
    vk.auth()
    date_previous_command = 0
    while True:
        values = {'count': 1, 'user_id': target_user_id}
        response = vk.method('messages.getHistory', values)
        for messages in response['items']:
            message = messages.get('text')
            date_now_command = messages.get('date')
            if date_now_command == date_previous_command:
                pass
            else:
                date_previous_command = messages.get('date')
                try:
                    if message[0] == '!':
                        img_links = links_list(message.split('!')[1])
                        # for a in img_links:
                        #     print(a)
                        # vk.method('messages.send', {'user_id': target_user_id, 'message': img_links[0]})
                except IndexError:
                    pass


if __name__ == '__main__':
    sender_bot()
    # links_list('aaa')
