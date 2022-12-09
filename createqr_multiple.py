import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps
from fpdf import FPDF
import pandas as pd
import os, os.path
import shutil




def concat_sidebyside(imgs):
    im1 = Image.open(imgs[0])
    dst = Image.new('RGB', (1386, 230))
    dst.paste(im1, (0, 0))
    return dst

def get_concat_h(im1, im2):
    dst = Image.new('RGB', (460, 230))
    im1=im1.resize((230,230))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (230, 0))
    color = "black"
    border =(1, 1, 1, 1)
    dst_border = ImageOps.expand(dst, border=border, fill=color)
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
    path = "letters/"
    rows=[]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        rows.append(os.path.join(path,f))
    #print(rows)
    rows.sort()
    for row in rows:
        pdf.add_page()
        pdf.image(row,x=1,y=1,w=60, h= 27)

    created_path="multiple_shelfs.pdf"
    pdf.output(created_path, "F")
    return created_path

    
def send_multiple_pdf():
    df = pd.read_excel("shelfs.xlsx",engine='openpyxl')
    #print (len(df))
    #print (df)


    imgs = []
    path = "letters/"

    for i in  range(0,len(df),1):
        print(i)

        for j in range(1):
            data = df.at[i+j,"Shelfs"]
            get_concat_h(create_qr(data),create_number(data)).save("letters/letter"+str(i+j).zfill(2)+".png")
            print(data)
        for f in os.listdir(path):
            ext = os.path.splitext(f)[1]
            imgs.append(os.path.join(path,f))
        imgs.sort()
        print(imgs)

    created_path = create_pdf()
    print("returned")
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
    return created_path
    

