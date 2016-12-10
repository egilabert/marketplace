#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
import os, sys

path = "/Users/Enric/Documents/MarketPlace/Code/Web/static/images/TBR/Original/"
dirs = os.listdir( path )

def is_image_file(filename):
    """Does `filename` appear to be an image file?"""
    img_types = [".jpg", ".jpeg", ".png", ".gif"]
    ext = os.path.splitext(filename)[1]
    return ext in img_types

def resize(basewidth):
	for item in dirs:
		route = path+item
		try:
			if os.path.isfile(route) and is_image_file(route):
				print(route)
				img = Image.open(route)
				wpercent = (basewidth / float(img.size[0]))
				hsize = int((float(img.size[1]) * float(wpercent)))
				f, e = os.path.splitext(route)
				imResize = img.resize((basewidth, hsize), Image.ANTIALIAS)
				#print(f + '_resized.jpg')
				imResize.save(f + '_resized.jpg', 'JPEG', quality=90)
		except:
			if os.path.isfile(route) and is_image_file(route):
				print(route)
				img = Image.open(route).convert('RGB').save(route)
				wpercent = (basewidth / float(img.size[0]))
				hsize = int((float(img.size[1]) * float(wpercent)))
				f, e = os.path.splitext(route)
				imResize = img.resize((basewidth, hsize), Image.ANTIALIAS)
				#print(f + '_resized.jpg')
				imResize.save(f + '_resized.jpg', 'JPEG', quality=90)

resize(400)