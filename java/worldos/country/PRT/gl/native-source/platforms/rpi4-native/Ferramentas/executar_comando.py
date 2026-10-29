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

Project_raíz = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for CAMIÑO in _난수파일들:
        try:
            os.unlink(CAMIÑO)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Ficheiro:
        Ficheiro.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Ficheiro.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Ficheiro.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    hospedar = Project_raíz.parent / 'rpi4/build/host'
    적재기 = hospedar / 'lib/ld-musl-x86_64.so.1'
    binario = hospedar / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and binario.is_file():
        return [str(적재기), '--library-path', str(hospedar / 'usr/lib') + ':' + str(hospedar / 'lib'),
                str(binario), '-L', str(hospedar / 'usr/share/qemu')]
    binario = shutil.which('qemu-system-aarch64')
    if not binario:
        raise SystemExit('raspi4b soporte_VALOR QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binario]


def 해상도읽기(Texto):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Texto):
        raise argparse.ArgumentTypeError('resolución_VALOR formato_VALOR: 1920x1080')
    너비, 높이 = map(int, Texto.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('soporte_VALOR clip: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Orde(resolución_VALOR=(640, 480)):
    Fondo_VALOR = 모의기계()
    지원목록 = subprocess.check_output(Fondo_VALOR + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*resolución_VALOR))
    return Fondo_VALOR + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(Project_raíz / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Executar_2():
    analizador = argparse.ArgumentParser(description='자체 Java Pi4 kernel_VALOR. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 saír_apl.')
    analizador.add_argument('--display', default='none', help='none 또는 gtk/sdl (hospedar soporte_VALOR 필요)')
    analizador.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Tamaño. 예: 1920x1080; valor_predefinido 640x480')
    analizador.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Chave_VALOR 입력은 UART 터미널에서 합니다.')
    analizador.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    analizador.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    analizador.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Conectar; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    analizador.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    analizador.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP control_VALOR 포트 (데이터 50000..50007)')
    analizador.add_argument('--guest-ip', default=None, help='QEMU NAT Adiante_VALOR obxectivo_VALOR. 기본은 ip.conf의 IP; modificar_VALOR 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    analizador.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ENDEREZO. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ENDEREZO: externo_VALOR conexión_e05f319b')
    analizador.add_argument('--forward', action='append', default=[], help='--network Anexar_introdución Conectar: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    analizador.add_argument('--pip', action='store_true', help='PyPI fonte_árbore paquete 중계 Executar_2 (--network 필요, MicroPython 호환 소스만)')
    analizador.add_argument('--pip-port', type=int, default=8027, help='paquete 중계의 localhost TCP 포트')
    analizador.add_argument('--pip-cache', type=Path, default=Project_raíz/'build/pip-cache')
    analizador.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    argumento_MATRIZ = analizador.parse_args()
    if argumento_MATRIZ.remote:
        argumento_MATRIZ.network=True
        argumento_MATRIZ.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; contrasinal_VALOR: python3 Ferramentas/remoto_Configuración.py show'.format(argumento_MATRIZ.network_host,argumento_MATRIZ.network_host),flush=True)
    if argumento_MATRIZ.pip and not argumento_MATRIZ.network: analizador.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argumento_MATRIZ.pip_port <= 65535: analizador.error('--pip-port 범위는 1~65535입니다.')
    if argumento_MATRIZ.forward and not argumento_MATRIZ.network: analizador.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as Recurso_VALOR:
        if argumento_MATRIZ.pip:
            from 꾸러미중계 import 꾸러미중계
            Recurso_VALOR.enter_context(꾸러미중계(argumento_MATRIZ.pip_port, argumento_MATRIZ.pip_cache, argumento_MATRIZ.pip_offline))
            print('paquete 중계: 127.0.0.1:' + str(argumento_MATRIZ.pip_port), flush=True)
        Executar(argumento_MATRIZ)


def Executar(argumento_MATRIZ):
    if argumento_MATRIZ.desktop:
        if argumento_MATRIZ.vnc or argumento_MATRIZ.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from escritorio_ver import executar_escritorio
        raise SystemExit(executar_escritorio(argumento_MATRIZ.port, Rede=argumento_MATRIZ.network, transferencia_de_ficheiros_número_do_porto=argumento_MATRIZ.ftp_port, 전달규칙들=argumento_MATRIZ.forward, resolución_VALOR=argumento_MATRIZ.resolution, convidado_ENDEREZO=argumento_MATRIZ.guest_ip, hospedar_ENDEREZO=argumento_MATRIZ.network_host))
    Opcións = ['-display', argumento_MATRIZ.display, '-serial', 'mon:stdio']
    if argumento_MATRIZ.vnc:
        Opcións += ['-vnc', argumento_MATRIZ.vnc]
    if argumento_MATRIZ.network:
        from Rede_ponte import Rede_ponte
        with Rede_ponte(argumento_MATRIZ.ftp_port, argumento_MATRIZ.forward, convidado_ENDEREZO=argumento_MATRIZ.guest_ip, hospedar_ENDEREZO=argumento_MATRIZ.network_host) as ponte:
            Estado_VALOR = subprocess.call(Orde(argumento_MATRIZ.resolution) + Opcións + ponte.전달인수())
            if ponte.ERRO: raise SystemExit('network bridge: ' + ponte.ERRO)
        raise SystemExit(Estado_VALOR)
    raise SystemExit(subprocess.call(Orde(argumento_MATRIZ.resolution) + Opcións))


if __name__ == '__main__':
    Executar_2()
