from numpy import dstack
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps
from fpdf import FPDF
import pandas as pd
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
    dst = Image.new('RGB', (460, 230),color="white")
    im1=im1.resize((230,230))
    dst.paste(im1, (round((230-(im1.width))/2), 0))
    dst.paste(im2, (230, 0))
    border =(1, 1, 1, 1)
    dst_border = ImageOps.expand(dst, border=border)
    return dst_border
    

def create_qr(data):
    qr = qrcode.QRCode(version = 1, box_size = 8, border = 2)
    qr.add_data(data)
    qr.make(fit = True)
    img_qr = qr.make_image(fill_color = 'black', back_color = 'white')
    return img_qr 


def create_number(data):
    img_number = Image.new('RGB', (230, 230), color = (255,255,255))
    font = ImageFont.truetype(r'Roboto-Black.ttf', 150) 
    font2 = ImageFont.truetype(r'Roboto-Black.ttf', 30) 
    d = ImageDraw.Draw(img_number)
    d.text((25,0), data[-3],font = font,align='center', fill=(0,0,0))
    d.text((125,0), data[-1],font = font,align='center', fill=(0,0,0))
    d.text((20,190), data,font = font2,align='center', fill=(0,0,0))
    return img_number 




def create_pdf():
    pdf = FPDF('P', 'mm', (62, 29))
    pdf.add_page() #add a page first
    path = "letters/"
    rows=[]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        rows.append(os.path.join(path,f))
    #print(rows)
    rows.sort()
    for row in rows:
        pdf.image(row,x=1,y=1,w=60, h= 27)

    pdf.output("shelfs.pdf", "F")

    
def send_single_pdf(data):
    #print (len(df))
    #print (df)


    imgs = []
    path = "letters/"
    print("datareceived: "+data)

    get_concat_h(create_qr(data),create_number(data)).save("letters/letter.png")


    

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

    path="shelfs.pdf"

    return path
    
    

