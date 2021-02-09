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

    if owner_id.isdigit():
        params['owner_id'] = owner_id
    else:
        params['domain'] = owner_id

    response = requests.get(
        url='https://api.vk.com/method/wall.get',
        params=params)

    return response.json()


def parse_hastags(response):
    posts = response['response']['items']
    hashtags = collections.Counter()
    for post in posts:
        text = post.get('text')

        if not text:
            continue
        for tag in re.findall(r'[#@][^\s#@]+', text):
            hashtags[tag.lower()] += 1

    return hashtags


def create_cloud(group_id):
    vk_token = os.getenv('VK_TOKEN')

    response = get_posts(vk_token, group_id)
    hastags = parse_hastags(response)

    wc = WordCloud(
        width=2600, height=2200,
        background_color="white", relative_scaling=1.0,
        collocations=False, min_font_size=10).generate_from_frequencies(dict(hastags))

    plt.switch_backend('Agg')
    plt.axis("off")
    plt.figure(figsize=(9, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.title(f'tag cloud {group_id}')
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    filename = f"{group_id}.png"
    path = os.path.join(os.getcwd(), 'static/images/', filename)
    plt.savefig(path)


if __name__ == "__main__":
    create_cloud()

    # error = posts.get('error')
    # if error:
    # TODO типа кастомная проверка потом
