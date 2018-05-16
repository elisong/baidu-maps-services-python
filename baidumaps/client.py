# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright © 2015-2018 Eli Song<elisong.ah@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re
import hashlib
import requests
import baidumaps
from baidumaps import apis
from baidumaps import exceptions
from baidumaps import parse

try: # Python 3
    from urllib.parse import urlencode, quote, quote_plus
except ImportError: # Python 2
    from urllib import urlencode, quote, quote_plus

class Client(object):
    def __init__(self, ak=None, sk=None, domain='http://api.map.baidu.com',
                 output='json'):
        if not ak:
            raise ValueError("Must provide API when creating client. Refer to:\
                             \nthe link: http://lbsyun.baidu.com/apiconsole/key")

        self.ak = ak
        self.domain = domain
        self.output = output
        self.s = requests.Session()

    def _get(self, params):
        url = self._generate_url(params)
        response = self.s.get(url)
        status_code = response.status_code


        url = self._generate_url(params)
        response = self.s.get(url).json()

        status = response['status']
        server_name = params['server_name']
        subserver_name = params['subserver_name']
        if status != 0:
            raise exceptions.StatusError(server_name, subserver_name, status)
        elif 'raw' in params and params['raw']:
            result = response
        else:
            result = self.parse(server_name, subserver_name, response)
        return result

    def _generate_url(self, params):
        api = '/' + '/'.join([params['server_name'],
                              params['version'],
                              params['subserver_name']]) + '?'
        api = re.sub(r'//ip', '/ip', api)  # for ip_locate()
        temp = params.copy()
        {temp.pop(key) for key in ['server_name', 'version', 'subserver_name']}
        temp.update({'output': params.get('output', self.output), 'ak': self.ak})
        query = api + urlencode(temp)
        if self.sk:
            quoted = quote(query, safe="/:=&?#+!$,;'@()*[]") + self.sk
            sn = hashlib.md5(quote_plus(quoted).encode('utf-8')).hexdigest()
            query += '&sn=' + sn

        url = self.domain + query
        return url


Client.place_search = apis.place_search
Client.place_detail = apis.place_detail
Client.place_eventsearch = apis.place_eventsearch
Client.place_eventdetail = apis.place_eventdetail
Client.place_suggest = apis.place_suggest
Client.geocode = apis.geocode
Client.direct = apis.direct
Client.ip_locate = apis.ip_locate
Client.route_matrix = apis.route_matrix
Client.geoconv = apis.geoconv
Client.parse = parse.parse


if __name__ == "__main__":
    bdmaps = Client(ak='<Your Baidu Auth Key>')
    result = bdmaps.geoconv('114.21892734521,29.575429778924')
    print result
