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

raízProyecto = Path(__file__).resolve().parents[1]
ArchivosAleatorio = []


def AleatorioLimpieza():
    for ruta in ArchivosAleatorio:
        try:
            os.unlink(ruta)
        except FileNotFoundError:
            pass


atexit.register(AleatorioLimpieza)


def argumentosAleatorioRemoto():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Archivo:
        Archivo.write(b'JKRENRG1' + os.urandom(32))
        ArchivosAleatorio.append(Archivo.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Archivo.name)]


def MáquinaDoblePrueba():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    Anfitrión = raízProyecto.parent / 'rpi4/build/host'
    cargador = Anfitrión / 'lib/ld-musl-x86_64.so.1'
    binario = Anfitrión / 'usr/bin/qemu-system-aarch64'
    if cargador.is_file() and binario.is_file():
        return [str(cargador), '--library-path', str(Anfitrión / 'usr/lib') + ':' + str(Anfitrión / 'lib'),
                str(binario), '-L', str(Anfitrión / 'usr/share/qemu')]
    binario = shutil.which('qemu-system-aarch64')
    if not binario:
        raise SystemExit('raspi4b valorSoporte QEMU valorNecesario. QEMU_AARCH64로 경로를 지정하세요.')
    return [binario]


def leerResolución(texto):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', texto):
        raise argparse.ArgumentTypeError('valorResolución valorFormato: 1920x1080')
    valorAnchura, valorAltura = map(int, texto.split('x'))
    if not (640 <= valorAnchura <= 1920 and 480 <= valorAltura <= 1080):
        raise argparse.ArgumentTypeError('valorSoporte recortar: valorAnchura 640~1920, valorAltura 480~1080')
    return valorAnchura, valorAltura


def comando(valorResolución=(640, 480)):
    valorFondo = MáquinaDoblePrueba()
    funcionalidadesAdmitido = subprocess.check_output(valorFondo + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in funcionalidadesAdmitido:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. valorÚltimoReciente QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    valorAnchura, valorAltura = leerResolución('{}x{}'.format(*valorResolución))
    return valorFondo + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(valorAnchura),
                   '-global', 'bcm2835-fb.yres=' + str(valorAltura), '-kernel',
                   str(raízProyecto / 'build/kernel8.img'), '-no-reboot'] + argumentosAleatorioRemoto()


def ponerEnMarcha():
    analizador = argparse.ArgumentParser(description='propio Java Pi4 valorNúcleo. valorSerie 셸은 Ctrl+A X, --desktop은 Ctrl+C로 programaSalir.')
    analizador.add_argument('--display', default='none', help='none 또는 gtk/sdl (Anfitrión valorSoporte valorNecesario)')
    analizador.add_argument('--resolution', type=leerResolución, default=(640, 480), help='Arranque Pantalla tamaño. 예: 1920x1080; valorPredeterminado 640x480')
    analizador.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC puertoEquipoFísico 5902. valorTecla 입력은 UART 터미널에서 합니다.')
    analizador.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    analizador.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC puertoEquipoFísico')
    analizador.add_argument('--network', action='store_true', help='valorAuxiliar UART SLIP와 QEMU NAT를 conectar; --desktop과 함께 valorUsar 가능; 게스트에서 ftpd start')
    analizador.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    analizador.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP valorControl puertoEquipoFísico (데이터 50000..50007)')
    analizador.add_argument('--guest-ip', default=None, help='QEMU NAT valorAdelante valorObjetivo. 기본은 ip.conf의 IP; cambiarValor 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    analizador.add_argument('--network-host', default='127.0.0.1', help='NAT recibirValor dirección. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN dirección: valorExterno conexión')
    analizador.add_argument('--forward', action='append', default=[], help='--network añadirFinalEntradaElemento conectar: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    analizador.add_argument('--pip', action='store_true', help='PyPI árbolFuente Paquete retransmitirValor ponerEnMarcha (--network valorNecesario, MicroPython 호환 소스만)')
    analizador.add_argument('--pip-port', type=int, default=8027, help='Paquete 중계의 localhost TCP puertoEquipoFísico')
    analizador.add_argument('--pip-cache', type=Path, default=raízProyecto/'build/pip-cache')
    analizador.add_argument('--pip-offline', action='store_true', help='이미 받은 valorDistribución 파일만 제공')
    arregloArgumento = analizador.parse_args()
    if arregloArgumento.remote:
        arregloArgumento.network=True
        arregloArgumento.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; valorContraseña: python3 Herramientas/ajustesRemoto.py show'.format(arregloArgumento.network_host,arregloArgumento.network_host),flush=True)
    if arregloArgumento.pip and not arregloArgumento.network: analizador.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= arregloArgumento.pip_port <= 65535: analizador.error('--pip-port 범위는 1~65535입니다.')
    if arregloArgumento.forward and not arregloArgumento.network: analizador.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as valorRecurso:
        if arregloArgumento.pip:
            from retransmitirPaquete import retransmitirPaquete
            valorRecurso.enter_context(retransmitirPaquete(arregloArgumento.pip_port, arregloArgumento.pip_cache, arregloArgumento.pip_offline))
            print('Paquete retransmitirValor: 127.0.0.1:' + str(arregloArgumento.pip_port), flush=True)
        ejecutarTarea(arregloArgumento)


def ejecutarTarea(arregloArgumento):
    if arregloArgumento.desktop:
        if arregloArgumento.vnc or arregloArgumento.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from vistaEscritorio import ponerEnMarchaEscritorio
        raise SystemExit(ponerEnMarchaEscritorio(arregloArgumento.port, red=arregloArgumento.network, númeroPuertoTransferenciaArchivo=arregloArgumento.ftp_port, reglasReenvíoEnCurso=arregloArgumento.forward, valorResolución=arregloArgumento.resolution, direcciónInvitado=arregloArgumento.guest_ip, direcciónAnfitrión=arregloArgumento.network_host))
    opciones = ['-display', arregloArgumento.display, '-serial', 'mon:stdio']
    if arregloArgumento.vnc:
        opciones += ['-vnc', arregloArgumento.vnc]
    if arregloArgumento.network:
        from puenteRed import puenteRed
        with puenteRed(arregloArgumento.ftp_port, arregloArgumento.forward, direcciónInvitado=arregloArgumento.guest_ip, direcciónAnfitrión=arregloArgumento.network_host) as puente:
            valorEstadoValor = subprocess.call(comando(arregloArgumento.resolution) + opciones + puente.argumentoReenviado())
            if puente.error: raise SystemExit('network bridge: ' + puente.error)
        raise SystemExit(valorEstadoValor)
    raise SystemExit(subprocess.call(comando(arregloArgumento.resolution) + opciones))


if __name__ == '__main__':
    ponerEnMarcha()
