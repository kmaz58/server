import qrcode
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageOps
from fpdf import FPDF
import pandas as pd
import os, os.path
import shutil
import barcode







def get_concat_h(im1, im2):
    dst = Image.new('RGB', (460, 230),color="white")
    dst.paste(im1, (0, 0))
    im2.resize((460,115))
    dst.paste(im2, (0,115))
    border =(1, 1, 1, 1)
    dst_border = ImageOps.expand(dst, border=border)
    return dst_border
    

def create_qr(data):

    number = str(data)
    ean = barcode.codex.Code39(number, writer=barcode.writer.ImageWriter(), add_checksum=False)
    image = ean.render()
    rs= image.resize((460,230), resample= PIL.Image.NEAREST)

    return rs 


def create_number(data):
    W,H= (460,115)
    img_number = Image.new('RGB', (W, H), color = (255,255,255))
    font2 = ImageFont.truetype(r'Roboto-Black.ttf', 100) 
    d = ImageDraw.Draw(img_number)
    w, h = d.textsize(data)
    d.text(((W-w)/2,(H-h)/2),data,font = font2,anchor="mm", align='center', fill=(0,0,0))
    
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

    
def send_single_barcode_pdf(data):
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
    
    

