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

import os
import csv
import time
import pandas as pd
import random as rd
import storage as sg

# now profile.csv file directly created on main application folder
pathx = f"{sg.get_loc()}/DarshilSoft/Pixelverse/profile.csv"

query = [
    "landscape",
    "mountain landscape",
    "space",
    "galaxy",
    "milky way",
    "nebula space",
    "earth from space",
    "night sky stars",
    "sunset landscape",
    "sunrise landscape",
    "forest landscape",
    "waterfall landscape",
    "lake reflection mountains",
    "ocean waves",
    "beach sunset",
    "desert dunes",
    "snow mountains",
    "aurora borealis",
    "northern lights sky",
    "volcano landscape",
    "cliff landscape",
    "valley mountains",
    "road trip landscape",
    "city skyline night",
    "cyberpunk city",
    "futuristic city",
    "minimal landscape",
    "abstract dark background",
    "amoled dark wallpaper",
    "foggy forest",
    "misty mountains",
    "dramatic clouds sky",
    "thunderstorm sky"
]

def get_date():
    return time.strftime("%Y-%m-%d", time.localtime())

def get_category():
    if not os.path.exists(pathx):
        with open(pathx, "w", newline="", encoding="utf-8") as fp:
            writer = csv.DictWriter(fp, fieldnames=["type", "last-modify-date", "score"])
            writer.writeheader()
            for x in query:
                writer.writerow({
                    "type": x,
                    "last-modify-date": get_date(),
                    "score": 30
                })
        df = pd.read_csv(pathx)
        df.loc[df['type'] == 'landscape', 'score'] = 35
        df.loc[df['type'] == 'space', 'score'] = 35
        df.loc[df['type'] == 'mountain landscape', 'score'] = 35
        df.to_csv(pathx)
                
    else:
        df = pd.read_csv(pathx)
        top_3 = df.sort_values(by="score",ascending=False)
        two_random=top_3.iloc[3:].sample(n=3)
        final_cat = pd.concat([top_3.head(5),two_random],ignore_index=True).sample(n=1)
        cat_type = final_cat.iloc[0]['type']
        df.loc[df['type'] == cat_type,'last-modify-date'] = get_date()
        df.loc[df['type'] == cat_type,'score'] = final_cat.iloc[0]['score'] + 5
        df.to_csv(pathx)
        return str(cat_type)
get_category()

# actual resone behind not use top 3 and 2 from random it do unfair with random values and also with top 4 and 5 who deserve chance
# curruntly i not added minus 3 if category was skipped becuse i need to change in main file

# i tink repetation protection not needed becuse in pixabay api there was millions of wallpaper collection on a spacific serch keyword note here what i mention category it is actual search keywords