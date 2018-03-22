## 开发备忘

> 以下模块都会尽量设计为可复用的形式，但又带有一定特性

###### 基本通用的 连接sql的 用户模块（finished）Tiny_storage

**事实上这种建模对结构型数据库有点多余，不如做个Nosql的类似ORM的建模模块（挖坑+1）**

[用于后台便捷操作用户] 

api功能:

对用户建模
1）确定创建时需要的信息 （用户名 密码或md5
2）确定有哪些属性/默认值
（动态属性要支持默认为 自定义函数）

对用户进行操作
input->action
1）init info->建模存入db
2）attr,value->确认信息 (用于身份确认
3）attr,new value->更新信息
4）user name->删除用户
5）user name->用户信息对象


采用快捷的骚操作
输入所需属性，自定义函数
由函数产生子类

用一定格式储存数据库结构

---

###### 一个基础队列模块（finished） Tiny_Q

[用于聊天记录客户端持久化]
在接收到新消息，但没查看这个频道时，使用对应队列储存
要支持硬盘储存，实现本地持久化(消息记录

func:
实现一般队列的功能
将每个队列封装为对象
1）init params->初始化队列创建参数（容量等）

2）name,create signal ->创建并以一定格式保存队列

3）name,msg->将信息加入队列，更新本地储存

4）name,consume signal->取出信息

5）name->销毁无效队列

---

###### Cookie管理模块 (working)  Zookie

**形式**

- 时间管理（默认30/无/自定义），可作为一个选项，让模块使用者（或由使用者暴露给用户）选择，也可以放在Get函数中动态更改
- 包含信息字段选择可变
- Get/Check函数由cookie模型建立时自动产生
  - Get(user_info) -> cookie_str
  - Check(cookie_str) -> Info/Unknown(None)/TLE 

>举个栗子：Check(cookie) -> Unknown -> Get(guest , True) 
>
>未能识别（或无）cookie，则返回游客用cookie(无限制)
>
>这种逻辑是由使用者写的，当然也可以作为本模块的增量

**存储**

- 模块基础功能不包含信息的存储，但作为扩展的session功能会提供简单的信息存储

**交换**

- 安全性：无加密/内建加解密/传入加解密函数
- 函数传入/出都为转码/计算后的字串

---

###### 通用用户身份管理模块



---

###### rmq封装模块(信息交换核心模块)

消息分发
【上层】有N个room exchange对应不同的room，1个topic exchange处理p2p对话

> 如何进行保密？
>
> 每个room ex需要以特定key来bind（那么如何确定聊天身份呢？
> 公用的topic ex则需要以一个加密串作为key来证明身份 这个串的列表由管理服务维护

【中层】对每个用户，维护一个room队列，一个topic队列 在连接后自动本地持久化
【下层】每个用户切换一次频道只需要维护一个publisher（旧的x掉）

> 如果能多开，那么开几个窗口，就需要维护几个publisher，
>
> 需要两个consumenr（如果有协议的话一个consumer也是足够的）
>
> 根据协议（？）对新收到的信息进行分类、本地队列储存。接入某频道时	
>
> 本地consume对应队列的信息

以上这些都在服务端进行

因为身份验证的问题，需要在服务和用户间有一个对接服务
用户po上验证信息后，反馈给其一个cookie，用于对接专用进程

对每个新链接用户创建进程（可以分布处理？）维护一个进程池（用户标志-进程标志dict）
每条进程用线程维护多个exchanger（???）和一个（或多个）publisher

用socket或web api都行吧 欸socket好像不行，要维护那么多连接的话 端口不够用啊（udp的话还要做ack机制）
请求处理的话，要用异步或多线程维护了 暂定用tornado的wsgi异步框架
**（已经实现了特性很舒服的web服务器，不需要其他框架了）**

---

###### 具有特定特性的web服务器（finished,waiting for new feature） Homer

要求有如下特性：

1. web api 方便注册
2. 适应基于http的 多订阅-推送机制
3. 动态添加api

**突然想到的新特性：应用层协议可选，自定义协议类[参数列表，注册函数中可暴露的参数列表，解析函数，封装函数......] 从解析过程到函数生成看来都要改一下呢 = = **

而且这个即时通讯服务，也不必要使用HTTP协议，完全可以自己设计协议嘛......

---

###### 业务逻辑核心代码

---

###### 最外层interface （用户直接接触的代码）

---

###### 有关客户端（功能实现）

1）切换频道
2）未读消息保存
3）...

---

###### 其他

字符画表情
固定光标位置

---

Q1：

exchange要把信息传进queue之前 要先声明这个queue或用bindingkey绑定 

一个离线用户想要接入某公共频道 并且想获知一段时间内的历史消息

只能在其创建时对公共频道开一个专用queue一直保持等待接受吗

对每个用户在后端只维护一个Q 或者一个roomQ 一个topicQ 

用户每次连接直接拿取所有信息，在信息头加上一串码，相当于一个伪协议（？）

根据编码在本地创建持久化队列（这个要用一个队列模块实现）