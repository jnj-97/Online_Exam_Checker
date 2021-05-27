# -*- coding: utf-8 -*-
"""
Created on Mon May 17 22:28:26 2021

@author: nobin
"""
import boto3
#import os
#from google.cloud import vision
import tensorflow_hub as hub
from scipy.spatial import distance
import pymongo
client=pymongo.MongoClient('mongodb://ec2-18-223-112-213.us-east-2.compute.amazonaws.com',6000)
Exam=client.user_Database
students=Exam.Table
students.drop()
marks=[]
count=1
mark_count=0
def run_and_plot(messages_):
    global count,mark_count
    message_embeddings_ = embed(messages_)
    sub=[]
    for messages in range(0,5):
      # a = (message_embeddings_[messages][0],message_embeddings_[messages][1],message_embeddings_[messages][2])
      # b = (message_embeddings_[messages+5][0],message_embeddings_[messages+5][1],message_embeddings_[messages+5][2])
          dst = distance.euclidean(message_embeddings_[messages], message_embeddings_[messages+5])
          sub.append(dst)
    for things in sub:
        if mark_count == 5:
            break
        elif things >=0 and things<=1:
            marks.append(full_marks[mark_count])
        elif things >=1 and things<=1.25:
            marks.append(((full_marks[mark_count])* 0.5))
        elif things>=1.25 and things<=1.5:
            marks.append(((full_marks[mark_count])* 0.33))
        else:
                marks.append(0)
        mark_count=mark_count+1
    students.insert_one({'Student':'Student{}'.format(count),'Password':'12345','1':marks[0],'2':marks[1],'3':marks[2],'4':marks[3],'5':marks[4],})
    count=count+1
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
full_marks=(4,3,1,2,2)
client = boto3.client('textract')
for student in range(0,3):
    answer_key=["Object-oriented programming (OOP) is a programming paradigm based on the concept of objects, which can contain data and code: data in the form of fields (often known as attributes or properties), and code, in the form of procedures (often known as methods).A feature of objects is that an object's own procedures can access and often modify the data fields of itself (objects have a notion of this or self). In OOP, computer programs are designed by making them out of objects that interact with one another.[OOP languages are diverse, but the most popular ones are class-based, meaning that objects are instances of classes, which also determine their types.Many of the most widely used programming languages (such as C++, Java, Python, etc) are multi-paradigm and they support object-oriented programming to a greater or lesser degree",
            "Uses of Operating System.The operating system is used everywhere today, such as banks, schools, hospitals, companies, mobiles, etc. No device can operate without an operating system because it controls all the user's commands.The operating system has many notable features that are developing day by day. The growth of the operating system is commendable as it was developed in 1950 to handle storage tape. It acts as an interface. The features of operating system are given below.Error detection and handling. Handling I/O operations. Virtual Memory Multitasking. Program Execution. Allows disk access and file systems. Memory management. Protected and supervisor mode. Security. Resource allocation. Easy to run. Information and Resource Protection. Manipulation of the file system",
            "google.com",
            "An array is a collection of items stored at contiguous memory locations. The idea is to store multiple items of the same type together. This makes it easier to calculate the position of each element by simply adding an offset to a base value, i.e., the memory location of the first element of the array (generally denoted by the name of the array). The base value is index 0 and the difference between the two indexes is the offset",
            "Define a,b,c. Let a=b+c.Print c"]
    for number in range(1,6):
        with open('Student1/{}.jpg'.format(number), 'rb') as document:
            img = bytearray(document.read())
            response = client.detect_document_text(Document={'Bytes': img})
            x=''
            for item in response["Blocks"]:
                if item["BlockType"] == "WORD":
                    x=x+item["Text"] + ' '
            answer_key.append(x)
    run_and_plot(answer_key)