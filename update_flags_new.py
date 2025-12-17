import urllib.request
import ssl
import os

assets = [
    ("https://www.axl.cefan.ulaval.ca/europe/images/royaumeunidrap.gif", "flag_en.png"),
    ("https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Flag_of_the_Netherlands.svg/langfr-250px-Flag_of_the_Netherlands.svg.png", "flag_nl.png")
]

dest_dir = r"c:\Users\ammourth\Documents\ESIEA\test\cryptris\img"

def download_file(url, filename):
    filepath = os.path.join(dest_dir, filename)
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        context = ssl._create_unverified_context()
        
        with urllib.request.urlopen(req, context=context) as response:
            data = response.read()
            
        with open(filepath, "wb") as f:
            f.write(data)
            
        print(f"Successfully downloaded {filename} ({len(data)} bytes)")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

for url, name in assets:
    download_file(url, name)
