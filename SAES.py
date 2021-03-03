#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 21:17:15 2021

@author: hbueno2
"""


import pandas as pd

def splitInts(intList):
    if(type(intList)!=str):
        strList=str(intList)
        intList=map(int, strList)
    else:
        intList=map(int, intList)
    return list(intList)

def lstStr(ls):
    str1=""
    for i in ls:
        str1+=str(i)
    return str1

def lstStrSpace(ls):
    str1=""
    cnt=0
    for i in ls:
        cnt+=1
        str1+=str(i)
        if(cnt%4==0 and cnt!=len(ls)):
            str1+=" "
    return str1

def halfSplit(key):
    return key[0:8], key[8:]

def binNum(x):
    return splitInts(bin(x)[2:].zfill(4))

def rota(w):
    w2=w[4:]+w[0:4]
    return w2

def sub(w,num_type):     ### add a new variable and new column in df
    w_new=["",""]
    w_new[0]=lstStr(w[0:4])
    w_new[1]=lstStr(w[4:])
    d={"bit":['0000','0001','0010','0011','0100','0101','0110','0111',
              '1000','1001','1010','1011','1100','1101','1110','1111'], 
       "val":[9, 4, 10,11,13,1,8,5,
              6,2,0,3,12,14,15,7],
       "val2":[10,5,9,11,1,7,8,15,
               6,0,2,3,12,4,13,14]}
    
    for i in range(16):
        if(w_new[0]==d["bit"][i]):
            if(num_type==1):
                num1=binNum(d["val"][i])
            else:
                num1=binNum(d["val2"][i])
        if(w_new[1]==d["bit"][i]):
            if(num_type==1):
                num2=binNum(d["val"][i])
            else:
                num2=binNum(d["val2"][i])
    return num1+num2
    
def xOr(w,w2):
    new_w=[]
    for i in range(len(w)):
        new_w.append(1 if w[i]!=w2[i] else 0)
    return new_w
        
def wORsubRota(w0,w1,wType):
    if(wType==2):
        w_const=splitInts("10000000")
    else:
        w_const=splitInts("00110000")
    new_w=xOr(w0,w_const)
    new_w=xOr(new_w,sub(rota(w1),1))
    return new_w    

def swap(w):
    new_w=w[0:4]+w[12:]+w[8:12]+w[4:8]
    return new_w

def matrixmul(key, crypt_type):
    a=int(lstStr(key[0:4]),2)
    b=int(lstStr(key[4:8]),2)
    c=int(lstStr(key[8:12]),2)
    d1=int(lstStr(key[12:]),2)
    if(crypt_type==1):
        x=1
        z=4
    else: 
        x=9
        z=2
    d={0:[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
       1:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
       2:[0,2,4,6,8,10,12,14,3,1,7,5,11,9,15,13],
       3:[0,3,6,5,12,15,10,9,11,8,13,14,7,4,1,2],
       4:[0,4,8,12,3,7,11,15,6,2,14,10,5,1,13,9],
       5:[0,5,10,15,7,2,13,8,14,11,4,1,9,12,3,6],
       6:[0,6,12,10,11,13,7,1,5,3,9,15,14,8,2,4],
       7:[0,7,14,9,15,8,1,6,13,10,3,4,2,5,12,11],   ###7x3=9? 
       8:[0,8,3,11,6,14,5,13,12,4,15,7,10,2,9,1],
       9:[0,9,1,8,2,11,3,10,4,13,5,12,6,15,7,14],
       10:[0,10,7,13,14,4,9,3,15,5,8,2,1,11,6,12],
       11:[0,11,5,14,10,1,15,4,7,12,2,9,13,6,8,3],
       12:[0,12,11,7,5,9,14,2,10,6,1,13,15,3,4,8],
       13:[0,13,9,4,1,12,8,5,2,15,11,6,3,14,10,7],
       14:[0,14,15,1,13,3,2,12,9,7,6,8,4,10,11,5],
       15:[0,15,13,2,9,6,4,11,1,14,12,3,8,7,5,10]}   
    df=pd.DataFrame(data=d)
    one=xOr(binNum(df[a][x]),binNum(df[b][z]))
    two=xOr(binNum(df[a][z]),binNum(df[b][x]))
    num3=xOr(binNum(df[c][x]),binNum(df[d1][z]))
    four=xOr(binNum(df[c][z]),binNum(df[d1][x]))
    mtrx_new=one+two+num3+four
    return mtrx_new

key="1010010111110011"
plain_t="1000010000100001"

print("\n ------------------------- \nKey Generation:")

k0=splitInts(key)

w0,w1=halfSplit(k0)

w2=wORsubRota(w0,w1,2)

w3=xOr(w2,w1)  ###w2xorw1

w4=wORsubRota(w2,w3,4)

w5=xOr(w4,w3)

k1=w2+w3
k2=w4+w5

print("Key_0:",lstStrSpace(k0))
print("Key_1:",lstStrSpace(k1))
print("Key_2:",lstStrSpace(k2))

print("\n ------------------------- \nEncryption:")
### Step 1
blk1=xOr(splitInts(plain_t), k0)
print("Add Round Key:",lstStrSpace(blk1))

### Step 2
blk2=sub(blk1[0:8],1)+sub(blk1[8:],1)
print("Sub Byte:",lstStrSpace(blk2))

### Step 3
blk3=swap(blk2)
print("Shift Rows:", lstStrSpace(blk3))

### Step 4
blk4=matrixmul(blk3,1)
print("Mix Columns:", lstStrSpace(blk4))

### Step 5
blk5=xOr(k1, blk4)
print("Add Round Key (k1):", lstStrSpace(blk5))

### Step 6
blk6=sub(blk5[0:8],1)+sub(blk5[8:16],1)
print("Sub Bytes:", lstStrSpace(blk6))

### Step 7
blk7=swap(blk6)
print("Shift Rows:", lstStrSpace(blk7))

### Step 8/Cipher Text
blk8=xOr(blk7, k2)
print("Cipher Text (Round Key - k2):\n", lstStrSpace(blk8))

##################  Decryption process below
print("\n ------------------------- \nDecryption:")
ci8=xOr(blk8,k2)
ci7=swap(ci8)
ci6=sub(ci7[0:8],2)+sub(ci7[8:16],2)
ci5=xOr(k1,ci6)
print('Add Round Key (k1):', lstStrSpace(ci5))
ci4=matrixmul(ci5,2)
print('Mix Columns:', lstStrSpace(ci4))
ci3=swap(ci4)
ci2=sub(ci3[0:8],2)+sub(ci3[8:16],2)
ci1=xOr(k0,ci2)
print("Verified PlainText:",lstStrSpace(ci1))
print("\n ------------------------- \n Verification")
print("Are plaintext and decrypted cipher equal?",ci1==splitInts(plain_t))



input_3="1010101011100100"
input2_3=matrixmul(splitInts(input_3), 1)
print(lstStrSpace(input2_3))


