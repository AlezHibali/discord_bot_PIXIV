import requests
from bs4 import BeautifulSoup
from pixivpy3 import *
from pixivapi import Client
from pixivapi import Size
import io
import re
import os

def handle_response(message, K):
    p_message = message.lower()
    
    if p_message == 'hello':
        return 'Hey there!'
    
    if p_message.startswith('search '):
        # Get the search term from the message
        search_words = p_message[6:]
        out = search_pixiv(search_words=search_words, k = K.value)
        return out
    
    if p_message.startswith('rank '):
        # Get the search term from the message
        arg = p_message[5:]

        if arg in ['day', 'week', 'month', 'day_male', 'day_female', 'week_original',\
                   'week_rookie', 'day_r18', 'day_male_r18', 'day_female_r18',\
                    'week_r18', 'week_r18g']:
            out = rank_pixiv(arg=arg, k = K.value)
        else:
            out = "`Argument should be 'day' or 'week'`"
        return out
    
    if p_message.startswith('setk '):
        # change value of K
        k_val = p_message[5:]

        if k_val.isdigit() and int(k_val) >= 1 and int(k_val) <= 20:
            K.value = int(k_val)
            return "`Output image number changed to {}`".format(k_val)
        return "`Input value should be int ranging 1-20`"

    if p_message == 'help':
        return "List of commands available:\n`/hello\n/search prompt\n/rank [day, week]\n/setk k_value`"

    return '`Try typing "/help" for specific command lines.`'

def search_pixiv(search_words, k = 5):
    # authentification
    api = AppPixivAPI()
    ref_tok = '************************' # <------------------------- REFRESH TOKEN HERE
    try:
        api.auth(refresh_token = ref_tok)
    except Exception as e:
        print('Error during login:', e)

    # Search for illustrations with the given tags
    # Get the top three illustrations from the search results
    search_result = api.search_illust(search_words, search_target='exact_match_for_tags', sort='date_desc')
    top_k = search_result.illusts[:k]

    img_list = []
    # Print information about the top k illustrations
    for item in top_k:
        # Get image data from the illustration URL
        img_name = os.path.basename(item.image_urls['large'])
        link = link_proc(item.image_urls.large)

        try:
            api.download(link, path='./temp', name= img_name)
        except Exception as e:
            print('Error during download:', e)

        # append to output
        img_list.append(os.path.join("./temp/", img_name))

    return img_list

# Remove everything between '.net/' and '/img-master'
def link_proc(url):
    clean_url = re.sub(r'\.net\/.*\/img-master', '.net/img-master', url)
    return clean_url

def rank_pixiv(arg, k = 5):
    # authentification
    api = AppPixivAPI()
    ref_tok = '************************' # <------------------------- REFRESH TOKEN HERE
    try:
        api.auth(refresh_token = ref_tok)
    except Exception as e:
        print('Error during login:', e)

    # Get illustrations of ranking day/week
    # Get the top three illustrations from the ranking
    result = api.illust_ranking(arg)
    top_k = result.illusts[:k]

    img_list = []
    # Print information about the top k illustrations
    for item in top_k:
        # Get image data from the illustration URL
        img_name = os.path.basename(item.image_urls['large'])
        link = link_proc(item.image_urls.large)

        try:
            api.download(link, path='./temp', name= img_name)
        except Exception as e:
            print('Error during download:', e)

        # append to output
        img_list.append(os.path.join("./temp/", img_name))

    return img_list
