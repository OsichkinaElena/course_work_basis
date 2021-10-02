import requests
from pprint import pprint
import time
from tqdm import tqdm

def download_photo(token, version):
    url = "https://api.vk.com/method/photos.get"
    params = {"access_token": token, "v": version, "album_id": "profile", "count": 5, "extended": 1}
    req = requests.get(url, params=params)
    # pprint(req.json())
    req_ = req.json()["response"]["items"]
    list_name = []
    for photo_info in tqdm(req_):
        size_max = "a"
        for photo in photo_info["sizes"]:
            photo_size = photo["type"]
            if photo_size > size_max:
                size_max = photo_size
                url = photo["url"]
            file_name = photo_info["likes"]["count"]
            data = photo_info["date"]
            api = requests.get(url, params={"access_token": token, "v": version})
            with open(f"image/{file_name}_{data}.jpg", "wb") as file:
                file.write(api.content)
                name = photo_info["likes"]["count"]
        list_name.append((f"{name}_{data}.jpg", size_max ))
        time.sleep(1)
    list_name.append("image")
    return list_name


def upload(folder_name, token_):
    token = token_
    headers = {"Content-Type": "application/json", "Authorization": "OAuth {}".format(token)}
    # params_creat = {"path": f"Photos/{folder_name}"}
    # url_creat = "https://cloud-api.yandex.net/v1/disk/resources"
    # r_creat = requests.put(url_creat, headers=headers, params=params_creat)
    # res_cr = r_creat.json()
    # pprint("CR", r_creat.json())
    list_photo_info = []
    for name_ in tqdm(list_name):
        name = name_[0]
        params = {"path": f"{name}", "overwrite": True}
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        r = requests.get(url, headers=headers, params=params)
        res = r.json()
        upload_ = requests.put(url=res["href"], data=open(f"{folder_name}/{name}", "rb"), headers=headers, params=params)
        dict_ = {"file_name": name, "size": name_[1]}
        # list_photo_info.append(dict_)
        print(dict_)
        time.sleep(1)
    # print(list_photo_info)

token = "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"
folder_name = download_photo(token, "5.131")[-1]
list_name = download_photo(token, "5.131")[:5]
token_ = ""

upload(folder_name, token_)

