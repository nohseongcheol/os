#!/usr/bin/env python3
import argparse
from contextlib import ExitStack
import os
import re
from pathlib import Path
import shutil
import subprocess
import atexit
import tempfile

项目根 = Path(__file__).resolve().parents[1]
随机文件集 = []


def 清理随机():
    for 路径 in 随机文件集:
        try:
            os.unlink(路径)
        except FileNotFoundError:
            pass


atexit.register(清理随机)


def 远程随机参数列():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as 文件:
        文件.write(b'JKRENRG1' + os.urandom(32))
        随机文件集.append(文件.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(文件.name)]


def 测试替身计算机():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    宿主 = 项目根.parent / 'rpi4/build/host'
    加载器 = 宿主 / 'lib/ld-musl-x86_64.so.1'
    二进制 = 宿主 / 'usr/bin/qemu-system-aarch64'
    if 加载器.is_file() and 二进制.is_file():
        return [str(加载器), '--library-path', str(宿主 / 'usr/lib') + ':' + str(宿主 / 'lib'),
                str(二进制), '-L', str(宿主 / 'usr/share/qemu')]
    二进制 = shutil.which('qemu-system-aarch64')
    if not 二进制:
        raise SystemExit('raspi4b 支持值 QEMU 所需条件值. QEMU_AARCH64로 경로를 지정하세요.')
    return [二进制]


def 读取分辨率(文本):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', 文本):
        raise argparse.ArgumentTypeError('分辨率值 格式值: 1920x1080')
    宽度值, 高度值 = map(int, 文本.split('x'))
    if not (640 <= 宽度值 <= 1920 and 480 <= 高度值 <= 1080):
        raise argparse.ArgumentTypeError('支持值 裁剪: 宽度值 640~1920, 高度值 480~1080')
    return 宽度值, 高度值


def 命令(分辨率值=(640, 480)):
    背景值 = 测试替身计算机()
    支持功能列 = subprocess.check_output(背景值 + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 支持功能列:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 最新值 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    宽度值, 高度值 = 读取分辨率('{}x{}'.format(*分辨率值))
    return 背景值 + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(宽度值),
                   '-global', 'bcm2835-fb.yres=' + str(高度值), '-kernel',
                   str(项目根 / 'build/kernel8.img'), '-no-reboot'] + 远程随机参数列()


def 运行():
    参数解析器 = argparse.ArgumentParser(description='内置 Java Pi4 内核值. 串行值 셸은 Ctrl+A X, --desktop은 Ctrl+C로 退出程序.')
    参数解析器.add_argument('--display', default='none', help='none 또는 gtk/sdl (宿主 支持值 所需条件值)')
    参数解析器.add_argument('--resolution', type=读取分辨率, default=(640, 480), help='启动 屏幕 大小. 예: 1920x1080; 默认值 640x480')
    参数解析器.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 硬件端口 5902. 键值 입력은 UART 터미널에서 합니다.')
    参数解析器.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    参数解析器.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 硬件端口')
    参数解析器.add_argument('--network', action='store_true', help='辅助值 UART SLIP와 QEMU NAT를 连接; --desktop과 함께 使用值 가능; 게스트에서 ftpd start')
    参数解析器.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    参数解析器.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP 控制值 硬件端口 (데이터 50000..50007)')
    参数解析器.add_argument('--guest-ip', default=None, help='QEMU NAT 前向值 目标值. 기본은 ip.conf의 IP; 更改值 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    参数解析器.add_argument('--network-host', default='127.0.0.1', help='NAT 接收值 地址. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN 地址: 外部值 接通状态')
    参数解析器.add_argument('--forward', action='append', default=[], help='--network 追加条目 连接: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    参数解析器.add_argument('--pip', action='store_true', help='PyPI 源代码树 软件包 中继值 运行 (--network 所需条件值, MicroPython 호환 소스만)')
    参数解析器.add_argument('--pip-port', type=int, default=8027, help='软件包 중계의 localhost TCP 硬件端口')
    参数解析器.add_argument('--pip-cache', type=Path, default=项目根/'build/pip-cache')
    参数解析器.add_argument('--pip-offline', action='store_true', help='이미 받은 分发值 파일만 제공')
    参数数组 = 参数解析器.parse_args()
    if 参数数组.remote:
        参数数组.network=True
        参数数组.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; 密码值: python3 工具集/远程设置.py show'.format(参数数组.network_host,参数数组.network_host),flush=True)
    if 参数数组.pip and not 参数数组.network: 参数解析器.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= 参数数组.pip_port <= 65535: 参数解析器.error('--pip-port 범위는 1~65535입니다.')
    if 参数数组.forward and not 参数数组.network: 参数解析器.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as 资源值:
        if 参数数组.pip:
            from 捆绑中继 import 捆绑中继
            资源值.enter_context(捆绑中继(参数数组.pip_port, 参数数组.pip_cache, 参数数组.pip_offline))
            print('软件包 中继值: 127.0.0.1:' + str(参数数组.pip_port), flush=True)
        执行任务(参数数组)


def 执行任务(参数数组):
    if 参数数组.desktop:
        if 参数数组.vnc or 参数数组.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from 桌面视图 import 运行桌面
        raise SystemExit(运行桌面(参数数组.port, 使用网络=参数数组.network, 文件传送端口编号=参数数组.ftp_port, 转发中规则列=参数数组.forward, 分辨率值=参数数组.resolution, 客户机地址=参数数组.guest_ip, 宿主地址=参数数组.network_host))
    选择项集 = ['-display', 参数数组.display, '-serial', 'mon:stdio']
    if 参数数组.vnc:
        选择项集 += ['-vnc', 参数数组.vnc]
    if 参数数组.network:
        from 网络桥接 import 网络桥接
        with 网络桥接(参数数组.ftp_port, 参数数组.forward, 客户机地址=参数数组.guest_ip, 宿主地址=参数数组.network_host) as 桥接:
            状态值 = subprocess.call(命令(参数数组.resolution) + 选择项集 + 桥接.已转发参数())
            if 桥接.错误: raise SystemExit('network bridge: ' + 桥接.错误)
        raise SystemExit(状态值)
    raise SystemExit(subprocess.call(命令(参数数组.resolution) + 选择项集))


if __name__ == '__main__':
    运行()
