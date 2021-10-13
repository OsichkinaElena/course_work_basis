import requests
from pprint import pprint
import time
from tqdm import tqdm
import datetime


def get_id(user_name, token_vk):
    headers = {"Accept": "application/json", "Content-Type": "application/json",
               "Authorization": "OAuth {}".format(token_vk)}
    url = "https://api.vk.com/method/users.get"
    params = {"access_token": token_vk, "v": "5.131", "user_ids": user_name}
    req = requests.get(url, params=params, headers=headers)
    r = req.json()
    id = r["response"][0]["id"]
    return id


def get_token_vk():
    with open("token.txt", encoding="utf-8") as f:
        token_ = f.readline()
        token = token_[3:-1]
    return token


def create_folder(token_yd):
    while True:
        path = input("Введите имя папки на яндекс диске: ")
        headers = {"Accept": "application/json", "Content-Type": "application/json",
                   "Authorization": "OAuth {}".format(token_yd)}
        params = {"path": path}
        url = "https://cloud-api.yandex.net/v1/disk/resources/"
        r = requests.put(url=url, headers=headers, params=params)
        res = r.json()
        if r.status_code == 201:
            break
        else:
            print("Папка с таким названием уже существует")
            continue
    return path


def copy_photo(album_id, count, owner_id, token_yd, path):
    url = "https://api.vk.com/method/photos.get"
    params = {"access_token": token_vk, "v": "5.131", "owner_id": owner_id, "album_id": album_id,
              "count": count, "extended": 1}
    headers = {"Accept": "application/json", "Content-Type": "application/json",
               "Authorization": "OAuth {}".format(token_vk)}
    req = requests.get(url, params=params, headers=headers)
    req_ = req.json()["response"]["items"]
    list_photo_info = []
    list_name = []
    url_photo = ""
    for photo in tqdm(req_):
        sizes_dict = {}
        for size in photo["sizes"]:
            sizes_dict[size["type"]] = size["url"]
            if "w" in sizes_dict.keys():
                photo_size = "w"
                url_photo = sizes_dict["w"]
            elif "z" in sizes_dict.keys():
                photo_size = "z"
                url_photo = sizes_dict["z"]
            elif "y" in sizes_dict.keys():
                photo_size = "y"
                url_photo = sizes_dict["y"]
            elif "r" in sizes_dict.keys():
                photo_size = "r"
                url_photo = sizes_dict["r"]
        file_name_ = photo["likes"]["count"]
        if file_name_ not in list_name:
            file_name = file_name_
            list_name.append(file_name)
        else:
            unix_data = photo["date"]
            data_ = str(datetime.datetime.fromtimestamp(unix_data))
            data = data_.replace(":", "-", 2)
            file_name = f"{file_name_}_{data}"
        params_up = {"path": f"{path}/{file_name}", "url": url_photo}
        headers_up = {"Accept": "application/json", "Authorization": "OAuth {}".format(token_yd)}
        url_yd = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        upload = requests.post(url=url_yd, params=params_up, headers=headers_up)
        dict_ = {"file_name": f"{file_name}.jpg", "size": photo_size}
        list_photo_info.append(dict_)
        time.sleep(1)
    print(list_photo_info)


if __name__ == "__main__":
    token_yd = input("Введите токен яндекс диска: ")
    path = create_folder(token_yd)
    token_vk = get_token_vk()
    album_id = input("Введите идентификатор альбома "
                     "(wall - со стены, profile - фото профиля, saved - сохраненные фото): ")
    count = int(input("Введите количество фотографий: "))
    owner_id_ = input("Введите user_id или user_name: ")
    if owner_id_.isdigit():
        owner_id = int(owner_id_)
    else:
        user_name = owner_id_
        owner_id = get_id(user_name, token_vk)
    copy_photo(album_id, count, owner_id, token_yd, path)








