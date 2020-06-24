from flask import Flask, render_template, request
import joblib
import pickle
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
import converter as converter

app = Flask(__name__)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

UPLOAD_FOLDER = 'cvs/'
ALLOWED_EXTENSIONS = {'pdf'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predicter(arr):
    model_ml=joblib.load(open('models/model_ml.sav','rb'))
    model_cs=joblib.load(open('models/model_cs.sav','rb'))
    model_swd=joblib.load(open('models/model_swd.sav','rb'))
    model_prog=joblib.load(open('models/model_prog.sav','rb'))
    model_gen=joblib.load(open('models/model_gen.sav','rb'))
    data=[]
    data.append(arr)
    print(data)
    ans=[]
    ans.append(model_ml.predict(data)[0])
    ans.append(model_cs.predict(data)[0])
    ans.append(model_swd.predict(data)[0])
    ans.append(model_prog.predict(data)[0])
    ans.append(model_gen.predict(data)[0])
    for i in range(len(ans)):
        ans[i]=round(ans[i],2)
        while(ans[i]>100):
            ans[i]-=5
    return ans

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('upload.html')

@app.route('/result', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            arr=[]
            arr=converter.convertAll(filename)
            res=predicter(arr)
            return render_template("result.html",result=res)
    return redirect(url_for('home'))


    
