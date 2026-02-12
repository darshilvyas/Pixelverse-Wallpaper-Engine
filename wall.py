"""
© 2026 Darshil Vyas
All Rights Reserved.

This source code is part of a personal portfolio project.
It may not be copied, distributed, or used commercially
without explicit permission from the author.

For any queries regarding this project, feel free to contact me:
Email: darshilvyas7@gmail.com
LinkedIn: https://www.linkedin.com/in/darshil-vyas


"""



import ctypes
import requests as re
import random as rn
import urllib.request as ul
import time
import os
import storage as sg
path_wall= f"{sg.get_loc()}/DarshilSoft/Pixelverse"

# api_key="api_key"
# wallpaper query topics
# query = [
#     "landscape",
#     "mountain landscape",
#     "space",
#     "galaxy",
#     "milky way",
#     "nebula space",
#     "earth from space",
#     "night sky stars",
#     "sunset landscape",
#     "sunrise landscape",
#     "forest landscape",
#     "waterfall landscape",
#     "lake reflection mountains",
#     "ocean waves",
#     "beach sunset",
#     "desert dunes",
#     "snow mountains",
#     "aurora borealis",
#     "northern lights sky",
#     "volcano landscape",
#     "cliff landscape",
#     "valley mountains",
#     "road trip landscape",
#     "city skyline night",
#     "cyberpunk city",
#     "futuristic city",
#     "minimal landscape",
#     "abstract dark background",
#     "amoled dark wallpaper",
#     "foggy forest",
#     "misty mountains",
#     "dramatic clouds sky",
#     "thunderstorm sky"
# ]


def get_req(search_query,api_key):

         
    try:
        print(search_query,"i am here")
        call_url= f"https://pixabay.com/api/?key={api_key}&q={search_query}&image_type=photo&orientation=horizontal&min_width=2560&min_height=1440&editors_choice=false&per_page=200&pretty=true"
        # print(get_random(get_urls(re.get(call_url).json()["hits"])))
        return get_random(get_urls(re.get(call_url).json()["hits"]))
    except:
        # default wall in error situation
        set_desktop_wallpaper(f"{path_wall}/temp.jpg")


def get_random(wall_list):
    return(rn.choice(wall_list))

# def get_random_query():
#     global query
#     return (rn.choice(query))


def get_urls(json):
    result=[]
    for x in json:
        result.append(x["largeImageURL"])
    return result


def set_desktop_wallpaper(path):
    # 20 = SPI_SETDESKWALLPAPER
    # 3 = SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    # 0 is IGNORED PARAMETER
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)

# url=get_req()
# ul.urlretrieve(url,"1.jpg",headers=header)
#this function work final task
def set_up_wall (search_query,api_key):
    url = get_req(search_query,api_key)

    # for user-agent to Solve 403 errors forbidden
    headers = {
    "User-Agent": "Mozilla/5.0"
    }
    # header packet for req
    req = ul.Request(url, headers=headers)

    # fetch the binary bytes of image
    with ul.urlopen(req) as response:
        data = response.read()
    # save image
    with open(f"{path_wall}/temp1.jpg", "wb") as f:
        f.write(data)
    os.replace(f"{path_wall}/temp1.jpg", f"{path_wall}/temp.jpg")

    set_desktop_wallpaper(f"{path_wall}/temp1.jpg") # the final wallpaper setup ......

def main(search_query,api_key):
    set_up_wall(search_query,api_key)
    return True



        

def check_api(api_key):
    call_url= f"https://pixabay.com/api/?key={api_key}&q=cars&image_type=photo&orientation=horizontal&min_width=2560&min_height=1440&editors_choice=false&per_page=20&pretty=true"
    res= re.get(call_url)
    if(res.status_code == 400):
            return False
    else:
            return True

if __name__ == "__main__":
    pass
# set_desktop_wallpaper(r"C:\Users\darsh\Downloads\Soft Colorful Aesthetic Beach and Quote Desktop Wallpaper.png")

# next step is setup wallpaper final and also bg activ and also startup run and optimization 