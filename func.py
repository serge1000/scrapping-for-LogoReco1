#!/usr/bin/python

import requests
from bs4 import  BeautifulSoup
import shutil 
import socket
import time
import datetime
#import hashlib
import os
import sys
import random

#import re
from IPython.core.display import clear_output
import numpy as np


def getipandhosname():
   hostname = socket.gethostname()
   ip = socket.gethostbyname(hostname)
   return ip,hostname  

def readlistfromfile(filename):
    with open(filename) as f:
        list1 = f.read().splitlines()
    return list1


#  take randomly proxy from the  list (func paramer) 
def getrandproxy(proxylist):
    return proxylist[random.randint(0, len(proxylist)-1 )]


#  take randomly user agent from the  list (func paramer) , add to header template and return header
def getrandheader(ualist):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Dnt": "1",
        "Upgrade-Insecure-Requests": "1",
     }

    headers["User-Agent"]  = ualist[random.randint(0, len(ualist)-1 )]

    return headers

# mX - strings only
def logascsv(logfilename,m1="",m2="",m3="",m4="",m5="",m6="",m7=""):
    
    ip_address1,hostname1 = getipandhosname()
    ip_address1 = '"' + ip_address1 + '",' 
    hostname1 = '"' + hostname1 + '",' 
    logdate = str(datetime.datetime.now())
    logdate = '"' + logdate + '",' 
    m1 = '"' + m1.replace('"', "'")+ '",'
    m2 = '"' + m2.replace('"', "'") + '",'
    m3 = '"' + m3.replace('"', "'") + '",'
    m4 = '"' + m4.replace('"', "'") + '",'
    m5 = '"' + m5.replace('"', "'") + '",'
    m6 = '"' + m6.replace('"', "'") + '",'
    m7 = '"' + m7.replace('"', "'")  + '"'
    data_string = logdate+hostname1+ip_address1+m1+m2+m3+m4+m5+m6+m7+'\n'

    f = open(logfilename, 'a')
    f.write(data_string)
    f.close()


def sendrequestnoproxy(furl,ualist,logpath,logfilename):
    randheader = getrandheader(ualist)
    r = ""
    try:
        r = requests.get(furl, stream = True, headers = randheader, timeout=4)
    except Exception as e:
        #logascsv(logpath+"reqerror-"+logfilename+".log.csv", m1="proxy="+proxy,m2=furl,m3=str(e)) 
        r = "error"   
        print("ERROR :  "+furl)

    if(r != "error"): # Got response
        if r.status_code == 404:  # 4040 - don't try one more
            print("404"+furl+"  "+str(r.status_code))
            #logascsv(logpath+"reqerror-"+logfilename+".log.csv", m1="proxy="+proxy,m2=furl,m3=str(r.status_code)) 

        if r.status_code != 200: #if not good response (not 200/404)- write log and again
            print("??? 403"+furl+"  "+str(r.status_code))
            #logascsv(logpath+"reqerror-"+logfilename+".log.csv", m1="proxy="+proxy,m2=furl,m3=str(r.status_code)) 
        else:
            print("OK :  "+furl)
    return r

def sendrequest(furl,proxylist,ualist,logpath,logfilename):

    for x in range(5):

        proxy = getrandproxy(proxylist)
        randheader = getrandheader(ualist)
        r = ""
        #print("TRY "+str(x))

        try:
            #print("proxy = "+proxy)
            r = requests.get(furl, stream = True, headers = randheader,proxies={'http' : proxy,'https': proxy}, timeout=4)
        except Exception as e:
            #print("====================\nproxy="+proxy+" "+furl+'\n'+str(e)+'\n=================')
            logascsv(logpath+"reqerror-"+logfilename+".log.csv", m1="proxy="+proxy,m2=furl,m3=str(e)) 
            r = "error"   

        if(r != "error"): # Got response

            if r.status_code == 404:  # 4040 - don't try one more
                #print("404"+furl+"  "+str(r.status_code))
                logascsv(logpath+"reqerror-"+logfilename+".log.csv", m1="proxy="+proxy,m2=furl,m3=str(r.status_code)) 
                break

            if r.status_code != 200: #if not good response (not 200/404)- write log and again
                #print("??? 403"+furl+"  "+str(r.status_code))
                #logascsv(logpath+"reqerror-"+logfilename+".log.csv", m1="proxy="+proxy,m2=furl,m3=str(r.status_code)) 
                fake = 1
            else:
                print("OK :"+furl)
                break # if good response  - get out from "for"
    #END of for x in range(6):
    return r


#  function gets delay for each request (delayinseconds) and generates/executes delay between 0.2 sec and delayinseconds
def randdelay(delayinseconds):
    randdelay =  round(((random.randint(2, delayinseconds/0.1))*0.1) , 1)
    print("randdelay = " + str(randdelay) )
    time.sleep(randdelay)
