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

Project_korzeń = Path(__file__).resolve().parents[1]
losowy_Files = []


def _난수정리():
    for ścieżka_2 in losowy_Files:
        try:
            os.unlink(ścieżka_2)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as nazwa_pliku:
        nazwa_pliku.write(b'JKRENRG1' + os.urandom(32))
        losowy_Files.append(nazwa_pliku.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(nazwa_pliku.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    host = Project_korzeń.parent / 'rpi4/build/host'
    moduł_ładujący = host / 'lib/ld-musl-x86_64.so.1'
    binarny = host / 'usr/bin/qemu-system-aarch64'
    if moduł_ładujący.is_file() and binarny.is_file():
        return [str(moduł_ładujący), '--library-path', str(host / 'usr/lib') + ':' + str(host / 'lib'),
                str(binarny), '-L', str(host / 'usr/share/qemu')]
    binarny = shutil.which('qemu-system-aarch64')
    if not binarny:
        raise SystemExit('raspi4b wsparcie_WARTOŚĆ QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binarny]


def 해상도읽기(tekst):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', tekst):
        raise argparse.ArgumentTypeError('rozdzielczość_WARTOŚĆ format_WARTOŚĆ: 1920x1080')
    너비, wysokość_WARTOŚĆ = map(int, tekst.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= wysokość_WARTOŚĆ <= 1080):
        raise argparse.ArgumentTypeError('wsparcie_WARTOŚĆ obcinać: 너비 640~1920, wysokość_WARTOŚĆ 480~1080')
    return 너비, wysokość_WARTOŚĆ


def polecenie(rozdzielczość_WARTOŚĆ=(640, 480)):
    Tło_WARTOŚĆ = 모의기계()
    지원목록 = subprocess.check_output(Tło_WARTOŚĆ + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, wysokość_WARTOŚĆ = 해상도읽기('{}x{}'.format(*rozdzielczość_WARTOŚĆ))
    return Tło_WARTOŚĆ + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(wysokość_WARTOŚĆ), '-kernel',
                   str(Project_korzeń / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Uruchom_2():
    parser = argparse.ArgumentParser(description='własny Java Pi4 jądro_WARTOŚĆ. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 wyjść_program.')
    parser.add_argument('--display', default='none', help='none 또는 gtk/sdl (host wsparcie_WARTOŚĆ 필요)')
    parser.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='rozruch_maszyny 화면 Rozmiar. 예: 1920x1080; wartość_domyślna 640x480')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC sprzęt_port 5902. Klucz_WARTOŚĆ 입력은 UART 터미널에서 합니다.')
    parser.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    parser.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC sprzęt_port')
    parser.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Połącz; --desktop과 함께 używać_WARTOŚĆ 가능; 게스트에서 ftpd start')
    parser.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    parser.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP kontrola_WARTOŚĆ sprzęt_port (데이터 50000..50007)')
    parser.add_argument('--guest-ip', default=None, help='QEMU NAT Dalej_WARTOŚĆ wartość_docelowa. 기본은 ip.conf의 IP; zmienić_WARTOŚĆ 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    parser.add_argument('--network-host', default='127.0.0.1', help='NAT odbierać_WARTOŚĆ Adres. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN Adres: zewnętrzny_WARTOŚĆ połączenie_e05f319b')
    parser.add_argument('--forward', action='append', default=[], help='--network dołączać_wpis Połącz: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    parser.add_argument('--pip', action='store_true', help='PyPI źródło_drzewo pakiet Przekazywanie_WARTOŚĆ Uruchom_2 (--network 필요, MicroPython 호환 소스만)')
    parser.add_argument('--pip-port', type=int, default=8027, help='pakiet 중계의 localhost TCP sprzęt_port')
    parser.add_argument('--pip-cache', type=Path, default=Project_korzeń/'build/pip-cache')
    parser.add_argument('--pip-offline', action='store_true', help='이미 받은 dystrybucja_WARTOŚĆ 파일만 제공')
    argument_TABLICA = parser.parse_args()
    if argument_TABLICA.remote:
        argument_TABLICA.network=True
        argument_TABLICA.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; hasło_WARTOŚĆ: python3 narzędzia/zdalny_Ustawienia.py show'.format(argument_TABLICA.network_host,argument_TABLICA.network_host),flush=True)
    if argument_TABLICA.pip and not argument_TABLICA.network: parser.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argument_TABLICA.pip_port <= 65535: parser.error('--pip-port 범위는 1~65535입니다.')
    if argument_TABLICA.forward and not argument_TABLICA.network: parser.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as zasób_WARTOŚĆ:
        if argument_TABLICA.pip:
            from pakiet_Przekazywanie import pakiet_Przekazywanie
            zasób_WARTOŚĆ.enter_context(pakiet_Przekazywanie(argument_TABLICA.pip_port, argument_TABLICA.pip_cache, argument_TABLICA.pip_offline))
            print('pakiet Przekazywanie_WARTOŚĆ: 127.0.0.1:' + str(argument_TABLICA.pip_port), flush=True)
        Uruchom(argument_TABLICA)


def Uruchom(argument_TABLICA):
    if argument_TABLICA.desktop:
        if argument_TABLICA.vnc or argument_TABLICA.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from Pulpit_Widok import przebieg_Pulpit
        raise SystemExit(przebieg_Pulpit(argument_TABLICA.port, sieć=argument_TABLICA.network, transfer_plików_numer_portu=argument_TABLICA.ftp_port, 전달규칙들=argument_TABLICA.forward, rozdzielczość_WARTOŚĆ=argument_TABLICA.resolution, gość_ADRES=argument_TABLICA.guest_ip, host_ADRES=argument_TABLICA.network_host))
    Opcje = ['-display', argument_TABLICA.display, '-serial', 'mon:stdio']
    if argument_TABLICA.vnc:
        Opcje += ['-vnc', argument_TABLICA.vnc]
    if argument_TABLICA.network:
        from mostek_3de4fe3a import mostek_3de4fe3a
        with mostek_3de4fe3a(argument_TABLICA.ftp_port, argument_TABLICA.forward, gość_ADRES=argument_TABLICA.guest_ip, host_ADRES=argument_TABLICA.network_host) as mostek:
            Stan_WARTOŚĆ = subprocess.call(polecenie(argument_TABLICA.resolution) + Opcje + mostek.전달인수())
            if mostek.błąd: raise SystemExit('network bridge: ' + mostek.błąd)
        raise SystemExit(Stan_WARTOŚĆ)
    raise SystemExit(subprocess.call(polecenie(argument_TABLICA.resolution) + Opcje))


if __name__ == '__main__':
    Uruchom_2()
