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

Project_rel = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for Camí in _난수파일들:
        try:
            os.unlink(Camí)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Fitxer:
        Fitxer.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Fitxer.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Fitxer.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    allotjar = Project_rel.parent / 'rpi4/build/host'
    적재기 = allotjar / 'lib/ld-musl-x86_64.so.1'
    binari = allotjar / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and binari.is_file():
        return [str(적재기), '--library-path', str(allotjar / 'usr/lib') + ':' + str(allotjar / 'lib'),
                str(binari), '-L', str(allotjar / 'usr/share/qemu')]
    binari = shutil.which('qemu-system-aarch64')
    if not binari:
        raise SystemExit('raspi4b suport_VALOR QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binari]


def tancar_resolució(SMS):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', SMS):
        raise argparse.ArgumentTypeError('resolució_VALOR format_VALOR: 1920x1080')
    너비, 높이 = map(int, SMS.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('suport_VALOR clip: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Ordre(resolució_VALOR=(640, 480)):
    Fons_VALOR = 모의기계()
    지원목록 = subprocess.check_output(Fons_VALOR + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = tancar_resolució('{}x{}'.format(*resolució_VALOR))
    return Fons_VALOR + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(Project_rel / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Executa_2():
    analitzador = argparse.ArgumentParser(description='propi Java Pi4 nucli_VALOR. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Surt_programa.')
    analitzador.add_argument('--display', default='none', help='none 또는 gtk/sdl (allotjar suport_VALOR 필요)')
    analitzador.add_argument('--resolution', type=tancar_resolució, default=(640, 480), help='부팅 화면 Mida. 예: 1920x1080; valor_per_defecte 640x480')
    analitzador.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Clau_VALOR 입력은 UART 터미널에서 합니다.')
    analitzador.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    analitzador.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    analitzador.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Connecta; --desktop과 함께 ús_VALOR 가능; 게스트에서 ftpd start')
    analitzador.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    analitzador.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP control_VALOR 포트 (데이터 50000..50007)')
    analitzador.add_argument('--guest-ip', default=None, help='QEMU NAT desviar_VALOR objectiu. 기본은 ip.conf의 IP; canviar_VALOR 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    analitzador.add_argument('--network-host', default='127.0.0.1', help='NAT rebre_VALOR Adreça. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN Adreça: extern_VALOR connexió_e05f319b')
    analitzador.add_argument('--forward', action='append', default=[], help='--network Annexa_introducció Connecta: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    analitzador.add_argument('--pip', action='store_true', help='PyPI font_arbre paquet 중계 Executa_2 (--network 필요, MicroPython 호환 소스만)')
    analitzador.add_argument('--pip-port', type=int, default=8027, help='paquet 중계의 localhost TCP 포트')
    analitzador.add_argument('--pip-cache', type=Path, default=Project_rel/'build/pip-cache')
    analitzador.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    arg_MATRIU = analitzador.parse_args()
    if arg_MATRIU.remote:
        arg_MATRIU.network=True
        arg_MATRIU.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; contrasenya_VALOR: python3 Eines/remot_Configuració.py show'.format(arg_MATRIU.network_host,arg_MATRIU.network_host),flush=True)
    if arg_MATRIU.pip and not arg_MATRIU.network: analitzador.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= arg_MATRIU.pip_port <= 65535: analitzador.error('--pip-port 범위는 1~65535입니다.')
    if arg_MATRIU.forward and not arg_MATRIU.network: analitzador.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as recurs_VALOR:
        if arg_MATRIU.pip:
            from 꾸러미중계 import 꾸러미중계
            recurs_VALOR.enter_context(꾸러미중계(arg_MATRIU.pip_port, arg_MATRIU.pip_cache, arg_MATRIU.pip_offline))
            print('paquet 중계: 127.0.0.1:' + str(arg_MATRIU.pip_port), flush=True)
        Executa(arg_MATRIU)


def Executa(arg_MATRIU):
    if arg_MATRIU.desktop:
        if arg_MATRIU.vnc or arg_MATRIU.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from escriptori_visualitzar import execució_escriptori
        raise SystemExit(execució_escriptori(arg_MATRIU.port, xarxa=arg_MATRIU.network, transferència_de_fitxers_número_de_port=arg_MATRIU.ftp_port, 전달규칙들=arg_MATRIU.forward, resolució_VALOR=arg_MATRIU.resolution, convidat_ADREÇA=arg_MATRIU.guest_ip, allotjar_ADREÇA=arg_MATRIU.network_host))
    Opcions = ['-display', arg_MATRIU.display, '-serial', 'mon:stdio']
    if arg_MATRIU.vnc:
        Opcions += ['-vnc', arg_MATRIU.vnc]
    if arg_MATRIU.network:
        from xarxa_pont import xarxa_pont
        with xarxa_pont(arg_MATRIU.ftp_port, arg_MATRIU.forward, convidat_ADREÇA=arg_MATRIU.guest_ip, allotjar_ADREÇA=arg_MATRIU.network_host) as pont:
            Estat_VALOR = subprocess.call(Ordre(arg_MATRIU.resolution) + Opcions + pont.전달인수())
            if pont.s_ha_produït_un_error: raise SystemExit('network bridge: ' + pont.s_ha_produït_un_error)
        raise SystemExit(Estat_VALOR)
    raise SystemExit(subprocess.call(Ordre(arg_MATRIU.resolution) + Opcions))


if __name__ == '__main__':
    Executa_2()
