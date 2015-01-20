Instagram NO-API Downloaders
====================
Instagram crawler capable of asynchronously download media (images/videos) files of any public user without using Instagram's API.

  This is meant to be part of a larger project I'm contemplating on implementing.

  I will update this repo as I find new ways to implement it without using Instagram's API.
  So far I implemented 2 different ways.
  1. Gather images from 3rd party service like webstagram.  (**instagramCrawler1.py**)
  2. Use the .json data instagram stores under /media/ and iterate its content (**instagramCrawler2.py**)

Here are some other ways I haven't had the time to implement:

1. use a testing framework such as selenium to open a browser and iterate through the dynamically generated content.
2. Use a headless browser to load dynamically generated contents.

Warning
-------
Before you use this crawler, make sure you obtain permission from the instagram user to download their images. I do not approve of any usage of this script without the original user's consent.

Usage
----------
All the scripts I upload will follow the format stated below:

    instagramCrawlerX.py [username]

Dependencies
------------
Python 3

instagramCrawler1.py requires [BeautifulSoup](https://github.com/bdoms/beautifulsoup)

License
-----------------
MIT License
