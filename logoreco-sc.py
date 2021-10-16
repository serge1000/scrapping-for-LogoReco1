#!/usr/bin/python

import requests
from bs4 import  BeautifulSoup
import shutil 
#import socket
import time
#import hashlib
import os
from urllib.parse import urlparse
import sys
import random
#import re
from warnings import warn
from IPython.core.display import clear_output
import numpy as np
import uuid
import func

print("---------- Start ----------")

pathtoimages = '../images_for_logoreco4/'




ualist =  func.readlistfromfile("user-agents-list.txt")

logpath = ""
logfilename = ""

# Create list of images on https://www.brandsoftheworld.com/logos?page=7

fullURL = "https://www.brandsoftheworld.com/logos?page=7"
fullURL = "https://www.brandsoftheworld.com/logos?page=4"
# 5-7 8-16 17-116 8000-8300 3000-3100

for x in range(8250, 8350):
    fullURL = "https://www.brandsoftheworld.com/logos?page=" + str(x) 
    print("+++++++++ "+fullURL+" +++++++++")
    response =  func.sendrequestnoproxy(fullURL,ualist,"","")

    page_html = BeautifulSoup(response.text, 'html.parser')

    for ultag in page_html.find_all('ul', {'class': 'logos'}):
        for litag in ultag.find_all('li'):

            #func.randdelay(3)

            image_href = litag.img['src']



            # Retrive and save  one image

            #image_href = "https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-thumbnail/s3/092021/screenshot_2021-09-22_at_13.25.31.png?1cYMrmBvtMHICwZp1JMw4kl.v2AQFOna&amp;itok=bKdP89e5"
            #image_href = "https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-thumbnail/s3/092021/ovice.jpg?WZ.cSYQdBhLBmlZ9uapNatMs8bKEcUE8&amp;itok=xxWILxIP"


            response =  func.sendrequestnoproxy(image_href,ualist,"","")

            if response.status_code == 200:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                response.raw.decode_content = True
                #  Open a local file with wb ( write binary ) permission.
                a = urlparse(image_href)
                ifilename = os.path.basename(a.path)
                randfilename = uuid.uuid4().hex + os.path.splitext(ifilename)[1]
                ifilename = pathtoimages+randfilename 
                print("new file  :  " + ifilename)

                try:
                    with open(ifilename,'wb') as ff:
                        shutil.copyfileobj(response.raw, ff) 
                except Exception as e:
                    fake = 1
                    #if FG: print("====================\nIMAGE WRITING PROBLEM" + href_imagelink + '\n'+str(e)+'\n=================')
                    #func.logascsv(logpath+"reqerror-"+logfilename+".log.csv", m1="IMAGE WRITING PROBLEM",m2=href_imagelink,m3=post_one_link,m4=str(e)) 
                    #func.logascsv(logpath+"glblmsgs-"+logfilename+".log.csv", m1="IMAGE WRITING PROBLEM",m2=href_imagelink,m3=post_one_link,m4="",m5="",m6="",m7="")
                else:
                    # func.logascsv(logpath+"images-"+logfilename+".log.csv", m1=str(response.status_code),m2=post_one_link,m3=href_imagelink,m4="") 
                            fake = 1


