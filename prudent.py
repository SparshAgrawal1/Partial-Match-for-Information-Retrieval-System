#importing packages
#all changed references are based on line numbers from the original Prudent_python.py file.
import pandas as pd 
import numpy as np
import pickle as pkl
import nltk
nltk.download('punkt')
import random

gloabl_df = pd.read_csv('../Planning-master/PRUDENT/data/unspsc_dataset.csv')

#added RL Epsilon Decay (Random selection)

def extract_query(query, dir_df, dir_name):
    if dir_name == 'unspsc':

        c1 = " ".join(dir_df['Commodity Title'].values.tolist())
        c2 = " ".join(dir_df['Family Title'].values.tolist())
        c3 = " ".join(dir_df['Class Title'].values.tolist())
        c4 = " ".join(dir_df['Segment Title'].values.tolist())
        c5 = "" + c1 +" "+ c2 +" "+ c3 +" "+ c4
        temp = nltk.word_tokenize(c5)
        temp = [word.lower() for word in temp if len(word)>2 and word!= 'and' and word!='other']
        temp = " ".join(temp)

    elif dir_name == 'icd10':

        check  = ""
        for i in dir_df.keys():
            check = check + i + " "
            temp = dir_df[i][1]
            try:
                temp.keys()
                for j in temp.keys():
                    check = check + j + " "
                    temp2 = dir_df[i][1][j][1]
                    try:
                        temp2.keys()
                        for k in temp2.keys():
                            check = check + k + " "
                            temp3 = dir_df[i][1][j][1][k][1]
                            try:
                                temp3.keys()
                                for l in temp3.keys():
                                    check = check + l + " "
                            except AttributeError:
                                check = check + temp3 + " "
                                continue
                    except AttributeError:
                        check = check + temp2 + " "
                        continue
            except AttributeError:
                check = check + temp + " "
                continue
        
        temp = nltk.word_tokenize(check)
        temp = [word.lower() for word in temp if len(word)>2 and word!= 'and' and word!='other']
        temp = " ".join(temp)
    
    tkquery = nltk.word_tokenize(query)
    tkquery = [i.lower() for i in tkquery if i!='want' and i!='query' and i!='code' and i!='the' and i!='about' and i!='code' and i!='tell' and i!='for'and i!='more' and len(i)>2 and i!='info' and i!= 'and' and i!= 'other'and i!='know' and i!='information']
    tkquery = list(set(tkquery))
    match = list()
    for i in tkquery:
        if(temp.lower().count(i.lower())>0):
            match.append(i.lower())
    send = list()
    for i in nltk.word_tokenize(query):
        if(i.lower() in match):
            send.append(i.lower())
    if(len(send)>1):
        return " ".join(send)
    elif(len(send)==1):
        return send[0]
    else:
        return ""

def match_score( query, dir_df, dir_name):
    if dir_name == 'unspsc':

        c1 = " ".join(dir_df['Commodity Title'].values.tolist())
        c2 = " ".join(dir_df['Family Title'].values.tolist())
        c3 = " ".join(dir_df['Class Title'].values.tolist())
        c4 = " ".join(dir_df['Segment Title'].values.tolist())
        c5 = "" + c1 +" "+ c2 +" "+ c3 +" "+ c4
        temp = nltk.word_tokenize(c5)
        temp = [word.lower() for word in temp if len(word)>2 and word!= 'and' and word!='other']
        temp = " ".join(temp)

    elif dir_name == 'icd10':

        check  = ""
        for i in dir_df.keys():
            check = check + i + " "
            temp = dir_df[i][1]
            try:
                temp.keys()
                for j in temp.keys():
                    check = check + j + " "
                    temp2 = dir_df[i][1][j][1]
                    try:
                        temp2.keys()
                        for k in temp2.keys():
                            check = check + k + " "
                            temp3 = dir_df[i][1][j][1][k][1]
                            try:
                                temp3.keys()
                                for l in temp3.keys():
                                    check = check + l + " "
                            except AttributeError:
                                check = check + temp3 + " "
                                continue
                    except AttributeError:
                        check = check + temp2 + " "
                        continue
            except AttributeError:
                check = check + temp + " "
                continue
        
        temp = nltk.word_tokenize(check)
        temp = [word.lower() for word in temp if len(word)>2 and word!= 'and' and word!='other']
        temp = " ".join(temp)
    
    tkquery = nltk.word_tokenize(query)
    tkquery = [i.lower() for i in tkquery if i!='want' and i!='query' and i!='code' and i!='the' and i!='about' and i!='code' and i!='tell' and i!='for'and i!='more' and len(i)>2 and i!='info' and i!= 'and' and i!= 'other'and i!='know' and i!='information']
    score = 0
    tkquery = list(set(tkquery))
    match = list()
    for i in tkquery:
        if(temp.lower().count(i.lower())>0):
            score = score + 1
            match.append(i.lower())
    send = list()
    if(dir_name=='unspsc'):
        for i in nltk.word_tokenize(query):
            if(i.lower() in match):
                send.append(i.lower())
        if(len(send)>1):
            return score, " ".join(send) 
        elif(len(send)==1):
            return score, send[0]
        else:
            return score, ""
    elif(dir_name == 'icd10'):
        #return score, query.lower().replace("i want the code for ","")
        return score, " ".join(tkquery)

