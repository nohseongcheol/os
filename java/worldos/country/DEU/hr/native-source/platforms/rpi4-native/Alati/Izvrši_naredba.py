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

akcija_korijen = Path(__file__).resolve().parents[1]
slučajan_Datoteke = []


def _난수정리():
    for PUTANJA in slučajan_Datoteke:
        try:
            os.unlink(PUTANJA)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Datoteka:
        Datoteka.write(b'JKRENRG1' + os.urandom(32))
        slučajan_Datoteke.append(Datoteka.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Datoteka.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    domaćin = akcija_korijen.parent / 'rpi4/build/host'
    učitavač = domaćin / 'lib/ld-musl-x86_64.so.1'
    binarni_podaci = domaćin / 'usr/bin/qemu-system-aarch64'
    if učitavač.is_file() and binarni_podaci.is_file():
        return [str(učitavač), '--library-path', str(domaćin / 'usr/lib') + ':' + str(domaćin / 'lib'),
                str(binarni_podaci), '-L', str(domaćin / 'usr/share/qemu')]
    binarni_podaci = shutil.which('qemu-system-aarch64')
    if not binarni_podaci:
        raise SystemExit('raspi4b Podrška_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binarni_podaci]


def 해상도읽기(Tekst):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Tekst):
        raise argparse.ArgumentTypeError('razlučivost_VALUE oblik_VALUE: 1920x1080')
    너비, 높이 = map(int, Tekst.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Podrška_VALUE isječak: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Naredba(razlučivost_VALUE=(640, 480)):
    podloga_VALUE = 모의기계()
    지원목록 = subprocess.check_output(podloga_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*razlučivost_VALUE))
    return podloga_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(akcija_korijen / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Pokreni():
    analizator = argparse.ArgumentParser(description='vlastiti Java Pi4 jezgra_sustava_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Izlaz_program.')
    analizator.add_argument('--display', default='none', help='none 또는 gtk/sdl (domaćin Podrška_VALUE 필요)')
    analizator.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Veličina. 예: 1920x1080; zadana_vrijednost 640x480')
    analizator.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Ključ_VALUE 입력은 UART 터미널에서 합니다.')
    analizator.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    analizator.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    analizator.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Spoji_se; --desktop과 함께 uporaba_VALUE 가능; 게스트에서 ftpd start')
    analizator.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    analizator.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP kontrola_VALUE 포트 (데이터 50000..50007)')
    analizator.add_argument('--guest-ip', default=None, help='QEMU NAT Naprijed_VALUE cilj. 기본은 ip.conf의 IP; promijeniti_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    analizator.add_argument('--network-host', default='127.0.0.1', help='NAT primiti_VALUE adresa. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN adresa: vanjski_VALUE veza_e05f319b')
    analizator.add_argument('--forward', action='append', default=[], help='--network dodati_unos Spoji_se: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    analizator.add_argument('--pip', action='store_true', help='PyPI izvor_stablo komplet 중계 Pokreni (--network 필요, MicroPython 호환 소스만)')
    analizator.add_argument('--pip-port', type=int, default=8027, help='komplet 중계의 localhost TCP 포트')
    analizator.add_argument('--pip-cache', type=Path, default=akcija_korijen/'build/pip-cache')
    analizator.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    argument_ARRAY = analizator.parse_args()
    if argument_ARRAY.remote:
        argument_ARRAY.network=True
        argument_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; lozinka_VALUE: python3 Alati/udaljeno_Postavke.py show'.format(argument_ARRAY.network_host,argument_ARRAY.network_host),flush=True)
    if argument_ARRAY.pip and not argument_ARRAY.network: analizator.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argument_ARRAY.pip_port <= 65535: analizator.error('--pip-port 범위는 1~65535입니다.')
    if argument_ARRAY.forward and not argument_ARRAY.network: analizator.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as resurs_VALUE:
        if argument_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            resurs_VALUE.enter_context(꾸러미중계(argument_ARRAY.pip_port, argument_ARRAY.pip_cache, argument_ARRAY.pip_offline))
            print('komplet 중계: 127.0.0.1:' + str(argument_ARRAY.pip_port), flush=True)
        Izvrši(argument_ARRAY)


def Izvrši(argument_ARRAY):
    if argument_ARRAY.desktop:
        if argument_ARRAY.vnc or argument_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from stolni_Prikaz import izvršiti_stolni
        raise SystemExit(izvršiti_stolni(argument_ARRAY.port, mreža=argument_ARRAY.network, prijenos_datoteka_broj_priključka=argument_ARRAY.ftp_port, 전달규칙들=argument_ARRAY.forward, razlučivost_VALUE=argument_ARRAY.resolution, gost_adresa=argument_ARRAY.guest_ip, domaćin_adresa=argument_ARRAY.network_host))
    Mogućnosti = ['-display', argument_ARRAY.display, '-serial', 'mon:stdio']
    if argument_ARRAY.vnc:
        Mogućnosti += ['-vnc', argument_ARRAY.vnc]
    if argument_ARRAY.network:
        from most_3de4fe3a import most_3de4fe3a
        with most_3de4fe3a(argument_ARRAY.ftp_port, argument_ARRAY.forward, gost_adresa=argument_ARRAY.guest_ip, domaćin_adresa=argument_ARRAY.network_host) as most:
            Stanje_VALUE = subprocess.call(Naredba(argument_ARRAY.resolution) + Mogućnosti + most.전달인수())
            if most.GREŠKA: raise SystemExit('network bridge: ' + most.GREŠKA)
        raise SystemExit(Stanje_VALUE)
    raise SystemExit(subprocess.call(Naredba(argument_ARRAY.resolution) + Mogućnosti))


if __name__ == '__main__':
    Pokreni()
