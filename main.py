import requests
from dotenv import load_dotenv
import os
import random

API_VERSION = 5.122
VK_URL = 'https://api.vk.com/method/'
GROUP_ID = 198065570


def fetch_comic(comic_num):
    response = requests.get('http://xkcd.com/{}/info.0.json'.format(comic_num))
    response.raise_for_status()
    return response.json()


def fetch_image(url, name, resolution):
    response = requests.get(url)
    response.raise_for_status()
    with open('{}.{}'.format(name, resolution), 'wb') as file:
        file.write(response.content)


def get_vk_groups_list(token):
    params = {'access_token': token, 'v': API_VERSION}
    response = requests.get('{}groups.get'.format(VK_URL), params=params)
    response.raise_for_status()
    return response.json()


def get_server_to_upload_image(token, group_id):
    params = {'group_id': group_id, 'access_token': token, 'v': API_VERSION}
    response = requests.get('{}photos.getWallUploadServer/'.format(VK_URL), params=params)
    response.raise_for_status()
    return response.json()


def upload_photo_to_server_to_wall(file_name, upload_uri):
    with open('/home/dmitriy/Desktop/projects/vk/{}'.format(file_name), 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_uri, files=files)
        response.raise_for_status()
    return response.json()


def upload_photo_to_wall(server_num, photo_url, hash_num, token):
    params = {
        'group_id': GROUP_ID,
        'photo': photo_url,
        'server': server_num,
        'hash': hash_num,
        'access_token': token,
        'v': API_VERSION,
    }
    response = requests.post('{}photos.saveWallPhoto?'.format(VK_URL), data=params)
    response.raise_for_status()
    return response.json()


def post_photo_to_wall(owner_id, media_id, description, token):
    params = {
        'owner_id': f'-{GROUP_ID}',
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}',
        'message': description,
        'access_token': token,
        'v': API_VERSION,
    }
    response = requests.post('{}wall.post?'.format(VK_URL), data=params)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    last_comic = fetch_comic('')['num']
    comic_id = random.randint(0, last_comic)
    comic_json = fetch_comic(comic_id)
    fetch_image(comic_json['img'], 'meme', 'png')
    comic_description = comic_json['alt']
    load_dotenv()
    vk_key = os.getenv('VK_TOKEN')
    upload_url = get_server_to_upload_image(vk_key, GROUP_ID)['response']['upload_url']
    on_server_photo = upload_photo_to_server_to_wall('meme.png', upload_url)
    try:
        os.remove('meme.png')
    except Exception:
        print('error, please retry later')
    finally:
        os.remove('meme.png')
    server, photo, hash_id = on_server_photo['server'], on_server_photo['photo'], on_server_photo['hash']
    uploaded_photo = upload_photo_to_wall(server, photo, hash_id, vk_key)
    upload_media_id = uploaded_photo['response'][0]['id']
    upload_owner_id = uploaded_photo['response'][0]['owner_id']
    post_photo_to_wall(upload_owner_id, upload_media_id, comic_description, vk_key)
