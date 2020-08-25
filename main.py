import requests
from dotenv import load_dotenv
import os
import random


API_VERSION = 5.122
VK_URL = 'https://api.vk.com/method/'
GROUP_ID = 198065570


def fetch_comic(id):
    response = requests.get('http://xkcd.com/{}/info.0.json'.format(id))
    python_meme = response.json()
    return python_meme


def fetch_image(url, name, format):
    response = requests.get(url)
    response.raise_for_status()
    with open('{}.{}'.format(name, format), 'wb') as file:
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


def upload_photo_to_wall(server, photo, hash):
    params = {
        'group_id': GROUP_ID,
        'photo': photo,
        'server': server,
        'hash': hash,
        'access_token': VK_KEY,
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
    comic_url = fetch_comic(comic_id)['img']
    fetch_image(comic_url, 'meme', 'png')
    comic_description = fetch_comic(comic_id)['alt']
    load_dotenv()
    VK_KEY = os.getenv('TOKEN')
    upload_url = get_server_to_upload_image(VK_KEY, GROUP_ID)['response']['upload_url']
    on_server_photo = upload_photo_to_server_to_wall('meme.png', upload_url)
    os.remove('meme.png')
    server, photo, hash = on_server_photo['server'], on_server_photo['photo'], on_server_photo['hash']
    uploaded_photo = upload_photo_to_wall(server, photo, hash)
    upload_media_id = uploaded_photo['response'][0]['id']
    upload_owner_id = uploaded_photo['response'][0]['owner_id']
    post_photo_to_wall(upload_owner_id, upload_media_id, comic_description, VK_KEY)
