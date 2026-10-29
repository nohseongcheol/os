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

akce_kořen = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for cesta_2 in _난수파일들:
        try:
            os.unlink(cesta_2)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as název_souboru:
        název_souboru.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(název_souboru.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(název_souboru.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    hostit = akce_kořen.parent / 'rpi4/build/host'
    zavaděč = hostit / 'lib/ld-musl-x86_64.so.1'
    binary = hostit / 'usr/bin/qemu-system-aarch64'
    if zavaděč.is_file() and binary.is_file():
        return [str(zavaděč), '--library-path', str(hostit / 'usr/lib') + ':' + str(hostit / 'lib'),
                str(binary), '-L', str(hostit / 'usr/share/qemu')]
    binary = shutil.which('qemu-system-aarch64')
    if not binary:
        raise SystemExit('raspi4b vzpěra_HODNOTA QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binary]


def 해상도읽기(text):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', text):
        raise argparse.ArgumentTypeError('řešení_HODNOTA formát_HODNOTA: 1920x1080')
    너비, výška_HODNOTA = map(int, text.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= výška_HODNOTA <= 1080):
        raise argparse.ArgumentTypeError('vzpěra_HODNOTA oříznout: 너비 640~1920, výška_HODNOTA 480~1080')
    return 너비, výška_HODNOTA


def příkaz(řešení_HODNOTA=(640, 480)):
    Pozadí_HODNOTA = 모의기계()
    지원목록 = subprocess.check_output(Pozadí_HODNOTA + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, výška_HODNOTA = 해상도읽기('{}x{}'.format(*řešení_HODNOTA))
    return Pozadí_HODNOTA + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(výška_HODNOTA), '-kernel',
                   str(akce_kořen / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Spustit_2():
    analyzátor = argparse.ArgumentParser(description='vlastní Java Pi4 jádro_HODNOTA. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Konec_program.')
    analyzátor.add_argument('--display', default='none', help='none 또는 gtk/sdl (hostit vzpěra_HODNOTA 필요)')
    analyzátor.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='spuštění_stroje 화면 Velikost. 예: 1920x1080; výchozí_hodnota 640x480')
    analyzátor.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC hardware_port 5902. Klíč_HODNOTA 입력은 UART 터미널에서 합니다.')
    analyzátor.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    analyzátor.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC hardware_port')
    analyzátor.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Připojit; --desktop과 함께 použít_HODNOTA 가능; 게스트에서 ftpd start')
    analyzátor.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    analyzátor.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP řízení_HODNOTA hardware_port (데이터 50000..50007)')
    analyzátor.add_argument('--guest-ip', default=None, help='QEMU NAT Vpřed_HODNOTA cílová_úroveň. 기본은 ip.conf의 IP; změnit_HODNOTA 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    analyzátor.add_argument('--network-host', default='127.0.0.1', help='NAT dostat_HODNOTA Adresa. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN Adresa: externí_HODNOTA kontakt_e05f319b')
    analyzátor.add_argument('--forward', action='append', default=[], help='--network Připojit_položka Připojit: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    analyzátor.add_argument('--pip', action='store_true', help='PyPI zdroj_strom sada Přenos_HODNOTA Spustit_2 (--network 필요, MicroPython 호환 소스만)')
    analyzátor.add_argument('--pip-port', type=int, default=8027, help='sada 중계의 localhost TCP hardware_port')
    analyzátor.add_argument('--pip-cache', type=Path, default=akce_kořen/'build/pip-cache')
    analyzátor.add_argument('--pip-offline', action='store_true', help='이미 받은 distribuce_HODNOTA 파일만 제공')
    argument_pole = analyzátor.parse_args()
    if argument_pole.remote:
        argument_pole.network=True
        argument_pole.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; heslo_HODNOTA: python3 nástroje/vzdálený_Nastavení.py show'.format(argument_pole.network_host,argument_pole.network_host),flush=True)
    if argument_pole.pip and not argument_pole.network: analyzátor.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argument_pole.pip_port <= 65535: analyzátor.error('--pip-port 범위는 1~65535입니다.')
    if argument_pole.forward and not argument_pole.network: analyzátor.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as zdroj_HODNOTA:
        if argument_pole.pip:
            from sada_Přenos import sada_Přenos
            zdroj_HODNOTA.enter_context(sada_Přenos(argument_pole.pip_port, argument_pole.pip_cache, argument_pole.pip_offline))
            print('sada Přenos_HODNOTA: 127.0.0.1:' + str(argument_pole.pip_port), flush=True)
        Spustit(argument_pole)


def Spustit(argument_pole):
    if argument_pole.desktop:
        if argument_pole.vnc or argument_pole.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from Plocha_pohled import spustit_Plocha
        raise SystemExit(spustit_Plocha(argument_pole.port, síť=argument_pole.network, přenos_souborů_číslo_portu=argument_pole.ftp_port, 전달규칙들=argument_pole.forward, řešení_HODNOTA=argument_pole.resolution, host_ODKAZ=argument_pole.guest_ip, hostit_ODKAZ=argument_pole.network_host))
    Možnosti = ['-display', argument_pole.display, '-serial', 'mon:stdio']
    if argument_pole.vnc:
        Možnosti += ['-vnc', argument_pole.vnc]
    if argument_pole.network:
        from most_3de4fe3a import most_3de4fe3a
        with most_3de4fe3a(argument_pole.ftp_port, argument_pole.forward, host_ODKAZ=argument_pole.guest_ip, hostit_ODKAZ=argument_pole.network_host) as most:
            Stav_HODNOTA = subprocess.call(příkaz(argument_pole.resolution) + Možnosti + most.전달인수())
            if most.chyba: raise SystemExit('network bridge: ' + most.chyba)
        raise SystemExit(Stav_HODNOTA)
    raise SystemExit(subprocess.call(příkaz(argument_pole.resolution) + Možnosti))


if __name__ == '__main__':
    Spustit_2()
