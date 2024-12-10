# Music Spider

一个简单的网易云音乐爬虫工具，用于获取歌单信息和下载链接。

## 功能特性

- 获取歌单中的歌曲信息
- 支持获取不同音质的下载链接
- 支持自定义获取数量

## 支持的音质等级

- standard => 标准,
- higher => 较高,
- exhigh => 极高,
- lossless => 无损,
- hires => Hi-Res,
- jyeffect => 高清环绕声,
- sky => 沉浸环绕声,
- dolby => 杜比全景声,
- jymaster => 超清母带

## 环境变量配置

在 `.env` 文件中配置以下信息：

```plaintext
NETEASE_COOKIE=你的网易云音乐cookie
USER_AGENT=你的浏览器用户代理
```

## 致谢

感谢[NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)提供支持
