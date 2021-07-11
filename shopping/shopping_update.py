import urllib.request
import re 
import json
import ftplib 


content = []


def load_helifree():
    urls = [
        ["https://helifree.ch/caddx-digital-fpv/4785-caddx-air-unit-hd-micro-version", "Caddx Air Unit"],
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
                    "link": url[0]
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
                        "link": url[0]
                    }
                )
            else:
                content.append(
                    {
                        "shop": "Helifree",
                        "item": url[1],
                        "availability": "unkown",
                        "link": url[0]
                    }
                )


load_helifree()

f = open("shopping.json", "w")
f.write(json.dumps(content))
f.close()

with ftplib.FTP('y737d.ftp.infomaniak.com') as ftp:

    filename = 'shopping.json'

    try:
        ftp.login('y737d_cocktail', '')  

        with open(filename, 'rb') as fp:

            res = ftp.storlines("STOR /web/shopping/" + filename, fp)

            if not res.startswith('226 Transfer complete'):

                print('Upload failed')

    except ftplib.all_errors as e:
        print('FTP error:', e)
