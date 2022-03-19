# Bing Wallpaper API

***一次请求直接获取 JPG 图像***

![今日中国大陆区必应美图 @ 1080P](https://api.effects.space/bing "今日中国大陆区必应美图")
*今日中国大陆区必应美图 @ 1080P*

---

## 前言

必应的壁纸很好看，但是官方 API 仅返回 Json 或 XML 而不是直接提供图片。  
为了在以后使用的时候更方便，我随手整了这东西出来。  
并使用了 Docker 以便部署与管理。

~~*请尽可能忽略我的垃圾代码所带来的不适*~~

---

## Have a try

GET https://api.effects.space/bing

>为了减少处理时间，这里使用了 `Cachelib` 的 `SimpleCache` 作为缓存，过期时间为 60 分钟。  
>也可以在源代码中手动改为使用 `Memcached`，需用 `pip` 安装 `libmc`，详见[Cachelib文档](https://cachelib.readthedocs.io/en/stable/memcached/)。

| Query String | Type   | Default | Definition                                     |
| ------------ | ------ | ------- | ---------------------------------------------- |
| mkt          | string | "zh-cn" | 必应的区域，图片可能因该值变化而变化           |
| idx          | int    | 0       | 图片日期与今天的偏差值，"0" 是今天，"1" 是昨天 |
| w            | int    | 1920    | 图片宽度                                       |
| h            | int    | 1080    | 图片高度                                       |
| original     | bool   | 0       | 是否获取未缩放的原始图片，将会覆盖 "w" 和 "h"  |

---

## 如何部署

使用 Docker：
```shell
docker run -d -p 80:<外部端口> effectwei/bing-wallpaper-api:latest
```
容器内 `HTTP 协议`默认使用 `80` 端口，`uwsgi 协议`默认使用 `81` 端口，可以在 `uwsgi.ini` 中更改。

---

## 可能的问与答

Q：这有什么优势吗？  
A：完全符合了我的需求。~~并为我旷课提供了理由。~~

Q：它有什么足以让我转向它的理由吗？  
A：没有，我部署的版本甚至不保障稳定运行时间。不妨看看[这里](https://status.effects.space/)以查看其是否在线。
