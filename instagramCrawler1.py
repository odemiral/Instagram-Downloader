'''
Written By Onur Demiralay
MIT License Copyright(c) 2014 Onur Demiralay
Simple No-API Instagram crawler that uses webstagram to download images of any given public profile.
'''

import sys
import os
from bs4 import BeautifulSoup
from threading import Thread
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import time
#download files asynchronously with multithreads.
class DownloadWorker(Thread):
    def __init__(self, url, dir):
        Thread.__init__(self)
        self.url = url
        self.directory = dir
        self.start()
    def run(self):
        downloadFile(self.url, self.directory)


# Returns the url of the next page
def getNextPage(soup):
    res = soup.find(class_="pager")
    pageUrl = None
    for link in res.findAll('a'):
        pageUrl = link.get('href')

    # if there is no next page return false
    if (pageUrl):
        return "http://web.stagram.com" + pageUrl
    else:
        return False

#given directory, download file in url
def downloadFile(url,dir):
    try:
        fileName = url.split('/')[-1]
        response = urllib2.urlopen(url)
        path = dir + "/" + fileName
        print("downloading the file to: ", path)
        with open(path, 'wb') as f:
            f.write(response.read())
    #when this occurs it's most likely server couldn't find _7 of the image, try it again with _8.jpg instead
    except urllib2.HTTPError as e:
        print("HTTP Error! ", e.code, url)
        url = url.replace("_7.jpg", "_8.jpg")
        downloadFile(url,dir)
    except urllib2.URLError as e:
        print("URL Error! ", e.reason, url)

#if the directory in given path, doesn't exist, create one.
def createDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main(argv):
    if len(argv) != 2:
        print('Usage:', os.path.basename(__file__),'[username]')
        exit(1)

    directory = argv[1]
    createDirectory(directory)
    url = "http://web.stagram.com/n/" +argv[1]
    pagesToBrowse = True #Indicates if there are any extra pages to browse other than the one it's currently browsing.
    start = time.time()
    while(pagesToBrowse):
        response = urllib2.urlopen(url,data=None)
        html = response.read()
        soup = BeautifulSoup(html) #load the html file onto soup object

        for imgLink in soup.find_all('img'):
            src = imgLink.get('src')
            #imgType will represent whether or not image is resized, if it's a, then n will return the original image
            imgType =  src[len(src)-5:len(src)-4]
            cdnType = src[7:15]
            if src and (imgType == "a" and cdnType == "scontent"):
                src = src.replace("_a.jpg", "_n.jpg") #get n
                DownloadWorker(src,directory)
            elif src and (imgType == "6" and cdnType == "scontent"):
                src = src.replace("_6.jpg", "_7.jpg") #get 7
                DownloadWorker(src,directory)
        url = getNextPage(soup)
        if not url:
            pagesToBrowse = False
    end = time.time()
    print("took ",(end-start)," seconds.")
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))