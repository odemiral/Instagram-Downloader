'''
Written By Onur Demiralay
MIT License Copyright(c) 2014 Onur Demiralay

Simple NO-API crawler that asynchronously downloads all the images from any public instagram profile.
Before you use this crawler, make sure you obtain permission from the instagram user to download their images. 
I don't approve of any usage of this script without the original user's consent.
'''

import sys
import os
import json
from threading import Thread

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import time

#download files async with multithreads.
class DownloadWorker(Thread):
    def __init__(self, url, dir):
        Thread.__init__(self)
        self.url = url
        self.directory = dir
        self.start()
    def run(self):
        downloadFile(self.url, self.directory)

#given directory, download the file in given url.
def downloadFile(url,dir):
    try:
        fileName = url.split('/')[-1]
        response = urllib2.urlopen(url)
        path = dir + "/" + fileName
        print("downloading the file to: ", path)
        with open(path, 'wb') as f:
            f.write(response.read())
    except urllib2.HTTPError as e:
        print("HTTP Error! ", e.code, url)
        raise e
    except urllib2.URLError as e:
        print("URL Error! ", e.reason, url)
        raise e

#given url, returns the json data as python json object
def getJSON(url):
    #print(url)
    response = None
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
       print("HTTP Error!", e.code)
       exit(1)
    strResponse = response.readall().decode('utf-8')
    #print(strResponse)
    jsonData = json.loads(strResponse)
    return jsonData

#if the directory in given path, doesn't exsist, create one.
def createDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)

'''
Get the media data (in json) associated with the given username, if the username does exist, then iterates through
the json data and asynchronously downloads all the images in the json.
once all the items in json are iterated, it checks more_available field to check if there are more images to download.
'''
def main(argv):
    if len(argv) != 2:
        print('Usage:', os.path.basename(__file__),'[username]')
        exit(1)

    directory = argv[1]
    createDirectory(directory)

    url = "http://instagram.com/" + argv[1] + "/media/?max_id="
    print(url)

    moreDataToFetch = True
    max_id = ""
    #while more_available is True, there are more images to fetch.
    start = time.time()
    #client_id = 8035129ee63e4f25a8a90f174bc65ab1
    while(moreDataToFetch):
        nextUrl = url + max_id
        jsonData = getJSON(nextUrl)
        moreDataToFetch = jsonData['more_available']
        # print(moreDataToFetch)
        # print(jsonData['more_available'])
        # print(nextUrl)
        for item in jsonData['items']:
            imgUrl = None
            max_id = item['id'] #keep track of the id of the last post.
            if item['type'] == 'image':
                imgUrl = item['images']['standard_resolution']['url']
            elif item['type'] == 'video':
                imgUrl = item['videos']['standard_resolution']['url']
            if imgUrl:
                DownloadWorker(imgUrl,directory)
    end = time.time()
    print("took ",(end-start)," seconds.")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))