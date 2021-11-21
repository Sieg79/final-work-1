import requests
from pprint import pprint
import time
import sys
import datetime


class VkAccess:
    url = 'https://api.vk.com/method/'

    def __init__(self, vk_token, version='5.131'):
        self.params = {'access_token': vk_token, 'v': version}

    def album_selection(self, user_id):
        get_albums_url = self.url + 'photos.getAlbums'
        get_albums_params = {'user_id': user_id}
        albums_res = requests.get(get_albums_url, params={**self.params, **get_albums_params})
        albums = (albums_res.json()['response']['items'])
        albums_list = {'стена': 'wall', 'профиль': 'profile'}
        for album in albums:
            title = album.get('title', 0)
            if title == 0:
                pass
            else:
                albums_list[title] = album['id']
        i = 0
        for album in albums_list:
            i += 1
            print(f'альбом {album} - введите {i}')
        selected_album = int(input('выберите альбом:'))
        if selected_album > i:
            print('выбор не корректен')
            sys.exit()
        else:
            selected_album_id = list(albums_list.values())[selected_album - 1]
            return selected_album_id

    def get_photos(self, album_id):
        get_photos_url = self.url + 'photos.get'
        q = int(input('Введите количество фото для загрузки:'))
        get_photos_params = {'user_id': user_id, 'album_id': album_id, 'extended': 1, 'count': q, 'rev': '1'}
        photos_res = requests.get(get_photos_url, params={**self.params, **get_photos_params})
        photos = photos_res.json()['response']['items']
        photos_list = []
        likes_count = []
        i = 0
        for photo in photos:
            if str(photo['likes']['count']) in likes_count:
                dt = photo['date']
                date = datetime.datetime.fromtimestamp(dt)
                r_date = date.strftime('%H ч %M м %m.%d.%Y года')
                name = (str(photo['likes']['count']) + 'L  ' + str(r_date))
                likes_count.append(name)
            else:
                name = str(photo['likes']['count'])
                likes_count.append(name)
            sizes = photo['sizes']
            photos_list_record = {'file name': likes_count[i], 'size': sizes[-1]['type'], 'url': sizes[-1]['url']}
            photos_list.append(photos_list_record)
            i += 1
        return photos_list

    def folder_name(self, user_id):
        folder_name_url = self.url + 'users.get'
        folder_name_params = {'user_ids': user_id, 'name_case': 'nom'}
        folder_name_res = requests.get(folder_name_url, params={**self.params, **folder_name_params})
        folder_name_list = folder_name_res.json()['response']
        folder_name = folder_name_list[0]['first_name'] + ' ' + folder_name_list[0]['last_name']
        return folder_name


class YaUploader:
    def __init__(self, ya_token: str):
        self.ya_token = ya_token
        self.url = 'https://cloud-api.yandex.net/v1/disk/'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth ' + self.ya_token}

    def folders_list(self):
        url = self.url + 'resources'
        

    def create_folder(self, path):
        headers = self.headers
        folder_params = {'path': '/'}
        folder_res = requests.get(self.url + 'resources', headers=headers, params=folder_params)
        folders_responce = folder_res.json()['_embedded']['items']
        folders_list = []
        for folder in folders_responce:
            folder_name = folder['name']
            folders_list.append(folder_name)
        if path in folders_list:
            pass
        else:
            params = {'path': path}
            url = self.url + 'resources'
            response = requests.put(url, headers=headers, params=params)
            response.raise_for_status()
            if response.status_code == 201:
                print(f'Папка {path} создана')

    def upload_vk_to_ya(self):
        upload_url = self.url + 'resources/upload'
        headers = self.headers
        album_id = vk.album_selection(user_id)
        photos = vk.get_photos(album_id)
        folder_name = vk.folder_name(user_id)
        folder = ya.create_folder(folder_name)

        for photo in photos:
            url = photo['url']
            file_path = folder_name + '/' + photo['file name'] + '.jpg'
            params = {'url': url, 'path': file_path, 'disable_redirects': 'true'}
            response = requests.post(upload_url, headers=headers, params=params)
            response.raise_for_status()
            if response.status_code == 202:
                photo_name = photo['file name']
                print(f'фото {photo_name} загружено')


if __name__ == '__main__':

    vk_token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    user_id = '185505817'
    vk = VkAccess(vk_token)
    ya_token = ')(&*^*&%^$&%^#%$@'
    ya = YaUploader(ya_token)
    res = ya.upload_vk_to_ya()
