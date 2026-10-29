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

tilg_freumh = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for Slighe in _난수파일들:
        try:
            os.unlink(Slighe)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as faidhle:
        faidhle.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(faidhle.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(faidhle.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    òstair = tilg_freumh.parent / 'rpi4/build/host'
    적재기 = òstair / 'lib/ld-musl-x86_64.so.1'
    bìnearaidh = òstair / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and bìnearaidh.is_file():
        return [str(적재기), '--library-path', str(òstair / 'usr/lib') + ':' + str(òstair / 'lib'),
                str(bìnearaidh), '-L', str(òstair / 'usr/share/qemu')]
    bìnearaidh = shutil.which('qemu-system-aarch64')
    if not bìnearaidh:
        raise SystemExit('raspi4b taic_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [bìnearaidh]


def 해상도읽기(SMS):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', SMS):
        raise argparse.ArgumentTypeError('dùmhlachd_bhreacaidh_VALUE fòrmat_VALUE: 1920x1080')
    너비, 높이 = map(int, SMS.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('taic_VALUE cliop: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def àithne(dùmhlachd_bhreacaidh_VALUE=(640, 480)):
    cùlaibh_VALUE = 모의기계()
    지원목록 = subprocess.check_output(cùlaibh_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*dùmhlachd_bhreacaidh_VALUE))
    return cùlaibh_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(tilg_freumh / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def ruith():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 eitean_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 fàg_ap.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (òstair taic_VALUE 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 atharraich_am_meud. 예: 1920x1080; luach_bunaiteach 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Iuchair_VALUE 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 CONNECT; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP smachd_VALUE 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT sìn_air_adhart_VALUE_24592b8a targaid. 기본은 ip.conf의 IP; atharraich_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ADDRESS. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ADDRESS: 외부 ceangal_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 CONNECT: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI tùs_craobh trusgan 중계 ruith (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='trusgan 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=tilg_freumh/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    argamaid_ARRAY = 인수해석기.parse_args()
    if argamaid_ARRAY.remote:
        argamaid_ARRAY.network=True
        argamaid_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; facal_faire_VALUE: python3 innealan/cian_roghainnean.py show'.format(argamaid_ARRAY.network_host,argamaid_ARRAY.network_host),flush=True)
    if argamaid_ARRAY.pip and not argamaid_ARRAY.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argamaid_ARRAY.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if argamaid_ARRAY.forward and not argamaid_ARRAY.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as goireas_VALUE:
        if argamaid_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            goireas_VALUE.enter_context(꾸러미중계(argamaid_ARRAY.pip_port, argamaid_ARRAY.pip_cache, argamaid_ARRAY.pip_offline))
            print('trusgan 중계: 127.0.0.1:' + str(argamaid_ARRAY.pip_port), flush=True)
        Ruith(argamaid_ARRAY)


def Ruith(argamaid_ARRAY):
    if argamaid_ARRAY.desktop:
        if argamaid_ARRAY.vnc or argamaid_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from deasg_seall import ruith_deasg
        raise SystemExit(ruith_deasg(argamaid_ARRAY.port, lìonra=argamaid_ARRAY.network, 파일전송접속번호=argamaid_ARRAY.ftp_port, 전달규칙들=argamaid_ARRAY.forward, dùmhlachd_bhreacaidh_VALUE=argamaid_ARRAY.resolution, aoigh_ADDRESS=argamaid_ARRAY.guest_ip, òstair_ADDRESS=argamaid_ARRAY.network_host))
    Roghainnean = ['-display', argamaid_ARRAY.display, '-serial', 'mon:stdio']
    if argamaid_ARRAY.vnc:
        Roghainnean += ['-vnc', argamaid_ARRAY.vnc]
    if argamaid_ARRAY.network:
        from lìonra_drochaid import lìonra_drochaid
        with lìonra_drochaid(argamaid_ARRAY.ftp_port, argamaid_ARRAY.forward, aoigh_ADDRESS=argamaid_ARRAY.guest_ip, òstair_ADDRESS=argamaid_ARRAY.network_host) as drochaid:
            cor_VALUE = subprocess.call(àithne(argamaid_ARRAY.resolution) + Roghainnean + drochaid.전달인수())
            if drochaid.Mearachd: raise SystemExit('network bridge: ' + drochaid.Mearachd)
        raise SystemExit(cor_VALUE)
    raise SystemExit(subprocess.call(àithne(argamaid_ARRAY.resolution) + Roghainnean))


if __name__ == '__main__':
    ruith()
