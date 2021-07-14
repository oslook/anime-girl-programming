#!/usr/bin/env python
import os
import sys
import json

from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import cloudinary


# config
os.chdir(os.path.join(os.path.dirname(sys.argv[0]), '.'))
if os.path.exists('settings.py'):
    exec(open('settings.py').read())

DEFAULT_TAG = "Anime-Girls-Holding-Programming-Books"
BASE_URL= "https://github.com/laynH/Anime-Girls-Holding-Programming-Books/blob/master/{}?raw=true"
DEFAULT_ITEMS_PATH = "../src/itemData.js"
# DEFAULT_ITEMS_PATH = "itemData.js"

def dump_response(response):
    print("Upload response:")
    for key in sorted(response.keys()):
        print("  %s: %s" % (key, response[key]))

def listdir(path, list_name):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        elif os.path.splitext(file_path)[1].lower() in ('.jpeg', '.png', '.jpg'):
            list_name.append(file_path)

def upload_files():
    ps = list()
    items = list()
    # this file must be in the git repo root folder
    basedir=os.path.abspath(os.path.dirname(__file__)) + "/"
    listdir(basedir, ps)
    ps=[i.replace(basedir, '') for i in ps]
#     ps=['C++/Kagamihara_Nadeshiko_CPP.png']
    for p in ps:
        author=os.popen('git --no-pager blame -L 1,1 {} --porcelain | grep  "^author " | sort -u'.format(os.path.join(basedir, p))).read()
        author=author.replace("author ", "").replace("\n", "")
        print("--- Upload by fetching a remote image", p, author)
        try:
            response = upload(
                BASE_URL.format(p),
                tags=[DEFAULT_TAG, p.split('/')[0]],
                folder="github",
                public_id=p.split("/")[-1].split(".")[0].replace(" ","").replace("#", ""),
                width=500,
                height=500,
                crop="fit",
                context={
                    "author": author, 
                    "caption": p.split("/")[-1], 
                    "alt": "",
                    "original_url": BASE_URL.format(p)},
                overwrite=True,
            )
        except Exception as e:
            print(e)
            continue
            
        dump_response(response)
        url, options = cloudinary_url(
            response['public_id'],
            format=response['format'],
            width=300,
            height=300,
            crop="fill",
            gravity="faces",
            effect="sepia",
        )
        items.append(
            {
            "id": response['public_id'],
            "filename": response["original_filename"],
            "context": response["context"],
            "img": response["url"],
            }
        )
        print("Face detection based 200x150 thumbnail url: " + url)
        print("")
    
    return items


def cleanup():
    response = resources_by_tag(DEFAULT_TAG)
    resources = response.get('resources', [])
    if not resources:
        print("No images found")
        return
    print("Deleting {0:d} images...".format(len(resources)))
    delete_resources_by_tag(DEFAULT_TAG)
    print("Done!")

def make_items(items):
    with open(DEFAULT_ITEMS_PATH, 'w')  as f:
        f.write("const itemData = ")
        json.dump(items, f)
        f.write(";\nexport default itemData;")

if len(sys.argv) > 1:
    if sys.argv[1] == 'upload':
        items = upload_files()
        make_items(items)
    if sys.argv[1] == 'cleanup':
        cleanup()
else:
    print("--- Uploading files and then cleaning up")
    print("    you can only choose one instead by passing 'upload' or 'cleanup' as an argument")
    print("    deps: git tool")
    print("")

    
