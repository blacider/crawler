#!/usr/bin/python  
import re   
import urllib
import random
import urllib2
import cookielib
import subprocess
ids = {}
global filename
#init cookie
cookie = cookielib.CookieJar()
handler=urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
def getUrl():
    id = int(random.uniform(1, 4000))
    while ids.has_key("id"+str(id)):
        id = int(random.uniform(1, 4000))
    ids["id"+str(id)] = 1
    url = "http://www.720xx.top/vod-detail-id-"+str(id)+".html"
    print "generete url:%s" %url
    return url
def getHtml(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    req = urllib2.Request(url); # urllib2.Request: the HTTP request will be a POST instead of a GET when the data parameter is provided.
    req.add_header('User-Agent', user_agent);
    req.add_header('Content-Type', 'application/x-www-form-urlencoded');
    req.add_header('Cache-Control', 'no-cache');
    req.add_header('Accept', '*/*');
    req.add_header('Connection', 'Keep-Alive');
    response = opener.open(req)
    # for item in cookie:
    #     print 'Name = '+item.name
    #     print 'Value = '+item.value
    return response.read()
def getUrlPath(html):
    r = r'var urlpath ="(.*)";'
    re_id=re.compile(r)
    urlpath = re.findall(re_id,html)[0]
    r = r'var type ="(.*)";'
    re_id=re.compile(r)
    urltype = re.findall(re_id,html)[0]
    r = r'var from ="(.*)";'
    re_id=re.compile(r)
    from_ = re.findall(re_id,html)[0]
    r = r'<h1>(.*)</h1>'
    re_id=re.compile(r)
    global filename
    filename = re.findall(re_id,html)[0]
    print 'find urlpath:'+urlpath+', urltype:'+urltype+"title:"+filename
    return "http://www.720xx.top/kan.php?from="+from_+"&url="+urlpath
def getMp4(html):  
    r=r"f:'(http://.*\.mp4)'"
    re_mp4=re.compile(r)  
    mp4url=re.findall(re_mp4,html)[0]
    print mp4url
    global filename
    cmd='wget -O %s %s' % (filename+".mp4",mp4url)
    subprocess.call(cmd,shell=True)
for i in range(0, 20):
    cookie = cookielib.CookieJar()
    handler=urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    html=getHtml(getUrl())
    urlPath = ''
    try:
        urlPath = getUrlPath(html)
    except IndexError:
        continue
    else:
        print urlPath
        html = getHtml(urlPath)
        getMp4(html)
        print "\n\n"
print 'end'
