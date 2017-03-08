import strings as STR
import run_pipeline as DMP
from Peptide import run_peptide
from Protein import run_protein
import random
import string
import time
import csv
import ast
import os
import zipfile



def CallAnalyze(pwmfile,domainfile,session):
    if type(pwmfile) == list:
        i=0
        print 'type : list'
        print 'file name',str(pwmfile)
        options = {'domain': "cache/"+domainfile, 'p-value': 1e-05}
        gen_data = run_peptide.setup_peptide()
        cel_data = run_protein.setup_protein()
        for filename in pwmfile:
            i+=1
            DMP.pwm_runner("cache/"+session+"/" + filename, options['domain'], options['p-value'],"cache/"+session+"/result-"+filename, gen_data, cel_data)
        print 'analyze finished!'
        return 
    else:
        print 'type : single'
        options = {'output': "cache/"+session+"/result-"+pwmfile, 'pwm': "cache/"+session+"/"+pwmfile, 'domain': "cache/"+domainfile, 'p-value': 1e-05}
    DMP.process_options(options)
    print 'analyze finished!'

def formateData(rawdata):
    rawdata = rawdata.replace("\n","<br/>")
    return rawdata

def generateTable(rawdata):
    tablestr = STR.TABLE_HEAD
    piecedata = rawdata.split("\n")
    #piecedata[0] is table head,we're hard coding it in strings,so we delete it here
    del piecedata[0]
    # there are 10 columns in this table
    for data in piecedata:
        dseq = data.split("\t")
        if len(dseq) >=2:
            pstr = STR.TABLE_C_START + dseq[0] + STR.TABLE_C_REP + dseq[1] + STR.TABLE_C_REP + dseq[2] + \
            STR.TABLE_C_REP + dseq[3] + STR.TABLE_C_REP + dseq[4] + STR.TABLE_C_REP + dseq[5] + STR.TABLE_C_REP + dseq[6] +\
            STR.TABLE_C_REP + dseq[7] + STR.TABLE_C_REP + dseq[8] + STR.TABLE_C_REP + dseq[9] + STR.TABLE_C_END
            tablestr += pstr
    tablestr += STR.TABLE_TAIL
    return tablestr
    
#generate table via file list
def generateTableL(filelist,session):
    TABSTR = ""
    BUTTONSTR = ""
    xid = 0
    print 'start process file in filelist...'
    firstshow = True
    for pfilename in filelist:
        print 'processing...'
        f = open("cache/"+session+"/result-"+pfilename)
        rawdata = f.read()
        f.close()
        tablestr = STR.TABLE_HEAD
        piecedata = rawdata.split("\n")
        #piecedata[0] is table head,we're hard coding it in strings,so we delete it here
        del piecedata[0]
        # there are 10 columns in this table
        for data in piecedata:
            dseq = data.split("\t")
            if len(dseq) >=2:
                pstr = STR.TABLE_C_START + dseq[0] + STR.TABLE_C_REP + dseq[1] + STR.TABLE_C_REP + dseq[2] + \
                STR.TABLE_C_REP + dseq[3] + STR.TABLE_C_REP + dseq[4] + STR.TABLE_C_REP + dseq[5] + STR.TABLE_C_REP + dseq[6] +\
                STR.TABLE_C_REP + dseq[7] + STR.TABLE_C_REP + dseq[8] + STR.TABLE_C_REP + dseq[9] + STR.TABLE_C_END
                tablestr += pstr
        tablestr += STR.TABLE_TAIL
        if firstshow == True:
            tablestr = STR.DIV_HEAD + str(xid) + STR.DIV_A + tablestr + STR.DIV_TAIL
            firstshow = False
        else:
            tablestr = STR.DIV_HEAD_HIDE + str(xid) + STR.DIV_A + tablestr + STR.DIV_TAIL
        TABSTR += tablestr
        BUTTONSTR += STR.BUTTON_HEAD + str(xid) + STR.BUTTON_A + str(xid) + STR.BUTTON_B + pfilename[pfilename.find('P'):] + STR.BUTTON_TAIL
        xid+=1
    print 'table made up.'
    return TABSTR,BUTTONSTR,xid

#gernerate session id for better organised data
def generateSessionID():
    x = ''.join(random.sample(string.ascii_letters+string.digits, 32))
    x += ''.join(random.sample(string.ascii_letters+string.digits, 16))
    x += str(time.time()).replace('.','') #add time in case of the same id
    return  x

#save the relationship of a session id and uploaded files
def saveinfo(data):
    f = open("sessionmap.csv","a+")
    csvw = csv.writer(f)
    csvw.writerows([data])
    f.close()

#read certain data that match the session id
def readinfo(sessionid):
    f = open("sessionmap.csv","r")
    csvr = csv.reader(f)
    for data in csvr:
        if data[0] == sessionid:
            f.close()
            data[1] = ast.literal_eval(data[1])
            return data
    f.close()
    return ["NOT_FOUND"]
 
#used for pack session 
def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')    
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)    
            zipf.write(pathfile, arcname)
    zipf.close()
