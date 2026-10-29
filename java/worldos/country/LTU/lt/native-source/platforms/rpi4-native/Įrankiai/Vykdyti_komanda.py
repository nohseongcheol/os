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

Project_šaknis = Path(__file__).resolve().parents[1]
atsitiktinis_Failai = []


def _난수정리():
    for KELIAS in atsitiktinis_Failai:
        try:
            os.unlink(KELIAS)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Failas:
        Failas.write(b'JKRENRG1' + os.urandom(32))
        atsitiktinis_Failai.append(Failas.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Failas.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    organizuoti = Project_šaknis.parent / 'rpi4/build/host'
    įkelties_programa = organizuoti / 'lib/ld-musl-x86_64.so.1'
    dvejetainis = organizuoti / 'usr/bin/qemu-system-aarch64'
    if įkelties_programa.is_file() and dvejetainis.is_file():
        return [str(įkelties_programa), '--library-path', str(organizuoti / 'usr/lib') + ':' + str(organizuoti / 'lib'),
                str(dvejetainis), '-L', str(organizuoti / 'usr/share/qemu')]
    dvejetainis = shutil.which('qemu-system-aarch64')
    if not dvejetainis:
        raise SystemExit('raspi4b pagalba_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [dvejetainis]


def 해상도읽기(Tekstas):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Tekstas):
        raise argparse.ArgumentTypeError('skiriamoji_geba_VALUE formatas_VALUE: 1920x1080')
    너비, 높이 = map(int, Tekstas.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('pagalba_VALUE klipas: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Komanda(skiriamoji_geba_VALUE=(640, 480)):
    Fonas_VALUE = 모의기계()
    지원목록 = subprocess.check_output(Fonas_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*skiriamoji_geba_VALUE))
    return Fonas_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(Project_šaknis / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Paleisti():
    analizatorius = argparse.ArgumentParser(description='savas Java Pi4 branduolys_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Baigti_programa_086bb533.')
    analizatorius.add_argument('--display', default='none', help='none 또는 gtk/sdl (organizuoti pagalba_VALUE 필요)')
    analizatorius.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Dydis. 예: 1920x1080; numatytoji_reikšmė 640x480')
    analizatorius.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC aparatūra_jungtis 5902. Raktas_VALUE 입력은 UART 터미널에서 합니다.')
    analizatorius.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    analizatorius.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC aparatūra_jungtis')
    analizatorius.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Prisijungti; --desktop과 함께 naudoti_VALUE 가능; 게스트에서 ftpd start')
    analizatorius.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    analizatorius.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP valdymas_VALUE aparatūra_jungtis (데이터 50000..50007)')
    analizatorius.add_argument('--guest-ip', default=None, help='QEMU NAT Pirmyn_VALUE tikslas. 기본은 ip.conf의 IP; keisti_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    analizatorius.add_argument('--network-host', default='127.0.0.1', help='NAT gauti_VALUE_cef4d8ab ADDRESS. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ADDRESS: išorinis_VALUE ryšys_e05f319b')
    analizatorius.add_argument('--forward', action='append', default=[], help='--network sujungti_įrašas Prisijungti: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    analizatorius.add_argument('--pip', action='store_true', help='PyPI šaltinis_medis paketas 중계 Paleisti (--network 필요, MicroPython 호환 소스만)')
    analizatorius.add_argument('--pip-port', type=int, default=8027, help='paketas 중계의 localhost TCP aparatūra_jungtis')
    analizatorius.add_argument('--pip-cache', type=Path, default=Project_šaknis/'build/pip-cache')
    analizatorius.add_argument('--pip-offline', action='store_true', help='이미 받은 paskirstymas_VALUE 파일만 제공')
    argumentas_ARRAY = analizatorius.parse_args()
    if argumentas_ARRAY.remote:
        argumentas_ARRAY.network=True
        argumentas_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; slaptažodis_VALUE: python3 Įrankiai/nuotolinis_Parametrai.py show'.format(argumentas_ARRAY.network_host,argumentas_ARRAY.network_host),flush=True)
    if argumentas_ARRAY.pip and not argumentas_ARRAY.network: analizatorius.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argumentas_ARRAY.pip_port <= 65535: analizatorius.error('--pip-port 범위는 1~65535입니다.')
    if argumentas_ARRAY.forward and not argumentas_ARRAY.network: analizatorius.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ištekliai_VALUE:
        if argumentas_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            ištekliai_VALUE.enter_context(꾸러미중계(argumentas_ARRAY.pip_port, argumentas_ARRAY.pip_cache, argumentas_ARRAY.pip_offline))
            print('paketas 중계: 127.0.0.1:' + str(argumentas_ARRAY.pip_port), flush=True)
        Vykdyti(argumentas_ARRAY)


def Vykdyti(argumentas_ARRAY):
    if argumentas_ARRAY.desktop:
        if argumentas_ARRAY.vnc or argumentas_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from darbalaukis_rodyti import vykdyti_darbalaukis
        raise SystemExit(vykdyti_darbalaukis(argumentas_ARRAY.port, tinklas=argumentas_ARRAY.network, failo_perdavimas_prievado_numeris=argumentas_ARRAY.ftp_port, 전달규칙들=argumentas_ARRAY.forward, skiriamoji_geba_VALUE=argumentas_ARRAY.resolution, svečias_ADDRESS=argumentas_ARRAY.guest_ip, organizuoti_ADDRESS=argumentas_ARRAY.network_host))
    Parinktys = ['-display', argumentas_ARRAY.display, '-serial', 'mon:stdio']
    if argumentas_ARRAY.vnc:
        Parinktys += ['-vnc', argumentas_ARRAY.vnc]
    if argumentas_ARRAY.network:
        from tiltas_3de4fe3a import tiltas_3de4fe3a
        with tiltas_3de4fe3a(argumentas_ARRAY.ftp_port, argumentas_ARRAY.forward, svečias_ADDRESS=argumentas_ARRAY.guest_ip, organizuoti_ADDRESS=argumentas_ARRAY.network_host) as tiltas:
            Būsena_VALUE = subprocess.call(Komanda(argumentas_ARRAY.resolution) + Parinktys + tiltas.전달인수())
            if tiltas.KLAIDA: raise SystemExit('network bridge: ' + tiltas.KLAIDA)
        raise SystemExit(Būsena_VALUE)
    raise SystemExit(subprocess.call(Komanda(argumentas_ARRAY.resolution) + Parinktys))


if __name__ == '__main__':
    Paleisti()
