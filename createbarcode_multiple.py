import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps
from fpdf import FPDF
import os, os.path
import shutil




def concat_sidebyside(imgs):
    im1 = Image.open(imgs[0])
    im2 = Image.open(imgs[1])
    im3 = Image.open(imgs[2])
    dst = Image.new('RGB', (1386, 230))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (462, 0))
    dst.paste(im3, (924, 0))
    return dst

def get_concat_h(im1, im2):
    dst = Image.new('RGB', (230, 230), color = (255,255,255) )
    dst.paste(im1, (20, 5))
    dst.paste(im2, (0, 185))
    color = "black"
    border =(1, 1, 1, 1)
    dst_border = ImageOps.expand(dst, border=border, fill=color)
    return dst_border
    

def create_qr(data):
    qr = qrcode.QRCode(version = 3, box_size = 6, border = 1)
    qr.add_data(data)
    qr.make(fit = True)
    img_qr = qr.make_image(fill_color = 'black', back_color = 'white')
    return img_qr 


def create_number(data):
    img_number = Image.new('RGB', (230, 50), color = (255,255,255))
    font2 = ImageFont.truetype(r'Roboto-Black.ttf', 34) 
    d = ImageDraw.Draw(img_number)
    d.text((115,25), data,font = font2,align='center', fill=(0,0,0), anchor="mm")
    return img_number 




def create_pdf():
    pdf = FPDF('P', 'mm', (23, 23))
    path = "letters/"
    rows=[]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        rows.append(os.path.join(path,f))
    #print(rows)
    rows.sort()
    for row in rows:
        pdf.add_page() #add a page first
        pdf.image(row,x=0.5,y=0.5,w=22, h= 22)

    pdf.output("barcode.pdf", "F")

    

def send_multiple_barcode_pdf(from_barcode,to_barcode):
    #print (len(df))
    #print (df)


    imgs = []
    path = "letters/"
    print("datareceived: "+from_barcode+", "+to_barcode)

    for i in  range(int(from_barcode),int(to_barcode)+1,1):
        print(i)

        for j in range(1):
            data = i
            get_concat_h(create_qr(str(i)),create_number(str(i))).save("letters/letter"+str(i).zfill(2)+".png")
            print(i)
        for f in os.listdir(path):
            ext = os.path.splitext(f)[1]
            imgs.append(os.path.join(path,f))
        imgs.sort()
        print(imgs)

    create_pdf()
    for root, dirs, files in os.walk('letters'):
        for f in files:
                os.unlink(os.path.join(root, f))
        for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        
    for root, dirs, files in os.walk('rows'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    path="barcode.pdf"

    return path
    
    

