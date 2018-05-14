# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright © 2015-2018 Eli Song<elisong.ah@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from convert import conv2str, ip_check

def place_search(client, query, region=None, location=None, bounds=None, **kwargs):
    """Returns general geographic information. 

    Assigns one and only one of arguments: 'region', 'bounds', 'location' 
    for different searching types. More details is available here:
    http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi.

    :param query: searching key word, e.g. '银行'.
    :type query: string

    :param region: region name or related cityCode, e.g. '北京', '131'.
    :type region: string

    :param location: lat & lng pair, e.g. '39.915,116.404'.
    :type location: string, list, tuple

    :param bounds: lat & lng pair of bottom-left, top-right points, 
        e.g. '39.915,116.404,39.975,116.414'.
    :type bounds: string, list/tuple of list/tuple

    :param **kwargs: optional parameters, e.g. output='json'.
    :type **kwargs: <key>=<value>

    :rtype: parsed result defiend in Parser, list or dict, default.
        raw callback, xml or json if setting 'raw=True'.
    
    """
    if not any([region, location, bounds]):
        raise ValueError("Assigns one and only one of arguments:\
                         'region', 'bounds', 'location'.")
    elif region:
        kwargs['region'] = region.strip()
    elif location:
        conv_loc = conv2str(location, 'location')
        if not conv_loc:
            raise ValueError("'location' incorrect! May as follows:\
                \nlocation = '39.915,116.404'\
                \nlocation = '39.915;116.404'\
                \nlocation = '39.915|116.404'\
                \nlocation = [39.915, 116.404]\
                \nlocation = (39.915, 116.404)")
        kwargs['location'] = conv_loc
    else:
        conv_bou = conv2str(bounds, 'location', 2, 2)
        if not conv_bou:
            raise ValueError("'bounds' incorrect! May as follows:\
                \nbounds = '39.915,116.404,39.975,116.414'\
                \nbounds = '39.915,116.404;39.975,116.414'\
                \nbounds = '39.915,116.404|39.975,116.414'\
                \nbounds = [[39.915, 116.404], [39.975, 116.414]]\
                \nbounds = ((39.915, 116.404), (39.975, 116.414))")
        kwargs['bounds'] = conv_bou
    kwargs.update({'server_name': 'place', 'version': 'v2', 'subserver_name': 'search',
                   'query': query.strip()})

    return client._get(kwargs)


def place_detail(client, uid=None, uids=None, **kwargs):
    """Returns detail geographic information for uid.

    Assigns one and only one of arguments: 'uid', 'uids'. 
    More details is available here:
    http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi.

    :param uid: uid of POI,  e.g. '8ee4560cf91d160e6cc02cd7'.
    :type uid: string

    :param uids: uid set, e.g. '8ee4560cf91d160e6cc02cd7,5ffb1816cf771a226f476058'.
    :type uids: string, list, tuple

    :param **kwargs: optional parameters, e.g. output='json'.
    :type **kwargs: <key>=<value>

    :rtype: parsed result defiend in Parser, list or dict, default.
        raw callback, xml or json if setting 'raw=True'.
    """
    if not any([uid, uids]):
        raise ValueError("Assigns one and only one of arguments:\
                          'uid' or 'uids'.")
    elif uid:
        kwargs['uid'] = uid.strip()
    else:
        conv_uids = conv2str(uids, 'location', 1, 5)
        if not conv_uids:
            raise ValueError("'uids' incorrect! May as follows:\
                \nuids = '8ee4560cf91d160e6cc02cd7,5ffb1816cf771a226f476058'\
                \nuids = '8ee4560cf91d160e6cc02cd7;5ffb1816cf771a226f476058'\
                \nuids = '8ee4560cf91d160e6cc02cd7|5ffb1816cf771a226f476058''\
                \nuids = ['8ee4560cf91d160e6cc02cd7', '5ffb1816cf771a226f476058']\
                \nuids = ('8ee4560cf91d160e6cc02cd7', '5ffb1816cf771a226f476058')")
        kwargs['uids'] = conv_uids
    kwargs.update({'server_name': 'place', 'version': 'v2', 'subserver_name': 'detail'})

    return client._get(kwargs)


