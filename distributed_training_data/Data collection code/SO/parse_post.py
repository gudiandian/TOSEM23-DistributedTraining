"""
Parse xml file into json and map answer to question.
Since the initial file is too big to use single thread, use map-reduce framework for multithread to parse efficiently.
You have to split the big input file into several small files first.
"""

import os
import shutil
import json
import multiprocessing
import time
import traceback
from itertools import groupby
from operator import itemgetter
import xml.etree.cElementTree as et

INPUT_DIR = 'StackOverflow'
MAPRES_DIR = 'MapRes'
OUTPUT_DIR = 'Posts'

PROCESS_NUM = 10
HASH_SEED = 200

def _readlines(file, separator='\t'):
    for line in file:
        line = line.strip().split('\t')
        yield line

def _mapper(input_dir, filename):
    '''
    Parse post and map to the specific file according to OwnerUserId
    '''
    with open('{}/{}'.format(input_dir, filename), 'r') as f:
        for line in f:
            try:
                if '<row' not in line:
                    continue
                # parse xml
                tree = et.fromstring(line.strip())
                post = tree.attrib

                if int(post['PostTypeId']) == 1:
                    # question post
                    key = post['Id']
                    post_type = 'question'
                else:
                    # answer post
                    if 'ParentId' not in post:
                        continue
                    key = post['ParentId']
                    post_type = 'answer'

                file_id = int(key) % HASH_SEED
                out_file = '{}/{}_mapres.txt'.format(MAPRES_DIR, file_id)
                with open(out_file, 'a') as f_res:
                    f_res.write('{}\t{}\t{}\n'.format(key, post_type, json.dumps(post)))
            except:
                traceback.print_exc()
        
        print('Finish map file ', filename)

def _reducer(file_id):
    # sort
    os.system("sort -t '\t' {}/{}_mapres.txt > {}/{}_sortres.txt".format(MAPRES_DIR, file_id, MAPRES_DIR, file_id))
    
    # map answer to its corresponding question
    f_res = open('{}/{}.txt'.format(OUTPUT_DIR, file_id), 'w')
    with open('{}/{}_sortres.txt'.format(MAPRES_DIR, file_id)) as f:
        lines = _readlines(f)
        
        # group by id
        for q_id, group in groupby(lines, itemgetter(0)):
            question_info = {}
            answer_list = []
            for item in group:
                if item[1] == 'question':
                    question_info = json.loads(item[2])
                if item[1] == 'answer':
                    answer_list.append(json.loads(item[2]))
            if 'Id' not in question_info:
                continue
            question_info['answers'] = answer_list
            f_res.write('{}\r\n'.format(json.dumps(question_info)))
    
    
    f_res.close()
    
    print('Finish reduce file ', file_id)

def map():
    if os.path.exists(MAPRES_DIR):
        shutil.rmtree(MAPRES_DIR)
    os.makedirs(MAPRES_DIR, exist_ok=True)

    print('Mapping...')
    
    start = time.time()
    pool = multiprocessing.Pool(processes = PROCESS_NUM)
    post_files = os.listdir(INPUT_DIR)
    for post_file in post_files:
        pool.apply_async(_mapper, (INPUT_DIR, post_file, ))  
    pool.close()
    pool.join()
    
    print('Done in {} seconds.'.format(time.time() - start))



def reduce():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print('Reducing...')

    start = time.time()
    pool = multiprocessing.Pool(processes = PROCESS_NUM)
    for file_id in range(0, HASH_SEED):
        pool.apply_async(_reducer, (file_id, ))
    pool.close()
    pool.join()

    print('Done in {} seconds.'.format(time.time() - start))

def main():
    map()
    reduce()
    if os.path.exists(MAPRES_DIR):
        shutil.rmtree(MAPRES_DIR)


if __name__ == '__main__':
    main()
