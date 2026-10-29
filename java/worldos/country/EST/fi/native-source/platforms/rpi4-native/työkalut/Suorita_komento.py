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

aloite_juuri = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for polku_2 in _난수파일들:
        try:
            os.unlink(polku_2)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as tiedoston_nimi:
        tiedoston_nimi.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(tiedoston_nimi.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(tiedoston_nimi.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    isäntä = aloite_juuri.parent / 'rpi4/build/host'
    latausohjelma = isäntä / 'lib/ld-musl-x86_64.so.1'
    binaarinen = isäntä / 'usr/bin/qemu-system-aarch64'
    if latausohjelma.is_file() and binaarinen.is_file():
        return [str(latausohjelma), '--library-path', str(isäntä / 'usr/lib') + ':' + str(isäntä / 'lib'),
                str(binaarinen), '-L', str(isäntä / 'usr/share/qemu')]
    binaarinen = shutil.which('qemu-system-aarch64')
    if not binaarinen:
        raise SystemExit('raspi4b Tuki_ARVO QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binaarinen]


def lukea_tarkkuus(teksti):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', teksti):
        raise argparse.ArgumentTypeError('tarkkuus_ARVO muoto_ARVO: 1920x1080')
    너비, 높이 = map(int, teksti.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Tuki_ARVO leikata: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def komento(tarkkuus_ARVO=(640, 480)):
    Tausta_ARVO = 모의기계()
    지원목록 = subprocess.check_output(Tausta_ARVO + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = lukea_tarkkuus('{}x{}'.format(*tarkkuus_ARVO))
    return Tausta_ARVO + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(aloite_juuri / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Suorita_2():
    jäsennin = argparse.ArgumentParser(description='oma Java Pi4 ydin_ARVO. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Lopeta_ohjelma.')
    jäsennin.add_argument('--display', default='none', help='none 또는 gtk/sdl (isäntä Tuki_ARVO 필요)')
    jäsennin.add_argument('--resolution', type=lukea_tarkkuus, default=(640, 480), help='koneen_käynnistys 화면 Koko. 예: 1920x1080; oletusarvo 640x480')
    jäsennin.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC laitteisto_portti 5902. Avain_ARVO 입력은 UART 터미널에서 합니다.')
    jäsennin.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    jäsennin.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC laitteisto_portti')
    jäsennin.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Yhdistä; --desktop과 함께 käyttö_ARVO 가능; 게스트에서 ftpd start')
    jäsennin.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    jäsennin.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP ohjain_ARVO laitteisto_portti (데이터 50000..50007)')
    jäsennin.add_argument('--guest-ip', default=None, help='QEMU NAT siirrä_ARVO_24592b8a tavoite. 기본은 ip.conf의 IP; muuttaa_ARVO 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    jäsennin.add_argument('--network-host', default='127.0.0.1', help='NAT saada_ARVO OSOITE. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN OSOITE: ulkoinen_ARVO yhteys_e05f319b')
    jäsennin.add_argument('--forward', action='append', default=[], help='--network liitä_merkintä Yhdistä: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    jäsennin.add_argument('--pip', action='store_true', help='PyPI lähde_puu nippu 중계 Suorita_2 (--network 필요, MicroPython 호환 소스만)')
    jäsennin.add_argument('--pip-port', type=int, default=8027, help='nippu 중계의 localhost TCP laitteisto_portti')
    jäsennin.add_argument('--pip-cache', type=Path, default=aloite_juuri/'build/pip-cache')
    jäsennin.add_argument('--pip-offline', action='store_true', help='이미 받은 jakelu_ARVO 파일만 제공')
    argumentti_MATRIISI = jäsennin.parse_args()
    if argumentti_MATRIISI.remote:
        argumentti_MATRIISI.network=True
        argumentti_MATRIISI.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; salasana_ARVO: python3 työkalut/etä_Asetukset.py show'.format(argumentti_MATRIISI.network_host,argumentti_MATRIISI.network_host),flush=True)
    if argumentti_MATRIISI.pip and not argumentti_MATRIISI.network: jäsennin.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argumentti_MATRIISI.pip_port <= 65535: jäsennin.error('--pip-port 범위는 1~65535입니다.')
    if argumentti_MATRIISI.forward and not argumentti_MATRIISI.network: jäsennin.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as resurssi_ARVO:
        if argumentti_MATRIISI.pip:
            from 꾸러미중계 import 꾸러미중계
            resurssi_ARVO.enter_context(꾸러미중계(argumentti_MATRIISI.pip_port, argumentti_MATRIISI.pip_cache, argumentti_MATRIISI.pip_offline))
            print('nippu 중계: 127.0.0.1:' + str(argumentti_MATRIISI.pip_port), flush=True)
        Suorita(argumentti_MATRIISI)


def Suorita(argumentti_MATRIISI):
    if argumentti_MATRIISI.desktop:
        if argumentti_MATRIISI.vnc or argumentti_MATRIISI.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from työpöytä_Näkymä import suorittaa_työpöytä
        raise SystemExit(suorittaa_työpöytä(argumentti_MATRIISI.port, verkko=argumentti_MATRIISI.network, tiedostonsiirto_portin_numero=argumentti_MATRIISI.ftp_port, 전달규칙들=argumentti_MATRIISI.forward, tarkkuus_ARVO=argumentti_MATRIISI.resolution, vieras_OSOITE=argumentti_MATRIISI.guest_ip, isäntä_OSOITE=argumentti_MATRIISI.network_host))
    Asetukset_7f769d16 = ['-display', argumentti_MATRIISI.display, '-serial', 'mon:stdio']
    if argumentti_MATRIISI.vnc:
        Asetukset_7f769d16 += ['-vnc', argumentti_MATRIISI.vnc]
    if argumentti_MATRIISI.network:
        from silta_3de4fe3a import silta_3de4fe3a
        with silta_3de4fe3a(argumentti_MATRIISI.ftp_port, argumentti_MATRIISI.forward, vieras_OSOITE=argumentti_MATRIISI.guest_ip, isäntä_OSOITE=argumentti_MATRIISI.network_host) as silta:
            Tila_ARVO = subprocess.call(komento(argumentti_MATRIISI.resolution) + Asetukset_7f769d16 + silta.전달인수())
            if silta.VIRHE: raise SystemExit('network bridge: ' + silta.VIRHE)
        raise SystemExit(Tila_ARVO)
    raise SystemExit(subprocess.call(komento(argumentti_MATRIISI.resolution) + Asetukset_7f769d16))


if __name__ == '__main__':
    Suorita_2()
