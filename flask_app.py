
from flask import Flask, jsonify, make_response, request, Response, session, send_file
from flask_cors import CORS, cross_origin
import pandas as pd
import shutil
from createqr_multiple import send_multiple_pdf
from createqr_single import send_single_pdf
from createbarcode_single import send_single_barcode_pdf
from createbarcode_multiple import send_multiple_barcode_pdf
from createvoucher import send_voucher
from create_number import send_number_pdf



async_mode = None
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/create_barcode', methods = ["POST"])
def create_barcode():
   if request.method == 'POST':
      
      json_data = request.json
      print(json_data)
      from_barcode =json_data.get("from")
      to_barcode =json_data.get("to")
      print(from_barcode)
      print(to_barcode)
      
      if (from_barcode==to_barcode):
         path=send_single_barcode_pdf(from_barcode)
      else:
         path=send_multiple_barcode_pdf(from_barcode,to_barcode)
    
      return send_file(path, as_attachment=True)   

    
@app.route('/create_single_label', methods = ["POST"])
def create_single_label():
   if request.method == 'POST':
    
    json_data = request.json
    # a_value = json_data["a_key"]
    print(json_data)
    qr=json_data.get("Floor")+"-"+json_data.get("Shelf")+"-"+json_data.get("Column")+"-"+json_data.get("lRow")
    print(qr)
    # print("1")
    # #path = functions_disabled_products.kikkaboo()
    # #print(path)
    # #return send_file(path, as_attachment=True)
    # print(type(json_data))
    # tmp=json_data.items()
    # print(tmp)
    # qr = {str(value) for key, value in tmp}
    # print("qr data: "+ str(qr))
    path = send_single_pdf(str(qr))
    #path="shelfs.pdf"
    return send_file(path, as_attachment=True)    

@app.route('/create_voucher', methods = ["POST"])
def create_voucher():
   if request.method == 'POST':
    
    json_data = request.json
    print(json_data)
    #voucher=json_data.get("Name")+"-"+json_data.get("Shelf")+"-"+json_data.get("Column")+"-"+json_data.get("lRow")
    path= send_voucher(json_data)
    
    return send_file(path, as_attachment=True) 


@app.route('/upload_multiple_shelfs_file', methods = ["POST"])
def upload_excludeproducts():
   if request.method == 'POST':
        #print(request.f['file']) 
        print(request.files)
        f = request.files['file']
        f.save('shelfs.xlsx')
        print("upload")
        path=send_multiple_pdf()
        print(path)
        return send_file(path, as_attachment=True)  



@app.route('/upload_multiple_numbers_file', methods = ["POST"])
def upload_numbers():
   if request.method == 'POST':
        #print(request.f['file']) 
        print(request.files)
        f = request.files['file']
        f.save('numbers.xlsx')
        print("upload")
        path=send_number_pdf()
        print(path)
        return send_file(path, as_attachment=True)  


@app.route('/downloadtemplates', methods = ["POST"])
def download_templates():
   if request.method == 'POST':
        #print(request.f['file']) 
        path = "Templates.zip"
        return send_file(path, as_attachment=True) 





app.config['DEBUG'] = True
app.run(host="localhost", port=8001)
