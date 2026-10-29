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

speile_rot = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for Sti in _난수파일들:
        try:
            os.unlink(Sti)
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
    vert = speile_rot.parent / 'rpi4/build/host'
    laster = vert / 'lib/ld-musl-x86_64.so.1'
    binær = vert / 'usr/bin/qemu-system-aarch64'
    if laster.is_file() and binær.is_file():
        return [str(laster), '--library-path', str(vert / 'usr/lib') + ':' + str(vert / 'lib'),
                str(binær), '-L', str(vert / 'usr/share/qemu')]
    binær = shutil.which('qemu-system-aarch64')
    if not binær:
        raise SystemExit('raspi4b støtte_VERDI QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binær]


def 해상도읽기(Tekst):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Tekst):
        raise argparse.ArgumentTypeError('oppløsning_VERDI format_VERDI: 1920x1080')
    너비, 높이 = map(int, Tekst.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('støtte_VERDI klippe: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Kommando(oppløsning_VERDI=(640, 480)):
    bakgrunn_VERDI = 모의기계()
    지원목록 = subprocess.check_output(bakgrunn_VERDI + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*oppløsning_VERDI))
    return bakgrunn_VERDI + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(speile_rot / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Kjør_2():
    parser = argparse.ArgumentParser(description='eget Java Pi4 kjerne_VERDI. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Utgang_app.')
    parser.add_argument('--display', default='none', help='none 또는 gtk/sdl (vert støtte_VERDI 필요)')
    parser.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 skjermbilde Størrelse. 예: 1920x1080; standardverdi 640x480')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC maskinvare_port 5902. tast_VERDI 입력은 UART 터미널에서 합니다.')
    parser.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    parser.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC maskinvare_port')
    parser.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Koble_til; --desktop과 함께 bruk_VERDI 가능; 게스트에서 ftpd start')
    parser.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    parser.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP kontroll_VERDI maskinvare_port (데이터 50000..50007)')
    parser.add_argument('--guest-ip', default=None, help='QEMU NAT Frem_VERDI mål. 기본은 ip.conf의 IP; endre_VERDI 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    parser.add_argument('--network-host', default='127.0.0.1', help='NAT motta_VERDI e_post. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN e_post: ekstern_VERDI kontakt_e05f319b')
    parser.add_argument('--forward', action='append', default=[], help='--network Tilføye_oppføring Koble_til: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    parser.add_argument('--pip', action='store_true', help='PyPI kilde_tre bunt 중계 Kjør_2 (--network 필요, MicroPython 호환 소스만)')
    parser.add_argument('--pip-port', type=int, default=8027, help='bunt 중계의 localhost TCP maskinvare_port')
    parser.add_argument('--pip-cache', type=Path, default=speile_rot/'build/pip-cache')
    parser.add_argument('--pip-offline', action='store_true', help='이미 받은 distribusjon_VERDI 파일만 제공')
    argument_MATRISE = parser.parse_args()
    if argument_MATRISE.remote:
        argument_MATRISE.network=True
        argument_MATRISE.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; passord_VERDI: python3 Verktøy/ekstern_Innstillinger.py show'.format(argument_MATRISE.network_host,argument_MATRISE.network_host),flush=True)
    if argument_MATRISE.pip and not argument_MATRISE.network: parser.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argument_MATRISE.pip_port <= 65535: parser.error('--pip-port 범위는 1~65535입니다.')
    if argument_MATRISE.forward and not argument_MATRISE.network: parser.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ressurs_VERDI:
        if argument_MATRISE.pip:
            from 꾸러미중계 import 꾸러미중계
            ressurs_VERDI.enter_context(꾸러미중계(argument_MATRISE.pip_port, argument_MATRISE.pip_cache, argument_MATRISE.pip_offline))
            print('bunt 중계: 127.0.0.1:' + str(argument_MATRISE.pip_port), flush=True)
        Kjør(argument_MATRISE)


def Kjør(argument_MATRISE):
    if argument_MATRISE.desktop:
        if argument_MATRISE.vnc or argument_MATRISE.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from stasjonær_vise import kjøre_stasjonær
        raise SystemExit(kjøre_stasjonær(argument_MATRISE.port, nettverk=argument_MATRISE.network, filoverføring_portnummer=argument_MATRISE.ftp_port, 전달규칙들=argument_MATRISE.forward, oppløsning_VERDI=argument_MATRISE.resolution, gjest_e_post=argument_MATRISE.guest_ip, vert_e_post=argument_MATRISE.network_host))
    Alternativer = ['-display', argument_MATRISE.display, '-serial', 'mon:stdio']
    if argument_MATRISE.vnc:
        Alternativer += ['-vnc', argument_MATRISE.vnc]
    if argument_MATRISE.network:
        from bro_3de4fe3a import bro_3de4fe3a
        with bro_3de4fe3a(argument_MATRISE.ftp_port, argument_MATRISE.forward, gjest_e_post=argument_MATRISE.guest_ip, vert_e_post=argument_MATRISE.network_host) as bro:
            status_VERDI = subprocess.call(Kommando(argument_MATRISE.resolution) + Alternativer + bro.전달인수())
            if bro.feil: raise SystemExit('network bridge: ' + bro.feil)
        raise SystemExit(status_VERDI)
    raise SystemExit(subprocess.call(Kommando(argument_MATRISE.resolution) + Alternativer))


if __name__ == '__main__':
    Kjør_2()
