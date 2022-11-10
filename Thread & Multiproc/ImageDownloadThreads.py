import threading
import time
import requests

img_urls = ['https://cdn.pixabay.com/photo/2015/08/10/12/02/avocados-882635_960_720.jpg',
            'https://cdn.pixabay.com/photo/2015/12/01/20/28/road-1072823_960_720.jpg',
            'https://cdn.pixabay.com/photo/2013/11/28/10/36/road-220058_960_720.jpg']


def download_image(img_url):
    img_bytes = requests.get(img_url).content
    img_name = img_url.split('/')[9]
    with open(img_name, 'wb') as img_file:
        img_file.write(img_bytes)
        print(f"{img_name} was downloaded")

if __name__ == '__main__':
    start = time.perf_counter()
    t1 = threading.Thread(target=download_image, args=[img_urls[0]])
    t2 = threading.Thread(target=download_image, args=[img_urls[1]])
    t3 = threading.Thread(target=download_image, args=[img_urls[2]])
    t1.start()  # lancement des deux threads en meme temps (a peu près)
    t2.start()
    t3.start()
    t1.join()  # fin des deux threads
    t2.join()
    t3.join()
    end = time.perf_counter()
    print(f"Tasks ended in {round(end - start, 2)} second(s)")