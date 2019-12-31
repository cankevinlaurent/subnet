# -*- coding: utf-8 -*-

import sqlite3
import CommonConfigProcessor
import CommonDBProcessor
from flask import Flask
from flask import jsonify
from flask import make_response
from flask_httpauth import HTTPBasicAuth

###############################################################################


class DBHandler(CommonDBProcessor.CommonDBProcessor):
    """数据库操作"""

    def __init__(self, database):
        super(DBHandler, self).__init__(database)

    def get_subnets(self):
        query = "SELECT * FROM subnets"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_gateways(self):
        query = "SELECT * FROM gateways"
        self.cursor.execute(query)
        return self.cursor.fetchall()

##############################################################################


app = Flask(__name__)

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == confprocessor.get_username():
        return confprocessor.get_password()
    else: return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'results': 'Unauthorized access'}), 401)

@app.route('/', methods=['GET'])
def index():
    """Introduction of platform"""
    port = confprocessor.get_port()
    return u'''<html><head><title>欢迎使用网段查询平台</title></head>
               <body><h1>本平台开放以下能力</h1>
               <ul>
               <li>查询能力：[get] https://x.x.x.x:%d/query</li>
               </ul>
               </body></html>
            ''' %(port)

@app.route('/query', methods=['GET'])
def query():
    """Introduction of query function"""
    port = confprocessor.get_port()
    return u'''<html><head><title>查询能力</title></head>
               <body><h1>【查询】能力提供以下API</h1>
               <ul>
               <li>全部网段：[get] https://x.x.x.x:%d/query/subnets</li>
               </ul>
               </body></html>
            ''' %(port)

@app.route('/query/subnets', methods=['GET'])
@auth.login_required
def subnets():
    """Query all subnets"""
    subnets = DBHandler('subnet.db').get_subnets()
    gateways = DBHandler('subnet.db').get_gateways()
    results = []
    if subnets and gateways:
        for subnet, netmask, location in subnets:
            result = {'subnet': subnet, 'netmask': netmask,
                'location': location, 'gateways': []}
            for subnet_g, gateway in gateways:
                if subnet == subnet_g: result['gateways'].append(gateway)
            results.append(result)
    return jsonify({'results': results})

##############################################################################


if __name__ == '__main__':
    confprocessor = CommonConfigProcessor.CommonConfigProcessor(
        'config_subnet.txt')
    app.run(
        host='0.0.0.0', port=confprocessor.get_port(), ssl_context='adhoc')

