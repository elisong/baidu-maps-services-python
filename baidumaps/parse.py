# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright © 2015-2018 Eli Song<elisong.ah@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import xml.etree.ElementTree as ET

# from collections import OrderedDict
from collections import OrderedDict
import pandas as pd

def parse_json(response):
    records = []
    jso = response.json()
    record = OrderedDict()
    def iter_dct(dct):
        for key, val in dct.items():
            if isinstance(val, dict):
                iter_dct(val)
            else:
                record[key] = val
    try:
        dct_list = jso['results']
    except KeyError:
        dct_list = jso['result']
        if isinstance(dct_list, dict):
            dct_list = [dct_list]
    for dct in dct_list:
        iter_dct(dct)
        records.append(record.copy())
        record.clear()
    return pd.DataFrame(records)

def parse_xml(response):
    records = []
    root = ET.fromstring(response.text)
    record = OrderedDict()
    def iter_tree(parent):
        for son in parent:
            if len(son):
                iter_tree(son)
            elif son.text:
                record[son.tag] = son.text.strip()
    for parent in root.iter('result'):
        iter_tree(parent)
        records.append(record.copy())
        record.clear()
    return pd.DataFrame(records)


def parse(client, server_name, subserver_name, response, output):
    name = server_name + subserver_name
    options = {'geoconv': parse_gcv,
               'directionroutematrix': parse_drx,
               'locationip': parse_lip,
               'direction': parse_drn,
               'geocoder': parse_gcr,
               'placesuggestion': parse_psn,
               'placesearch': parse_psh,
               'placedetail': parse_pdl,
               'placeeventsearch': parse_peh,
               'placeeventdetail': parse_pel
               }

    return options[name](response)


def parse_gcv(response, output):
    if output == 'xml':
        result_raw = response.text
        soup = BeautifulSoup(result_raw, 'xml')
        points = soup.findAll('point')
        if len(points) > 1:
            result_parse = [{'lng': point.x.text, 'lat': point.y.text} for point in points]
        else:
            result_parse = {'lng': points[0].x.text, 'lat': points[0].y.text}
    else:
        result_raw = response.json()
        points = result_raw['result']
        if len(points) > 1:
            result_parse = [{'lng': point['x'], 'lat': point['y']} for point in points]
        else:
            result_parse = {'lng': points[0]['x'], 'lat': points[0]['y']}
    return result_parse


def parse_drx(response):
    result_raw = response['result']['elements']
    if len(result_raw) > 1:
        result_parse = []
        for rr in result_raw:
            if 'distance' in rr:
                result_parse.append({'distance': rr['distance']['value'],
                                    'duration': rr['duration']['value']})
            else:
                result_parse.append({'status': rr['status'],
                                    'message': rr['message']})
    else:
        if 'distance' in rr:
            result_parse = {'distance': result_raw[0]['distance']['value'],
                            'duration': result_raw[0]['duration']['value']}
        else:
            result_parse = {'status': result_raw[0]['status'],
                            'message': result_raw[0]['message']}

    return result_parse


def parse_lip(response):
    result_raw = response['content']
    result_raw['address_detail'].pop('city_code')
    result_parse = {'address': result_raw['address_detail'],
                    'location': {'lng': float(result_raw['point']['x']),
                                 'lat': float(result_raw['point']['y'])}}
    return result_parse


def parse_drn(response):
    # if type==1
    if response['type'] == 1:
        result_raw = response['result']
        # if mode==drving/walking
        if 'content' in result_raw['origin']:
            origin = result_raw['origin']['content']
            for i, ori in enumerate(origin):
                ori.pop('telephone')
                origin[i] = ori

            destination = result_raw['destination']
            for j, des in enumerate(destination):
                des.pop('telephone')
                destination[j] = des

        # if mode=transit
        else:
            origin = result_raw['origin']
            for i, ori in enumerate(origin):
                ori.pop('uid')
                origin[i] = ori

            destination = result_raw['destination']
            for j, des in enumerate(destination):
                des.pop('uid')
                destination[j] = des

        result_parse = {'origin_maybe': origin,
                        'destination_maybe': destination}
    # if type==2
    else:
        origin_raw = response['result']['origin']
        destination_raw = response['result']['destination']
        routes = response['result']['routes']
        # if mode=transit
        if 'scheme' in routes[0]:
            routes = [rou['scheme'][0] for rou in routes]
        origin = origin_raw['originPt']
        destination = destination_raw['destinationPt']

        result_parse = {'routes': routes, 'origin': origin,
                        'destination': destination}
    return result_parse


