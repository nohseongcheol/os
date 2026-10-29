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

Project_wortel = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for Pad in _난수파일들:
        try:
            os.unlink(Pad)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Lêer:
        Lêer.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Lêer.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Lêer.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    hou = Project_wortel.parent / 'rpi4/build/host'
    적재기 = hou / 'lib/ld-musl-x86_64.so.1'
    binêr = hou / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and binêr.is_file():
        return [str(적재기), '--library-path', str(hou / 'usr/lib') + ':' + str(hou / 'lib'),
                str(binêr), '-L', str(hou / 'usr/share/qemu')]
    binêr = shutil.which('qemu-system-aarch64')
    if not binêr:
        raise SystemExit('raspi4b Bystand_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binêr]


def 해상도읽기(Teks):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Teks):
        raise argparse.ArgumentTypeError('resolusie_VALUE formaat_VALUE: 1920x1080')
    너비, 높이 = map(int, Teks.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Bystand_VALUE snit: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Opdrag(resolusie_VALUE=(640, 480)):
    muur_VALUE = 모의기계()
    지원목록 = subprocess.check_output(muur_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*resolusie_VALUE))
    return muur_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(Project_wortel / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Loop():
    ontleder = argparse.ArgumentParser(description='자체 Java Pi4 kern_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Verlaat_program.')
    ontleder.add_argument('--display', default='none', help='none 또는 gtk/sdl (hou Bystand_VALUE 필요)')
    ontleder.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Grootte. 예: 1920x1080; verstekwaarde 640x480')
    ontleder.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC hardeware_ombou 5902. Sleutel_VALUE 입력은 UART 터미널에서 합니다.')
    ontleder.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    ontleder.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC hardeware_ombou')
    ontleder.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Koppel; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    ontleder.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    ontleder.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP kontrole_VALUE hardeware_ombou (데이터 50000..50007)')
    ontleder.add_argument('--guest-ip', default=None, help='QEMU NAT aanstuur_VALUE_24592b8a teiken. 기본은 ip.conf의 IP; verander_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    ontleder.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 adres. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN adres: 외부 verbinding_e05f319b')
    ontleder.add_argument('--forward', action='append', default=[], help='--network 추가 Koppel: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    ontleder.add_argument('--pip', action='store_true', help='PyPI bron_boom bondel 중계 Loop (--network 필요, MicroPython 호환 소스만)')
    ontleder.add_argument('--pip-port', type=int, default=8027, help='bondel 중계의 localhost TCP hardeware_ombou')
    ontleder.add_argument('--pip-cache', type=Path, default=Project_wortel/'build/pip-cache')
    ontleder.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    argument_ARRAY = ontleder.parse_args()
    if argument_ARRAY.remote:
        argument_ARRAY.network=True
        argument_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; wagwoord_VALUE: python3 Nutsmiddels/afstands_Instellings.py show'.format(argument_ARRAY.network_host,argument_ARRAY.network_host),flush=True)
    if argument_ARRAY.pip and not argument_ARRAY.network: ontleder.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argument_ARRAY.pip_port <= 65535: ontleder.error('--pip-port 범위는 1~65535입니다.')
    if argument_ARRAY.forward and not argument_ARRAY.network: ontleder.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as hulpbron_VALUE:
        if argument_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            hulpbron_VALUE.enter_context(꾸러미중계(argument_ARRAY.pip_port, argument_ARRAY.pip_cache, argument_ARRAY.pip_offline))
            print('bondel 중계: 127.0.0.1:' + str(argument_ARRAY.pip_port), flush=True)
        Voer_uit(argument_ARRAY)


def Voer_uit(argument_ARRAY):
    if argument_ARRAY.desktop:
        if argument_ARRAY.vnc or argument_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from werkskerm_bekyk import ry_werkskerm
        raise SystemExit(ry_werkskerm(argument_ARRAY.port, Netwerk=argument_ARRAY.network, 파일전송접속번호=argument_ARRAY.ftp_port, 전달규칙들=argument_ARRAY.forward, resolusie_VALUE=argument_ARRAY.resolution, gas_adres=argument_ARRAY.guest_ip, hou_adres=argument_ARRAY.network_host))
    opsies = ['-display', argument_ARRAY.display, '-serial', 'mon:stdio']
    if argument_ARRAY.vnc:
        opsies += ['-vnc', argument_ARRAY.vnc]
    if argument_ARRAY.network:
        from Netwerk_brug import Netwerk_brug
        with Netwerk_brug(argument_ARRAY.ftp_port, argument_ARRAY.forward, gas_adres=argument_ARRAY.guest_ip, hou_adres=argument_ARRAY.network_host) as brug:
            stand_VALUE = subprocess.call(Opdrag(argument_ARRAY.resolution) + opsies + brug.전달인수())
            if brug.Fout: raise SystemExit('network bridge: ' + brug.Fout)
        raise SystemExit(stand_VALUE)
    raise SystemExit(subprocess.call(Opdrag(argument_ARRAY.resolution) + opsies))


if __name__ == '__main__':
    Loop()
