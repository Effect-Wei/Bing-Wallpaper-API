import json
import flask
import requests
#from cachelib import SimpleCache
from cachelib import MemcachedCache


BING_URL = "https://www.bing.com"
BING_API_URL = "https://www.bing.com/HPImageArchive.aspx"
MC_SERVERS = ['172.17.0.1:11211']
KNOWN_RESOLUTION = [
    '1920x1200',
    '1920x1080',
    '1366x768',
    '1280x768',
    '1024x768',
    '800x600',
    '800x480',
    '768x1280',
    '720x1280',
    '640x480',
    '480x800',
    '400x240',
    '320x240',
    '240x320'
]

app = flask.Flask(__name__)
#app.config["DEBUG"] = True
#cache = SimpleCache()
cache = MemcachedCache(servers=MC_SERVERS)


@app.route("/bing", methods=["GET"])
def bing():
    """Get image from Bing and return it to user"""

    idx = 0
    mkt = "zh-cn"
    width = 1920
    height = 1080
    original = 0

    if 'mkt' in flask.request.args:
        mkt = flask.request.args['mkt']
    if 'idx' in flask.request.args:
        idx = int(flask.request.args['idx'])
    if 'w' in flask.request.args:
        width = int(flask.request.args['w'])
    if 'h' in flask.request.args:
        height = int(flask.request.args['h'])
    if 'original' in flask.request.args:
        original = flask.request.args['original']

    request_resolution = str(width) + "x" + str(height)

    bing_api_request_url = BING_API_URL + \
        "?format=js&n=1" + "&mkt=" + mkt + "&idx=" + str(idx)
    bing_api_response = requests.get(bing_api_request_url)
    info = json.loads(bing_api_response.text)

    bing_url_base = info["images"][0]["urlbase"]

    if original == str(1):
        bing_img_url = BING_URL + bing_url_base + "_UHD.jpg"
    elif request_resolution in KNOWN_RESOLUTION:
        bing_img_url = BING_URL + bing_url_base + "_" + request_resolution + ".jpg"
    else:
        bing_img_url = BING_URL + bing_url_base + "_UHD.jpg&rs=1&c=1" \
            + "&w=" + str(width) + "&h=" + str(height)

    cache_key = str(hash(bing_img_url))
    img = cache.get(cache_key)
    if img is None:
        img = requests.get(bing_img_url)
        cache.set(cache_key, img, timeout=60*60)

    response = flask.Response(img, mimetype="image/jpeg")
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
