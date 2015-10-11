Python Client for Baidu Maps Web Services
=============================================

![image](./data/baidumaps.png)

## Descriptions

This is an unofficial Python Client Library for [Baidu Maps Web Services APIs][baiduapis]:

- [Place API]
- [Place Suggestion API]
- [Geocoding API]
- [Direction API]
- [Route Matrix API]
- [IP Location API]
- [Geoconv API]

The author prepared the library just for occasional requirement from one of his friends. If high performance required, Baidu's official JavaScript API may be the best choice. Moreover, thank Google and their [Python Client library for Google Maps API Web Services][googleapis] for setting a good model to the author.

## Attentions

The library keeps almost the same inputs/outputs as official apis provides, except that:

- only parse `json` outputs just now, NO support for `xml`.
- default return is a simpler version of raw API callback. set `raw=True` for complete raw json callback.
- always use `<lng, lat>`, NOT `<lat, lng>` whenever you need.

>  Occationally, I met `Geoconv` API at the very beginning which fed on `<lng, lat>` coordinates order. Took it for granted, nothing surprise. Next, I wrapt Place API, it required `<lat, lng>`, so I added transform processing, keeping pace with `Geoconv` API wrapper... How funny it is! All of raw apis, except `Geoconv`, supported `<lat, lng>` coordinates order!

## Installation
```sh
$ git clone git@github.com:elisong/baidu-maps-services-python.git
$ cd baidu-maps-services-python
$ python setup.py install
```
Note the library was built under Ubuntu 14.04 LTS & Python 2.7.6.

## Simple Case

```python
>>> import baidumaps
>>> bdmaps = baidumaps.Client(ak='<Your Baidu Auth Key>')
>>> bdmaps.place_search(query='银行', region='北京')
[{"name": "中国工商银行(中关村支行)",
  "location": {"lng": 116.312202,
               "lat": 40.052384},
  "address": "信息路2-1号国际创业园1号楼1-4F",
  "uid": "50f7d1461e9309c472210b6c"},
 {...},
 {...}]
```

## Usage
Before using Baidu Maps APIs services, read at least these official pages:

- [概述.Web服务API][gaishu]
- [使用须知][xuzhi]
- [使用条款][tiaokuan]
- [申请ak密钥][aklink]


### Initialize Client
```python
>>> import baidumaps
>>> bdmaps = baidumaps.Client(ak='<Your Baidu Auth Key>',
                              domain='http://api.map.baidu.com',
                              output='json')
```

### Choose API

|APIs|Base URL|function here|
|:--|:--|:--|
|[Place API]|http://api.map.baidu.com/place/v2/search|place_search|
||http://api.map.baidu.com/place/v2/detail|place_detail|
||http://api.map.baidu.com/place/v2/eventsearch|place_eventsearch|
||http://api.map.baidu.com/place/v2/eventdetail|place_eventdetail|
|[Place Suggestion API]|http://api.map.baidu.com/place/v2/suggestion|place_suggest|
|[Geocoding API]|http://api.map.baidu.com/geocoder/v2/|geocode|
|[Direction API]|http://api.map.baidu.com/direction/v1|direct|
|[Route Matrix API]|http://api.map.baidu.com/direction/v1/routematrix|route_matrix|
|[IP Location API]|http://api.map.baidu.com/location/ip|ip_locate|
|[Geoconv API]|http://api.map.baidu.com/geoconv/v1|geoconv|

A base url usually conbined by `domain`(域名)+ `server_name`(服务名)+`version`(服务版本号)+`subserver_name`(子服务名). Take `http://api.map.baidu.com/place/v2/search` for example:

- domain: http://api.map.baidu.com
- server_name: place
- version: v2
- subserver_name: search

#### place_search()
```python
>>> bdmaps.place_search(query='银行', region='北京')
>>> bdmaps.place_search(query='银行', bounds='116.404,39.915,116.414,39.975')
>>> bdmaps.place_search(query='银行', location='116.404,39.915')
```

As for argument `bounds`,

- '116.404,39.915,116.414,39.975'
- '116.404,39.915;116.414,39.975'
- '116.404,39.915|116.414,39.975'
- [[116.404, 39.915], [116.414, 39.975]]

are all valid and equal. argument `location`, similarly.

#### place_detail()
```pyton
>>> bdmaps.place_detail(uid='8ee4560cf91d160e6cc02cd7')
>>> bdmaps.place_detail(uids='8ee4560cf91d160e6cc02cd7;5ffb1816cf771a226f476058')
```

#### place_eventsearch()
```python
>>> bdmaps.place_eventsearch(query='美食', event='groupon', region='北京',
                             bounds='116.404,39.915,116.414,39.975')
```

#### place_eventdetail()
```python
>>> bdmaps.place_eventdetail(uid='8ee4560cf91d160e6cc02cd7')
```
> no support for 2 uids or more in one request.


#### place_suggest()
>>> bdmaps.place_suggest(query='天安门', region='北京')
```

#### geocode()
```python
>>> bdmaps.geocode(address='百度大厦')
>>> bdmaps.geocode(location='116.43213,38.76623')
```

#### direct()
```python
>>> bdmaps.direct(origin='清华大学', destination='北京大学',
                  origin_region='北京', destination_region='北京')
>>> bdmaps.direct(origin='清华大学', destination='北京大学',
                  region='北京', mode='transit')
```

- when `mode=None` or `mode='driving'`,`origin_region`, `destination_region` needed;
- when `mode='walking'` or `mode='transit'`,`region` needed;

#### ip_locate()
```python
>>> bdmaps.ip_locate()
>>> bdmaps.ip_locate(ip='202.198.16.3')
```

#### route_matrix()
```python
>>> bdmaps.route_matrix(origins='114.21892734521,29.575429778924',
                        destinations='115.21892734521,29.575429778924')
>>> bdmaps.route_matrix(origins='天安门|鸟巢',
                        destinations='北京大学|东方明珠')
```

#### geoconv()
```python
>>> bdmaps.geoconv('114.21892734521,29.575429778924')
>>> bdmaps.geoconv([[114.21892734521, 29.575429778924],
                    [114.21892734521, 29.575429778924]])
```

[baiduapis]: http://developer.baidu.com/map/index.php?title=webapi
[Place API]: http://developer.baidu.com/map/index.php?title=webapi/guide/webservice-placeapi
[Place Suggestion API]: http://developer.baidu.com/map/index.php?title=webapi/place-suggestion-api
[Geocoding API]: http://developer.baidu.com/map/index.php?title=webapi/guide/webservice-geocoding
[Direction API]: http://developer.baidu.com/map/index.php?title=webapi/direction-api
[Route Matrix API]: http://developer.baidu.com/map/index.php?title=webapi/route-matrix-api
[IP Location API]: http://developer.baidu.com/map/index.php?title=webapi/ip-api
[Geoconv API]: http://developer.baidu.com/map/index.php?title=webapi/guide/changeposition
[googleapis]: https://github.com/googlemaps/google-maps-services-python
[application link]: http://lbsyun.baidu.com/apiconsole/key?application=key

[gaishu]: http://developer.baidu.com/map/index.php?title=webapi
[tiaokuan]: http://developer.baidu.com/map/index.php?title=open/law
[xuzhi]: http://developer.baidu.com/map/index.php?title=open/question
[aklink]: http://lbsyun.baidu.com/apiconsole/key?application=key
