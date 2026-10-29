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

åtgärd_rot = Path(__file__).resolve().parents[1]
slumpmässig_Filer = []


def _난수정리():
    for sökväg_2 in slumpmässig_Filer:
        try:
            os.unlink(sökväg_2)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as filnamn:
        filnamn.write(b'JKRENRG1' + os.urandom(32))
        slumpmässig_Filer.append(filnamn.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(filnamn.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    värd = åtgärd_rot.parent / 'rpi4/build/host'
    inläsare = värd / 'lib/ld-musl-x86_64.so.1'
    binär = värd / 'usr/bin/qemu-system-aarch64'
    if inläsare.is_file() and binär.is_file():
        return [str(inläsare), '--library-path', str(värd / 'usr/lib') + ':' + str(värd / 'lib'),
                str(binär), '-L', str(värd / 'usr/share/qemu')]
    binär = shutil.which('qemu-system-aarch64')
    if not binär:
        raise SystemExit('raspi4b stöd_värde QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binär]


def läsa_upplösning(text):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', text):
        raise argparse.ArgumentTypeError('upplösning_värde format_värde: 1920x1080')
    너비, 높이 = map(int, text.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('stöd_värde klipp: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def kommando(upplösning_värde=(640, 480)):
    Bakgrund_värde = 모의기계()
    지원목록 = subprocess.check_output(Bakgrund_värde + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = läsa_upplösning('{}x{}'.format(*upplösning_värde))
    return Bakgrund_värde + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(åtgärd_rot / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Kör():
    parser = argparse.ArgumentParser(description='eget Java Pi4 kärna_värde. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Utgång_app.')
    parser.add_argument('--display', default='none', help='none 또는 gtk/sdl (värd stöd_värde 필요)')
    parser.add_argument('--resolution', type=läsa_upplösning, default=(640, 480), help='maskinstart skärmbild Storlek. 예: 1920x1080; standardvärde 640x480')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC maskinvara_port 5902. Nyckel_värde 입력은 UART 터미널에서 합니다.')
    parser.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    parser.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC maskinvara_port')
    parser.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Anslut; --desktop과 함께 använda_värde 가능; 게스트에서 ftpd start')
    parser.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    parser.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP kontroll_värde maskinvara_port (데이터 50000..50007)')
    parser.add_argument('--guest-ip', default=None, help='QEMU NAT Framåt_värde mål. 기본은 ip.conf의 IP; ändra_värde 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    parser.add_argument('--network-host', default='127.0.0.1', help='NAT få_värde Adress. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN Adress: extern_värde kontakt_e05f319b')
    parser.add_argument('--forward', action='append', default=[], help='--network Lägga_till_post Anslut: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    parser.add_argument('--pip', action='store_true', help='PyPI källa_träd bunt 중계 Kör (--network 필요, MicroPython 호환 소스만)')
    parser.add_argument('--pip-port', type=int, default=8027, help='bunt 중계의 localhost TCP maskinvara_port')
    parser.add_argument('--pip-cache', type=Path, default=åtgärd_rot/'build/pip-cache')
    parser.add_argument('--pip-offline', action='store_true', help='이미 받은 fördelning_värde 파일만 제공')
    argument_MATRIS = parser.parse_args()
    if argument_MATRIS.remote:
        argument_MATRIS.network=True
        argument_MATRIS.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; lösenord_värde: python3 verktyg/fjärr_Inställningar.py show'.format(argument_MATRIS.network_host,argument_MATRIS.network_host),flush=True)
    if argument_MATRIS.pip and not argument_MATRIS.network: parser.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argument_MATRIS.pip_port <= 65535: parser.error('--pip-port 범위는 1~65535입니다.')
    if argument_MATRIS.forward and not argument_MATRIS.network: parser.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as resurs_värde:
        if argument_MATRIS.pip:
            from 꾸러미중계 import 꾸러미중계
            resurs_värde.enter_context(꾸러미중계(argument_MATRIS.pip_port, argument_MATRIS.pip_cache, argument_MATRIS.pip_offline))
            print('bunt 중계: 127.0.0.1:' + str(argument_MATRIS.pip_port), flush=True)
        Starta(argument_MATRIS)


def Starta(argument_MATRIS):
    if argument_MATRIS.desktop:
        if argument_MATRIS.vnc or argument_MATRIS.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from Dator_vy import köra_Dator
        raise SystemExit(köra_Dator(argument_MATRIS.port, nätverk=argument_MATRIS.network, filöverföring_portnummer=argument_MATRIS.ftp_port, 전달규칙들=argument_MATRIS.forward, upplösning_värde=argument_MATRIS.resolution, gäst_ADRESS=argument_MATRIS.guest_ip, värd_ADRESS=argument_MATRIS.network_host))
    Alternativ = ['-display', argument_MATRIS.display, '-serial', 'mon:stdio']
    if argument_MATRIS.vnc:
        Alternativ += ['-vnc', argument_MATRIS.vnc]
    if argument_MATRIS.network:
        from brygga_3de4fe3a import brygga_3de4fe3a
        with brygga_3de4fe3a(argument_MATRIS.ftp_port, argument_MATRIS.forward, gäst_ADRESS=argument_MATRIS.guest_ip, värd_ADRESS=argument_MATRIS.network_host) as brygga:
            status_värde = subprocess.call(kommando(argument_MATRIS.resolution) + Alternativ + brygga.전달인수())
            if brygga.fel: raise SystemExit('network bridge: ' + brygga.fel)
        raise SystemExit(status_värde)
    raise SystemExit(subprocess.call(kommando(argument_MATRIS.resolution) + Alternativ))


if __name__ == '__main__':
    Kör()
