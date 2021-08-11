import pandas as pd 
import streamlit
# data = pd.read_csv("unspsc_dataset.csv") 
# data.Code
file = open("plan0.txt","r")
lines=file.readlines()
# print(lines)
c1=False;
for line in lines:
    if(line.find("get_db_access user_dialogue")!=-1):
        c1=True
        print(line)
file.close()
        
print("Do you want to manually query the dataset or want to use RL")
c2=input()
c2=c2.lower()
if(c2=="unspsc"):
    data = pd.read_csv("unspsc_dataset.csv") 

elif(c2=="icd10"):
    data = pd.read_csv("icd_10.csv") 

# else:
    # RL part

    
    
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







print("Ask the query:")
x = input()






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

    #mapping
    sp1={}
    sp2={}
    sp3={}
    sp4=1
    for i in d2:
        sp1[i]=data.iloc[i][f1]
        sp2[i]=data.iloc[i][f2]
        sp3[sp4]=i
        sp4+=1
        
    if(len(d2)==1):
        print("The code is: ",end="")
        print(sp2[sp3[1]])
    else:
        print(len(d2),end=" ")
        print("instances found !")
        print()
        print("Select from one of these :")
        print()
        cc=1
        for i in d2:
            r1=sp3[cc]
            print(cc,end=": ")
            print(sp1[r1])
            # print(r1)
            cc+=1


        print("Which one do you want to select: ")
        print()
        y=int(input())
        print("The code is: ",end="")
        print(sp2[sp3[y]])
        







from collections import defaultdict
x=x.lower()
words = x.split(', ')
# size=len(words)

# To remove thestop words
pre1 = ["due","to","and","other","specified","of","the","a","from","for","without","not"]
pre2 = ['(',')',',','.']


# To store the the matches  
d2=[]
d3 = defaultdict(list)
full_search(data,pre1,pre2,words,d3,d2)

