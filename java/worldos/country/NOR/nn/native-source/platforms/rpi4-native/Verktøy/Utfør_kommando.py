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

spegle_rot = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for STIGE in _난수파일들:
        try:
            os.unlink(STIGE)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Fil:
        Fil.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Fil.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Fil.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    vert = spegle_rot.parent / 'rpi4/build/host'
    적재기 = vert / 'lib/ld-musl-x86_64.so.1'
    binær = vert / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and binær.is_file():
        return [str(적재기), '--library-path', str(vert / 'usr/lib') + ':' + str(vert / 'lib'),
                str(binær), '-L', str(vert / 'usr/share/qemu')]
    binær = shutil.which('qemu-system-aarch64')
    if not binær:
        raise SystemExit('raspi4b støtte_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binær]


def 해상도읽기(Tekst):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Tekst):
        raise argparse.ArgumentTypeError('oppløysing_VALUE format_VALUE: 1920x1080')
    너비, 높이 = map(int, Tekst.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('støtte_VALUE klipp: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Kommando(oppløysing_VALUE=(640, 480)):
    bakgrunn_VALUE = 모의기계()
    지원목록 = subprocess.check_output(bakgrunn_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*oppløysing_VALUE))
    return bakgrunn_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(spegle_rot / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Køyr_2():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 kjerne_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Utgang_app.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (vert støtte_VALUE 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Storleik. 예: 1920x1080; standardverdi 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. tast_VALUE 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Kopla_til; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP styring_VALUE 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT Fram_VALUE mål. 기본은 ip.conf의 IP; endre_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ADDRESS. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ADDRESS: ekstern_VALUE kontakt_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 Kopla_til: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI kjelde_tre bunt 중계 Køyr_2 (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='bunt 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=spegle_rot/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    argument_ARRAY = 인수해석기.parse_args()
    if argument_ARRAY.remote:
        argument_ARRAY.network=True
        argument_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; passord_VALUE: python3 Verktøy/fjern_Innstillingar.py show'.format(argument_ARRAY.network_host,argument_ARRAY.network_host),flush=True)
    if argument_ARRAY.pip and not argument_ARRAY.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argument_ARRAY.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if argument_ARRAY.forward and not argument_ARRAY.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ressurs_VALUE:
        if argument_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            ressurs_VALUE.enter_context(꾸러미중계(argument_ARRAY.pip_port, argument_ARRAY.pip_cache, argument_ARRAY.pip_offline))
            print('bunt 중계: 127.0.0.1:' + str(argument_ARRAY.pip_port), flush=True)
        Køyr(argument_ARRAY)


def Køyr(argument_ARRAY):
    if argument_ARRAY.desktop:
        if argument_ARRAY.vnc or argument_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from stasjonær_vise import køyre_stasjonær
        raise SystemExit(køyre_stasjonær(argument_ARRAY.port, Nettverk=argument_ARRAY.network, fil_Overfør_portnummer=argument_ARRAY.ftp_port, 전달규칙들=argument_ARRAY.forward, oppløysing_VALUE=argument_ARRAY.resolution, gjest_ADDRESS=argument_ARRAY.guest_ip, vert_ADDRESS=argument_ARRAY.network_host))
    Alternativ = ['-display', argument_ARRAY.display, '-serial', 'mon:stdio']
    if argument_ARRAY.vnc:
        Alternativ += ['-vnc', argument_ARRAY.vnc]
    if argument_ARRAY.network:
        from Nettverk_bru import Nettverk_bru
        with Nettverk_bru(argument_ARRAY.ftp_port, argument_ARRAY.forward, gjest_ADDRESS=argument_ARRAY.guest_ip, vert_ADDRESS=argument_ARRAY.network_host) as bru:
            status_VALUE = subprocess.call(Kommando(argument_ARRAY.resolution) + Alternativ + bru.전달인수())
            if bru.FEIL: raise SystemExit('network bridge: ' + bru.FEIL)
        raise SystemExit(status_VALUE)
    raise SystemExit(subprocess.call(Kommando(argument_ARRAY.resolution) + Alternativ))


if __name__ == '__main__':
    Køyr_2()
