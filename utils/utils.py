# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright © 2015-2018 Eli Song<elisong.ah@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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

