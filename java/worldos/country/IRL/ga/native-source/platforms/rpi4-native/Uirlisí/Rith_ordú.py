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

teilgean_fréamh = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for CONAIR in _난수파일들:
        try:
            os.unlink(CONAIR)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Comhad:
        Comhad.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Comhad.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Comhad.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    óstach = teilgean_fréamh.parent / 'rpi4/build/host'
    적재기 = óstach / 'lib/ld-musl-x86_64.so.1'
    dénártha = óstach / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and dénártha.is_file():
        return [str(적재기), '--library-path', str(óstach / 'usr/lib') + ':' + str(óstach / 'lib'),
                str(dénártha), '-L', str(óstach / 'usr/share/qemu')]
    dénártha = shutil.which('qemu-system-aarch64')
    if not dénártha:
        raise SystemExit('raspi4b Tacaíocht_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [dénártha]


def 해상도읽기(Téacs):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Téacs):
        raise argparse.ArgumentTypeError('taifeach_VALUE formáid_VALUE: 1920x1080')
    너비, 높이 = map(int, Téacs.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Tacaíocht_VALUE gearrthóg: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Ordú(taifeach_VALUE=(640, 480)):
    Cúlra_VALUE = 모의기계()
    지원목록 = subprocess.check_output(Cúlra_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*taifeach_VALUE))
    return Cúlra_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(teilgean_fréamh / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Rith_2():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 eithne_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 scoir_clár.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (óstach Tacaíocht_VALUE 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Méid. 예: 1920x1080; luach_réamhshocraithe 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. eochair_VALUE 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Nasc; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP rialú_VALUE 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT Ar_aghaidh_VALUE sprioc. 기본은 ip.conf의 IP; athraigh_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ADDRESS. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ADDRESS: 외부 nasc_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 Nasc: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI foinse_crann beart 중계 Rith_2 (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='beart 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=teilgean_fréamh/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    argóint_ARRAY = 인수해석기.parse_args()
    if argóint_ARRAY.remote:
        argóint_ARRAY.network=True
        argóint_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; pasfhocal_VALUE: python3 Uirlisí/cianda_Socruithe.py show'.format(argóint_ARRAY.network_host,argóint_ARRAY.network_host),flush=True)
    if argóint_ARRAY.pip and not argóint_ARRAY.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argóint_ARRAY.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if argóint_ARRAY.forward and not argóint_ARRAY.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as acmhainn_VALUE:
        if argóint_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            acmhainn_VALUE.enter_context(꾸러미중계(argóint_ARRAY.pip_port, argóint_ARRAY.pip_cache, argóint_ARRAY.pip_offline))
            print('beart 중계: 127.0.0.1:' + str(argóint_ARRAY.pip_port), flush=True)
        Rith(argóint_ARRAY)


def Rith(argóint_ARRAY):
    if argóint_ARRAY.desktop:
        if argóint_ARRAY.vnc or argóint_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from deasc_Amharc import rith_deasc
        raise SystemExit(rith_deasc(argóint_ARRAY.port, Líonra=argóint_ARRAY.network, comhad_traschur_uimhir_phoirt=argóint_ARRAY.ftp_port, 전달규칙들=argóint_ARRAY.forward, taifeach_VALUE=argóint_ARRAY.resolution, aoi_ADDRESS=argóint_ARRAY.guest_ip, óstach_ADDRESS=argóint_ARRAY.network_host))
    Roghanna = ['-display', argóint_ARRAY.display, '-serial', 'mon:stdio']
    if argóint_ARRAY.vnc:
        Roghanna += ['-vnc', argóint_ARRAY.vnc]
    if argóint_ARRAY.network:
        from Líonra_traschóiritheoir import Líonra_traschóiritheoir
        with Líonra_traschóiritheoir(argóint_ARRAY.ftp_port, argóint_ARRAY.forward, aoi_ADDRESS=argóint_ARRAY.guest_ip, óstach_ADDRESS=argóint_ARRAY.network_host) as traschóiritheoir:
            staid_VALUE = subprocess.call(Ordú(argóint_ARRAY.resolution) + Roghanna + traschóiritheoir.전달인수())
            if traschóiritheoir.ERREÁID: raise SystemExit('network bridge: ' + traschóiritheoir.ERREÁID)
        raise SystemExit(staid_VALUE)
    raise SystemExit(subprocess.call(Ordú(argóint_ARRAY.resolution) + Roghanna))


if __name__ == '__main__':
    Rith_2()
