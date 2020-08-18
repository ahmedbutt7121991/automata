from flask_restful import Resource, Api
from flask import send_file
from json import dumps
from flask import jsonify
from flask import Flask, request, render_template, redirect
import os
import sys
from flask_cors import CORS, cross_origin
sys.path.append('.')
import logging
import logging.config
from logging.handlers import RotatingFileHandler
import traceback
import pymysql
import requests
#from ConfigParser import SafeConfigParser
from configobj import ConfigObj 
import json

cors = None
app = Flask(__name__)
hook = None
configFile = "./config.ini"

def getColor():
    if os.environ.get('PG_COLOR') is not None: # None
        return os.environ.get('PG_COLOR')
    return 'white'

@app.route("/")
def home():
    color = getColor()
    print("color {}".format(color))
    context = { 'square' : 0, 'double' : 0, 'color' : color, 'key': 0}
    return render_template("index.html",value=context)

@app.route('/getData', methods = ['POST'])
def getData():
    key = request.form['key']
    print("the key is " + key)
    square_service_ip   =  conf['square']['IP']
    square_service_name   =  conf['square']['ClientName']
    square_service_port =  conf['square']['Port']
    double_service_ip   = conf['double']['IP']
    double_service_name   = conf['double']['ClientName']
    double_service_port = conf['double']['Port']
    response1 = requests.get('http://{}:{}/square/{}'.format(square_service_name,square_service_port,key)).content
    response2 = requests.get('http://{}:{}/double/{}'.format(double_service_name,double_service_port,key)).content
    color = getColor()
    context = { 'square' : json.loads(response1)["square"], 'double' : json.loads(response2)["double"], 'color' : color, 'key': key }
    return render_template("index.html",value=context)

class DbClient():
    """class for communicating with DB"""
    def __init__(self):
        self.db = None
        self.db_name = 'example'
        #self.table_name = 'auto_table'
        self.create_connection()

    def create_connection(self):
        try:
            self.db = pymysql.connect(
                    host = conf['credentials']['host'],
                    user = conf['credentials']['username'],
                    password = conf['credentials']['password'],
                    db = conf['credentials']['dbname']
                    )
            self.db.autocommit(True)
        except pymysql.Error as e:
            #logger.error("Failed to connect to DB - %s"%str(e))
            print('Failed to connect to DB:')

    def close_connection(self):
        self.db.close()

    def get_value(self,table_name,key):
        query = "SELECT val FROM {} WHERE num={} ".format(table_name,key)
        result = self.query_execute(query)
        if result == ():
            return 0
        return result[0][0]

    ## Executes query
    # @params query
    # @params logger
    # @returns result of the query if successful else exception string
    def query_execute(self, query):
        cur = None
        try:
            result = None
            # self.create_connection()
            cur = self.db.cursor()
            cur.execute(query)
            result = cur.fetchall()
        except pymysql.ProgrammingError as e:
            #log.error("MySQL Error: %s" % (e))
            #logger.error("MySQL Error - %s"% str(e))
            print("MySQL Error: {}".format(e))
            return "MySQL Error: {}".format(e)
        except pymysql.OperationalError:
            #log.error("Operational Error trying to reconnect")
            print("Operational Error trying to reconnect")
            #logger.debug("Operational Error: trying to reconnect.")
            self.close_connection()
            self.create_connection()
            result = None
            cur = self.db.cursor()
            cur.execute(query)
            result = cur.fetchall()
        cur.close()
        # self.close_connection()
        return result

    def query_fruit(self,num):
        query = "select * from {} where auto_id={}".format(self.table_name,num)
        result = self.query_execute(query)
        # TODO: Check for empty result
        return result


class handler(Resource):
    def __init__(self):
        # read from config file
        conf = ConfigObj('config.ini')
        app_ip = conf[app_name]['IP']
        app_port = conf[app_name]['Port']


        self.square_service_ip   =  conf['square']['IP']
        self.square_service_port =  conf['square']['Port']

        self.fruit_service_ip   = conf['fruit']['IP']
        self.fruit_service_port = conf['fruit']['Port']

        self.double_service_ip   = conf['double']['IP']
        self.double_service_port = conf['double']['Port']

    def get(self, num):
        response1 = requests.get('http://{}:{}/square/{}'.format(self.square_service_ip,self.square_service_port,num)).content
        response2 = requests.get('http://{}:{}/double/{}'.format(self.double_service_ip,self.double_service_port,num)).content
        response3 = requests.get('http://{}:{}/fruit/{}'.format(self.fruit_service_ip,self.fruit_service_port,num)).content
        #print("responses {} {} {}".format(response1,response2,response3))
        return {'response1':response1, 'response2' : response2, 'response3' : response3}
        #return response1, response2, response3


class square(Resource):
    def get(self, num):
        print type(num)
        #return {'square': int(num)*int(num)}
        client = DbClient()
        return {'square' : int(client.get_value('square',num)) }

class double(Resource):
    def get(self, num):
        client = DbClient()
        return {'double' : int(client.get_value('dbl',num)) }
        #return {'double':int(num)*2}


class fruit(Resource):

    def get(self, num):
        """ Picks fruit from db """
        if int(num)<1 or int(num)>9:
            return {'fruit':'NOT_FOUND'}
        client = DbClient()
        fruit = client.query_fruit(int(num))
        client.close_connection()
        return {'fruit': fruit[0][1]}


def start_webserver(ip,port):
    global hook
    cors = CORS(app)

    api = Api(app)
    api.add_resource(square, '/square/<num>')       # Route_1   square
    api.add_resource(double, '/double/<num>')       # Route_2   double
    api.add_resource(fruit, '/fruit/<num>')         # Route_3   fruit
    api.add_resource(handler, '/handler/<num>')     # Route_4   handler
    
    wk_log = logging.getLogger('werkzeug')
    wk_log.disabled = False
    wk_log.info("....Starting API Server at port %s...."%(port))
    app.run(host=ip, port=port, debug = False)
    # app.run(host='192.168.10.125', port=port, debug = False)


if __name__ == "__main__":
    app_name = sys.argv[1]
    conf = ConfigObj('config.ini')
    app_ip = conf[app_name]['IP']
    app_port = conf[app_name]['Port']
    start_webserver(app_ip,app_port)
