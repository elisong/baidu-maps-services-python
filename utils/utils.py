# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright © 2015-2018 Eli Song<elisong.ah@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import re
import os
import json
import bs4
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


d = os.path.dirname(__file__)
par_d = os.path.join(d, '..')

def get_status_code(url='http://lbsyun.baidu.com/index.php?title=webapi/appendix')
    response = urlopen(url)
    data = response.read()
    soup = bs4.BeautifulSoup(data, 'lxml')

    status_code = {}
    tab = soup.table
    for ta in tab:
        if isinstance(ta, bs4.element.Tag) and ta.find('td'):
            row = [tdh.string.strip() if tdh.string else None for tdh in ta.findAll('td')]
            status_code.update({row[0]: row[1]})

    with open(os.path.join(par_d, 'data/status_code.json'), 'w') as f: 
        json.dump(status_code, f)
    return 1 if status_code else 0

def get_city_code():
    pass

def ip_check(ip):
    IP4_pattern = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    IP6_pattern = re.compile(r"^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$")
    check_ok = IP4_pattern.match(ip) or IP6_pattern.match(ip)
    if not check_ok:
        raise ValueError("'ip' incorrect!")
    else:
        pass

def conv2str(x, name, len_expect_l=1, len_expect_r=1, sep=',', reverse=False):
    seps = re.compile(r'[,;|]')

    if isinstance(x, str):
        x = seps.split(x)
        x = list(zip(x[0::2], x[1::2]))
    elif isinstance(x, (list, tuple)):
        if isinstance(x[0], str) or isinstance(x[0], float):
            x = list(zip(x[0::2], x[1::2]))
    else:
        raise ValueError("'{}' should be 'str', 'list' or 'tuple' instance.".format(name))

    if len(x) >= len_expect_l and len(x) <= len_expect_r and not reverse:
        return sep.join([str(lat).strip()+','+str(lng).strip() for lat, lng in x])
    elif len(x) >= len_expect_l and len(x) <= len_expect_r and reverse:
        return sep.join([str(lng).strip()+','+str(lat).strip() for lat, lng in x])
    else:
        return None