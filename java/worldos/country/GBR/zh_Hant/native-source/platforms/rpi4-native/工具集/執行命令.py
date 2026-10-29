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

項目根 = Path(__file__).resolve().parents[1]
隨機檔案集 = []


def 清理隨機():
    for 路徑 in 隨機檔案集:
        try:
            os.unlink(路徑)
        except FileNotFoundError:
            pass


atexit.register(清理隨機)


def 遠程隨機參數列():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as 檔案:
        檔案.write(b'JKRENRG1' + os.urandom(32))
        隨機檔案集.append(檔案.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(檔案.name)]


def 測試替身計算機():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    宿主 = 項目根.parent / 'rpi4/build/host'
    加載器 = 宿主 / 'lib/ld-musl-x86_64.so.1'
    二進制 = 宿主 / 'usr/bin/qemu-system-aarch64'
    if 加載器.is_file() and 二進制.is_file():
        return [str(加載器), '--library-path', str(宿主 / 'usr/lib') + ':' + str(宿主 / 'lib'),
                str(二進制), '-L', str(宿主 / 'usr/share/qemu')]
    二進制 = shutil.which('qemu-system-aarch64')
    if not 二進制:
        raise SystemExit('raspi4b 支持值 QEMU 所需條件值. QEMU_AARCH64로 경로를 지정하세요.')
    return [二進制]


def 讀取分辨率(文本):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', 文本):
        raise argparse.ArgumentTypeError('分辨率值 格式值: 1920x1080')
    寬度值, 高度值 = map(int, 文本.split('x'))
    if not (640 <= 寬度值 <= 1920 and 480 <= 高度值 <= 1080):
        raise argparse.ArgumentTypeError('支持值 裁剪: 寬度值 640~1920, 高度值 480~1080')
    return 寬度值, 高度值


def 命令(分辨率值=(640, 480)):
    背景值 = 測試替身計算機()
    支持功能列 = subprocess.check_output(背景值 + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 支持功能列:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 最新值 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    寬度值, 高度值 = 讀取分辨率('{}x{}'.format(*分辨率值))
    return 背景值 + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(寬度值),
                   '-global', 'bcm2835-fb.yres=' + str(高度值), '-kernel',
                   str(項目根 / 'build/kernel8.img'), '-no-reboot'] + 遠程隨機參數列()


def 運行():
    參數解析器 = argparse.ArgumentParser(description='內建 Java Pi4 內核值. 串行值 셸은 Ctrl+A X, --desktop은 Ctrl+C로 退出程式.')
    參數解析器.add_argument('--display', default='none', help='none 또는 gtk/sdl (宿主 支持值 所需條件值)')
    參數解析器.add_argument('--resolution', type=讀取分辨率, default=(640, 480), help='啓動 屏幕 大小. 예: 1920x1080; 默認值 640x480')
    參數解析器.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 硬件埠 5902. 鍵值 입력은 UART 터미널에서 합니다.')
    參數解析器.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    參數解析器.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 硬件埠')
    參數解析器.add_argument('--network', action='store_true', help='輔助值 UART SLIP와 QEMU NAT를 連接; --desktop과 함께 使用值 가능; 게스트에서 ftpd start')
    參數解析器.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    參數解析器.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP 控制值 硬件埠 (데이터 50000..50007)')
    參數解析器.add_argument('--guest-ip', default=None, help='QEMU NAT 前向值 目標值. 기본은 ip.conf의 IP; 更改值 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    參數解析器.add_argument('--network-host', default='127.0.0.1', help='NAT 接收值 地址. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN 地址: 外部值 接通狀態')
    參數解析器.add_argument('--forward', action='append', default=[], help='--network 追加條目 連接: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    參數解析器.add_argument('--pip', action='store_true', help='PyPI 原始碼樹 軟件包 中繼值 運行 (--network 所需條件值, MicroPython 호환 소스만)')
    參數解析器.add_argument('--pip-port', type=int, default=8027, help='軟件包 중계의 localhost TCP 硬件埠')
    參數解析器.add_argument('--pip-cache', type=Path, default=項目根/'build/pip-cache')
    參數解析器.add_argument('--pip-offline', action='store_true', help='이미 받은 分發值 파일만 제공')
    實際參數陣列 = 參數解析器.parse_args()
    if 實際參數陣列.remote:
        實際參數陣列.network=True
        實際參數陣列.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; 密碼值: python3 工具集/遠程設置.py show'.format(實際參數陣列.network_host,實際參數陣列.network_host),flush=True)
    if 實際參數陣列.pip and not 實際參數陣列.network: 參數解析器.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= 實際參數陣列.pip_port <= 65535: 參數解析器.error('--pip-port 범위는 1~65535입니다.')
    if 實際參數陣列.forward and not 實際參數陣列.network: 參數解析器.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as 資源值:
        if 實際參數陣列.pip:
            from 捆綁中繼 import 捆綁中繼
            資源值.enter_context(捆綁中繼(實際參數陣列.pip_port, 實際參數陣列.pip_cache, 實際參數陣列.pip_offline))
            print('軟件包 中繼值: 127.0.0.1:' + str(實際參數陣列.pip_port), flush=True)
        執行任務(實際參數陣列)


def 執行任務(實際參數陣列):
    if 實際參數陣列.desktop:
        if 實際參數陣列.vnc or 實際參數陣列.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from 桌面視圖 import 運行桌面
        raise SystemExit(運行桌面(實際參數陣列.port, 使用網路=實際參數陣列.network, 檔案傳送埠編號=實際參數陣列.ftp_port, 轉發中規則列=實際參數陣列.forward, 分辨率值=實際參數陣列.resolution, 客戶機地址=實際參數陣列.guest_ip, 宿主地址=實際參數陣列.network_host))
    選擇項集 = ['-display', 實際參數陣列.display, '-serial', 'mon:stdio']
    if 實際參數陣列.vnc:
        選擇項集 += ['-vnc', 實際參數陣列.vnc]
    if 實際參數陣列.network:
        from 網路橋接 import 網路橋接
        with 網路橋接(實際參數陣列.ftp_port, 實際參數陣列.forward, 客戶機地址=實際參數陣列.guest_ip, 宿主地址=實際參數陣列.network_host) as 橋接:
            狀態值 = subprocess.call(命令(實際參數陣列.resolution) + 選擇項集 + 橋接.已轉發實際參數())
            if 橋接.錯誤: raise SystemExit('network bridge: ' + 橋接.錯誤)
        raise SystemExit(狀態值)
    raise SystemExit(subprocess.call(命令(實際參數陣列.resolution) + 選擇項集))


if __name__ == '__main__':
    運行()
