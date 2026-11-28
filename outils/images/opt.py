import sys,os
from PIL import Image
for f in sys.argv[1:]:
    im=Image.open(f).convert('RGB')
    bg=Image.new('RGB',im.size,'white');bg.paste(im)
    q=bg.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    q.save(f,optimize=True)
    print(f,im.size,os.path.getsize(f)//1024,'Ko')
