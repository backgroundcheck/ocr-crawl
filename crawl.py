import os
import time
import logging
from thready import threaded
from threading import Lock
from extractors.tesseract import extract_image_data
from extractors.cache import get_cache

FILE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff',
                   '.gif']
DATA_PATH = os.environ.get('DATA_PATH')

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('ocr-crawl')

START_TIME = time.time()
counter_lock = Lock()
processed = 0


def crawl_file(file_path):
    global processed
    _, ext = os.path.splitext(file_path)
    ext = ext.strip().lower()
    if ext.lower() not in FILE_EXTENSIONS:
        return
    with open(file_path, 'rb') as fh:
        data = fh.read()
    key, text = get_cache(data)
    if text is not None:
        return
    text = extract_image_data(data)
    counter_lock.acquire()
    try:
        processed += 1
        time_taken = time.time() - START_TIME
        img_per_sec = time_taken / processed
    finally:
        counter_lock.release()
    log.info('Extracted: %s (%d characters of text), %.3fs/img', file_path,
             len(text), img_per_sec)


def crawl_directory(base_path):
    for (dirpath, _, files) in os.walk(base_path):
        for file_name in files:
            file_path = os.path.abspath(os.path.join(dirpath, file_name))
            file_path = os.path.normpath(file_path)
            yield file_path

if __name__ == '__main__':
    if not os.environ.get('EXTRACTORS_CACHE_DIR'):
        print 'No cache dir, this makes no sense'
    else:
        threaded(crawl_directory(DATA_PATH), crawl_file, num_threads=5)