def query_dirFinder( query):
    dir_df1 = pd.read_csv("../Planning-master/PRUDENT/data/unspsc_dataset.csv")
    check1, q1 = match_score( query, dir_df1,'unspsc')
    dir_df2 = pkl.load(open("../Planning-master/PRUDENT/data/icd10_dict1.pkl","rb"))
    check2, q2 = match_score( query, dir_df2,'icd10')
    #print(check1, check2)
    #raise KeyboardInterrupt
    q = ""
    if(check1>0 and check2>0 and check1==check2):
        return "noidea", q
    elif(check1>check2):
        return "UNSPSC", q1
    elif(check2>check1):
        return "ICD-10", q2
    elif(check1>0):
        return "UNSPSC", q1
    elif(check2>0):
        return "ICD-10", q2
    else:
        return "RandomChitChat", q

def reward_func(query, dir_name):
    reward = 0
    if(dir_name=='UNSPSC'):
        dir_df = pd.read_csv("../Planning-master/PRUDENT/data/unspsc_dataset.csv")
        check = match_score( query, dir_df,'unspsc')
        reward += check
    elif(dir_name=='ICD-10'):
        dir_df = pkl.load(open("../Planning-master/PRUDENT/data/icd10_dict1.pkl","rb"))
        check = match_score( query, dir_df,'icd10')
        reward += check
    else:
        dir_df = pd.read_csv("../Planning-master/PRUDENT/data/unspsc_dataset.csv")
        check = match_score( query, dir_df,'unspsc')
        reward -= check
        dir_df = pkl.load(open("../Planning-master/PRUDENT/data/icd10_dict1.pkl","rb"))
        check = match_score( query, dir_df,'icd10')
        reward -= check

    return reward

#RL Source
def rlsource(query):
    global global_df
    check = ''
    ep_count = 0
    epsilon = 0.9
    decay = 0.1
    temp, q = query_dirFinder( query)
    checkrw = 0
    #print(temp)
    #raise KeyboardInterrupt
    if(temp=='noidea'):
        return "Match is found in both UNSPSC and ICD-10. Please choose one or enter another query to further disambiguation", False, q
        #print("Match is found in both the directories UNSPSC and ICD10. Please choose one or enter another query to further disambiguate")
        #query = input("Enter your query:\n")
        #temp = query_dirFinder( query)
    while(check != temp):
        print("\nEpoch - {}".format(ep_count))
        print("The epsilon value is: {}".format(epsilon))
        ep_count += 1
        thresh = random.uniform(0, 1)
        if thresh <= epsilon:
            check  = ''.join(random.choice(['UNSPSC','ICD-10','RandomChitChat']))
        else:
            check  = temp
        if check == temp:
            checkrw = checkrw + 10
            if(check in ['UNSPSC','ICD-10']):
                #print(check,temp)
                #raise KeyboardInterrupt
                if(check == 'UNSPSC'):
                    gloabl_df = pd.read_csv('../Planning-master/PRUDENT/data/unspsc_dataset.csv')
                    #self.unspsc = True
                    #print("Yes Did it true")
                    #raise KeyboardInterrupt
                elif(check == 'ICD-10'):
                    gloabl_df = pkl.load(open('../Planning-master/PRUDENT/data/icd10_dict1.pkl', "rb"))
                    #self.icd10 = True
                    #print("Yes Did it true")
                    #raise KeyboardInterrupt
                return "Information you are looking for is available in directory {}".format(check), True, q
            else:
                return "I am sorry. I do not understand, please rephrase your query.", False, q
        epsilon -= decay
        #check['episode_done'] = False

##changed: Deleted line 3-13. (Error no file plan0.txt found).       
#Added Flag varibale: Directory found for unambiguous query. Query input is not necessary.
flag_dir = False
print("Enter your query -")
while(flag_dir==False):
    c2=input()
    c2=c2.lower()
    if(c2=="icd10"):#changed: unspsc-> icd10
        data = pd.read_csv("unspsc_dataset.csv") 
        break

    elif(c2=="unspsc"):#changed icd10-> unspsc
        data = pd.read_csv("icd10.csv") #changed: icd_10 -> icd10
        break

    else: #changed rl to find the directory
        temp = rlsource(c2)
        print(temp)
        #raise KeyboardInterrupt
        if(temp[0].count("ICD-10")>0):
            data = pd.read_csv("unspsc_dataset.csv") 
            flag_dir = True
        elif(temp[0].count("UNSPSC")>0):
            data = pd.read_csv("icd10.csv")
            flag_dir = True
        else:
            print("I do not understand your query. \n Please re-tner the dataset you want to query.")
            #raise KeyboardInterrupt
    

f1=-1
f2=-1
f3=-1

# To distinguish the querying column and output column in case of both dataset i.e, ICD-10 and UNSPSC on the basis of dimension
if(data.shape==(94765,4)):
    f1=3
    f2=2
    f3=94765
