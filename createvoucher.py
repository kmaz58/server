import qrcode
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageOps
from fpdf import FPDF
import pandas as pd
import os, os.path
import shutil
import barcode





def create_voucher(json_data):
    img_number = Image.new('RGB', (620, 2480), color = (255,255,255))
    font = ImageFont.truetype(r'Roboto-Black.ttf', 20)
    font2 = ImageFont.truetype(r'Roboto-Black.ttf', 15) 
    d = ImageDraw.Draw(img_number)
    d.text((0,0), json_data.get("Name"),font = font,align='center', fill=(0,0,0))
    d.text((0,25), json_data.get("Telephone"),font = font,align='center', fill=(0,0,0))
    d.text((0,50), json_data.get("Zip"),font = font,align='center', fill=(0,0,0))
    d.text((0,75), json_data.get("Region"),font = font,align='center', fill=(0,0,0))
    d.text((0,100), json_data.get("Comment"),font = font2,align='center', fill=(0,0,0))
    d.text((0,120), json_data.get("Comment"),font = font2,align='center', fill=(0,0,0))
    d.text((0,152), "Αντικαταβολή:",font = font2,align='center', fill=(0,0,0))
    d.text((110,150), json_data.get("Cod"),font = font,align='center', fill=(0,0,0))
    




    
    return img_number




def create_pdf():
    pdf = FPDF('P', 'mm', (248, 62))
    pdf.add_page() #add a page first
    path = "vouchers/"
    voucher_list=[]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        voucher_list.append(os.path.join(path,f))
    #print(rows)
    voucher_list.sort()
    for row in voucher_list:
        pdf.image(row,x=1,y=1,w=0 , h= 0)

    pdf.output("shelfs.pdf", "F")

    
def send_voucher(json_data):
    #print (len(df))
    print (json_data)

    
    imgs = []
    # voucher=json_data.get("Name")+"-"+json_data.get("Telephone")+"-"+json_data.get("Address")+"-"+json_data.get("Zip")+"-"+json_data.get("Region")+"-"+json_data.get("Comment")+"-"+"-"+json_data.get("Cod")

    # print("datareceived:"+json_data)
    create_voucher(json_data).save("vouchers/voucher.png")
    create_pdf()
    
    path="shelfs.pdf"

    return path
    
    

