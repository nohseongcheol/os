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

Project_erro = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for Bide_izena in _난수파일들:
        try:
            os.unlink(Bide_izena)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Fitxategia:
        Fitxategia.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Fitxategia.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Fitxategia.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    Ostalari = Project_erro.parent / 'rpi4/build/host'
    적재기 = Ostalari / 'lib/ld-musl-x86_64.so.1'
    bitar = Ostalari / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and bitar.is_file():
        return [str(적재기), '--library-path', str(Ostalari / 'usr/lib') + ':' + str(Ostalari / 'lib'),
                str(bitar), '-L', str(Ostalari / 'usr/share/qemu')]
    bitar = shutil.which('qemu-system-aarch64')
    if not bitar:
        raise SystemExit('raspi4b Laguntza_balio QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [bitar]


def 해상도읽기(Testua):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Testua):
        raise argparse.ArgumentTypeError('bereizmen_balio formatu_balio: 1920x1080')
    너비, 높이 = map(int, Testua.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Laguntza_balio klip: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Komandoa(bereizmen_balio=(640, 480)):
    horma_paper_balio = 모의기계()
    지원목록 = subprocess.check_output(horma_paper_balio + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*bereizmen_balio))
    return horma_paper_balio + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(Project_erro / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Exekutatu_2():
    analizatzaile = argparse.ArgumentParser(description='자체 Java Pi4 nukleo_balio. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 irten_aplik.')
    analizatzaile.add_argument('--display', default='none', help='none 또는 gtk/sdl (Ostalari Laguntza_balio 필요)')
    analizatzaile.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Tamaina. 예: 1920x1080; balio_lehenetsi 640x480')
    analizatzaile.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. gako_balio 입력은 UART 터미널에서 합니다.')
    analizatzaile.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    analizatzaile.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    analizatzaile.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Konektatu; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    analizatzaile.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    analizatzaile.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP kontrol_balio 포트 (데이터 50000..50007)')
    analizatzaile.add_argument('--guest-ip', default=None, help='QEMU NAT Aurrera_balio helburu_balio. 기본은 ip.conf의 IP; aldatu_balio 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    analizatzaile.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 helbide. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN helbide: 외부 konexio_e05f319b')
    analizatzaile.add_argument('--forward', action='append', default=[], help='--network Erantsi_sarrera Konektatu: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    analizatzaile.add_argument('--pip', action='store_true', help='PyPI iturburu_zuhaitz multzo 중계 Exekutatu_2 (--network 필요, MicroPython 호환 소스만)')
    analizatzaile.add_argument('--pip-port', type=int, default=8027, help='multzo 중계의 localhost TCP 포트')
    analizatzaile.add_argument('--pip-cache', type=Path, default=Project_erro/'build/pip-cache')
    analizatzaile.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    arg_matrize = analizatzaile.parse_args()
    if arg_matrize.remote:
        arg_matrize.network=True
        arg_matrize.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; pasahitz_balio: python3 Tresnak/urruneko_Ezarpenak.py show'.format(arg_matrize.network_host,arg_matrize.network_host),flush=True)
    if arg_matrize.pip and not arg_matrize.network: analizatzaile.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= arg_matrize.pip_port <= 65535: analizatzaile.error('--pip-port 범위는 1~65535입니다.')
    if arg_matrize.forward and not arg_matrize.network: analizatzaile.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as baliabide_balio:
        if arg_matrize.pip:
            from 꾸러미중계 import 꾸러미중계
            baliabide_balio.enter_context(꾸러미중계(arg_matrize.pip_port, arg_matrize.pip_cache, arg_matrize.pip_offline))
            print('multzo 중계: 127.0.0.1:' + str(arg_matrize.pip_port), flush=True)
        Exekutatu(arg_matrize)


def Exekutatu(arg_matrize):
    if arg_matrize.desktop:
        if arg_matrize.vnc or arg_matrize.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from mahaigain_ikusi import exekutatu_mahaigain
        raise SystemExit(exekutatu_mahaigain(arg_matrize.port, sare=arg_matrize.network, fitxategi_transferitu_ataka_zenbaki=arg_matrize.ftp_port, 전달규칙들=arg_matrize.forward, bereizmen_balio=arg_matrize.resolution, gonbidatu_helbide=arg_matrize.guest_ip, Ostalari_helbide=arg_matrize.network_host))
    aukerak = ['-display', arg_matrize.display, '-serial', 'mon:stdio']
    if arg_matrize.vnc:
        aukerak += ['-vnc', arg_matrize.vnc]
    if arg_matrize.network:
        from sare_zubi import sare_zubi
        with sare_zubi(arg_matrize.ftp_port, arg_matrize.forward, gonbidatu_helbide=arg_matrize.guest_ip, Ostalari_helbide=arg_matrize.network_host) as zubi:
            Egoera_balio = subprocess.call(Komandoa(arg_matrize.resolution) + aukerak + zubi.전달인수())
            if zubi.errorea: raise SystemExit('network bridge: ' + zubi.errorea)
        raise SystemExit(Egoera_balio)
    raise SystemExit(subprocess.call(Komandoa(arg_matrize.resolution) + aukerak))


if __name__ == '__main__':
    Exekutatu_2()
