import os 
import json
import multiprocessing
import re
import string
import time 
import traceback
from bs4 import BeautifulSoup

INPUT_DIR = '../Posts'
DISTRIBUTED_FILE = 'distributed_set.csv'

PROCESS_NUM = 10
TAGS = ['horovod']
EXTRACT_TAGS = ['tensorflow', 'pytorch', 'keras']
KEYWORDS = ['distributed', 'distribute', 'parallel', 'paralleled', 'parallelism', 'multi-server', 
'multi-gpu', 'data-parallel', 'model-parallel', 'dataparallel', 'multi-machine', 'multi_gpu', 
'multi-gpus', 'workers']
KEY_PHRASES = ['multiple gpus', 'multiple machines', 'multiple gpu', 'multiple machine', 
'multiple servers', 'multiple server']

url_regex = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^`{|}~'

def worker(input_file):
    global count, distributed_count
    f_distributed = open(DISTRIBUTED_FILE, 'a')
    
    with open(input_file, 'r') as f:
        for line in f:
            try:
                line = line.strip()
                content = json.loads(line)
                
                accepted = False
                if 'AcceptedAnswerId' in content:
                    accepted = True
                
                contain_tag = False
                contain_keyword = False
                
                # filter by tag
                tags = content['Tags'].split('><')
                for tag in tags:
                    tag = tag.strip().replace('<', '').replace('>', '')
                    if tag in TAGS:
                        contain_tag = True
                        contain_keyword = True
                        break
                    elif tag in EXTRACT_TAGS:
                        contain_tag = True

                # filter by keyword
                if not contain_keyword:
                    title = content["Title"]
                    title = title.strip().lower()
                    for punc in punctuation:
                        title = title.replace(punc, ' ')
                    for keyphrase in KEY_PHRASES:
                        if title.find(keyphrase) != -1:
                            contain_keyword = True
                            break
                    if not contain_keyword:
                        title = title.split(' ')
                        for keyword in KEYWORDS:
                            if keyword in title != -1:
                                contain_keyword = True
                                break
                
                if not contain_keyword:
                    # remove code
                    body = '<html>{}</html>'.format(content['Body'].strip())
                    soup = BeautifulSoup(body, 'html.parser')
                    for c in soup.find_all('code'):
                        c.string = ''
                        break

                    # extract text
                    text = []
                    for child in soup.find_all('p'):
                        text.append(child.text.strip().lower())
                    text = ' '.join(text)

                    # replace url
                    text = url_regex.sub(' url ', text)
                    #for punc in string.punctuation:
                    for punc in punctuation:
                        text = text.replace(punc, ' ')

                    for keyphrase in KEY_PHRASES:
                        if text.find(keyphrase) != -1:
                            contain_keyword = True
                            break

                    if not contain_keyword:
                        text = text.split(' ')

                        for keyword in KEYWORDS:
                            if keyword in text != -1:
                                contain_keyword = True
                                break

                if contain_tag and contain_keyword and accepted:
                    f_distributed.write('https://stackoverflow.com/questions/{},{}\n'.format(content['Id'], content['Tags']))
            except:
                traceback.print_exc()

def main():
    print('Start to extract posts...')
    f_res = open(DISTRIBUTED_FILE, 'a')
    if os.path.getsize(DISTRIBUTED_FILE) == 0:
        f_res.write('question,tags\n')
    f_res.close()

    start = time.time()
    pool = multiprocessing.Pool(processes = PROCESS_NUM)
    files = os.listdir(INPUT_DIR)
    for file in files:
        pool.apply_async(worker, ('{}/{}'.format(INPUT_DIR, file), ))
    pool.close()
    pool.join()
    
    print('Done in {} seconds.'.format(time.time() - start))
    

if __name__ == '__main__':
    main()