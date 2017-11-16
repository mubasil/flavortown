from bs4 import BeautifulSoup
from watson_developer_cloud import VisualRecognitionV3 as VisualRecognition
import zipfile
from zipfile import ZipFile
import requests
import re
import urllib2
import os
import argparse
import sys
import json
import pdb

# adapted from http://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

def main(args):
    
    
    visual_recognition = VisualRecognition(version='2016-05-20', api_key='7b851fccf7f17a35fc7569a5dad6e1eb4f650f70')
    
    with open('ingredients.txt') as f:
        lines = f.read().splitlines()

    for line in lines:
        directory = "C:/Dev/GitHub/flavortown/imagetesting/zips" + line
        
        query = line
        max_images = 25
        save_directory = directory
        image_type="Action"
        query= query.split()
        query='+'.join(query)
        query = query + "+walmart"
        url="https://www.google.com/search?q="+query+"&source=lnms&tbm=isch"
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        soup = get_soup(url,header)
        ActualImages=[]# contains the link for Large original images, type of  image
        for a in soup.find_all("div",{"class":"rg_meta"}):
            link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
            ActualImages.append((link,Type))
            
        fileNames = []
        for i , (img , Type) in enumerate( ActualImages[0:max_images]):
            try:
                req = urllib2.Request(img, headers={'User-Agent' : header})
                raw_img = urllib2.urlopen(req).read()
                fileName = ""
                if len(Type)==0:
                    fileName = "img" + "_"+ str(i)+".jpg"
                    f = open(fileName, 'wb')
                else :
                    fileName = "img" + "_"+ str(i)+"."+Type
                    f = open(fileName, 'wb')
                f.write(raw_img)
                f.close()
                fileNames.append(fileName)
            except Exception as e:
                print ("could not load : "+img)
        
        myzip = ZipFile(line + '.zip', 'w',zipfile.ZIP_DEFLATED)
        for fileName in fileNames:
            myzip.write(fileName)
        
        myzip.printdir()
        myzip.close()
        
        for fileName in fileNames:
            os.remove(fileName)

if __name__ == '__main__':
    from sys import argv
    try:
        main(argv)
    except KeyboardInterrupt:
        pass
    sys.exit()
