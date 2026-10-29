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

To_do_rod = Path(__file__).resolve().parents[1]
vilkårlig_Filer = []


def _난수정리():
    for Sti in vilkårlig_Filer:
        try:
            os.unlink(Sti)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Fil:
        Fil.write(b'JKRENRG1' + os.urandom(32))
        vilkårlig_Filer.append(Fil.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Fil.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    vært = To_do_rod.parent / 'rpi4/build/host'
    indlæsningsfunktion = vært / 'lib/ld-musl-x86_64.so.1'
    binær = vært / 'usr/bin/qemu-system-aarch64'
    if indlæsningsfunktion.is_file() and binær.is_file():
        return [str(indlæsningsfunktion), '--library-path', str(vært / 'usr/lib') + ':' + str(vært / 'lib'),
                str(binær), '-L', str(vært / 'usr/share/qemu')]
    binær = shutil.which('qemu-system-aarch64')
    if not binær:
        raise SystemExit('raspi4b støtte_VÆRDI QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binær]


def 해상도읽기(Tekst):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Tekst):
        raise argparse.ArgumentTypeError('opløsning_VÆRDI format_VÆRDI: 1920x1080')
    너비, 높이 = map(int, Tekst.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('støtte_VÆRDI klippe: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Kommando(opløsning_VÆRDI=(640, 480)):
    Baggrund_VÆRDI = 모의기계()
    지원목록 = subprocess.check_output(Baggrund_VÆRDI + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*opløsning_VÆRDI))
    return Baggrund_VÆRDI + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(To_do_rod / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Kør_2():
    parser = argparse.ArgumentParser(description='eget Java Pi4 kerne_VÆRDI. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Afslut_app.')
    parser.add_argument('--display', default='none', help='none 또는 gtk/sdl (vært støtte_VÆRDI 필요)')
    parser.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 skærmbillede Størrelse. 예: 1920x1080; standardværdi 640x480')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC hardware_port 5902. tast_VÆRDI 입력은 UART 터미널에서 합니다.')
    parser.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    parser.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC hardware_port')
    parser.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Tilslut; --desktop과 함께 brug_VÆRDI 가능; 게스트에서 ftpd start')
    parser.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    parser.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP kontrol_VÆRDI hardware_port (데이터 50000..50007)')
    parser.add_argument('--guest-ip', default=None, help='QEMU NAT Frem_VÆRDI mål. 기본은 ip.conf의 IP; ændre_VÆRDI 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    parser.add_argument('--network-host', default='127.0.0.1', help='NAT modtage_VÆRDI mail. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN mail: ekstern_VÆRDI forbindelse_e05f319b')
    parser.add_argument('--forward', action='append', default=[], help='--network tilføj_post Tilslut: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    parser.add_argument('--pip', action='store_true', help='PyPI kilde_træ bundt 중계 Kør_2 (--network 필요, MicroPython 호환 소스만)')
    parser.add_argument('--pip-port', type=int, default=8027, help='bundt 중계의 localhost TCP hardware_port')
    parser.add_argument('--pip-cache', type=Path, default=To_do_rod/'build/pip-cache')
    parser.add_argument('--pip-offline', action='store_true', help='이미 받은 distribution_VÆRDI 파일만 제공')
    argument_MATRIX = parser.parse_args()
    if argument_MATRIX.remote:
        argument_MATRIX.network=True
        argument_MATRIX.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; adgangskode_VÆRDI: python3 Værktøjer/fjern_Indstillinger.py show'.format(argument_MATRIX.network_host,argument_MATRIX.network_host),flush=True)
    if argument_MATRIX.pip and not argument_MATRIX.network: parser.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argument_MATRIX.pip_port <= 65535: parser.error('--pip-port 범위는 1~65535입니다.')
    if argument_MATRIX.forward and not argument_MATRIX.network: parser.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ressource_VÆRDI:
        if argument_MATRIX.pip:
            from 꾸러미중계 import 꾸러미중계
            ressource_VÆRDI.enter_context(꾸러미중계(argument_MATRIX.pip_port, argument_MATRIX.pip_cache, argument_MATRIX.pip_offline))
            print('bundt 중계: 127.0.0.1:' + str(argument_MATRIX.pip_port), flush=True)
        Kør(argument_MATRIX)


def Kør(argument_MATRIX):
    if argument_MATRIX.desktop:
        if argument_MATRIX.vnc or argument_MATRIX.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from desktop_Visning import køre_desktop
        raise SystemExit(køre_desktop(argument_MATRIX.port, netværk=argument_MATRIX.network, filoverførsel_portnummer=argument_MATRIX.ftp_port, 전달규칙들=argument_MATRIX.forward, opløsning_VÆRDI=argument_MATRIX.resolution, gæst_mail=argument_MATRIX.guest_ip, vært_mail=argument_MATRIX.network_host))
    Indstillinger_7f769d16 = ['-display', argument_MATRIX.display, '-serial', 'mon:stdio']
    if argument_MATRIX.vnc:
        Indstillinger_7f769d16 += ['-vnc', argument_MATRIX.vnc]
    if argument_MATRIX.network:
        from bro_3de4fe3a import bro_3de4fe3a
        with bro_3de4fe3a(argument_MATRIX.ftp_port, argument_MATRIX.forward, gæst_mail=argument_MATRIX.guest_ip, vært_mail=argument_MATRIX.network_host) as bro:
            status_VÆRDI = subprocess.call(Kommando(argument_MATRIX.resolution) + Indstillinger_7f769d16 + bro.전달인수())
            if bro.fejl: raise SystemExit('network bridge: ' + bro.fejl)
        raise SystemExit(status_VÆRDI)
    raise SystemExit(subprocess.call(Kommando(argument_MATRIX.resolution) + Indstillinger_7f769d16))


if __name__ == '__main__':
    Kør_2()
