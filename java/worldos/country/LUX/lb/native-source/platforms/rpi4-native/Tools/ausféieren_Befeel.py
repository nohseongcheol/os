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

projezéieren_Racinn = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for Wee in _난수파일들:
        try:
            os.unlink(Wee)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Fichier:
        Fichier.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Fichier.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Fichier.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    Host = projezéieren_Racinn.parent / 'rpi4/build/host'
    적재기 = Host / 'lib/ld-musl-x86_64.so.1'
    Binär = Host / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and Binär.is_file():
        return [str(적재기), '--library-path', str(Host / 'usr/lib') + ':' + str(Host / 'lib'),
                str(Binär), '-L', str(Host / 'usr/share/qemu')]
    Binär = shutil.which('qemu-system-aarch64')
    if not Binär:
        raise SystemExit('raspi4b Support_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [Binär]


def 해상도읽기(SMS):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', SMS):
        raise argparse.ArgumentTypeError('Opléisung_VALUE Format_VALUE: 1920x1080')
    너비, 높이 = map(int, SMS.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Support_VALUE Clip: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Befeel(Opléisung_VALUE=(640, 480)):
    Hannergrond_VALUE = 모의기계()
    지원목록 = subprocess.check_output(Hannergrond_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*Opléisung_VALUE))
    return Hannergrond_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(projezéieren_Racinn / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Laf():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 Kernel_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Schluss_App.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (Host Support_VALUE 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 d_Gréisst_veränneren. 예: 1920x1080; Standardwäert 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Tast_VALUE 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Verbannen; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP Kontroll_VALUE 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT Virun_VALUE Zil. 기본은 ip.conf의 IP; änneren_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 Adress. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN Adress: 외부 Verbindung_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 Verbannen: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI Quell_Bamstruktur Bëndel 중계 Laf (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='Bëndel 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=projezéieren_Racinn/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    Argument_ARRAY = 인수해석기.parse_args()
    if Argument_ARRAY.remote:
        Argument_ARRAY.network=True
        Argument_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; Passwuert_VALUE: python3 Tools/extern_Astellungen.py show'.format(Argument_ARRAY.network_host,Argument_ARRAY.network_host),flush=True)
    if Argument_ARRAY.pip and not Argument_ARRAY.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= Argument_ARRAY.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if Argument_ARRAY.forward and not Argument_ARRAY.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as Ressource_VALUE:
        if Argument_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            Ressource_VALUE.enter_context(꾸러미중계(Argument_ARRAY.pip_port, Argument_ARRAY.pip_cache, Argument_ARRAY.pip_offline))
            print('Bëndel 중계: 127.0.0.1:' + str(Argument_ARRAY.pip_port), flush=True)
        Ausféieren(Argument_ARRAY)


def Ausféieren(Argument_ARRAY):
    if Argument_ARRAY.desktop:
        if Argument_ARRAY.vnc or Argument_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from Desktop_Vue import Laf_Desktop
        raise SystemExit(Laf_Desktop(Argument_ARRAY.port, Reseau=Argument_ARRAY.network, 파일전송접속번호=Argument_ARRAY.ftp_port, 전달규칙들=Argument_ARRAY.forward, Opléisung_VALUE=Argument_ARRAY.resolution, Gaascht_Adress=Argument_ARRAY.guest_ip, Host_Adress=Argument_ARRAY.network_host))
    Optiounen = ['-display', Argument_ARRAY.display, '-serial', 'mon:stdio']
    if Argument_ARRAY.vnc:
        Optiounen += ['-vnc', Argument_ARRAY.vnc]
    if Argument_ARRAY.network:
        from Reseau_Bréck import Reseau_Bréck
        with Reseau_Bréck(Argument_ARRAY.ftp_port, Argument_ARRAY.forward, Gaascht_Adress=Argument_ARRAY.guest_ip, Host_Adress=Argument_ARRAY.network_host) as Bréck:
            Status_VALUE = subprocess.call(Befeel(Argument_ARRAY.resolution) + Optiounen + Bréck.전달인수())
            if Bréck.Feeler: raise SystemExit('network bridge: ' + Bréck.Feeler)
        raise SystemExit(Status_VALUE)
    raise SystemExit(subprocess.call(Befeel(Argument_ARRAY.resolution) + Optiounen))


if __name__ == '__main__':
    Laf()
