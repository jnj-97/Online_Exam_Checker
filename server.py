# -*- coding: utf-8 -*-
"""
Created on Sat May 22 21:14:21 2021

@author: nobin
"""
import pymongo
from flask import Flask,render_template,request,redirect,flash
client=pymongo.MongoClient()
Exam=client.user_Database
students=Exam.Table
username=""
password=""


page=Flask(__name__)
page.config['SECRET_KEY'] = 'super secret key'
@page.route("/",methods =["GET", "POST"])
def gfg():
   return redirect("/login")


@page.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form
        if bool(students.find_one({"Student":userDetails['username'],"Password":userDetails['password']})):
             global username,password
             username=userDetails['username']
             password=userDetails['password']
             flash("Logged In Successfully")
             return redirect('/home')
        else:
             return '<h1>Incorrect Details</h1>'
        # return redirect("/home")
    return render_template('login.html')

@page.route('/home', methods=['GET','POST'])
def home():
    global username,password
    if username != "":
        things=[]
        marks=0
        user_dict=students.find_one({'Student':username})
        things.append(user_dict['1'])
        things.append(user_dict['2'])
        things.append(user_dict['3'])
        things.append(user_dict['4'])
        things.append(user_dict['5'])
        for thing in things:
            marks= marks + thing
        return render_template('home.html')
    else:
        return "<h3>Please Log In</h3>"
    
@page.route('/logout')
def logout():
    global username,password
    username=""
    password=""
    return redirect('/login')

if __name__ == '__main__':
    page.run(debug=True,port=5000)