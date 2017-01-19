from flask import Flask
import os
from flask import render_template,request, redirect,make_response,send_file,request
from werkzeug import secure_filename
import analyze
import datetime


app = Flask(__name__)


UPLOAD_FOLDER = 'cache/'
ALLOWED_EXTENSIONS = set(['txt','',' '])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result')
@app.route('/result/<pocessid>')
def result(pocessid=""):
    if pocessid == "":
        return render_template('result.html',NAME="pwmfilename",RESULT="tablestr",FILENAME="pfilename")
    try:
        print 'pocessid=',pocessid
        f = open("cache/output/"+pocessid)
        data = f.read()
        f.close()
        print 'file found!'
        tablestr = analyze.generateTable(data)
        return render_template('result.html',NAME=pocessid[19:],RESULT=tablestr,FILENAME=pocessid,PWMFILE=pocessid,DOMAINFILE=pocessid[0:19]+"domain.txt",PLK="/result/"+pocessid,CURSHOW="div_1")
        #return render_template('result.html',NAME=pwmfilename,RESULT=tablestr,FILENAME=pfilename,PWMFILE=pfilename,DOMAINFILE=dfilename,PLK="/result/"+pfilename)
    except Exception as e:
        return e.message
        return "ERROR: Invaild ID"

@app.route('/download/<ftype>/<filename>')
def downloadresult(ftype,filename):
    if ftype == "result":
        try:
            response = make_response(send_file("cache/output/"+filename))
            response.headers["Content-Disposition"] = "attachment; filename=result_" + filename + ".txt;"
            return response
        except:
            return "ERROR: File Not Found"
    elif ftype == "raw":
        try:
            response = make_response(send_file("cache/"+filename))
            response.headers["Content-Disposition"] = "attachment; filename=src_" + filename + ".txt;"
            return response
        except:
            return "ERROR: File Not Found"
    elif ftype == "test":
        response = make_response(send_file("cache/test/TestDataset.zip"))
        response.headers["Content-Disposition"] = "attachment; filename=TestDataset.zip;"
        return response
    return "ERROR: Unknow Error"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print("check request type")
    if request.method == 'POST':
        print("querying file")
        pwmfilelist = request.files.getlist("file[]")
        #pwmfile = request.files['pwmfile']
        dofile = request.files['domainfile']
        #if pwmfile and allowed_file(pwmfile.filename):
        if True:
            #secure the filename
            pwmfilenamelist = []
            for pwmfile in pwmfilelist:
                pwmfilenamelist.append(secure_filename(pwmfile.filename))
            dofilename = secure_filename(dofile.filename)
            timesuffix = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            #make file name unique by adding time
            i=0
            for pwmfilename in pwmfilenamelist:
                pwmfilenamelist[i] = timesuffix + pwmfilename
                i+=1
            dfilename = timesuffix + dofilename
            #save file for pocess
            i=0
            for file in pwmfilelist:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], pwmfilenamelist[i]))
                i+=1
            dofile.save(os.path.join(app.config['UPLOAD_FOLDER'], dfilename))
            analyze.CallAnalyze(pwmfilenamelist,dfilename)
            #after operation above,data had been put into cache/output/pwmfilename
            tablestr,buttonstr,xid = analyze.generateTableL(pwmfilenamelist)
            if xid == 1:
                buttonstr = ""
            return render_template('result.html',NAME=pwmfilename,RESULT=tablestr,FILENAME="pfilename",PWMFILE="pfilename",DOMAINFILE=dfilename,PLK="/result/"+"pfilename",CURSHOW="div_1",BUTTONSTR=buttonstr)
    print("error: not POST")
    return "YOU ARE NOT ALLOWED TO VISIT THIS PAGE"

if __name__ == '__main__':
    #app.run(host='172.31.26.26',port=1996,debug=True)
    app.run(debug=True)
