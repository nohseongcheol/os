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

prosiect_gwraidd = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for LLWYBR in _난수파일들:
        try:
            os.unlink(LLWYBR)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Ffeil:
        Ffeil.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Ffeil.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Ffeil.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    lletya = prosiect_gwraidd.parent / 'rpi4/build/host'
    적재기 = lletya / 'lib/ld-musl-x86_64.so.1'
    deuaidd = lletya / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and deuaidd.is_file():
        return [str(적재기), '--library-path', str(lletya / 'usr/lib') + ':' + str(lletya / 'lib'),
                str(deuaidd), '-L', str(lletya / 'usr/share/qemu')]
    deuaidd = shutil.which('qemu-system-aarch64')
    if not deuaidd:
        raise SystemExit('raspi4b Cymorth_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [deuaidd]


def 해상도읽기(Testun):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Testun):
        raise argparse.ArgumentTypeError('cydraniad_VALUE fformat_VALUE: 1920x1080')
    너비, 높이 = map(int, Testun.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Cymorth_VALUE clip: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Gorchymyn(cydraniad_VALUE=(640, 480)):
    Cefndir_VALUE = 모의기계()
    지원목록 = subprocess.check_output(Cefndir_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*cydraniad_VALUE))
    return Cefndir_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(prosiect_gwraidd / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Gweithredu_2():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 cnewyllyn_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 gadael_Rhaglen.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (lletya Cymorth_VALUE 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Maint. 예: 1920x1080; gwerth_diofyn 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. bysell_VALUE 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Cysylltu; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP rheoli_VALUE 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT Ymlaen_VALUE targed. 기본은 ip.conf의 IP; newid_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ADDRESS. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ADDRESS: 외부 cyswllt_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 Cysylltu: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI ffynhonnell_coeden bwndel 중계 Gweithredu_2 (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='bwndel 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=prosiect_gwraidd/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    arg_ARAE = 인수해석기.parse_args()
    if arg_ARAE.remote:
        arg_ARAE.network=True
        arg_ARAE.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; cyfrinair_VALUE: python3 Offer/pell_Gosodiadau.py show'.format(arg_ARAE.network_host,arg_ARAE.network_host),flush=True)
    if arg_ARAE.pip and not arg_ARAE.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= arg_ARAE.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if arg_ARAE.forward and not arg_ARAE.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as adnodd_VALUE:
        if arg_ARAE.pip:
            from 꾸러미중계 import 꾸러미중계
            adnodd_VALUE.enter_context(꾸러미중계(arg_ARAE.pip_port, arg_ARAE.pip_cache, arg_ARAE.pip_offline))
            print('bwndel 중계: 127.0.0.1:' + str(arg_ARAE.pip_port), flush=True)
        Gweithredu(arg_ARAE)


def Gweithredu(arg_ARAE):
    if arg_ARAE.desktop:
        if arg_ARAE.vnc or arg_ARAE.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from bwrdd_gwaith_Gwedd import rhedeg_bwrdd_gwaith
        raise SystemExit(rhedeg_bwrdd_gwaith(arg_ARAE.port, Rhwydwaith=arg_ARAE.network, ffeil_trosglwyddo_rhif_porth=arg_ARAE.ftp_port, 전달규칙들=arg_ARAE.forward, cydraniad_VALUE=arg_ARAE.resolution, gwestai_ADDRESS=arg_ARAE.guest_ip, lletya_ADDRESS=arg_ARAE.network_host))
    Dewisiadau = ['-display', arg_ARAE.display, '-serial', 'mon:stdio']
    if arg_ARAE.vnc:
        Dewisiadau += ['-vnc', arg_ARAE.vnc]
    if arg_ARAE.network:
        from Rhwydwaith_pont import Rhwydwaith_pont
        with Rhwydwaith_pont(arg_ARAE.ftp_port, arg_ARAE.forward, gwestai_ADDRESS=arg_ARAE.guest_ip, lletya_ADDRESS=arg_ARAE.network_host) as pont:
            cyflwr_VALUE = subprocess.call(Gorchymyn(arg_ARAE.resolution) + Dewisiadau + pont.전달인수())
            if pont.Gwall: raise SystemExit('network bridge: ' + pont.Gwall)
        raise SystemExit(cyflwr_VALUE)
    raise SystemExit(subprocess.call(Gorchymyn(arg_ARAE.resolution) + Dewisiadau))


if __name__ == '__main__':
    Gweithredu_2()
