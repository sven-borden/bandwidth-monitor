import urllib.request
import re 
import json
import ftplib 
import datetime

content = []


def load_helifree():
    urls = [
        ["https://helifree.ch/caddx-digital-fpv/4785-caddx-air-unit-hd-micro-version", "Caddx Air Unit"],
        ["https://helifree.ch/caddx-digital-fpv/4910-caddx-polar-air-unit-hd-kit-silver", "Caddx Polar Vista"],
        ["https://helifree.ch/caddx-digital-fpv/4909-caddx-polar-air-unit-hd-kit-silver", "Caddx Polar Air Unit"]
    ]
    # Caddx air unit
    for url in urls:
        page = urllib.request.urlopen(url[0])
        page_content = str(page.read())
        if "Rupture de stock" in page_content:
            content.append(
                {
                    "shop": "Helifree",
                    "item": url[1],
                    "availability": "0",
                    "link": url[0],
                    "time": datetime.datetime.now().strftime("%c")
                }
            )
        else:
            # Look or <span data-stock="x"
            x = re.findall("data-stock=.{3}", page_content)
            if len(x) > 0:
                content.append(
                    {
                        "shop": "Helifree",
                        "item": url[1],
                        "availability": x[0].split("\"")[1],
                        "link": url[0],
                        "time": datetime.datetime.now().strftime("%c")
                    }
                )
            else:
                content.append(
                    {
                        "shop": "Helifree",
                        "item": url[1],
                        "availability": "unkown",
                        "link": url[0],
                        "time": datetime.datetime.now().strftime("%c")
                    }
                )


def load_optimum_racing():
    urls = [
        ["https://optimum-racing.ch/fr/cameras-fpv-numerique-hd/833-caddx-vista-air-unit-lite-la-vista-a-ete-entierement-autorise-par-dji-et-compatible-avec-leur-systeme-hd-fpv-encore-mieux-la-cad.html", "Caddx Vista"],
        ["https://optimum-racing.ch/fr/cameras-fpv-numerique-hd/1292-nebula-pro-vista-kit-nebula-pro-vista-kit-720p-120fps-systeme-fpv-numerique-hd-a-faible-latence-14990-chf.html", "Caddx Nebula Pro"]
    ]
    # Caddx air unit
    for url in urls:
        page = urllib.request.urlopen(url[0])
        page_content = str(page.read())
        if "pas assez de produits en stock" in page_content:
            content.append(
                {
                    "shop": "Optimum Racing",
                    "item": url[1],
                    "availability": "0",
                    "link": url[0],
                    "time": datetime.datetime.now().strftime("%c")
                }
            )
        else:
            # Look or <span data-stock="x"
            x = re.findall("data-stock=.{3}", page_content)
            if len(x) > 0:
                content.append(
                    {
                        "shop": "Optimum Racing",
                        "item": url[1],
                        "availability": x[0].split("\"")[1],
                        "link": url[0],
                        "time": datetime.datetime.now().strftime("%c")
                    }
                )
            else:
                content.append(
                    {
                        "shop": "Optimum Racing",
                        "item": url[1],
                        "availability": "unknown",
                        "link": url[0],
                        "time": datetime.datetime.now().strftime("%c")
                    }
                )


load_helifree()
load_optimum_racing()

f = open("shopping.json", "w")
f.write(json.dumps(content))
f.close()

with ftplib.FTP('y737d.ftp.infomaniak.com') as ftp:

    filename = 'shopping.json'

    try:
        ftp.login('y737d_cocktail', 'Im4g33k!')

        with open(filename, 'rb') as fp:

            res = ftp.storlines("STOR /web/shopping/" + filename, fp)

            if not res.startswith('226 Transfer complete'):

                print('Upload failed')

    except ftplib.all_errors as e:
        print('FTP error:', e)
