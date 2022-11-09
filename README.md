## 造梦西游的pygame复现（联机版/单机版）

### 单机版
#### 环境部署
1.安装pygame模块
```shell
pip3 install pygame
```
2.执行程序
```shell
cd zaomeng-offline
python3 zaomeng.py
```
#### 游戏演示
![image-20180902192805872](./md_image/1.gif)


### 联机版
#### 环境部署
1.首先要有一个具备公网ip的服务器

2.在服务器控制台里打开79号端口
![控制台](./md_image/1.png)

3.服务器内安装pygame模块
```shell
pip3 install pygame
```

4.在客户端主机上，修改服务器公网ip
```shell
cd zaomeng-online-client
```
将其中的client.py文件里第26行的sever_ip的值改为服务器的公网ip地址

4.服务器端执行服务端程序
```shell
cd zaomeng-online-server
python3 server.py
```

5.客户端执行程序
在两个具有联网功能的机器上打开客户端，执行客户端程序
```shell
cd zaomeng-online-client
python3 client.py
```
#### 游戏演示
![image-201882](./md_image/2.gif)

### 开发笔记
1.[基础场景控制篇](https://blog.csdn.net/weixin_43412878/article/details/110622207?spm=1001.2014.3001.5502)

2.[玩法开发——躲避游戏](https://blog.csdn.net/weixin_43412878/article/details/124714806?spm=1001.2014.3001.5502)

3.[BOSS与AI攻击](https://blog.csdn.net/weixin_43412878/article/details/124890497?spm=1001.2014.3001.5502)

4.[联机功能篇](https://blog.csdn.net/weixin_43412878/article/details/124916404?spm=1001.2014.3001.5502)

### 该功能只用于开发学习，不做商业用途~