#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

cd "$(
    cd "$(dirname "$0")" || exit
    pwd
)" || exit

#fonts color
Green="\033[32m"
Red="\033[31m"
# Yellow="\033[33m"
GreenBG="\033[42;37m"
RedBG="\033[41;37m"
Font="\033[0m"

#notification information
# Info="${Green}[信息]${Font}"
OK="${Green}[OK]${Font}"
Error="${Red}[错误]${Font}"
#简易随机数
random_num=$((RANDOM%12+4))
#生成伪装路径
camouflage="/$(head -n 10 /dev/urandom | md5sum | head -c ${random_num})/"

shell_version="0.0.1"

check_system() {
    if [[ "${ID}" == "centos" && ${VERSION_ID} -ge 7 ]]; then
        echo -e "${OK} ${GreenBG} 当前系统为 Centos ${VERSION_ID} ${VERSION} ${Font}"
        INS="yum"
    elif [[ "${ID}" == "debian" && ${VERSION_ID} -ge 8 ]]; then
        echo -e "${OK} ${GreenBG} 当前系统为 Debian ${VERSION_ID} ${VERSION} ${Font}"
        INS="apt"
        $INS update
        ## 添加 Nginx apt源
    elif [[ "${ID}" == "ubuntu" && $(echo "${VERSION_ID}" | cut -d '.' -f1) -ge 16 ]]; then
        echo -e "${OK} ${GreenBG} 当前系统为 Ubuntu ${VERSION_ID} ${UBUNTU_CODENAME} ${Font}"
        INS="apt"
        $INS update
    else
        echo -e "${Error} ${RedBG} 当前系统为 ${ID} ${VERSION_ID} 不在支持的系统列表内，安装中断 ${Font}"
        exit 1
    fi

    $INS install dbus

    systemctl stop firewalld
    systemctl disable firewalld
    echo -e "${OK} ${GreenBG} firewalld 已关闭 ${Font}"

    systemctl stop ufw
    systemctl disable ufw
    echo -e "${OK} ${GreenBG} ufw 已关闭 ${Font}"
}

is_root() {
    if [ 0 == $UID ]; then
        echo -e "${OK} ${GreenBG} 当前用户是root用户，进入安装流程 ${Font}"
        sleep 3
    else
        echo -e "${Error} ${RedBG} 当前用户不是root用户，请切换到root用户后重新执行脚本 ${Font}"
        exit 1
    fi
}

# 升级gcc、npm、sqlite等编译依赖
update_upgrade_compile() {
  is_root
  check_system
}

menu() {
    echo -e "\t Centos7 优化初始管理脚本 ${Red}[${shell_version}]${Font}"
    echo -e "\t---authored by Geeker---"
    echo -e "\t提供常用软件、依赖安装与优化，提供bbr加速等\n"

    echo -e "—————————————— 安装向导 ——————————————"""
    echo -e "${Green}1.${Font}  基本初始化"
    echo -e "${Green}2.${Font}  基本优化"
    echo -e "${Green}3.${Font}  BBR PLUS(by nan qiu ge)加速"
    echo -e "—————————————— 系统管理 ——————————————"
    echo -e "${Green}4.${Font}  查看 实时 Nginx 访问日志"
    echo -e "${Green}5.${Font}  查看 实时 系统 日志"
    echo -e "${Green}6.${Font}  查看端口占用进程"
    echo -e "${Green}7.${Font}  开放防火墙规则"
    echo -e "${Green}8.${Font}  升级安装gcc、sqlite、npm版本"
    echo -e "—————————————— 网盘服务 ——————————————"
    echo -e "${Green}70.${Font}  安装网盘服务"
    echo -e "—————————————— 其他选项 ——————————————"
    echo -e "${Green}0.${Font} 退出 \n"

    read -rp "请输入数字：" menu_num
    case $menu_num in
    0)
        exit 0
        ;;
    1)
        Basic_init
        ;;
    2)
        Basic_optimization
        ;;
    3)
        bash <(curl -L -s https://raw.githubusercontent.com/tcp-nanqinlang/general/master/General/CentOS/bash/tcp_nanqinlang-1.3.2.sh)
        ;;
    4)
        read -rp "请输入UUID:" UUID
        modify_UUID
        start_process_systemd
        ;;
    5)
        read -rp "请输入alterID:" alterID
        modify_alterid
        start_process_systemd
        ;;
    6)
        read -rp "请输入查询端口:" port
        if grep -q "ws" $v2ray_qr_config_file; then
            modify_nginx_port
        elif grep -q "h2" $v2ray_qr_config_file; then
            modify_inbound_port
        fi
        start_process_systemd
        ;;
    7)
        read -rp "请输入需要开启的端口:" port
        ;;
    8)
        update_upgrade_compile
        ;;
    9)
        show_error_log
        ;;
    10)
        basic_information
        if [[ $shell_mode == "ws" ]]; then
            vmess_link_image_choice
        else
            vmess_qr_link_image
        fi
        show_information
        ;;
    *)
        echo -e "${RedBG}请输入正确的数字${Font}"
        ;;
    esac
}

#list "$1"
menu

Centos 7默认gcc版本为4.8，有时需要更高版本的，这里以升级至8.3.1版本为例，分别执行下面三条命令即可，无需手动下载源码编译

1、安装centos-release-scl

sudo yum install centos-release-scl
2、安装devtoolset，注意，如果想安装7.*版本的，就改成devtoolset-7-gcc*，以此类推

sudo yum install devtoolset-8-gcc*
3、激活对应的devtoolset，所以你可以一次安装多个版本的devtoolset，需要的时候用下面这条命令切换到对应的版本

scl enable devtoolset-8 bash
大功告成，查看一下gcc版本

gcc -v
显示为 gcc version 8.3.1 20190311 (Red Hat 8.3.1-3) (GCC)

补充：这条激活命令只对本次会话有效，重启会话后还是会变回原来的4.8.5版本，要想随意切换可按如下操作。

首先，安装的devtoolset是在 /opt/sh 目录下的，如图



 每个版本的目录下面都有个 enable 文件，如果需要启用某个版本，只需要执行

source ./enable
所以要想切换到某个版本，只需要执行

source /opt/rh/devtoolset-8/enable
可以将对应版本的切换命令写个shell文件放在配了环境变量的目录下，需要时随时切换，或者开机自启

4、直接替换旧的gcc

旧的gcc是运行的 /usr/bin/gcc，所以将该目录下的gcc/g++替换为刚安装的新版本gcc软连接，免得每次enable

复制代码
mv /usr/bin/gcc /usr/bin/gcc-4.8.5

ln -s /opt/rh/devtoolset-8/root/bin/gcc /usr/bin/gcc

mv /usr/bin/g++ /usr/bin/g++-4.8.5

ln -s /opt/rh/devtoolset-8/root/bin/g++ /usr/bin/g++

gcc --version

g++ --version
