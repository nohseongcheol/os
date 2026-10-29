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

Project_sakne = Path(__file__).resolve().parents[1]
nejaušs_Faili = []


def _난수정리():
    for CEĻŠ in nejaušs_Faili:
        try:
            os.unlink(CEĻŠ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Fails:
        Fails.write(b'JKRENRG1' + os.urandom(32))
        nejaušs_Faili.append(Fails.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Fails.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    viesot = Project_sakne.parent / 'rpi4/build/host'
    ielādētājs = viesot / 'lib/ld-musl-x86_64.so.1'
    binary = viesot / 'usr/bin/qemu-system-aarch64'
    if ielādētājs.is_file() and binary.is_file():
        return [str(ielādētājs), '--library-path', str(viesot / 'usr/lib') + ':' + str(viesot / 'lib'),
                str(binary), '-L', str(viesot / 'usr/share/qemu')]
    binary = shutil.which('qemu-system-aarch64')
    if not binary:
        raise SystemExit('raspi4b Atbalsts_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binary]


def 해상도읽기(Teksts):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Teksts):
        raise argparse.ArgumentTypeError('izšķirtspēja_VALUE formāts_VALUE: 1920x1080')
    너비, 높이 = map(int, Teksts.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Atbalsts_VALUE klips: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Komanda(izšķirtspēja_VALUE=(640, 480)):
    Fons_VALUE = 모의기계()
    지원목록 = subprocess.check_output(Fons_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*izšķirtspēja_VALUE))
    return Fons_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(Project_sakne / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Palaist():
    parsētājs = argparse.ArgumentParser(description='savs Java Pi4 kodols_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Iziet_programma.')
    parsētājs.add_argument('--display', default='none', help='none 또는 gtk/sdl (viesot Atbalsts_VALUE 필요)')
    parsētājs.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Izmērs. 예: 1920x1080; noklusējuma_vērtība 640x480')
    parsētājs.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Atslēga_VALUE 입력은 UART 터미널에서 합니다.')
    parsētājs.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    parsētājs.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    parsētājs.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Savienoties; --desktop과 함께 lietot_VALUE 가능; 게스트에서 ftpd start')
    parsētājs.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    parsētājs.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP vadība_VALUE 포트 (데이터 50000..50007)')
    parsētājs.add_argument('--guest-ip', default=None, help='QEMU NAT pārsūtīt_VALUE mērķis. 기본은 ip.conf의 IP; mainīt_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    parsētājs.add_argument('--network-host', default='127.0.0.1', help='NAT saņemt_VALUE adrese. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN adrese: ārējs_VALUE paziņa_e05f319b')
    parsētājs.add_argument('--forward', action='append', default=[], help='--network Pievienot_ievade Savienoties: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    parsētājs.add_argument('--pip', action='store_true', help='PyPI avots_koks saistīt 중계 Palaist (--network 필요, MicroPython 호환 소스만)')
    parsētājs.add_argument('--pip-port', type=int, default=8027, help='saistīt 중계의 localhost TCP 포트')
    parsētājs.add_argument('--pip-cache', type=Path, default=Project_sakne/'build/pip-cache')
    parsētājs.add_argument('--pip-offline', action='store_true', help='이미 받은 sadale_VALUE 파일만 제공')
    arg_ARRAY = parsētājs.parse_args()
    if arg_ARRAY.remote:
        arg_ARRAY.network=True
        arg_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; parole_VALUE: python3 Rīki/attāls_Iestatījumi.py show'.format(arg_ARRAY.network_host,arg_ARRAY.network_host),flush=True)
    if arg_ARRAY.pip and not arg_ARRAY.network: parsētājs.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= arg_ARRAY.pip_port <= 65535: parsētājs.error('--pip-port 범위는 1~65535입니다.')
    if arg_ARRAY.forward and not arg_ARRAY.network: parsētājs.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as resurss_VALUE:
        if arg_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            resurss_VALUE.enter_context(꾸러미중계(arg_ARRAY.pip_port, arg_ARRAY.pip_cache, arg_ARRAY.pip_offline))
            print('saistīt 중계: 127.0.0.1:' + str(arg_ARRAY.pip_port), flush=True)
        Izpildīt(arg_ARRAY)


def Izpildīt(arg_ARRAY):
    if arg_ARRAY.desktop:
        if arg_ARRAY.vnc or arg_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from dators_Skats import virkne_dators
        raise SystemExit(virkne_dators(arg_ARRAY.port, tīkls=arg_ARRAY.network, faila_pārsūtīšana_porta_numurs=arg_ARRAY.ftp_port, 전달규칙들=arg_ARRAY.forward, izšķirtspēja_VALUE=arg_ARRAY.resolution, viesis_adrese=arg_ARRAY.guest_ip, viesot_adrese=arg_ARRAY.network_host))
    Opcijas = ['-display', arg_ARRAY.display, '-serial', 'mon:stdio']
    if arg_ARRAY.vnc:
        Opcijas += ['-vnc', arg_ARRAY.vnc]
    if arg_ARRAY.network:
        from tilts_3de4fe3a import tilts_3de4fe3a
        with tilts_3de4fe3a(arg_ARRAY.ftp_port, arg_ARRAY.forward, viesis_adrese=arg_ARRAY.guest_ip, viesot_adrese=arg_ARRAY.network_host) as tilts:
            Statuss_VALUE = subprocess.call(Komanda(arg_ARRAY.resolution) + Opcijas + tilts.전달인수())
            if tilts.Kļūda: raise SystemExit('network bridge: ' + tilts.Kļūda)
        raise SystemExit(Statuss_VALUE)
    raise SystemExit(subprocess.call(Komanda(arg_ARRAY.resolution) + Opcijas))


if __name__ == '__main__':
    Palaist()
