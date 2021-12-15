from datetime import datetime
from enum import unique
from flask import Flask,render_template,request,jsonify
from flask import Flask, render_template ,url_for , request , redirect
import os, requests
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from flask_restful import Resource, Api,reqparse
# from flask_res
import psycopg2
import json
app = Flask(__name__)
api = Api(app)
@app.route('/new_d/<name>')
def new(name):
    return name


@app.route('/data')
def data_my():
    parser = reqparse.RequestParser()  # initialize
        
    parser.add_argument('name', required=True)  # add args
    # parser.add_argument('name', required=True)
    # parser.add_argument('city', required=True)
    args = parser.parse_args()
    # print(args['name'])
    data = pd.read_csv('C:\\Users\\RahulD_Dev\\Desktop\\my_files\\vehicle_models.csv')  # read CSV
    m=data.get('name')
    dic2={}
    for m2 in m:
        if args['name']==m2:
            dic2['name']=m2
            dic2['msg']='we got what we want'

    # data = data.to_dict()

    return dic2
    
@app.route('/fromdb')
def fromdb():
    db = psycopg2.connect("dbname='****' user='****' host='****' password='****'")
    cur = db.cursor()
    cur.execute("SELECT array_to_json(array_agg(row_to_json(u))) FROM enterprisecouk_20211011 u")
    parser = reqparse.RequestParser()  # initialize
    
    parser.add_argument('id', type=int,required=True)  # add args
    # # parser.add_argument('name', required=True)
    # # parser.add_argument('city', required=True)
    args = parser.parse_args()
    # mmydbdata={}
    res=cur.fetchall()
    db.close()
    myall_d=res[0][0]
    for b in myall_d:
        # print('>>>>>>',b)
        if args['id']==b['id']:
            print('>>>>>>',b)
            myresultd=b

    return myresultd
db = psycopg2.connect("dbname='****' user='****' host='****' password='****'")
cur = db.cursor()
@app.route('/mydumpsdb')
def mydumpsdb():
    
    cur.execute("SELECT * FROM enterprisecouk_20211011 ")

    parser = reqparse.RequestParser()  # initialize
    parser.add_argument('id', type=int,required=True)  # add args
    args = parser.parse_args()
    res=cur.fetchall()
    print(res[0])
    db.commit()
    # db.close()
    #===================another method===============
    row_headers=[x[0] for x in cur.description]
    json_data=[]
    for result in res:
        json_data.append(dict(zip(row_headers,result)))
    all_my=json.dumps(json_data).replace('[','').replace(']','')
    mylist=all_my.split('},')
    for dd in mylist:
        if dd.endswith('"'):
            mydic=dd+'}'
        else:
            mydic=dd
        # print('========================',mydic)
        alljd=json.loads(json.dumps(mydic))
        
        myd=json.loads(alljd)
        if args['id']==myd['id']:
            my_res=myd
    #==================================
    # jsonify({'data':res[0]})
    return my_res

if __name__ == "__main__":
    app.run(debug=True)