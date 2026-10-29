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

Project_rrënjë = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for POZICIONI in _난수파일들:
        try:
            os.unlink(POZICIONI)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Kartelë:
        Kartelë.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Kartelë.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Kartelë.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    pritës = Project_rrënjë.parent / 'rpi4/build/host'
    적재기 = pritës / 'lib/ld-musl-x86_64.so.1'
    binar = pritës / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and binar.is_file():
        return [str(적재기), '--library-path', str(pritës / 'usr/lib') + ':' + str(pritës / 'lib'),
                str(binar), '-L', str(pritës / 'usr/share/qemu')]
    binar = shutil.which('qemu-system-aarch64')
    if not binar:
        raise SystemExit('raspi4b Mbështetje_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binar]


def 해상도읽기(Teksti):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Teksti):
        raise argparse.ArgumentTypeError('rezolucion_VALUE format_VALUE: 1920x1080')
    너비, 높이 = map(int, Teksti.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Mbështetje_VALUE fragment: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Komanda(rezolucion_VALUE=(640, 480)):
    Sfond_VALUE = 모의기계()
    지원목록 = subprocess.check_output(Sfond_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*rezolucion_VALUE))
    return Sfond_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(Project_rrënjë / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Ekzekuto():
    analizues = argparse.ArgumentParser(description='자체 Java Pi4 bërthamë_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 dal_program.')
    analizues.add_argument('--display', default='none', help='none 또는 gtk/sdl (pritës Mbështetje_VALUE 필요)')
    analizues.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Madhësi. 예: 1920x1080; vlerë_e_parazgjedhur 640x480')
    analizues.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. tast_VALUE 입력은 UART 터미널에서 합니다.')
    analizues.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    analizues.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    analizues.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Lidhu; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    analizues.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    analizues.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP kontroll_VALUE 포트 (데이터 50000..50007)')
    analizues.add_argument('--guest-ip', default=None, help='QEMU NAT paso_VALUE objektiv. 기본은 ip.conf의 IP; ndryshoj_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    analizues.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 email. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN email: 외부 lidhje_e05f319b')
    analizues.add_argument('--forward', action='append', default=[], help='--network 추가 Lidhu: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    analizues.add_argument('--pip', action='store_true', help='PyPI burim_degëzim grupoj 중계 Ekzekuto (--network 필요, MicroPython 호환 소스만)')
    analizues.add_argument('--pip-port', type=int, default=8027, help='grupoj 중계의 localhost TCP 포트')
    analizues.add_argument('--pip-cache', type=Path, default=Project_rrënjë/'build/pip-cache')
    analizues.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    argument_ARRAY = analizues.parse_args()
    if argument_ARRAY.remote:
        argument_ARRAY.network=True
        argument_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; fjalëkalim_VALUE: python3 Mjete/në_largësi_cilësimet.py show'.format(argument_ARRAY.network_host,argument_ARRAY.network_host),flush=True)
    if argument_ARRAY.pip and not argument_ARRAY.network: analizues.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argument_ARRAY.pip_port <= 65535: analizues.error('--pip-port 범위는 1~65535입니다.')
    if argument_ARRAY.forward and not argument_ARRAY.network: analizues.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as burim_VALUE:
        if argument_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            burim_VALUE.enter_context(꾸러미중계(argument_ARRAY.pip_port, argument_ARRAY.pip_cache, argument_ARRAY.pip_offline))
            print('grupoj 중계: 127.0.0.1:' + str(argument_ARRAY.pip_port), flush=True)
        Kryej(argument_ARRAY)


def Kryej(argument_ARRAY):
    if argument_ARRAY.desktop:
        if argument_ARRAY.vnc or argument_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from desktop_Pamja import varg_desktop
        raise SystemExit(varg_desktop(argument_ARRAY.port, rrjet=argument_ARRAY.network, skedar_transferim_numri_i_portës=argument_ARRAY.ftp_port, 전달규칙들=argument_ARRAY.forward, rezolucion_VALUE=argument_ARRAY.resolution, i_ftuar_email=argument_ARRAY.guest_ip, pritës_email=argument_ARRAY.network_host))
    Opsione = ['-display', argument_ARRAY.display, '-serial', 'mon:stdio']
    if argument_ARRAY.vnc:
        Opsione += ['-vnc', argument_ARRAY.vnc]
    if argument_ARRAY.network:
        from rrjet_urë import rrjet_urë
        with rrjet_urë(argument_ARRAY.ftp_port, argument_ARRAY.forward, i_ftuar_email=argument_ARRAY.guest_ip, pritës_email=argument_ARRAY.network_host) as urë:
            status_VALUE = subprocess.call(Komanda(argument_ARRAY.resolution) + Opsione + urë.전달인수())
            if urë.GABIM: raise SystemExit('network bridge: ' + urë.GABIM)
        raise SystemExit(status_VALUE)
    raise SystemExit(subprocess.call(Komanda(argument_ARRAY.resolution) + Opsione))


if __name__ == '__main__':
    Ekzekuto()
