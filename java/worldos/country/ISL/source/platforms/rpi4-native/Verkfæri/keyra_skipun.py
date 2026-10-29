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

verk_rót = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for SLÓÐ in _난수파일들:
        try:
            os.unlink(SLÓÐ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Skrá:
        Skrá.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Skrá.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Skrá.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    hýsa = verk_rót.parent / 'rpi4/build/host'
    적재기 = hýsa / 'lib/ld-musl-x86_64.so.1'
    tvíundar = hýsa / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and tvíundar.is_file():
        return [str(적재기), '--library-path', str(hýsa / 'usr/lib') + ':' + str(hýsa / 'lib'),
                str(tvíundar), '-L', str(hýsa / 'usr/share/qemu')]
    tvíundar = shutil.which('qemu-system-aarch64')
    if not tvíundar:
        raise SystemExit('raspi4b Aðstoð_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [tvíundar]


def 해상도읽기(Texti):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Texti):
        raise argparse.ArgumentTypeError('upplausn_VALUE snið_VALUE: 1920x1080')
    너비, 높이 = map(int, Texti.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Aðstoð_VALUE miðlaskrá: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Skipun(upplausn_VALUE=(640, 480)):
    veggfóður_VALUE = 모의기계()
    지원목록 = subprocess.check_output(veggfóður_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*upplausn_VALUE))
    return veggfóður_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(verk_rót / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Keyra_2():
    þáttari = argparse.ArgumentParser(description='eigin Java Pi4 kjarni_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 loka_forrit.')
    þáttari.add_argument('--display', default='none', help='none 또는 gtk/sdl (hýsa Aðstoð_VALUE 필요)')
    þáttari.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Stærð. 예: 1920x1080; sjálfgildi 640x480')
    þáttari.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Lykill_VALUE 입력은 UART 터미널에서 합니다.')
    þáttari.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    þáttari.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    þáttari.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Tengjast; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    þáttari.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    þáttari.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP stýring_VALUE 포트 (데이터 50000..50007)')
    þáttari.add_argument('--guest-ip', default=None, help='QEMU NAT Áfram_VALUE markmið. 기본은 ip.conf의 IP; breyta_VALUE_16f64fe4 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    þáttari.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 slóð. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN slóð: 외부 tenging_e05f319b')
    þáttari.add_argument('--forward', action='append', default=[], help='--network 추가 Tengjast: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    þáttari.add_argument('--pip', action='store_true', help='PyPI uppruni_tré búnt 중계 Keyra_2 (--network 필요, MicroPython 호환 소스만)')
    þáttari.add_argument('--pip-port', type=int, default=8027, help='búnt 중계의 localhost TCP 포트')
    þáttari.add_argument('--pip-cache', type=Path, default=verk_rót/'build/pip-cache')
    þáttari.add_argument('--pip-offline', action='store_true', help='이미 받은 dreifing_VALUE 파일만 제공')
    frumbreyta_ARRAY = þáttari.parse_args()
    if frumbreyta_ARRAY.remote:
        frumbreyta_ARRAY.network=True
        frumbreyta_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; aðgangsorð_VALUE: python3 Verkfæri/fjartengdur_Stillingar.py show'.format(frumbreyta_ARRAY.network_host,frumbreyta_ARRAY.network_host),flush=True)
    if frumbreyta_ARRAY.pip and not frumbreyta_ARRAY.network: þáttari.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= frumbreyta_ARRAY.pip_port <= 65535: þáttari.error('--pip-port 범위는 1~65535입니다.')
    if frumbreyta_ARRAY.forward and not frumbreyta_ARRAY.network: þáttari.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as tilfang_VALUE:
        if frumbreyta_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            tilfang_VALUE.enter_context(꾸러미중계(frumbreyta_ARRAY.pip_port, frumbreyta_ARRAY.pip_cache, frumbreyta_ARRAY.pip_offline))
            print('búnt 중계: 127.0.0.1:' + str(frumbreyta_ARRAY.pip_port), flush=True)
        Keyra(frumbreyta_ARRAY)


def Keyra(frumbreyta_ARRAY):
    if frumbreyta_ARRAY.desktop:
        if frumbreyta_ARRAY.vnc or frumbreyta_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from skjáborð_Sýn import runa_skjáborð
        raise SystemExit(runa_skjáborð(frumbreyta_ARRAY.port, Net=frumbreyta_ARRAY.network, skrá_flytja_tengisnúmer=frumbreyta_ARRAY.ftp_port, 전달규칙들=frumbreyta_ARRAY.forward, upplausn_VALUE=frumbreyta_ARRAY.resolution, gestur_slóð=frumbreyta_ARRAY.guest_ip, hýsa_slóð=frumbreyta_ARRAY.network_host))
    valkostir = ['-display', frumbreyta_ARRAY.display, '-serial', 'mon:stdio']
    if frumbreyta_ARRAY.vnc:
        valkostir += ['-vnc', frumbreyta_ARRAY.vnc]
    if frumbreyta_ARRAY.network:
        from Net_brú import Net_brú
        with Net_brú(frumbreyta_ARRAY.ftp_port, frumbreyta_ARRAY.forward, gestur_slóð=frumbreyta_ARRAY.guest_ip, hýsa_slóð=frumbreyta_ARRAY.network_host) as brú:
            staða_VALUE_e10195a1 = subprocess.call(Skipun(frumbreyta_ARRAY.resolution) + valkostir + brú.전달인수())
            if brú.Villa: raise SystemExit('network bridge: ' + brú.Villa)
        raise SystemExit(staða_VALUE_e10195a1)
    raise SystemExit(subprocess.call(Skipun(frumbreyta_ARRAY.resolution) + valkostir))


if __name__ == '__main__':
    Keyra_2()
