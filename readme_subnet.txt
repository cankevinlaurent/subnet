##############################################################################
- @Code:    205 Project / A
- @Purpose: 登记并提供上海IT运营中心IT系统所涉及的全部网段。
- @Author:  Kévin
- @Update:  17 Oct. 2018
##############################################################################

##################
I. 项目文件
##################
- /subnet                   项目文件夹。
- subnet.db                 数据库，记录网段信息。
- CommonConfigProcessor.py  公共类，读取配置文件config.txt。
- CommonDBProcessor.py      公共类，数据库操作。
- subnet.py                 使能程序，提供API接口，登记和查询网段信息。
- config_subnet.txt         配置文件，包括端口、认证等。
- start_subnet.sh           启动脚本。
- readme_subnet.txt         本说明文档。

##################
II. 项目部署条件
##################
- 推荐CentOS 6.9或更高
- 推荐python 2.7.14或更高
- 不需要root账号
- #visudo，增加一句：wangwei ALL=(jtitsm)   ALL
- 正确设置文件和文件夹权限，如db文件及其全路径文件夹必须可写
- requests库：wangwei$pip install --user requests
- flask库：wangwei$pip install --user flask
- flask-httpauth库：wangwei$pip install --user flask-httpauth
- pyOpenSSL库：wangwei$pip install --user pyOpenSSL
- ipaddr库：wangwei$pip install --user ipaddr

##################
III. 项目运行
##################
- 应用账号：jtitsm，部署/运维账号：wangwei
- 启动脚本赋可执行权限：wangwei$chmod +x start_subnet.sh
- wangwei$sudo -u jtitsm ./start_subnet.sh

##################
IV. 数据库元信息
##################
- 数据库：SQLite3
- 数据库编码：utf-8
CREATE TABLE "subnets" (
"subnet"  TEXT NOT NULL,
"netmask"  INTEGER NOT NULL,
"location"  TEXT NOT NULL,
PRIMARY KEY ("subnet")
);
CREATE TABLE "gateways" (
"subnet"  TEXT NOT NULL,
"gateway"  TEXT NOT NULL,
PRIMARY KEY ("subnet" ASC, "gateway" ASC),
CONSTRAINT "subnet_gateway" FOREIGN KEY ("subnet") REFERENCES "subnets" ("subnet") ON DELETE CASCADE ON UPDATE CASCADE
);

