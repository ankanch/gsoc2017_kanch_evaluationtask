import strings as STR
import run_pipeline as DMP
from Peptide import run_peptide
from Protein import run_protein



def CallAnalyze(pwmfile,domainfile):
    if type(pwmfile) == list:
        i=0
        print 'type : list'
        print 'file name',str(pwmfile)
        options = {'domain': "cache/"+domainfile, 'p-value': 1e-05}
        gen_data = run_peptide.setup_peptide()
        cel_data = run_protein.setup_protein()
        for filename in pwmfile:
            i+=1
            DMP.pwm_runner("cache/" + filename, options['domain'], options['p-value'],"cache/output/"+filename, gen_data, cel_data)
        print 'analyze finished!'
        return 
    else:
        print 'type : single'
        options = {'output': "cache/output/"+pwmfile, 'pwm': "cache/"+pwmfile, 'domain': "cache/"+domainfile, 'p-value': 1e-05}
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
def generateTableL(filelist):
    TABSTR = ""
    BUTTONSTR = ""
    xid = 0
    print 'start process file in filelist...'
    firstshow = True
    for pfilename in filelist:
        print 'processing...'
        f = open("cache/output/"+pfilename)
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
    return TABSTR,BUTTONSTR,xid
