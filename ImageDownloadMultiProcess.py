import requests
import time
import multiprocessing
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
    p1 = multiprocessing.Process(target=download_image(img_urls[0]))
    p2 = multiprocessing.Process(target=download_image(img_urls[1]))
    p3 = multiprocessing.Process(target=download_image(img_urls[2]))
    p1.start()
    p2.start()
    p3.start()
    end = time.perf_counter()
    print(f"Tasks ended in {round(end - start, 2)} second(s)")
