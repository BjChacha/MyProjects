# 自动登录校园网（Drcom）脚本

本项目包含两个子项目：

1. Python编写的自动登录校园网脚本，支持宿舍区/教工区，仅支持Windows。
2. Bash编写的自动登录校园网脚本，用于openwrt路由器运行，仅支持宿舍区。

## Usage

### Python版本

1. 在`account.ini`中相应位置填入校园网账号和密码；
2. 用Python运行`main.py`脚本，或双击`start.bat`运行。

### Bash版本

1. 把`drcom.sh`和`start.sh`两个文件上传到路由器中；
2. 将`start.sh`设置成开机自启（如openwer可通过编辑`/etc/rc.local`实现）。
3. 重启路由器，或者直接后台运行脚本`start.sh`。