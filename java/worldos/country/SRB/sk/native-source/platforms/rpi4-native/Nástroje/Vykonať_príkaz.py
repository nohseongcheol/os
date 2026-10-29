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

akcia_koreň = Path(__file__).resolve().parents[1]
náhodný_Súbory = []


def _난수정리():
    for Cesta in náhodný_Súbory:
        try:
            os.unlink(Cesta)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Súbor:
        Súbor.write(b'JKRENRG1' + os.urandom(32))
        náhodný_Súbory.append(Súbor.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Súbor.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    hostiteľ = akcia_koreň.parent / 'rpi4/build/host'
    zavádzací_program = hostiteľ / 'lib/ld-musl-x86_64.so.1'
    Binary = hostiteľ / 'usr/bin/qemu-system-aarch64'
    if zavádzací_program.is_file() and Binary.is_file():
        return [str(zavádzací_program), '--library-path', str(hostiteľ / 'usr/lib') + ':' + str(hostiteľ / 'lib'),
                str(Binary), '-L', str(hostiteľ / 'usr/share/qemu')]
    Binary = shutil.which('qemu-system-aarch64')
    if not Binary:
        raise SystemExit('raspi4b Podpora_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [Binary]


def 해상도읽기(Spracovanie_textu):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Spracovanie_textu):
        raise argparse.ArgumentTypeError('rozlíšenie_VALUE formát_VALUE: 1920x1080')
    너비, výška_VALUE = map(int, Spracovanie_textu.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= výška_VALUE <= 1080):
        raise argparse.ArgumentTypeError('Podpora_VALUE klip: 너비 640~1920, výška_VALUE 480~1080')
    return 너비, výška_VALUE


def Príkaz(rozlíšenie_VALUE=(640, 480)):
    tapeta_VALUE = 모의기계()
    지원목록 = subprocess.check_output(tapeta_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, výška_VALUE = 해상도읽기('{}x{}'.format(*rozlíšenie_VALUE))
    return tapeta_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(výška_VALUE), '-kernel',
                   str(akcia_koreň / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Spustiť_2():
    analyzátor = argparse.ArgumentParser(description='vlastné Java Pi4 jadro_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Skončiť_program.')
    analyzátor.add_argument('--display', default='none', help='none 또는 gtk/sdl (hostiteľ Podpora_VALUE 필요)')
    analyzátor.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Veľkosť. 예: 1920x1080; predvolená_hodnota 640x480')
    analyzátor.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC hardvér_port 5902. Kľúč_VALUE 입력은 UART 터미널에서 합니다.')
    analyzátor.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    analyzátor.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC hardvér_port')
    analyzátor.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Pripojiť; --desktop과 함께 používať_VALUE 가능; 게스트에서 ftpd start')
    analyzátor.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    analyzátor.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP riadenie_VALUE hardvér_port (데이터 50000..50007)')
    analyzátor.add_argument('--guest-ip', default=None, help='QEMU NAT Dopredu_VALUE cieľová_hodnota. 기본은 ip.conf의 IP; zmeniť_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    analyzátor.add_argument('--network-host', default='127.0.0.1', help='NAT dostať_VALUE adresa. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN adresa: externý_VALUE kontakt_e05f319b')
    analyzátor.add_argument('--forward', action='append', default=[], help='--network Pripojiť_položka Pripojiť: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    analyzátor.add_argument('--pip', action='store_true', help='PyPI zdroj_strom zväzok 중계 Spustiť_2 (--network 필요, MicroPython 호환 소스만)')
    analyzátor.add_argument('--pip-port', type=int, default=8027, help='zväzok 중계의 localhost TCP hardvér_port')
    analyzátor.add_argument('--pip-cache', type=Path, default=akcia_koreň/'build/pip-cache')
    analyzátor.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    argument_pole = analyzátor.parse_args()
    if argument_pole.remote:
        argument_pole.network=True
        argument_pole.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; heslo_VALUE: python3 Nástroje/vzdialený_Nastavenia.py show'.format(argument_pole.network_host,argument_pole.network_host),flush=True)
    if argument_pole.pip and not argument_pole.network: analyzátor.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argument_pole.pip_port <= 65535: analyzátor.error('--pip-port 범위는 1~65535입니다.')
    if argument_pole.forward and not argument_pole.network: analyzátor.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as zdroj_VALUE:
        if argument_pole.pip:
            from 꾸러미중계 import 꾸러미중계
            zdroj_VALUE.enter_context(꾸러미중계(argument_pole.pip_port, argument_pole.pip_cache, argument_pole.pip_offline))
            print('zväzok 중계: 127.0.0.1:' + str(argument_pole.pip_port), flush=True)
        Spustiť(argument_pole)


def Spustiť(argument_pole):
    if argument_pole.desktop:
        if argument_pole.vnc or argument_pole.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from počítač_zobraziť import spustiť_počítač
        raise SystemExit(spustiť_počítač(argument_pole.port, sieť=argument_pole.network, prenos_súborov_číslo_portu=argument_pole.ftp_port, 전달규칙들=argument_pole.forward, rozlíšenie_VALUE=argument_pole.resolution, hosť_adresa=argument_pole.guest_ip, hostiteľ_adresa=argument_pole.network_host))
    Možnosti = ['-display', argument_pole.display, '-serial', 'mon:stdio']
    if argument_pole.vnc:
        Možnosti += ['-vnc', argument_pole.vnc]
    if argument_pole.network:
        from sieťový_most import sieťový_most
        with sieťový_most(argument_pole.ftp_port, argument_pole.forward, hosť_adresa=argument_pole.guest_ip, hostiteľ_adresa=argument_pole.network_host) as most:
            Stav_VALUE = subprocess.call(Príkaz(argument_pole.resolution) + Možnosti + most.전달인수())
            if most.chyba: raise SystemExit('network bridge: ' + most.chyba)
        raise SystemExit(Stav_VALUE)
    raise SystemExit(subprocess.call(Príkaz(argument_pole.resolution) + Možnosti))


if __name__ == '__main__':
    Spustiť_2()
