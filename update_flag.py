import urllib.request
import ssl
import os

url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Flag_of_France.svg/1280px-Flag_of_France.svg.png"
dest = r"c:\Users\ammourth\Documents\ESIEA\test\cryptris\img\flag_fr.png"

try:
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    context = ssl._create_unverified_context()
    
    with urllib.request.urlopen(req, context=context) as response:
        data = response.read()
        
    with open(dest, "wb") as f:
        f.write(data)
        
    print(f"Successfully downloaded {dest} ({len(data)} bytes)")

except Exception as e:
    print(f"Error: {e}")
