from PIL import Image
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent.parent
IMG_DIR = BASE / 'static' / 'blog' / 'images'
SRC = IMG_DIR / 'pp400.png'

if not SRC.exists():
    print('Source image not found:', SRC)
    sys.exit(2)

sizes = [16, 32, 48]

for s in sizes:
    dst = IMG_DIR / f'favicon-{s}.png'
    with Image.open(SRC) as im:
        im = im.convert('RGBA')
        im_small = im.resize((s, s), Image.LANCZOS)
        im_small.save(dst, format='PNG')
        print('Wrote', dst)

# create multi-size .ico
ico_path = IMG_DIR / 'favicon.ico'
with Image.open(SRC) as im:
    im = im.convert('RGBA')
    im.save(ico_path, format='ICO', sizes=[(16,16),(32,32),(48,48)])
    print('Wrote', ico_path)

# apple touch icon 180x180
apple_path = IMG_DIR / 'apple-touch-icon-180.png'
with Image.open(SRC) as im:
    im = im.convert('RGBA')
    im_180 = im.resize((180,180), Image.LANCZOS)
    im_180.save(apple_path, format='PNG')
    print('Wrote', apple_path)

# manifest.json
manifest = {
    "name": "Apurba Barai",
    "short_name": "Apurba",
    "icons": [
        {"src": "./blog/images/favicon-48.png", "sizes": "48x48", "type": "image/png"},
        {"src": "./blog/images/favicon-96.png", "sizes": "96x96", "type": "image/png"}
    ],
    "start_url": "/",
    "display": "standalone",
}
import json
with open(IMG_DIR / '..' / 'manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)
    print('Wrote', IMG_DIR / '..' / 'manifest.json')

print('Done')
