# Ritaglia le illustrazioni di ChatGPT (PNG già trasparenti): toglie il vuoto attorno al disegno,
# le mette in un quadrato con un piccolo margine e le salva a 720 px in illustrazioni/
# Uso: python _materiale/ritaglia.py nome1 nome2 ...  (file in _materiale/illustrazioni-originali/nome.png)
import sys
from PIL import Image

for name in sys.argv[1:]:
    img = Image.open(f"_materiale/illustrazioni-originali/{name}.png").convert("RGBA")
    img = img.crop(img.getchannel("A").point(lambda v: 255 if v > 6 else 0).getbbox())
    side = int(max(img.size) * 1.06)
    can = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    can.paste(img, ((side - img.size[0]) // 2, (side - img.size[1]) // 2))
    can.resize((720, 720), Image.LANCZOS).save(f"illustrazioni/{name}.png", optimize=True)
    print("illustrazioni/" + name + ".png")