def place_suggest(client, query, region, **kwargs):
    """Returns place suggestions matched user's input.

    More details is available here:
    http://lbsyun.baidu.com/index.php?title=webapi/place-suggestion-api

    :param query: searching key word, e.g. '银行', 'yinhang'.
    :type query: string

    :param region: region name or related cityCode, e.g. '北京', '131'.
    :type region: string

    :param **kwargs: optional parameters, e.g. output='json'.
    :type **kwargs: <key>=<value>

    :rtype: parsed result defiend in Parser, list or dict, default.
        raw callback, xml or json if setting 'raw=True'.
    """
    if 'location' in kwargs:
        conv_loc = conv2str(kwargs['location'], 'location')
        if not conv_loc:
            raise ValueError("'location' incorrect! May as follows:\
                \nlocation = '39.915,116.404'\
                \nlocation = '39.915;116.404'\
                \nlocation = '39.915|116.404'\
                \nlocation = [39.915, 116.404]\
                \nlocation = (39.915, 116.404)")
        kwargs['location'] = conv_loc

    kwargs.update({'server_name': 'place', 'version': 'v2', 'subserver_name': 'suggestion',
                   'region': region.strip(), 'query': query.strip()})

    return client._get(kwargs)


def geocode(client, address, **kwargs):
    """Returns place coordinate.

    More details is available here:
    http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding

    :param address: e.g. '北京市海淀区上地十街10号', '北一环路和阜阳路的交叉路口'.
    :type address: string

    :param **kwargs: optional parameters, e.g. output='json'.
    :type **kwargs: <key>=<value>

    :rtype: parsed result defiend in Parser, list or dict, default.
        raw callback, xml or json if setting 'raw=True'.
    """
    kwargs.update({'server_name': 'geocoder', 'version': 'v2', 'subserver_name': '',
                   'address':address.strip()})

    return client._get(kwargs)


def direct(client, origin, destination, mode='driving', region=None, **kwargs):
    """Returns information for 4 types of direction demand.

    More details is available here:
    http://lbsyun.baidu.com/index.php?title=webapi/direction-api-v2

    :param origin: lat & lng pair, e.g. '39.915,116.404'.
    :type origin: string, list, tuple

    :param destination: lat & lng pair, e.g. '41.115,112.352'.
    :type destination: string, list, tuple

    :param mode: types of direction: {'driving', 'transit', 'riding', 'walking'}.
    :type mode: string

    :param region: region name or related cityCode for walking mode, e.g. '北京', '131'.
    :type region: string

    :param origin: lat & lng pair, e.g. '北京市海淀区上地十街10号', '北一环路和阜阳路的交叉路口'.
    :type origin: string

    :param **kwargs: optional parameters, e.g. output='json'.
    :type **kwargs: <key>=<value>

    :rtype: parsed result defiend in Parser, list or dict, default.
        raw callback, xml or json if setting 'raw=True'.
    """
    conv_ori = conv2str(origin, 'origin')
    if not conv_ori:
        raise ValueError("'origin' incorrect! May as follows:\
            \norigin = '39.915,116.404'\
            \norigin = '39.915;116.404'\
            \norigin = '39.915|116.404'\
            \norigin = [39.915, 116.404]\
            \norigin = (39.915, 116.404)")
    kwargs['origin'] = conv_ori

    conv_des = conv2str(destination, 'destination')
    if not conv_ori:
        raise ValueError("'destination' incorrect! May as follows:\
            \ndestination = '39.915,116.404'\
            \ndestination = '39.915;116.404'\
            \ndestination = '39.915|116.404'\
            \ndestination = [39.915, 116.404]\
            \ndestination = (39.915, 116.404)")
    kwargs['destination'] = conv_des

    if mode in ['driving', 'transit', 'riding']:
        kwargs.update({'version': 'v2', 'subserver_name': mode})
    elif mode ='walking':
        if not region:
            raise ValueError('Please assign "region".')
        kwargs.update({'region': region, 'version': 'v2', 
                       'subserver_name':'', 'mode': mode})
    else:
        raise ValueError("'mode' incorrect! May as follows: ['driving',\
                         'walking', 'transit', 'riding'].")

    kwargs.update({'server_name': 'direction', 'origin': origin, 'destination': destination})

    return client._get(kwargs)

