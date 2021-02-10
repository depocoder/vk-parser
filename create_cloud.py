import os
import collections
import re

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import requests


def get_posts(vk_token, owner_id):
    params = {
        'v': '5.52',
        'access_token': vk_token,
    }

    if owner_id.startswith('club'):
        owner_id = owner_id.split('club')[-1]
        params['owner_id'] = f'-{owner_id}'
    if owner_id.startswith('public'):
        owner_id = owner_id.split('public')[-1]
        params['owner_id'] = f'-{owner_id}'
    else:
        params['domain'] = owner_id

    response = requests.get(
        url='https://api.vk.com/method/wall.get',
        params=params)
    return response.json()


def parse_hashtags(response):
    posts = response['response']['items']
    hashtags = collections.Counter()
    post_texts = []
    for post in posts:
        text = post.get('text')

        if not text:
            continue
        for tag in re.findall(r'[#@][^\s#@]+', text):
            hashtags[tag.lower()] += 1
            post_texts.append(text)

    return hashtags, post_texts


def create_cloud(group_id):
    vk_token = os.getenv('VK_TOKEN')

    response = get_posts(vk_token, group_id)

    error = response.get('error')
    if error:
        return {"error": error['error_msg']}
    if not response['response']['items']:
        return {"error": 'Ошибка на строне VK'}

    hashtags, post_texts = parse_hashtags(response)

    wc = WordCloud(
        width=2600, height=2200,
        background_color="white", relative_scaling=1.0,
        collocations=False, min_font_size=10).generate_from_frequencies(dict(hashtags))

    plt.switch_backend('Agg')
    plt.axis("off")
    plt.figure(figsize=(9, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.title(f'tag cloud {group_id}')
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    filename = os.path.join(f"{group_id}.png")
    path = os.path.join(os.getcwd(), 'static/images/', filename)
    plt.savefig(path)
    return {"post_texts": post_texts}


if __name__ == "__main__":
    create_cloud()
