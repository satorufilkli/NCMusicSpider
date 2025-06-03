# NCMusicSpider

简易的网易云音乐爬虫工具，用于获取歌单信息和下载链接。

## *V2版本发布*

> 新增使用Pyside6编写GUI页面，并基于新版本进行重构。目前的功能依旧是爬取歌单信息并提取下载链接，为解决面向对象程序设计期末大作业而更新(本来想着有时间前端用vue，react写一下，但是老师要求要用pyside，那就一起做了)



## 使用事例

![图1](.\images\1.png)

![图2](.\images\2.png)



日志

![图3](.\images\3.png)



## 环境变量配置

在 `.env` 文件中配置以下信息：

```
PLAYLIST_API="https://example.com/playlist/track/all"
DOWNLOAD_API="https://example.com/song/url/v1"

NETEASE_COOKIE="your_netease_cookie_here(MUSIC_U=……)"

USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```

项目相关依赖：pyside6, dotenv, request等自行pip下载

部署网易云 API，详情参见 [Binaryify/NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)

>  emm，可暂用 https://musicapi.zjgsu-forum.top ,这个是我自己部署到vercel然后挂到自己的子域名上的，这个域名暂时应该还是会用着的，以后说不准，最好是自己搭一个，还可以对接一下 [qier222/YesPlayMusic](https://github.com/qier222/YesPlayMusic) 给自己用。cookie的话网页版网易云登录就可以从浏览器的开发者工具里获取，要的是“MUSIC_U”那个，歌单id的话网页版打开歌单后的网址参数里就有。



## 致谢

感谢[NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)提供支持
