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

Taken_wortel = Path(__file__).resolve().parents[1]
willekeurig_Files = []


def _난수정리():
    for pad in willekeurig_Files:
        try:
            os.unlink(pad)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as bestand:
        bestand.write(b'JKRENRG1' + os.urandom(32))
        willekeurig_Files.append(bestand.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(bestand.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    host = Taken_wortel.parent / 'rpi4/build/host'
    laadprogramma = host / 'lib/ld-musl-x86_64.so.1'
    binair = host / 'usr/bin/qemu-system-aarch64'
    if laadprogramma.is_file() and binair.is_file():
        return [str(laadprogramma), '--library-path', str(host / 'usr/lib') + ':' + str(host / 'lib'),
                str(binair), '-L', str(host / 'usr/share/qemu')]
    binair = shutil.which('qemu-system-aarch64')
    if not binair:
        raise SystemExit('raspi4b steun_WAARDE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binair]


def 해상도읽기(tekst):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', tekst):
        raise argparse.ArgumentTypeError('resolutie_WAARDE opmaak_WAARDE: 1920x1080')
    너비, hoogte_WAARDE = map(int, tekst.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= hoogte_WAARDE <= 1080):
        raise argparse.ArgumentTypeError('steun_WAARDE clip: 너비 640~1920, hoogte_WAARDE 480~1080')
    return 너비, hoogte_WAARDE


def opdracht(resolutie_WAARDE=(640, 480)):
    Achtergrond_WAARDE = 모의기계()
    지원목록 = subprocess.check_output(Achtergrond_WAARDE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, hoogte_WAARDE = 해상도읽기('{}x{}'.format(*resolutie_WAARDE))
    return Achtergrond_WAARDE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(hoogte_WAARDE), '-kernel',
                   str(Taken_wortel / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def starten():
    parser = argparse.ArgumentParser(description='Eigen Java Pi4 kernel_WAARDE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Einde_app.')
    parser.add_argument('--display', default='none', help='none 또는 gtk/sdl (host steun_WAARDE 필요)')
    parser.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='machineopstart scherm Grootte. 예: 1920x1080; standaardwaarde 640x480')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC hardware_poort 5902. toets_WAARDE 입력은 UART 터미널에서 합니다.')
    parser.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    parser.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC hardware_poort')
    parser.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Verbinden; --desktop과 함께 gebruik_WAARDE 가능; 게스트에서 ftpd start')
    parser.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    parser.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP controle_WAARDE hardware_poort (데이터 50000..50007)')
    parser.add_argument('--guest-ip', default=None, help='QEMU NAT Vooruit_WAARDE doel. 기본은 ip.conf의 IP; wijzigen_WAARDE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    parser.add_argument('--network-host', default='127.0.0.1', help='NAT ontvangen_WAARDE ADRES. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ADRES: extern_WAARDE verbinding_e05f319b')
    parser.add_argument('--forward', action='append', default=[], help='--network toevoegen_invoer Verbinden: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    parser.add_argument('--pip', action='store_true', help='PyPI bron_structuur bundel 중계 starten (--network 필요, MicroPython 호환 소스만)')
    parser.add_argument('--pip-port', type=int, default=8027, help='bundel 중계의 localhost TCP hardware_poort')
    parser.add_argument('--pip-cache', type=Path, default=Taken_wortel/'build/pip-cache')
    parser.add_argument('--pip-offline', action='store_true', help='이미 받은 distributie_WAARDE 파일만 제공')
    argument_MATRIX = parser.parse_args()
    if argument_MATRIX.remote:
        argument_MATRIX.network=True
        argument_MATRIX.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; wachtwoord_WAARDE: python3 hulpmiddelen/extern_Instellingen.py show'.format(argument_MATRIX.network_host,argument_MATRIX.network_host),flush=True)
    if argument_MATRIX.pip and not argument_MATRIX.network: parser.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argument_MATRIX.pip_port <= 65535: parser.error('--pip-port 범위는 1~65535입니다.')
    if argument_MATRIX.forward and not argument_MATRIX.network: parser.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as bron_WAARDE:
        if argument_MATRIX.pip:
            from 꾸러미중계 import 꾸러미중계
            bron_WAARDE.enter_context(꾸러미중계(argument_MATRIX.pip_port, argument_MATRIX.pip_cache, argument_MATRIX.pip_offline))
            print('bundel 중계: 127.0.0.1:' + str(argument_MATRIX.pip_port), flush=True)
        Uitvoeren(argument_MATRIX)


def Uitvoeren(argument_MATRIX):
    if argument_MATRIX.desktop:
        if argument_MATRIX.vnc or argument_MATRIX.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from pc_Weergave import uitvoeren_pc
        raise SystemExit(uitvoeren_pc(argument_MATRIX.port, net=argument_MATRIX.network, bestandsoverdracht_poortnummer=argument_MATRIX.ftp_port, 전달규칙들=argument_MATRIX.forward, resolutie_WAARDE=argument_MATRIX.resolution, gast_ADRES=argument_MATRIX.guest_ip, host_ADRES=argument_MATRIX.network_host))
    Opties = ['-display', argument_MATRIX.display, '-serial', 'mon:stdio']
    if argument_MATRIX.vnc:
        Opties += ['-vnc', argument_MATRIX.vnc]
    if argument_MATRIX.network:
        from brug_3de4fe3a import brug_3de4fe3a
        with brug_3de4fe3a(argument_MATRIX.ftp_port, argument_MATRIX.forward, gast_ADRES=argument_MATRIX.guest_ip, host_ADRES=argument_MATRIX.network_host) as brug:
            Status_WAARDE = subprocess.call(opdracht(argument_MATRIX.resolution) + Opties + brug.전달인수())
            if brug.fout: raise SystemExit('network bridge: ' + brug.fout)
        raise SystemExit(Status_WAARDE)
    raise SystemExit(subprocess.call(opdracht(argument_MATRIX.resolution) + Opties))


if __name__ == '__main__':
    starten()
