import requests
from bs4 import BeautifulSoup
import json
from canon import camera
import os
import readchar

details = {}

def capture_part_data():
    url = input("Enter MiniSpares URL (or enter for manual input): ")

    if (url == ''):
      details = {
        'article_number': input('Enter article number: '),
        'title': input('Enter title: '),
        'description': input('Enter description: '),
        'price_new': input('Enter price: '),
      }
    else:
      # Scrape MiniSpares data
      page = requests.get(url)
      soup = BeautifulSoup(page.content, 'html.parser')

      details = {
        'url': url,
        'article_number': soup.select('span.code')[0].text,
        'title': soup.select('.box-info-shopproduct h1')[0].text,
        'description': soup.select('.content .text-area')[0].text.strip(),
        'price_new': soup.select('.price .notranslate')[0].text[2:]
      }


    details['condition'] = input('Describe part condition: ')
    details['comment'] = input('Comment: ')

    return details

def capture_images(filename):
    cmd = f'gphoto2 --capture-image-and-download --force-overwrite --filename "{filename}"'
    os.system(cmd)


### Main ###
parts = []

while (True):
    parts.append(capture_part_data())

    print('\n')
    print(json.dumps(parts, indent=4))

    print("\nOptions: [a] add part; [d] discard and re-enter; [F] finished: ")
    choice = readchar.readchar()
    print(choice)

    if (choice == 'd'):
        parts.pop()
    elif (choice == 'f') or (choice == '\r'):
        break

partnumbers = []
for part in parts:
    partnumbers.append(part["article_number"])

dirname = "_".join(partnumbers)

path = f"parts/{dirname}/"
os.makedirs(path)

i = 1

while (True):
    print("Options: [C] Capture image; [f] finished: ")
    choice = readchar.readchar()

    if (choice == 'f'):
        break
    else:
        capture_images(f"{path}{i}.jpg")
        i = i + 1

with open(f'parts/{dirname}/details.json', 'w') as f:
    f.write(json.dumps(parts, indent=4))


