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

Project_rădăcină = Path(__file__).resolve().parents[1]
aleator_Fișiere = []


def _난수정리():
    for Cale in aleator_Fișiere:
        try:
            os.unlink(Cale)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Fișier:
        Fișier.write(b'JKRENRG1' + os.urandom(32))
        aleator_Fișiere.append(Fișier.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Fișier.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    gazdă = Project_rădăcină.parent / 'rpi4/build/host'
    încărcător = gazdă / 'lib/ld-musl-x86_64.so.1'
    binar = gazdă / 'usr/bin/qemu-system-aarch64'
    if încărcător.is_file() and binar.is_file():
        return [str(încărcător), '--library-path', str(gazdă / 'usr/lib') + ':' + str(gazdă / 'lib'),
                str(binar), '-L', str(gazdă / 'usr/share/qemu')]
    binar = shutil.which('qemu-system-aarch64')
    if not binar:
        raise SystemExit('raspi4b suport_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binar]


def 해상도읽기(SMS):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', SMS):
        raise argparse.ArgumentTypeError('rezoluție_VALUE format_VALUE: 1920x1080')
    너비, 높이 = map(int, SMS.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('suport_VALUE clip: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Comandă(rezoluție_VALUE=(640, 480)):
    tapet_VALUE = 모의기계()
    지원목록 = subprocess.check_output(tapet_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*rezoluție_VALUE))
    return tapet_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(Project_rădăcină / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Pornește():
    parser = argparse.ArgumentParser(description='propriu Java Pi4 nucleu_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 ieși_program.')
    parser.add_argument('--display', default='none', help='none 또는 gtk/sdl (gazdă suport_VALUE 필요)')
    parser.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Mărime. 예: 1920x1080; valoare_implicită 640x480')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Cheie_VALUE 입력은 UART 터미널에서 합니다.')
    parser.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    parser.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    parser.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Conectează; --desktop과 함께 utiliza_VALUE 가능; 게스트에서 ftpd start')
    parser.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    parser.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP control_VALUE 포트 (데이터 50000..50007)')
    parser.add_argument('--guest-ip', default=None, help='QEMU NAT Înainte_VALUE țintă. 기본은 ip.conf의 IP; schimba_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    parser.add_argument('--network-host', default='127.0.0.1', help='NAT primi_VALUE adresa. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN adresa: extern_VALUE conexiune_e05f319b')
    parser.add_argument('--forward', action='append', default=[], help='--network adăuga_intrare Conectează: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    parser.add_argument('--pip', action='store_true', help='PyPI sursă_arborescență set 중계 Pornește (--network 필요, MicroPython 호환 소스만)')
    parser.add_argument('--pip-port', type=int, default=8027, help='set 중계의 localhost TCP 포트')
    parser.add_argument('--pip-cache', type=Path, default=Project_rădăcină/'build/pip-cache')
    parser.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    argument_ARRAY = parser.parse_args()
    if argument_ARRAY.remote:
        argument_ARRAY.network=True
        argument_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; parolă_VALUE: python3 Instrumente/la_distanță_Setări.py show'.format(argument_ARRAY.network_host,argument_ARRAY.network_host),flush=True)
    if argument_ARRAY.pip and not argument_ARRAY.network: parser.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argument_ARRAY.pip_port <= 65535: parser.error('--pip-port 범위는 1~65535입니다.')
    if argument_ARRAY.forward and not argument_ARRAY.network: parser.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as resursă_VALUE:
        if argument_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            resursă_VALUE.enter_context(꾸러미중계(argument_ARRAY.pip_port, argument_ARRAY.pip_cache, argument_ARRAY.pip_offline))
            print('set 중계: 127.0.0.1:' + str(argument_ARRAY.pip_port), flush=True)
        Execută(argument_ARRAY)


def Execută(argument_ARRAY):
    if argument_ARRAY.desktop:
        if argument_ARRAY.vnc or argument_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from desktop_vizualiza import rula_desktop
        raise SystemExit(rula_desktop(argument_ARRAY.port, rețea=argument_ARRAY.network, transfer_de_fișiere_număr_port=argument_ARRAY.ftp_port, 전달규칙들=argument_ARRAY.forward, rezoluție_VALUE=argument_ARRAY.resolution, invitat_adresa=argument_ARRAY.guest_ip, gazdă_adresa=argument_ARRAY.network_host))
    Opțiuni = ['-display', argument_ARRAY.display, '-serial', 'mon:stdio']
    if argument_ARRAY.vnc:
        Opțiuni += ['-vnc', argument_ARRAY.vnc]
    if argument_ARRAY.network:
        from punte_3de4fe3a import punte_3de4fe3a
        with punte_3de4fe3a(argument_ARRAY.ftp_port, argument_ARRAY.forward, invitat_adresa=argument_ARRAY.guest_ip, gazdă_adresa=argument_ARRAY.network_host) as punte:
            Stare_VALUE = subprocess.call(Comandă(argument_ARRAY.resolution) + Opțiuni + punte.전달인수())
            if punte.eroare: raise SystemExit('network bridge: ' + punte.eroare)
        raise SystemExit(Stare_VALUE)
    raise SystemExit(subprocess.call(Comandă(argument_ARRAY.resolution) + Opțiuni))


if __name__ == '__main__':
    Pornește()
