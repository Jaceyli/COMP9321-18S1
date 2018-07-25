import os
from collections import defaultdict
from flask.ext.cors import CORS

import xlrd
from flask import Flask, request, render_template
import requests
from flask import jsonify
from flask_restful import reqparse

from server.app.auth import admin_required, login_required
from server.app.jsontoxml import toxml, tofeed
from server.app.mongo_operations import save_xlsx_data_to_monogo, delete_record_info, get_one_record, get_all_records, \
    get_records_with_filter, get_one_record_id

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer)
SECRET_KEY = "COMP9321"

app = Flask(__name__)
# To solve  cookies across domains is disabled due to the security implications
CORS(app)


# app = Flask(__name__,
#             static_folder = "../../client/static",
#             template_folder = "../../client/template")


# To solve Angularjs {{}} is not working in jinjia (⊙﹏⊙)b
# app.jinja_env.variable_start_string = '%%'
# app.jinja_env.variable_end_string = '%%'



data1_url = "http://www.bocsar.nsw.gov.au/Documents/RCS-Annual/"

dir = "tmp/"
# if not os.path.exists(dir):
#     os.makedirs(dir)

#generate postcode dict
data = xlrd.open_workbook("tmp/Australian LGA postcode mappings (2011 data).xlsx")
table = data.sheets()[0]
nrows = table.nrows
postcode = defaultdict(list)
areaset = set()
for i in range(0, nrows):
    line = table.row_values(i)
    if line[0] == "New South Wales":
        postcode[int(line[2])].append(line[1])
        areaset.add(line[1])


# @app.route('/')
# def root():
#     return render_template('index.html')

@app.route("/create_area/<name>", methods=['POST'])
@admin_required
def create_data(name):
    if name == 'undefined':
        return jsonify(message="Iganame or postcode is required"), 400, {'Access-Control-Allow-Origin': '*'}

    areas = []
    try:
        p = int(name)
        areas = postcode[p]
    except:
        area = name.replace(' ', '')
        if area not  in areaset:
            return jsonify(error='no such area'), 404, {'Access-Control-Allow-Origin': '*'}
        areas.append(area)
    # print(areas)
    new = 0
    results = []
    for area in areas:
        area = area.replace(' ', '')
        # get the .xlsx file, put it to "tmp"
        if os.path.exists(dir + area + '.xlsx'):
            result = get_one_record(area)
            if result.__len__():
                results.append(result[0])
                # return tofeed(result, detail=False), 200
            else:
                result = save_xlsx_data_to_monogo(area)
                new = 1
                results.append(result[0])

        else:
            dls = data1_url + area + "lga.xlsx"
            # print('--------',dls)
            resp = requests.get(dls)
            with open(dir + area + '.xlsx', 'wb') as output:
                try:
                    output.write(resp.content)
                finally:
                    output.close()
            result = save_xlsx_data_to_monogo(area)
            results.append(result[0])
            new = 1
    response = tofeed(results, detail=False)
    if new:
        return response, 201, {'Access-Control-Allow-Origin': '*'}
    else:
        return response, 200, {'Access-Control-Allow-Origin': '*'}


@app.route("/delete_one_area/<tid>", methods=['DELETE'])
@admin_required
def delete_data(tid):
    if tid == 'undefined':
        return jsonify(message="Id is required"), 400, {'Access-Control-Allow-Origin': '*'}

    try:
        tid = int(tid)
    except:
        return jsonify(message="Integer is required"), 400, {'Access-Control-Allow-Origin': '*'}

    result = get_one_record_id(tid)
    if not result.__len__():
        return jsonify(message="NOT FOUND"), 400, {'Access-Control-Allow-Origin': '*'}
    else:
        try:
            delete_record_info(tid)
        except Exception as e:
            return jsonify(message=e), 400, {'Access-Control-Allow-Origin': '*'}
    return jsonify(message="success"), 200, {'Access-Control-Allow-Origin': '*'}

@app.route("/get_one_area/<tid>", methods=['GET'])
@login_required
def get_one_area(tid):
    if tid =='undefined':
        return jsonify(message="Id is required"), 400, {'Access-Control-Allow-Origin': '*'}

    try:
        tid = int(tid)
    except:
        return jsonify(message="Integer is required"), 400, {'Access-Control-Allow-Origin': '*'}

    result = get_one_record_id(tid)
    if result.__len__():
        Accept_type = request.headers['Accept']

        if Accept_type == 'application/json':
            return jsonify(result), 200, {'Access-Control-Allow-Origin': '*'}
        else:
            return tofeed(result), 200, {'Access-Control-Allow-Origin': '*'}
    else:
        return jsonify(message="NOT FOUND"), 400, {'Access-Control-Allow-Origin': '*'}


@app.route("/get_all_areas", methods=['GET'])
@login_required
def get_all_areas():
    results = get_all_records()
    if results.__len__():
        results = get_all_records()
        Accept_type = request.headers['Accept']
        if Accept_type == 'application/json':
            return jsonify(results), 200, {'Access-Control-Allow-Origin': '*'}
        else:
            return tofeed(results), 200, {'Access-Control-Allow-Origin': '*'}
    else:
        return jsonify(message="NOT FOUND"), 400, {'Access-Control-Allow-Origin': '*'}


@app.route("/get_areas_with_filters", methods=['GET'])
@login_required
def get_areas_with_filters():
    parser = reqparse.RequestParser()
    parser.add_argument('filter', type=str)
    args = parser.parse_args()
    filter = args.get("filter")
    if filter is None:
        return jsonify(message="Filter is required"), 400, {'Access-Control-Allow-Origin': '*'}
    print(filter)
    filter_dict = defaultdict(list)
    token = filter.split(' ')
    if token.__len__() == 7:
        if token[3] in ['or', 'and'] and token[0] == 'lgaName' and token[4] in ['lgaName', 'year']:
            if token[4] == 'year':
                if len(token[6]) != 4:
                    return jsonify(message="Year should be 4 digits"), 400, {'Access-Control-Allow-Origin': '*'}
                try:
                    token[6] = int(token[6])
                except:
                    return jsonify(message="Year should be digits"), 400, {'Access-Control-Allow-Origin': '*'}
            filter_dict[token[0]].append(token[2])
            filter_dict['operation'] = token[3]
            filter_dict[token[4]].append(token[6])

            results = get_records_with_filter(filter_dict)
            Accept_type = request.headers['Accept']
            if Accept_type == 'application/json':
                return jsonify(results), 200, {'Access-Control-Allow-Origin': '*'}
            else:
                return tofeed(results), 200, {'Access-Control-Allow-Origin': '*'}
    return jsonify(message="Wrong Filter"), 400, {'Access-Control-Allow-Origin': '*'}



@app.route("/auth", methods=['GET'])
def generate_token():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str)
    parser.add_argument('password', type=str)
    args = parser.parse_args()
    username = args.get("username")
    password = args.get("password")
    if username is None or password is None:
        return jsonify(message="Username and password are required"), 404, {'Access-Control-Allow-Origin': '*'}
    s = Serializer(SECRET_KEY, expires_in=600)
    token = s.dumps(username)
    if username == 'admin' and password == 'admin':
        return jsonify(type='admin', token=token.decode()), {'Access-Control-Allow-Origin': '*'}
    elif username == 'guest' and password == 'guest':
        return jsonify(type='guest',token=token.decode()), {'Access-Control-Allow-Origin': '*'}
    else:
        return jsonify(message="wrong username or password"), 404, {'Access-Control-Allow-Origin': '*'}



if __name__ == "__main__":
    app.run()