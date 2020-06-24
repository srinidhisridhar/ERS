from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import nltk 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text



def appender(d):
    l=[]
    l.append(d['class 10'])
    l.append(d['class 12'])
    l.append(d['GPA '])
    l.append(d['Score_ml'])
    l.append(d['Score_cs'])
    l.append(d['Score_prog'])
    l.append(d['Score_swd'])
    l.append(d['PML'])
    l.append(d['PSWD'])
    l.append(d['PCS'])
    l.append(d['PProg'])
    l.append(d['ML'])
    l.append(d['SWD'])
    l.append(d['Prog'])
    l.append(d['CS'])
    l.append(d['GEN_PROJ'])
    l.append(d['GEN_INT'])
    for i in range(len(l)):
        l[i]=float(l[i])
    return l

def preprocess(arr):
    #print(arr)
    d={}
    flag=0
    flag2=0
    d['CSWD']=0
    d['CML']=0
    d['CCS']=0
    for i in range(len(arr)):
        if(arr[i]=='class 10'):
            d[arr[i]]=arr[i+1]
        if(arr[i]=='class 12'):
            d[arr[i]]=float(arr[i+1])
        if(arr[i]=='GPA ' and flag==0):
            d[arr[i]]=float(arr[i+1])
            flag=1
        if(arr[i]=='Experience'):
            d['ML']=arr[i+1]
            d['SWD']=arr[i+2]
            d['CS']=arr[i+3]
            if(d['ML']==0 and d['SWD']==0 and d['CS']==0):
                d['Prog']==1
            else:
                d['Prog']=0
        if(arr[i]=='Projects'):
            d['PML']=arr[i+1]
            d['PSWD']=arr[i+2]
            d['PCS']=arr[i+3]
            if(d['PML']==0 and d['PSWD']==0 and d['PCS']==0):
                d['PProg']==1
            else:
                d['PProg']=0
        if(arr[i]=='Courses' and flag2==0):
            flag2=1
            d['CML']=arr[i+1]
            d['CSWD']=arr[i+2]
            d['CCS']=arr[i+3]
            if(d['CML']==0 and d['CSWD']==0 and d['CCS']==0):
                d['CProg']=1
            else:
                d['CProg']=0
        if(arr[i]=='GEN_INT'):
            d[arr[i]]=arr[i+1]
        if(arr[i]=='GEN_PROJ'):
            d[arr[i]]=arr[i+1]      
    if(d['GEN_PROJ']==0):
        d['GEN_PROJ']+=1
    if(d['GEN_INT']==0):
        d['GEN_INT']+=1


    if(d['CML']>3):
        d['Score_ml']=100
    elif(d['CML']>1):
        d['Score_ml']=95
    elif(d['CML']==1):
        d['Score_ml']=90
    else:
        d['Score_ml']=0

    if(d['CSWD']>3):
        d['Score_swd']=100
    elif(d['CSWD']>1):
        d['Score_swd']=95
    elif(d['CSWD']==1):
        d['Score_swd']=90
    else:
        d['Score_swd']=0

    if(d['CCS']>3):
        d['Score_cs']=100
    elif(d['CCS']>1):
        d['Score_cs']=95
    elif(d['CCS']==1):
        d['Score_cs']=90
    else:
        d['Score_cs']=0

    if(d['Score_cs']==0 and d['Score_ml']==0 and d['Score_swd']==0):
        d['Score_prog']=95
    else:
        d['Score_prog']=80
    l=[]
    l=appender(d)
    return l


def convertAll(filename):
    text=convert_pdf_to_txt(os.path.join('cvs/', filename))
    tokens = word_tokenize(text)
    arr=[]
    a=[]
    keywords = ['Class','HSLC','class','Std','Standard','Grade',"SSLC"]
    for i in tokens:
        if i in [":",";",",",".","·"]:
            tokens.remove(i)
    for i in range(len(tokens)):
        if tokens[i] in keywords:
            if tokens[i] in {'Std','Standard'}:
                i=i-1
            else:
                i=i+1
            if tokens[i]=="X" or tokens[i]=="10":
                if tokens[i+1] in {'Std','Standard'}:
                    i=i+2
                else:
                    i=i+1
                arr.append(tokens[i])    
                if float(tokens[i])<=10.0:
                    arr.append("class 10")
                    arr.append(float(tokens[i])*10)
                if float(tokens[i])>100.0:
                        arr.append("class 10")
                        arr.append(float(tokens[i])/5)
                if tokens[i+1]=="%":
                    arr.append("class 10")
                    arr.append(tokens[i])
                elif len(tokens[i])>6:
                    a=tokens[i].split('/')
                    arr.append("class 10")
                    arr.append((float(a[0])/float(a[1]))*100)
            if tokens[i]=="XII" or tokens[i]=="12":
                if tokens[i+1] in {'Std','Standard'}:
                    i=i+2
                else:
                    i=i+1
                if float(tokens[i])<=500.0 and float(tokens[i])>100.0 :
                            arr.append("class 12")
                            arr.append(float(tokens[i])/5)
                if float(tokens[i])>500.0:
                            arr.append("class 12")
                            arr.append(float(tokens[i])/12)
                if tokens[i+1]=="%":
                            arr.append("class 12")
                            arr.append(tokens[i])
                elif len(tokens[i])>6:
                    a=tokens[i].split('/')
                    arr.append("class 12")
                    arr.append((float(a[0])/float(a[1]))*100)
        if tokens[i] in{"GPA","CGPA"}:
            arr.append("GPA ")
            arr.append(tokens[i+1])

    kw=["Courses","Projects","Experience","INTERN","Internships"]
    web=['develop','web','software','Web','Software','Development']
    mach=['Machine','machine','Deep','deep','Neural','neural','NLP']
    cyber=['Cyber','cyber','security','Security']
    for i in range(len(tokens)):
        countml=0
        countweb=0
        countsec=0
        if tokens[i] in kw:
            arr.append(tokens[i])
            for j in range(i+1,len(tokens)):
                if tokens[j] in kw:
                    break
                else:    
                    if(tokens[j] in mach):
                        countml+=1 
                    if(tokens[j] in web): 
                        countweb+=1      
                    if(tokens[j] in cyber):
                        countsec+=1
            if countml>3:
                countml=3
            if countweb>3:
                countweb=3
            if countsec>3:
                countsec=3
            arr.append(countml)
            arr.append(countweb)
            arr.append(countsec)
            
    #print(list(dict.fromkeys(arr)))


    for i in arr:
        if i=="Projects":
            arr.append('GEN_PROJ')
            arr.append('2')
            
        elif i=="Experience":
            arr.append('GEN_INT')
            arr.append('1')
    print(arr)
    arr=preprocess(arr)
    return arr
