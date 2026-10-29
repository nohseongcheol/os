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

azione_radice = Path(__file__).resolve().parents[1]
casuale_File = []


def _난수정리():
    for percorso in casuale_File:
        try:
            os.unlink(percorso)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as file:
        file.write(b'JKRENRG1' + os.urandom(32))
        casuale_File.append(file.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(file.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    host = azione_radice.parent / 'rpi4/build/host'
    caricatore = host / 'lib/ld-musl-x86_64.so.1'
    base_2 = host / 'usr/bin/qemu-system-aarch64'
    if caricatore.is_file() and base_2.is_file():
        return [str(caricatore), '--library-path', str(host / 'usr/lib') + ':' + str(host / 'lib'),
                str(base_2), '-L', str(host / 'usr/share/qemu')]
    base_2 = shutil.which('qemu-system-aarch64')
    if not base_2:
        raise SystemExit('raspi4b Supporto_VALORE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [base_2]


def 해상도읽기(testo):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', testo):
        raise argparse.ArgumentTypeError('risoluzione_VALORE formato_VALORE: 1920x1080')
    너비, altezza_VALORE = map(int, testo.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= altezza_VALORE <= 1080):
        raise argparse.ArgumentTypeError('Supporto_VALORE ritagliare: 너비 640~1920, altezza_VALORE 480~1080')
    return 너비, altezza_VALORE


def comando(risoluzione_VALORE=(640, 480)):
    sfondo_VALORE = 모의기계()
    지원목록 = subprocess.check_output(sfondo_VALORE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, altezza_VALORE = 해상도읽기('{}x{}'.format(*risoluzione_VALORE))
    return sfondo_VALORE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(altezza_VALORE), '-kernel',
                   str(azione_radice / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def avvia():
    parser = argparse.ArgumentParser(description='nativo Java Pi4 kernel_VALORE. seriale_VALORE 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Esci_app.')
    parser.add_argument('--display', default='none', help='none 또는 gtk/sdl (host Supporto_VALORE 필요)')
    parser.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='avvio_macchina schermata Dimensione. 예: 1920x1080; valore_predefinito 640x480')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC hardware_porta 5902. tasto_VALORE 입력은 UART 터미널에서 합니다.')
    parser.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    parser.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC hardware_porta')
    parser.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Connetti; --desktop과 함께 usare_VALORE 가능; 게스트에서 ftpd start')
    parser.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    parser.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP controllo_VALORE hardware_porta (데이터 50000..50007)')
    parser.add_argument('--guest-ip', default=None, help='QEMU NAT Avanti_VALORE target. 기본은 ip.conf의 IP; cambiare_VALORE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    parser.add_argument('--network-host', default='127.0.0.1', help='NAT ricevere_VALORE e_mail. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN e_mail: esterno_VALORE connessione_e05f319b')
    parser.add_argument('--forward', action='append', default=[], help='--network Aggiunta_voce Connetti: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    parser.add_argument('--pip', action='store_true', help='PyPI fonte_albero aggregare Inoltro_VALORE avvia (--network 필요, MicroPython 호환 소스만)')
    parser.add_argument('--pip-port', type=int, default=8027, help='aggregare 중계의 localhost TCP hardware_porta')
    parser.add_argument('--pip-cache', type=Path, default=azione_radice/'build/pip-cache')
    parser.add_argument('--pip-offline', action='store_true', help='이미 받은 distribuzione_VALORE 파일만 제공')
    argomento_array = parser.parse_args()
    if argomento_array.remote:
        argomento_array.network=True
        argomento_array.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; password_VALORE: python3 strumenti/remoto_Impostazioni.py show'.format(argomento_array.network_host,argomento_array.network_host),flush=True)
    if argomento_array.pip and not argomento_array.network: parser.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argomento_array.pip_port <= 65535: parser.error('--pip-port 범위는 1~65535입니다.')
    if argomento_array.forward and not argomento_array.network: parser.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as risorsa_VALORE:
        if argomento_array.pip:
            from aggregare_Inoltro import aggregare_Inoltro
            risorsa_VALORE.enter_context(aggregare_Inoltro(argomento_array.pip_port, argomento_array.pip_cache, argomento_array.pip_offline))
            print('aggregare Inoltro_VALORE: 127.0.0.1:' + str(argomento_array.pip_port), flush=True)
        Esegui(argomento_array)


def Esegui(argomento_array):
    if argomento_array.desktop:
        if argomento_array.vnc or argomento_array.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from PC_Vista import eseguire_PC
        raise SystemExit(eseguire_PC(argomento_array.port, rete=argomento_array.network, trasferimento_di_file_numero_di_porta=argomento_array.ftp_port, 전달규칙들=argomento_array.forward, risoluzione_VALORE=argomento_array.resolution, guest_e_mail=argomento_array.guest_ip, ID_host=argomento_array.network_host))
    Opzioni = ['-display', argomento_array.display, '-serial', 'mon:stdio']
    if argomento_array.vnc:
        Opzioni += ['-vnc', argomento_array.vnc]
    if argomento_array.network:
        from bridge_3de4fe3a import bridge_3de4fe3a
        with bridge_3de4fe3a(argomento_array.ftp_port, argomento_array.forward, guest_e_mail=argomento_array.guest_ip, ID_host=argomento_array.network_host) as bridge:
            Stato_VALORE = subprocess.call(comando(argomento_array.resolution) + Opzioni + bridge.전달인수())
            if bridge.errore: raise SystemExit('network bridge: ' + bridge.errore)
        raise SystemExit(Stato_VALORE)
    raise SystemExit(subprocess.call(comando(argomento_array.resolution) + Opzioni))


if __name__ == '__main__':
    avvia()
