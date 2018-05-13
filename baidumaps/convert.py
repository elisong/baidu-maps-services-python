# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright © 2015-2018 Eli Song<elisong.ah@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re

def simple2str(x, name, len_expect_l=2, len_expect_r=2):
    sep_pattern = re.compile(r'[,;|]')

    if isinstance(x, str):
        x = sep_pattern.split(x)
    elif isinstance(x, list) or isinstance(x, tuple):
        if isinstance(x[0], list) or isinstance(x[0], tuple):
            x = [val for sub in x for val in sub]
    else:
        raise ValueError("'{}' should be 'str', 'list' or 'tuple' instance.".format(name))

    if len(x) >= len_expect_l and len(x) <= len_expect_r:
        return ','.join([str(i).strip() for i in x])
    else:
        return None

def complex2str(x, name, len_expect_l=2, len_expect_r=2):
    sep_pattern = re.compile(r'[,;|]')

    if isinstance(x, str):
        x = sep_pattern.split(x)
    elif isinstance(x, list) or isinstance(x, tuple):
        if isinstance(x[0], list) or isinstance(x[0], tuple):
            x = [val for sub in x for val in sub]
    else:
        raise ValueError("'{}' should be 'str', 'list' or 'tuple' instance.".format(name))

    if len(x) >= len_expect_l and len(x) <= len_expect_r:
        tmp = [','.join(x[(2*i):(2*i+2)]) for i in range(0, int(len(x)/2))]
        return '|'.join(tmp)
    else:
        return None

def ip_check(ip):
    IP4_pattern = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    IP6_pattern = re.compile(r"^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$")
    check = IP4_pattern.match(ip) or IP6_pattern.match(ip)
    if not check:
        raise ValueError("'ip' incorrect!")
    else:
        pass


