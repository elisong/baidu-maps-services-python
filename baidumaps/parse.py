# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright © 2015-2018 Eli Song <elisong.ah@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import xml.etree.ElementTree as ET
import requests
from collections import OrderedDict
import pandas as pd

s = requests.Session()

def parse(client, response):
    """Transform response to pandas' DataFrame for easily read.

    :param response: call back from GET request
    :type response: 'Request' object defined by `requests` module

    :rtype: pandas.DataFrame
    """
    if client.server_name == 'direction':
        return parse_direct(response)
    elif client.output == 'json':
        return parse_json(response)
    else:
        return parse_xml(response)


def parse_json(response):
    """Transform response to pandas' DataFrame (output=json).

    :param response: call back from GET request.
    :type response: 'Request' object defined by `requests` module.

    :rtype: pandas.DataFrame
    """
    record = OrderedDict()
    def iter_dct(dct, prefix=''):
        for key, val in dct.items():
            key_extend = prefix + '_' + key if prefix else key
            if isinstance(val, dict):
                iter_dct(val, key_extend)
            elif not val or key.lower() in ['status', 'message', 'info', 'type']:
                continue
            else:
                record[key_extend] = val

    call_back = response.json()
    if 'results' in call_back:
        dct_list = call_back['results']
    elif 'result' in call_back:
        dct_list = call_back['result']
    elif 'recommendStops' in call_back:  # for parking api
        dct_list = call_back['recommendStops']
    elif 'content' in call_back:  # for location IP api
        dct_list = call_back['content']
    else:
        dct_list = call_back
    if isinstance(dct_list, dict):
        dct_list = [dct_list]

    records = []
    columns = []
    for dct in dct_list:
        iter_dct(dct)
        copied = record.copy()
        if set(columns).issubset(set(copied.keys())):
            columns = list(copied.keys())
        records.append(copied)
        record.clear()
    return pd.DataFrame(records, columns=columns)


def parse_xml(response):
    """Transform response to pandas' DataFrame (output=xml).
    Two special cases run parse_json() internally:
    1. Too difficult to transform.
    2. Only json type call back offered by Baidu.

    :param response: call back from GET request
    :type response: 'Request' object defined by `requests` module

    :rtype: pandas.DataFrame
    """
    record = OrderedDict()
    def iter_tree(parent, prefix=''):
        for son in parent:
            key_extend = prefix + '_' + son.tag if prefix else son.tag
            if len(son):
                iter_tree(son, key_extend)
            elif not son.text or son.tag.lower() in ['status', 'message', 'info', 'type']:
                continue
            else:
                record[key_extend] = son.text.strip()

    if 'place/v2/suggestion' in response.url or 'routematrix' in response.url:
        url_ = response.url.replace('xml', 'json')
        response = s.get(url_)
        return parse_json(response)

    try:
        call_back = ET.fromstring(response.text)
    except:
        return parse_json(response)

    records = []
    columns = []
    for parent in call_back.iter('result'):
        iter_tree(parent)
        copied = record.copy()
        if set(columns).issubset(set(copied.keys())):
            columns = list(copied.keys())
        records.append(copied)
        record.clear()
    return pd.DataFrame(records, columns=columns)


def parse_direct(response):
    """Transform response to pandas' DataFrame, especially for direction.

    :param response: call back from GET request
    :type response: 'Request' object defined by `requests` module

    :rtype: pandas.DataFrame
    """
    record = OrderedDict()
    def iter_dct(dct, prefix=''):
        for key, val in dct.items():
            key_extend = prefix + '_' + key if prefix else key
            if isinstance(val, dict):
                iter_dct(val, key_extend)
            elif not val or key.lower() in ['status', 'message', 'info', 'type']:
                continue
            else:
                record[key_extend] = val

    try:
        call_back = response.json()
    except:
        url_ = response.url.replace('xml', 'json')
        response = s.get(url_)
        call_back = response.json()

    result = call_back['result']
    routes = result.pop('routes')
    records = []
    columns = []
    for i, route in enumerate(routes):
        steps = route.pop('steps')
        route_i = {k: v for k, v in route.items() if v}
        route_i.update({'route': i + 1})
        tmp_col = list(route.keys())
        for j, step in enumerate(steps):
            route_i.update({'step': j + 1})
            if isinstance(step, list):
                for l, sub_step in enumerate(step):
                    route_i.update({'sub_step': l + 1})
                    iter_dct(sub_step)
                    copied = record.copy()
                    route_i.update(copied)
                    tmp_col.extend(['route', 'step', 'sub_step'] + list(copied.keys()))
                    if set(columns).issubset(set(tmp_col)):
                        columns = tmp_col
                    records.append(route_i.copy())
                    record.clear()
            else:
                iter_dct(step)
                copied = record.copy()
                route_i.update(copied)
                tmp_col.extend(['route', 'step'] + list(copied.keys()))
                if set(columns).issubset(set(tmp_col)):
                    columns = tmp_col
                records.append(route_i.copy())
                record.clear()
    return pd.DataFrame(records, columns=columns)


if __name__ == '__main__':
    urls=["http://api.map.baidu.com/place/v2/search?query=ATM机&tag=银行&region=北京",
         "http://api.map.baidu.com/place/v2/search?query=银行&location=39.915,116.404&radius=2000",
         "http://api.map.baidu.com/place/v2/search?query=银行&bounds=39.915,116.404,39.975,116.414",
         "http://api.map.baidu.com/place/v2/detail?uid=6334ddeb6a99710bfea77863&scope=2",
         "http://api.map.baidu.com/place/v2/suggestion?query=天安门&region=北京&city_limit=true",
         "http://api.map.baidu.com/geocoder/v2/?address=北京市海淀区上地十街10号",
         "http://api.map.baidu.com/direction/v2/transit?origin=40.056878,116.30815&destination=31.222965,121.505821",
         "http://api.map.baidu.com/direction/v2/riding?origin=40.01116,116.339303&destination=39.936404,116.452562",
         "http://api.map.baidu.com/direction/v2/driving?origin=40.01116,116.339303&destination=39.936404,116.452562",
         "http://api.map.baidu.com/routematrix/v2/driving?origins=40.45,116.34|40.54,116.35&destinations=40.34,116.45|40.35,116.46",
         "http://api.map.baidu.com/location/ip?ip=220.112.125.166",
         "http://api.map.baidu.com/parking/search?location=116.313064,40.048541&coordtype=bd09ll",
         "http://api.map.baidu.com/geoconv/v1/?coords=114.21892734521,29.575429778924&from=1&to=5",
          "http://api.map.baidu.com/timezone/v1?coord_type=wgs84ll&location=-36.52,174.46&timestamp=1473130354"]

    ak="GuMrViec3jLp1WCG4P3VLDlC"

    for i, url in enumerate(urls):
        print('--------------------- Order:',i+1, 'API:', url)
        for x in ['xml', 'json']:
            url_ = url+'&ak='+ak+'&output='+x
            print('--------------------- URL:', url_)
            res = s.get(url_)
            if x =='xml' and 'ip' not in url_:
                df = parse_xml(res)
            else:
                df = parse_json(res)
            print('---------------------PARSER: ', x)
            print(df)