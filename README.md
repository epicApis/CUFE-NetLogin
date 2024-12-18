# CUFE-NetLogin

登录中央财经大学总是需要重新验证的校园

# 这是什么？

作为一个多设备用户，因为校园网最大连接三台设备的限制，看见 CUFE 校园网的登录界面已然家常便饭。但是每次都要等待登录网页弹出并输入账号密码，即使是有自动填充也让人不胜其烦。加之以时不时的波动导致的重新登录，让在宿舍部署远程桌面变得及其不稳定。为什么不用程序来实现一键登录和断线重连呢？

本项目提供了一个简单网页工具和由 Python 编写的跨平台脚本，并计划包括 Windows、macOS 版本的应用以实现断线重连，作为跨平台开发的练习和运用。

本项目仅供交流、学习使用，作者不会通过该程序窃取用户信息，所有用户信息均于用户设备上计算和存储，但用户仍应该保持审慎态度并对自己的数据安全负责，特别是使用非由此项目发布的内容时。

# 使用方法

## 网页工具

访问 [epicapis.net](https://epicapis.net) 或 [epicapis.github.io/CUFE-NetLogin](https://epicapis.github.io/CUFE-NetLogin/)。

## Python 脚本

在确保当前环境安装了 Python 及其 requests 包的情况下，下载 releases 中的 logincufe.py 脚本后，编辑并保存其中的学号和密码，然后运行即可查看效果。

### 安装 Python 和 requests

#### 安装 Python

请访问 [Python 官方下载页面](https://www.python.org/downloads/) 并根据您的操作系统下载并安装最新版本的 Python。

#### 安装 requests 包

在安装 Python 后，您可以通过以下命令在命令行中安装 requests 包：

```bash
pip install requests
```

或者使用

```bash
python -m pip install requests
```

# 项目主要文件说明

## logincufe.py

这是主要的 Python 脚本文件，用于实现自动登录功能。用户需要在此文件中填写自己的学号和密码。

## login1page.html

这是一个备用的解决方案，提供了一个更复杂的操作流程，适合作为练习使用。

## docs\index.html

这是一个静态网页文件，提供了一个简单的用户界面，用户可以通过此网页进行登录链接生成操作。也是网页工具的使用的主页面。