else:
    f1=1
    f2=0
    f3=4302

#changed: Removed extra space.

if(flag_dir==False):
    print("Ask the query:")
    x = input()
else:
    x = temp[2]


# Function for searching the entire dataset
def full_search(data,pre1,pre2,words,d3,d2):
    #   Calculating the matches of the given words and mapping them to their corresponding matches
    for i in words:
        for j in range (0,f3):
            y = data.iloc[j][f1]
            if(y.lower().find(i)!=-1):
                d3[i].append(j)
    #   Calculating the matches which are common for all the words by calculating count 
    d1={}
    d2=[]
    for i in d3:
        for j in d3[i]:
            if(d1.get(j)==None):
                d1[j]=1
            else:
                d1[j]+=1
    size=len(words)
    for i,j in d1.items():
        if(j==size):
            d2.append(i)
    #   Removing the stop words and punctuations from the shortlisted matches in the dataset
    k={}
    for i in d2:
        y = data.iloc[i][f1]
        y=y.lower()
        for j in pre2:
            y=y.replace(j,'')
        y=y.split()
        # print(y)
        # Getting the count of all unique entities
        h={}
        for j in y:
            if(h.get(j)==None):
                h[j]=1
            else:
                h[j]+=1
        #Deleting the stop words
        for j in pre1:
            if(h.get(j)!=None):
                del h[j]
        #Deleting the original words on the basis on whom we shortlisted in dataset
        for j in words:
            if(h.get(j)!=None):
                del h[j]
            j = j+'s'
            if(h.get(j)!=None):
                del h[j]
        #  Storing in the common data which will be shared with all entries
        for j1,j2 in h.items():
            if(k.get(j1)==None):
                k[j1]=1
            else:
                k[j1]+=1
      
    # Sorting on the basis of their number of occurences
    k=sorted(k.items(), key=lambda x:x[1],reverse=True)
    #     If only single match is present
    if(len(d2)==1):
        return words, d2;
    else:
        
        print("Select from one of these :")
        print()
        cc=1
        for i in k:
            for j in i:
                print(cc,end=". ")
                print(j)
                cc+=1
                break
    #         print()
        print("Which one do you want to select: ")
        print()
        y=input()
        y=y.lower()
        words1=y.split(', ')
        for i in words1:
            words.append(i)
        print("----------------------")
        return words, d2

def shortlisted_search(data,pre1,pre2,words,d3,d2):
    #   Calculating the matches of the given words in d3 and mapping them to their corresponding matches
    d4=[]
    
    #   changed: Deleted code line 142-147
            
    d6=defaultdict(list)      
    for j in words:
        for i in d2:
            y=data.iloc[i][f1];
            y=y.lower()
            if(y.find(j)!=-1):
                d6[j].append(i)
    
    size=len(words)      
    #   Calculating the matches which are common for all the words by calculating count
    d7={}
    d8=[]
    for i in d6:
        for j in d6[i]:
            if(d7.get(j)==None):
                d7[j]=1
            else:
                d7[j]+=1
    for i,j in d7.items():
        if(j==size):
            d8.append(i)
    d4=d8
    
    k={}
    for i in d4:
        y=data.iloc[i][f1];
        y=y.lower()
        for j in pre2:
            y=y.replace(j,'')
        y=y.split()
        # Getting the count of all unique entities
        h={}
        for j in y:
            if(h.get(j)==None):
                h[j]=1
            else:
                h[j]+=1
        for j in pre1:
            if(h.get(j)!=None):
                del h[j]
        #Deleting the words on the basis on whom we again shortlisted in dataset
        for j in words:
            if(h.get(j)!=None):
                del h[j]
            j = j+'s'
            if(h.get(j)!=None):
                del h[j]
    #   Storing in common dictionary
        for j1,j2 in h.items():
            if(k.get(j1)==None):
                k[j1]=1
            else:
                k[j1]+=1
    #     If only single match is present  
    if(len(d4)==1):
        return words,d4
    else:
        
        print("Select from one of these :")
        print()
        cc=1
        for i in k:
            print(cc,end=". ")
            print(i)
            cc+=1
        print("Which one do you want to select: ")
        print()
        y=input()
        y=y.lower()
        words1=y.split(', ')
        for i in words1:
            words.append(i)
        print("----------------------")
        return words, d4

from collections import defaultdict
x=x.lower()
words = x.split(', ')
# size=len(words)

# To remove thestop words
pre1 = ["due","to","and","other","specified","of","the","a","from","for","without","not"]
pre2 = ['(',')',',','.']


# To store the the matches  
d2=[]

while(len(d2)!=1):
#   Initial search that is searching the entire dataset
    if(len(d2)==0):
        d3 = defaultdict(list)
        words,d2=full_search(data,pre1,pre2,words,d3,d2)
        gm=False
        if(len(d2)==1):
#             print("exact match")
            gm=True
        
#   Searching in our confined space after initial search
    else:
        d3 = defaultdict(list)
        words,d2=shortlisted_search(data,pre1,pre2,words,d3,d2)
        
print(data.iloc[d2[0]][f2])