def ip_locate(client, **kwargs):
    """Returns location for given ip or current ip.

    More details is available here:
    http://lbsyun.baidu.com/index.php?title=webapi/ip-api

    :param **kwargs: optional parameters, e.g. ip='211.161.240.85'.
    :type **kwargs: <key>=<value>

    :rtype: parsed result defiend in Parser, list or dict, default.
        raw callback, xml or json if setting 'raw=True'.
    """
    if 'ip' in kwargs:
        ip_check(kwargs['ip'])
    kwargs.update({'server_name': 'location', 'version': '', 'subserver_name': 'ip'})

    return client._get(kwargs)


def route_matrix(client, origins, destinations, mode='driving', **kwargs):
    """Returns multiple direction and time spent. 

    More details is available here:
    http://lbsyun.baidu.com/index.php?title=webapi/route-matrix-api-v2

    :param origins: lat & lng pairs, e.g. '39.915,116.404,39.975,116.414'.
    :type origins: string, list/tuple of list/tuple

    :param destinations: lat & lng pairs, e.g. '39.915,116.404,39.975,116.414'.
    :type destinations: string, list/tuple of list/tuple

    :param mode: types of direction: {'driving', 'riding', 'walking'}.
    :type mode: string

    :param **kwargs: optional parameters, e.g. output='json'.
    :type **kwargs: <key>=<value>

    :rtype: parsed result defiend in Parser, list or dict, default.
        raw callback, xml or json if setting 'raw=True'.
    """
    conv_oris = conv2str(origins, 'origins', 1, 50, '|')
    if not conv_oris:
        raise ValueError("'origins' incorrect! May as follows:\
                \norigins = '39.915,116.404,39.975,116.414'\
                \norigins = '39.915,116.404;39.975,116.414'\
                \norigins = '39.915,116.404|39.975,116.414'\
                \norigins = [[39.915, 116.404], [39.975, 116.414]]\
                \norigins = ((39.915, 116.404), (39.975, 116.414))")
    kwargs['origins'] = conv_oris

    conv_dess = conv2str(destinations, 'destinations', 1, 50, '|')
    if not conv_dess:
        raise ValueError("'destinations' incorrect! May as follows:\
                \ndestinations = '39.915,116.404,39.975,116.414'\
                \ndestinations = '39.915,116.404;39.975,116.414'\
                \ndestinations = '39.915,116.404|39.975,116.414'\
                \ndestinations = [[39.915, 116.404], [39.975, 116.414]]\
                \ndestinations = ((39.915, 116.404), (39.975, 116.414))")
    kwargs['destinations'] = conv_dess


    if mode not in ["driving", "walking", "riding"]:
        raise ValueError("'mode' incorrect! It should in {'driving', 'walking', 'riding'}.") 
    else:
        kwargs.update({'server_name': 'routematrix', 'version': 'v2', 'subserver_name': mode,
                       'origins': origins, 'destinations': destinations})

    return client._get(kwargs)

def geoconv(client, coords, **kwargs):
    """Convert none-Baidu coordinate to Baidu's. 

    More details is available here:
    http://lbsyun.baidu.com/index.php?title=webapi/guide/changeposition

    :param coords: lat & lng pairs, e.g. '39.915,116.404,39.975,116.414'.
    :type coords: string, list/tuple of list/tuple

    :param **kwargs: optional parameters, e.g. output='json'.
    :type **kwargs: <key>=<value>

    :rtype: parsed result defiend in Parser, list or dict, default.
        raw callback, xml or json if setting 'raw=True'.
    """
    conv_coos = conv2str(coords, 'coords', 1, 10000, ';')
    if not conv_oris:
        raise ValueError("'coords' incorrect! May as follows:\
                \ncoords = '39.915,116.404,39.975,116.414'\
                \ncoords = '39.915,116.404;39.975,116.414'\
                \ncoords = '39.915,116.404|39.975,116.414'\
                \ncoords = [[39.915, 116.404], [39.975, 116.414]]\
                \ncoords = ((39.915, 116.404), (39.975, 116.414))")

    kwargs.update({'server_name': 'geoconv', 'version': 'v1',
                  'subserver_name': '', 'coords': conv_coos})

    return client._get(kwargs)