def parse_gcr(response):
    result_parse = response['result']
    return result_parse


def parse_psn(response):
    result_parse = response['result']
    for i, rr in enumerate(result_parse):
        if 'cityid' in rr: rr.pop('cityid')
        if 'uid' in rr: rr.pop('uid')
        if 'business' in rr: rr.pop('business')
        result_parse[i] = rr
    return result_parse


def parse_psh(response):
    result_parse = response['results']
    for i, rp in enumerate(result_parse):
        if 'street_id' in rp: rp.pop('street_id')
        if 'detail' in rp: rp.pop('detail')
        result_parse[i] = rp
    return result_parse


def parse_pdl(response):
    result_parse = response['result']
    for i, rp in enumerate(result_parse):
        if 'detail' in rp: rp.pop('detail')
        result_parse[i] = rp
    return result_parse


def parse_peh(response):
    result_parse = response['results']
    return result_parse


def parse_pel(response):
    result_parse = response['result']
    return result_parse


if __name__ == '__main__':
    import requests
    from collections import OrderedDict

    s = requests.Session()
    def parse_json(response):
        record = OrderedDict()
        def iter_dct(dct, prefix=''):
            for key, val in dct.items():
                key_extend = prefix +'_' +key if prefix else key
                if isinstance(val, dict):
                    iter_dct(val, key_extend)
                elif not val or key.lower() in ['status', 'message', 'info']:
                    continue
                else:
                    record[key_extend] = val

        call_back = response.json()
        records = []
        columns = []
        if 'results' in call_back:
            dct_list = call_back['results']
        elif 'result' in call_back:
                dct_list = call_back['result']
        elif 'recommendStops' in call_back: # for parking api
            dct_list = call_back['recommendStops']
        elif 'content' in call_back: # for location IP api
            dct_list = call_back['content']
        else:
            dct_list = call_back

        if isinstance(dct_list, dict):
            dct_list = [dct_list]

        for dct in dct_list:
            iter_dct(dct)
            copied = record.copy()
            if set(columns).issubset(set(copied.keys())):
                columns = list(copied.keys())
            records.append(copied)
            record.clear()
        return pd.DataFrame(records, columns=columns)

    def parse_xml(response):
        record = OrderedDict()
        def iter_tree(parent, prefix=''):
            for son in parent:
                key_extend = prefix + '_' + son.tag if prefix else son.tag
                if len(son):
                    iter_tree(son, key_extend)
                elif not son.text or son.tag.lower() in ['status', 'message', 'info']:
                    continue
                else:
                    record[key_extend] = son.text.strip()

        if 'place/v2/suggestion' in response.url or 'routematrix' in response.url:
            url_ = response.url.replace('xml', 'json')
            response = s.get(url_)
            return parse_json(response)

        try:
            call_back = ET.fromstring(response.text)
        except :
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
        record = OrderedDict()
        def iter_dct(dct, prefix=''):
            for key, val in dct.items():
                key_extend = prefix+'_'+key if prefix else key
                if isinstance(val, dict):
                    iter_dct(val, key_extend)
                elif not val or key.lower() in ['status', 'message', 'info']:
                    continue
                else:
                    record[key_extend] = val

        call_back = response.json()
        result = call_back['result']
        routes = result.pop('routes')
        iter_dct(result)
        copied = record.copy()
        basic_df = pd.DataFrame([copied.values()], columns=copied.keys())
        record.clear()

        records = []
        columns = []
        for i, route in enumerate(routes):
            steps = route.pop('steps')
            route_i = {k: v for k, v in route.items() if v}
            route_i.update({'route': i+1})
            for j, step in enumerate(steps):
                route_i.update({'step': j+1})
                for l, sub_step in enumerate(step):
                    route_i.update({'sub_step': l+1})
                    iter_dct(sub_step)
                    copied = record.copy()
                    route_i.update(copied)
                    if set(columns).issubset(set(copied.keys())):
                        columns = list(copied.keys())
                    records.append(route_i.copy())
                    record.clear()
        routes_df = pd.DataFrame(records,
                                 columns=['route', 'step', 'sub_step'] + columns)
        return basic_df, routes_df


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