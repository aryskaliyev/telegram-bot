# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    randoum_bot.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aryskali <aryskaliyev@nu.edu.kz>           +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/01/01 14:43:13 by aryskali          #+#    #+#              #
#    Updated: 2020/04/01 15:13:14 by aryskali         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
#To run the code type: python3 randoum_bot.py

from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import ParseMode
from bs4 import BeautifulSoup
import html
import urllib.request
import re

class JobInfo:
    def __init__(self, job_title="No title", job_location="No location", job_close_date="No date", job_link="No link"):
        self.job_title = job_title
        self.job_location = job_location
        self.job_close_date = job_close_date
        self.job_link = job_link

    def print_self(self):
        print (self.job_title)
        print (self.job_location)
        print (self.job_close_date)
        print (self.job_link)

def print_arr(arr):
    for ind in arr:
        print(ind)

def print_obj_arr(arr):
    for ind in arr:
        ind.print_self()

def create_link(string):
    l_prefix = "tengizchevroil.amris.com/wizards_v2/tengiz/vacancyView.php?requirementId="
    return l_prefix + str(string)

def get_url():
    val = []
    response = urllib.request.urlopen("http://www.tengizchevroil.com/en/careers/openjobs")
    soup = BeautifulSoup(response)
    for iframe in soup.find_all('iframe'):
        link = urllib.request.urlopen(iframe.attrs['src'])
        ans = BeautifulSoup(link)
        for res in ans.find_all('td'):
            val.append(res)
    return val
    
def get_title(string):
    pattern = '>(.+)<'
    return re.findall(pattern, str(string))

def get_string(string):
    pattern = '<td valign="middle">(.+)</td>'
    return re.findall(pattern, str(string))

def get_ref(string):
    pattern = '\d{4}'
    return re.search(pattern, str(string))

def get_arr_obj(arr):
    res = []
    tmp = JobInfo()
    for ind in range(0, len(arr) - 2, 3):
        tmp = JobInfo(get_title(get_title(arr[ind])), get_string(arr[ind + 2]), get_string(arr[ind + 1]), create_link(str(get_ref(arr[ind]).group())))
        res.append(tmp)
    return (res)

def bop(bot, update):
    arr = get_url()
    arr2 = get_arr_obj(arr)
    chat_id = update.message.chat_id
    job_title_prefix = "<b>Job Title: </b>"
    job_link_prefix = "<b>Link: </b>"
    job_location_prefix = "<b>Location: </b>"
    job_closedate_prefix = "<b>Close date: </b>"
    el_item = "Sorry, no available positions yet."
    for ind in arr2:
        tmp_job_title = job_title_prefix + html.unescape(str(ind.job_title)[1:-1]).replace("'", "") + '\n'
        tmp_job_link = str(ind.job_link)
        tmp_job_location = job_location_prefix + str(ind.job_location)[1:-1].replace("'", "") + '\n'
        tmp_close_date = job_closedate_prefix + str(ind.job_close_date)[1:-1].replace("'", "") + '\n'
        el_item = tmp_job_title + tmp_job_location + tmp_close_date + tmp_job_link
        bot.send_message(chat_id=chat_id, text=el_item, parse_mode=ParseMode.HTML)

def main():
    updater = Updater("hashcode")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop', bop))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
