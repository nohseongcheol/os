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

teendő_gyök = Path(__file__).resolve().parents[1]
véletlenszerű_Files = []


def _난수정리():
    for ÚTVONAL in véletlenszerű_Files:
        try:
            os.unlink(ÚTVONAL)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Fájl:
        Fájl.write(b'JKRENRG1' + os.urandom(32))
        véletlenszerű_Files.append(Fájl.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Fájl.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    gazda = teendő_gyök.parent / 'rpi4/build/host'
    betöltő = gazda / 'lib/ld-musl-x86_64.so.1'
    bináris = gazda / 'usr/bin/qemu-system-aarch64'
    if betöltő.is_file() and bináris.is_file():
        return [str(betöltő), '--library-path', str(gazda / 'usr/lib') + ':' + str(gazda / 'lib'),
                str(bináris), '-L', str(gazda / 'usr/share/qemu')]
    bináris = shutil.which('qemu-system-aarch64')
    if not bináris:
        raise SystemExit('raspi4b támogat_ÉRTÉK QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [bináris]


def 해상도읽기(Szöveg):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Szöveg):
        raise argparse.ArgumentTypeError('felbontás_ÉRTÉK formáz_ÉRTÉK: 1920x1080')
    너비, 높이 = map(int, Szöveg.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('támogat_ÉRTÉK klip: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Parancs(felbontás_ÉRTÉK=(640, 480)):
    Háttér_ÉRTÉK = 모의기계()
    지원목록 = subprocess.check_output(Háttér_ÉRTÉK + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*felbontás_ÉRTÉK))
    return Háttér_ÉRTÉK + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(teendő_gyök / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Futtatás():
    elemző = argparse.ArgumentParser(description='saját Java Pi4 kernel_ÉRTÉK. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 kilép_app.')
    elemző.add_argument('--display', default='none', help='none 또는 gtk/sdl (gazda támogat_ÉRTÉK 필요)')
    elemző.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Méret. 예: 1920x1080; alapértelmezett_érték 640x480')
    elemző.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC hardver_port 5902. Kulcs_ÉRTÉK 입력은 UART 터미널에서 합니다.')
    elemző.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    elemző.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC hardver_port')
    elemző.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Kapcsolódás; --desktop과 함께 használ_ÉRTÉK 가능; 게스트에서 ftpd start')
    elemző.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    elemző.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP vezérlő_ÉRTÉK hardver_port (데이터 50000..50007)')
    elemző.add_argument('--guest-ip', default=None, help='QEMU NAT Előre_ÉRTÉK cél. 기본은 ip.conf의 IP; módosítás_ÉRTÉK 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    elemző.add_argument('--network-host', default='127.0.0.1', help='NAT fogad_ÉRTÉK CÍM. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN CÍM: külső_ÉRTÉK ismerős_e05f319b')
    elemző.add_argument('--forward', action='append', default=[], help='--network hozzáfűz_bejegyzés Kapcsolódás: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    elemző.add_argument('--pip', action='store_true', help='PyPI forrás_fa köteg 중계 Futtatás (--network 필요, MicroPython 호환 소스만)')
    elemző.add_argument('--pip-port', type=int, default=8027, help='köteg 중계의 localhost TCP hardver_port')
    elemző.add_argument('--pip-cache', type=Path, default=teendő_gyök/'build/pip-cache')
    elemző.add_argument('--pip-offline', action='store_true', help='이미 받은 elosztás_ÉRTÉK 파일만 제공')
    argumentum_TÖMB = elemző.parse_args()
    if argumentum_TÖMB.remote:
        argumentum_TÖMB.network=True
        argumentum_TÖMB.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; jelszó_ÉRTÉK: python3 Eszközök/távoli_Gépház.py show'.format(argumentum_TÖMB.network_host,argumentum_TÖMB.network_host),flush=True)
    if argumentum_TÖMB.pip and not argumentum_TÖMB.network: elemző.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argumentum_TÖMB.pip_port <= 65535: elemző.error('--pip-port 범위는 1~65535입니다.')
    if argumentum_TÖMB.forward and not argumentum_TÖMB.network: elemző.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as erőforrás_ÉRTÉK:
        if argumentum_TÖMB.pip:
            from 꾸러미중계 import 꾸러미중계
            erőforrás_ÉRTÉK.enter_context(꾸러미중계(argumentum_TÖMB.pip_port, argumentum_TÖMB.pip_cache, argumentum_TÖMB.pip_offline))
            print('köteg 중계: 127.0.0.1:' + str(argumentum_TÖMB.pip_port), flush=True)
        Végrehajtás(argumentum_TÖMB)


def Végrehajtás(argumentum_TÖMB):
    if argumentum_TÖMB.desktop:
        if argumentum_TÖMB.vnc or argumentum_TÖMB.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from Asztal_Nézet import futtat_Asztal
        raise SystemExit(futtat_Asztal(argumentum_TÖMB.port, hálózat=argumentum_TÖMB.network, fájlátvitel_portszám=argumentum_TÖMB.ftp_port, 전달규칙들=argumentum_TÖMB.forward, felbontás_ÉRTÉK=argumentum_TÖMB.resolution, vendég_CÍM=argumentum_TÖMB.guest_ip, gazda_CÍM=argumentum_TÖMB.network_host))
    Beállítások_7f769d16 = ['-display', argumentum_TÖMB.display, '-serial', 'mon:stdio']
    if argumentum_TÖMB.vnc:
        Beállítások_7f769d16 += ['-vnc', argumentum_TÖMB.vnc]
    if argumentum_TÖMB.network:
        from híd_3de4fe3a import híd_3de4fe3a
        with híd_3de4fe3a(argumentum_TÖMB.ftp_port, argumentum_TÖMB.forward, vendég_CÍM=argumentum_TÖMB.guest_ip, gazda_CÍM=argumentum_TÖMB.network_host) as híd:
            Állapot_ÉRTÉK = subprocess.call(Parancs(argumentum_TÖMB.resolution) + Beállítások_7f769d16 + híd.전달인수())
            if híd.HIBA: raise SystemExit('network bridge: ' + híd.HIBA)
        raise SystemExit(Állapot_ÉRTÉK)
    raise SystemExit(subprocess.call(Parancs(argumentum_TÖMB.resolution) + Beállítások_7f769d16))


if __name__ == '__main__':
    Futtatás()
