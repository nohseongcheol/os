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

ação_raiz = Path(__file__).resolve().parents[1]
aleatório_Arquivos = []


def _난수정리():
    for caminho in aleatório_Arquivos:
        try:
            os.unlink(caminho)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ficheiro:
        ficheiro.write(b'JKRENRG1' + os.urandom(32))
        aleatório_Arquivos.append(ficheiro.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ficheiro.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    host = ação_raiz.parent / 'rpi4/build/host'
    carregador = host / 'lib/ld-musl-x86_64.so.1'
    base_2 = host / 'usr/bin/qemu-system-aarch64'
    if carregador.is_file() and base_2.is_file():
        return [str(carregador), '--library-path', str(host / 'usr/lib') + ':' + str(host / 'lib'),
                str(base_2), '-L', str(host / 'usr/share/qemu')]
    base_2 = shutil.which('qemu-system-aarch64')
    if not base_2:
        raise SystemExit('raspi4b Suporte_VALOR QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [base_2]


def leitura_resolução(texto):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', texto):
        raise argparse.ArgumentTypeError('resolução_VALOR formato_VALOR: 1920x1080')
    너비, altura_VALOR = map(int, texto.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= altura_VALOR <= 1080):
        raise argparse.ArgumentTypeError('Suporte_VALOR recortar: 너비 640~1920, altura_VALOR 480~1080')
    return 너비, altura_VALOR


def comando(resolução_VALOR=(640, 480)):
    Tela_de_fundo_VALOR = 모의기계()
    지원목록 = subprocess.check_output(Tela_de_fundo_VALOR + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, altura_VALOR = leitura_resolução('{}x{}'.format(*resolução_VALOR))
    return Tela_de_fundo_VALOR + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(altura_VALOR), '-kernel',
                   str(ação_raiz / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def iniciar():
    analisador = argparse.ArgumentParser(description='nativo Java Pi4 kernel_VALOR. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 sair_app.')
    analisador.add_argument('--display', default='none', help='none 또는 gtk/sdl (host Suporte_VALOR 필요)')
    analisador.add_argument('--resolution', type=leitura_resolução, default=(640, 480), help='arranque_da_máquina tela Tamanho. 예: 1920x1080; valor_padrão 640x480')
    analisador.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC hardware_porta 5902. Chave_VALOR 입력은 UART 터미널에서 합니다.')
    analisador.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    analisador.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC hardware_porta')
    analisador.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Ligar; --desktop과 함께 uso_VALOR 가능; 게스트에서 ftpd start')
    analisador.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    analisador.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP visual_VALOR hardware_porta (데이터 50000..50007)')
    analisador.add_argument('--guest-ip', default=None, help='QEMU NAT Avançar_VALOR meta. 기본은 ip.conf의 IP; alterar_VALOR 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    analisador.add_argument('--network-host', default='127.0.0.1', help='NAT receber_VALOR Endereço. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN Endereço: externo_VALOR conexão_e05f319b')
    analisador.add_argument('--forward', action='append', default=[], help='--network Acrescentar_entrada Ligar: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    analisador.add_argument('--pip', action='store_true', help='PyPI fonte_árvore grupo relé_VALOR iniciar (--network 필요, MicroPython 호환 소스만)')
    analisador.add_argument('--pip-port', type=int, default=8027, help='grupo 중계의 localhost TCP hardware_porta')
    analisador.add_argument('--pip-cache', type=Path, default=ação_raiz/'build/pip-cache')
    analisador.add_argument('--pip-offline', action='store_true', help='이미 받은 distribuição_VALOR 파일만 제공')
    argumento_MATRIZ = analisador.parse_args()
    if argumento_MATRIZ.remote:
        argumento_MATRIZ.network=True
        argumento_MATRIZ.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; senha_VALOR: python3 ferramentas/remoto_Configurações.py show'.format(argumento_MATRIZ.network_host,argumento_MATRIZ.network_host),flush=True)
    if argumento_MATRIZ.pip and not argumento_MATRIZ.network: analisador.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argumento_MATRIZ.pip_port <= 65535: analisador.error('--pip-port 범위는 1~65535입니다.')
    if argumento_MATRIZ.forward and not argumento_MATRIZ.network: analisador.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as recurso_VALOR:
        if argumento_MATRIZ.pip:
            from grupo_relé import grupo_relé
            recurso_VALOR.enter_context(grupo_relé(argumento_MATRIZ.pip_port, argumento_MATRIZ.pip_cache, argumento_MATRIZ.pip_offline))
            print('grupo relé_VALOR: 127.0.0.1:' + str(argumento_MATRIZ.pip_port), flush=True)
        Executar(argumento_MATRIZ)


def Executar(argumento_MATRIZ):
    if argumento_MATRIZ.desktop:
        if argumento_MATRIZ.vnc or argumento_MATRIZ.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from desktop_Exibir import executar_desktop
        raise SystemExit(executar_desktop(argumento_MATRIZ.port, rede=argumento_MATRIZ.network, transferência_de_arquivo_número_da_porta=argumento_MATRIZ.ftp_port, 전달규칙들=argumento_MATRIZ.forward, resolução_VALOR=argumento_MATRIZ.resolution, convidado_email=argumento_MATRIZ.guest_ip, ID_do_host=argumento_MATRIZ.network_host))
    Opções = ['-display', argumento_MATRIZ.display, '-serial', 'mon:stdio']
    if argumento_MATRIZ.vnc:
        Opções += ['-vnc', argumento_MATRIZ.vnc]
    if argumento_MATRIZ.network:
        from ponte_3de4fe3a import ponte_3de4fe3a
        with ponte_3de4fe3a(argumento_MATRIZ.ftp_port, argumento_MATRIZ.forward, convidado_email=argumento_MATRIZ.guest_ip, ID_do_host=argumento_MATRIZ.network_host) as ponte:
            Estado_VALOR = subprocess.call(comando(argumento_MATRIZ.resolution) + Opções + ponte.전달인수())
            if ponte.erro: raise SystemExit('network bridge: ' + ponte.erro)
        raise SystemExit(Estado_VALOR)
    raise SystemExit(subprocess.call(comando(argumento_MATRIZ.resolution) + Opções))


if __name__ == '__main__':
    iniciar()
