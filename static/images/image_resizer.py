#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
import os, sys

path = "/Users/Enric/Documents/MarketPlace/Code/Web/static/images/TBR"
dirs = os.listdir( path )

def resize(basewidth):
	for item in dirs:
		route = path+item
		if os.path.isfile(route):
			img = Image.open(route)
			wpercent = (basewidth / float(img.size[0]))
			 			hsize = int((float(img.size[1]) * float(wpercent)))
			f, e = os.path.splitext(route)
			imResize = img.resize((basewidth, hsize), Image.ANTIALIAS)
			imResize.save(f + 'z_' + item + ' resized.jpg', 'JPEG', quality=90)

resize(200)