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

judge() {
    if [[ 0 -eq $? ]]; then
        echo -e "${OK} ${GreenBG} $1 完成 ${Font}"
        sleep 1
    else
        echo -e "${Error} ${RedBG} $1 失败${Font}"
        exit 1
    fi
}
chrony_install() {
    yum -y install chrony
    judge "安装 chrony 时间同步服务 "

    timedatectl set-ntp true

    systemctl enable chronyd && systemctl restart chronyd

    judge "chronyd 启动 "

    timedatectl set-timezone Asia/Shanghai

    echo -e "${OK} ${GreenBG} 等待时间同步 ${Font}"
    sleep 10

    chronyc sourcestats -v
    chronyc tracking -v
    date
    read -rp "请确认时间是否准确,误差范围±3分钟(Y/N): " chrony_install
    [[ -z ${chrony_install} ]] && chrony_install="Y"
    case $chrony_install in
    [yY][eE][sS] | [yY])
        echo -e "${GreenBG} 继续安装 ${Font}"
        sleep 2
        ;;
    *)
        echo -e "${RedBG} 安装终止 ${Font}"
        exit 2
        ;;
    esac
}

dependency_install() {
    yum install wget git lsof -y

    yum -y install crontabs
    judge "安装 crontab"

    touch /var/spool/cron/root && chmod 600 /var/spool/cron/root
    systemctl start crond && systemctl enable crond


    judge "crontab 自启动配置 "

    yum -y install bc
    judge "安装 bc"

    yum -y install unzip
    judge "安装 unzip"

    yum -y install qrencode
    judge "安装 qrencode"

    yum -y install curl
    judge "安装 curl"

    yum -y groupinstall "Development tools"
    judge "编译工具包 安装"

    yum -y install pcre pcre-devel zlib-devel epel-release

    #    yum -y install rng-tools
    #    judge "rng-tools 安装"

    yum -y install haveged
    #    judge "haveged 安装"

    #    sed -i -r '/^HRNGDEVICE/d;/#HRNGDEVICE=\/dev\/null/a HRNGDEVICE=/dev/urandom' /etc/default/rng-tools

    systemctl start haveged && systemctl enable haveged
}

init_install() {
    # 常见软件安装(npm单独编译安装)
    yum update
    yum install lrzsz ntpdate sysstat net-tools gcc gcc-g++ make cmake wget vim git -y
    # 常用依赖安装
    yum install -y gmp-devel mpfr-devel libmpc-devel glibc autoconf openssl openssl-devel pcre-devel pam-devel
    yum -y groupinstall "Development tools"
    yum install -y pam* zlib*
    mkdir -p /opt/bak
    mkdir -p /opt/software
}

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

    yum install dbus

    # systemctl stop firewalld
    # systemctl disable firewalld
    # echo -e "${OK} ${GreenBG} firewalld 已关闭 ${Font}"

    # systemctl stop ufw
    # systemctl disable ufw
    # echo -e "${OK} ${GreenBG} ufw 已关闭 ${Font}"
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

# 升级gcc、npm、sqlite、openssl等编译依赖
update_upgrade_compile() {
  is_root
  update_gcc
  update_npm
  update_sqlite
  update_openssl
}

Basic_optimization() {
  is_root

}

Basic_init() {
  is_root
  # 初始化文件安装
  init_install
  # 时钟同步
  chrony_install
  # 安装crontab
  dependency_install
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
    echo -e "${Green}8.${Font}  升级安装gcc、sqlite、npm、openssl版本"
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