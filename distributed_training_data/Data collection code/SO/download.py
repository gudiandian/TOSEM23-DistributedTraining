from internetarchive import download
import sys
import os

def unzip():
    files = os.listdir('stackexchange')
    for f in files:
        if '.7z' in f:
            print('Unzip ', f)
            os.system('7z e stackexchange/'+f+' -oarchive/'+f)


def download_posts():
    download('stackexchange', files='stackoverflow.com-Posts.7z', verbose=True)

def main():
    download_posts()
    unzip()

if __name__ == '__main__':
    main()