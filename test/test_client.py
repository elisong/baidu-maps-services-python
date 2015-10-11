# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright © 2015 Eli Song

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest
import baidumaps
from baidumaps import client as _client


class ClientTest(unittest.TestCase):
    def setUp(self):
        self.client = _client.Client('ak=GuMrViec3jLp1WCG4P3VLDlC')

    def tearDown(self):
        self._client = None

    def test_no_ak_key(self):
        with self.assertRaises(Exception):
            client = baidumaps.Client()

    def test_invalid_ak_key(self):
        with self.assertRaises(Exception):
            client = baidumaps.Client(ak='Invalid key.')

    def test_generate_url_ip_locate(self):
        genurl = self.client.generate_url({'server_name': 'location',
                                          'version': '',
                                          'subserver_name': 'ip'})
        expected_url = 'http://api.map.baidu.com/location/\
                        ip?ak=GuMrViec3jLp1WCG4P3VLDlC'
        self.assertEqual(expected_url, genurl)

    def test_get_nothing(self):
        with self.assertRaises(Exception):
            result = self.client.get({'server_name': 'location',
                                     'version': '',
                                     'subserver_name': 'ip',
                                     'ip': '64.233.160.0'})

    def test_get_something(self):
        result = self.client.get({'server_name': 'location',
                                 'version': '',
                                 'subserver_name': 'ip',
                                 'ip': '202.198.16.3'})
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
