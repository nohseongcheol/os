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

Project_root = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for path in _난수파일들:
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as file:
        file.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(file.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(file.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    host = Project_root.parent / 'rpi4/build/host'
    적재기 = host / 'lib/ld-musl-x86_64.so.1'
    binary = host / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and binary.is_file():
        return [str(적재기), '--library-path', str(host / 'usr/lib') + ':' + str(host / 'lib'),
                str(binary), '-L', str(host / 'usr/share/qemu')]
    binary = shutil.which('qemu-system-aarch64')
    if not binary:
        raise SystemExit('raspi4b Suporta_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binary]


def 해상도읽기(SMS):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', SMS):
        raise argparse.ArgumentTypeError('resolution_VALUE format_VALUE: 1920x1080')
    너비, 높이 = map(int, SMS.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Suporta_VALUE clip: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def utos(resolution_VALUE=(640, 480)):
    wallpaper_VALUE = 모의기계()
    지원목록 = subprocess.check_output(wallpaper_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*resolution_VALUE))
    return wallpaper_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(Project_root / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def run():
    parser = argparse.ArgumentParser(description='자체 Java Pi4 kernel_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Paglabas_app.')
    parser.add_argument('--display', default='none', help='none 또는 gtk/sdl (host Suporta_VALUE 필요)')
    parser.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 sukat_82232621. 예: 1920x1080; value_ng_default 640x480')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. key_VALUE 입력은 UART 터미널에서 합니다.')
    parser.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    parser.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    parser.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 CONNECT; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    parser.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    parser.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP control_VALUE 포트 (데이터 50000..50007)')
    parser.add_argument('--guest-ip', default=None, help='QEMU NAT ipasa_VALUE_24592b8a layunin. 기본은 ip.conf의 IP; baguhin_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    parser.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 email. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN email: 외부 koneksyon_e05f319b')
    parser.add_argument('--forward', action='append', default=[], help='--network 추가 CONNECT: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    parser.add_argument('--pip', action='store_true', help='PyPI pinagmulan_balangkas bundle 중계 run (--network 필요, MicroPython 호환 소스만)')
    parser.add_argument('--pip-port', type=int, default=8027, help='bundle 중계의 localhost TCP 포트')
    parser.add_argument('--pip-cache', type=Path, default=Project_root/'build/pip-cache')
    parser.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    argumento_ARRAY = parser.parse_args()
    if argumento_ARRAY.remote:
        argumento_ARRAY.network=True
        argumento_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; password_VALUE: python3 Mga_Tool/malayuan_Mga_Setting.py show'.format(argumento_ARRAY.network_host,argumento_ARRAY.network_host),flush=True)
    if argumento_ARRAY.pip and not argumento_ARRAY.network: parser.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argumento_ARRAY.pip_port <= 65535: parser.error('--pip-port 범위는 1~65535입니다.')
    if argumento_ARRAY.forward and not argumento_ARRAY.network: parser.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as resource_VALUE:
        if argumento_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            resource_VALUE.enter_context(꾸러미중계(argumento_ARRAY.pip_port, argumento_ARRAY.pip_cache, argumento_ARRAY.pip_offline))
            print('bundle 중계: 127.0.0.1:' + str(argumento_ARRAY.pip_port), flush=True)
        Mag_execute_gawain(argumento_ARRAY)


def Mag_execute_gawain(argumento_ARRAY):
    if argumento_ARRAY.desktop:
        if argumento_ARRAY.vnc or argumento_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from desktop_View import run_desktop
        raise SystemExit(run_desktop(argumento_ARRAY.port, Network=argumento_ARRAY.network, file_lipat_numero_ng_port=argumento_ARRAY.ftp_port, 전달규칙들=argumento_ARRAY.forward, resolution_VALUE=argumento_ARRAY.resolution, bisita_email=argumento_ARRAY.guest_ip, host_email=argumento_ARRAY.network_host))
    Mga_Opsyon = ['-display', argumento_ARRAY.display, '-serial', 'mon:stdio']
    if argumento_ARRAY.vnc:
        Mga_Opsyon += ['-vnc', argumento_ARRAY.vnc]
    if argumento_ARRAY.network:
        from Network_bridge import Network_bridge
        with Network_bridge(argumento_ARRAY.ftp_port, argumento_ARRAY.forward, bisita_email=argumento_ARRAY.guest_ip, host_email=argumento_ARRAY.network_host) as bridge:
            katayuan_VALUE = subprocess.call(utos(argumento_ARRAY.resolution) + Mga_Opsyon + bridge.전달인수())
            if bridge.error: raise SystemExit('network bridge: ' + bridge.error)
        raise SystemExit(katayuan_VALUE)
    raise SystemExit(subprocess.call(utos(argumento_ARRAY.resolution) + Mga_Opsyon))


if __name__ == '__main__':
    run()
