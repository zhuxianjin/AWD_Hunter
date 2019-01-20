### AWD_Hunter, 一个基于Python2.7的AWD自动化工具

免得比赛时手忙脚乱，时间有限，后续或加入自动submit flag什么的

安装依赖库

`sudo python -m pip install -r requirements.txt`

运行

`Usage：python run.py`

过程中间对整体代码进行了重构和优化，理清程序逻辑，提高代码的可读性

```
.
├── app			//程序主体
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── app_common_class.py
│   ├── app_common_class.pyc
│   ├── app_core.py
│   ├── app_core.pyc
│   ├── app_func.py
│   └── app_func.pyc
├── extension		//拓展模块
│   └── ssh-auto-chpass.py
├── run.py		//运行
├── runtime
│   └── log.json	//log文件
└── script		//存放脚本
    ├── php
    │   ├── log-record.php
    │   └── null_shell.php
    └── py
        └── addlog.py

```

主要使用paramiko和重写cmd基本类方法实现ssh连接和程序交互式命令行处理

使用json格式储存数据更灵活方便

![https://i.loli.net/2019/01/19/5c431123ca36b.png](https://i.loli.net/2019/01/19/5c431123ca36b.png)

ps查看查看记录的主机和webshell

![https://i.loli.net/2019/01/20/5c442f2fe8f23.png](https://i.loli.net/2019/01/20/5c442f2fe8f23.png)

使用ps中的序号就可以直接连接主机或者webshell

![https://i.loli.net/2019/01/20/5c442f7ee7bf5.png](https://i.loli.net/2019/01/20/5c442f7ee7bf5.png)