from flask import Flask
import os
from flask import render_template,request, redirect,make_response,send_file,request
from werkzeug import secure_filename
import analyze


app = Flask(__name__)


UPLOAD_FOLDER = 'cache/'
ALLOWED_EXTENSIONS = set(['txt','',' '])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result')
@app.route('/result/<session>')
def result(session=""):
    if session == "":
        return render_template('result.html',NAME="pwmfilename",RESULT="tablestr",FILENAME="pfilename")
    try:
        info = analyze.readinfo(session)
        print 'session=',session,'info=',info
        tablestr,buttonstr,xid = analyze.generateTableL(info[1],session)
        if xid == 1:
            buttonstr = ""
        #check if it is mulitifile or single file .then render the result page in different ways
        print("history result load done.")
        if len(info[1]) == 1:
            #single file 
            return render_template('result.html',NAME=info[1][0],RESULT=tablestr,PLK="/result/"+session,SHOWHEAD="none",SESSION=session)
        #multifile  pwmfilelist[0].filename
        return render_template('result.html',NAME=info[1][0],RESULT=tablestr,PLK="/result/"+session,CURSHOW="div_0",BUTTONSTR=buttonstr,SESSION=session)
    except Exception as e:
        return e.message

@app.route('/download/<ftype>/<session>')
def downloadresult(ftype,session):
    if ftype == "result":
        try:
            analyze.make_zip("cache/"+session,"cache/output/"+session+".zip")
            response = make_response(send_file("cache/output/"+session+".zip"))
            response.headers["Content-Disposition"] = "attachment; filename=" + session + ".zip;"
            return response
        except Exception as e:
            return e.message
    elif ftype == "domain":
        response = make_response(send_file("cache/domain.txt"))
        response.headers["Content-Disposition"] = "attachment; filename=domain.txt;"
        return response
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
        use_built_in = request.form['hid1']
        print("wether to use built-in domain data:",use_built_in)
        dofile = None
        UBI = True
        if use_built_in == 'false':
            UBI = False
            dofile = request.files['domainfile']
        #if pwmfile and allowed_file(pwmfile.filename):
        if True:
            #secure the filename
            pwmfilenamelist = []
            for pwmfile in pwmfilelist:
                pwmfilenamelist.append(secure_filename(pwmfile.filename))
            dofilename = ""
            if UBI == False:
                dofilename = secure_filename(dofile.filename)
            #generate session id for organising the upload files
            #all files that upload are in the same session folder
            session = analyze.generateSessionID()
            os.makedirs(app.config['UPLOAD_FOLDER']+"/"+session)
            #save info to the sessionmap.csv
            dfilename = dofilename
            if UBI == False:
                #Structure: [session-id,[pwm-file-list],domain-file]
                analyze.saveinfo([session,pwmfilenamelist,dofilename])
            else:
                analyze.saveinfo([session,pwmfilenamelist,"UBI"])
            #save file for pocess
            #we have to save a session id for future lookup results and download results 
            #we have to save those uploaded file in a session-id named folder for analyze and organize
            i=0
            for file in pwmfilelist:
                file.save(os.path.join(app.config['UPLOAD_FOLDER']+session+"/", pwmfilenamelist[i]))
                i+=1
            if UBI == False:
                dofile.save(os.path.join(app.config['UPLOAD_FOLDER']+session+"/", dfilename))
                analyze.CallAnalyze(pwmfilenamelist,session+"/"+dfilename,session)
            else:
                analyze.CallAnalyze(pwmfilenamelist,"domain.txt",session)
            #after operation above,data had been put into cache/output/pwmfilename
            return redirect("/result/"+session)
            tablestr,buttonstr,xid = analyze.generateTableL(pwmfilenamelist,session)
            print("analyze session done.")
            if xid == 1:
                buttonstr = ""
            #check if it is mulitifile or single file .then render the result page in different ways
            if len(pwmfilenamelist) == 1:
                #single file 
                return render_template('result.html',NAME=pwmfilelist[0].filename,RESULT=tablestr,FILENAME=pwmfilenamelist[0],PLK="/result/"+session,SHOWHEAD="none",SESSION=session)
            #multifile  pwmfilelist[0].filename
            return render_template('result.html',NAME=pwmfilelist[0].filename,RESULT=tablestr,FILENAME="pfilename",PLK="/result/"+session,CURSHOW="div_0",BUTTONSTR=buttonstr,SESSION=session)
    print("error: not POST")
    return "YOU ARE NOT ALLOWED TO VISIT THIS PAGE"

if __name__ == '__main__':
    app.run(host='138.68.4.76',port=1996,debug=True)
    #app.run(debug=True)
