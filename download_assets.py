import os
import urllib.request
import ssl

def download_file(url, filename):
    try:
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
        )
        # Create an unverified context
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=context) as response, open(filename, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

img_dir = r"c:\Users\ammourth\Documents\ESIEA\test\cryptris\img"

assets = [
    ("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Flag_of_France.svg/100px-Flag_of_France.svg.png", "flag_fr.png"),
    ("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Flag_of_the_United_Kingdom.svg/100px-Flag_of_the_United_Kingdom.svg.png", "flag_en.png"),
    ("https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Flag_of_the_Netherlands.svg/100px-Flag_of_the_Netherlands.svg.png", "flag_nl.png")
]

for url, name in assets:
    download_file(url, os.path.join(img_dir, name))
