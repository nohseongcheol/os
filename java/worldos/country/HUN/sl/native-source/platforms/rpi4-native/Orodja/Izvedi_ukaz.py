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

pobuda_koren = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for POT in _난수파일들:
        try:
            os.unlink(POT)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Datoteka:
        Datoteka.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Datoteka.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Datoteka.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    gostiti = pobuda_koren.parent / 'rpi4/build/host'
    nalagalnik = gostiti / 'lib/ld-musl-x86_64.so.1'
    binary = gostiti / 'usr/bin/qemu-system-aarch64'
    if nalagalnik.is_file() and binary.is_file():
        return [str(nalagalnik), '--library-path', str(gostiti / 'usr/lib') + ':' + str(gostiti / 'lib'),
                str(binary), '-L', str(gostiti / 'usr/share/qemu')]
    binary = shutil.which('qemu-system-aarch64')
    if not binary:
        raise SystemExit('raspi4b Podpora_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binary]


def 해상도읽기(Besedilo):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Besedilo):
        raise argparse.ArgumentTypeError('ločljivost_VALUE oblika_VALUE: 1920x1080')
    너비, višina_VALUE = map(int, Besedilo.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= višina_VALUE <= 1080):
        raise argparse.ArgumentTypeError('Podpora_VALUE izrezek: 너비 640~1920, višina_VALUE 480~1080')
    return 너비, višina_VALUE


def Ukaz(ločljivost_VALUE=(640, 480)):
    Ozadje_VALUE = 모의기계()
    지원목록 = subprocess.check_output(Ozadje_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, višina_VALUE = 해상도읽기('{}x{}'.format(*ločljivost_VALUE))
    return Ozadje_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(višina_VALUE), '-kernel',
                   str(pobuda_koren / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Zaženi():
    razčlenjevalnik = argparse.ArgumentParser(description='lastno Java Pi4 jedro_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Izhod_aplikacija.')
    razčlenjevalnik.add_argument('--display', default='none', help='none 또는 gtk/sdl (gostiti Podpora_VALUE 필요)')
    razčlenjevalnik.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Velikost. 예: 1920x1080; privzeta_vrednost 640x480')
    razčlenjevalnik.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC strojna_oprema_vrata 5902. Ključ_VALUE 입력은 UART 터미널에서 합니다.')
    razčlenjevalnik.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    razčlenjevalnik.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC strojna_oprema_vrata')
    razčlenjevalnik.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Poveži; --desktop과 함께 uporaba_VALUE 가능; 게스트에서 ftpd start')
    razčlenjevalnik.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    razčlenjevalnik.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP nadzor_VALUE strojna_oprema_vrata (데이터 50000..50007)')
    razčlenjevalnik.add_argument('--guest-ip', default=None, help='QEMU NAT Naprej_VALUE tarča. 기본은 ip.conf의 IP; spremeniti_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    razčlenjevalnik.add_argument('--network-host', default='127.0.0.1', help='NAT sprejeti_sprejemati_prejeti_prejemati_VALUE naslov. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN naslov: zunanji_VALUE povezava_e05f319b')
    razčlenjevalnik.add_argument('--forward', action='append', default=[], help='--network dodati_vnos Poveži: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    razčlenjevalnik.add_argument('--pip', action='store_true', help='PyPI vir_drevo sveženj 중계 Zaženi (--network 필요, MicroPython 호환 소스만)')
    razčlenjevalnik.add_argument('--pip-port', type=int, default=8027, help='sveženj 중계의 localhost TCP strojna_oprema_vrata')
    razčlenjevalnik.add_argument('--pip-cache', type=Path, default=pobuda_koren/'build/pip-cache')
    razčlenjevalnik.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    argument_ARRAY = razčlenjevalnik.parse_args()
    if argument_ARRAY.remote:
        argument_ARRAY.network=True
        argument_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; geslo_VALUE: python3 Orodja/oddaljen_Nastavitve.py show'.format(argument_ARRAY.network_host,argument_ARRAY.network_host),flush=True)
    if argument_ARRAY.pip and not argument_ARRAY.network: razčlenjevalnik.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argument_ARRAY.pip_port <= 65535: razčlenjevalnik.error('--pip-port 범위는 1~65535입니다.')
    if argument_ARRAY.forward and not argument_ARRAY.network: razčlenjevalnik.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as vir_VALUE:
        if argument_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            vir_VALUE.enter_context(꾸러미중계(argument_ARRAY.pip_port, argument_ARRAY.pip_cache, argument_ARRAY.pip_offline))
            print('sveženj 중계: 127.0.0.1:' + str(argument_ARRAY.pip_port), flush=True)
        Izvedi(argument_ARRAY)


def Izvedi(argument_ARRAY):
    if argument_ARRAY.desktop:
        if argument_ARRAY.vnc or argument_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from namizje_Pogled import izvajati_namizje
        raise SystemExit(izvajati_namizje(argument_ARRAY.port, mreža=argument_ARRAY.network, prenos_datotek_številka_vrat=argument_ARRAY.ftp_port, 전달규칙들=argument_ARRAY.forward, ločljivost_VALUE=argument_ARRAY.resolution, gost_naslov=argument_ARRAY.guest_ip, gostiti_naslov=argument_ARRAY.network_host))
    Možnosti = ['-display', argument_ARRAY.display, '-serial', 'mon:stdio']
    if argument_ARRAY.vnc:
        Možnosti += ['-vnc', argument_ARRAY.vnc]
    if argument_ARRAY.network:
        from most_3de4fe3a import most_3de4fe3a
        with most_3de4fe3a(argument_ARRAY.ftp_port, argument_ARRAY.forward, gost_naslov=argument_ARRAY.guest_ip, gostiti_naslov=argument_ARRAY.network_host) as most:
            stanje_VALUE = subprocess.call(Ukaz(argument_ARRAY.resolution) + Možnosti + most.전달인수())
            if most.NAPAKA: raise SystemExit('network bridge: ' + most.NAPAKA)
        raise SystemExit(stanje_VALUE)
    raise SystemExit(subprocess.call(Ukaz(argument_ARRAY.resolution) + Možnosti))


if __name__ == '__main__':
    Zaženi()
