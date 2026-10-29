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

пројектовати_корен = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for ПУТАЊА in _난수파일들:
        try:
            os.unlink(ПУТАЊА)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Датотека:
        Датотека.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Датотека.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Датотека.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    хост = пројектовати_корен.parent / 'rpi4/build/host'
    적재기 = хост / 'lib/ld-musl-x86_64.so.1'
    бинарно = хост / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and бинарно.is_file():
        return [str(적재기), '--library-path', str(хост / 'usr/lib') + ':' + str(хост / 'lib'),
                str(бинарно), '-L', str(хост / 'usr/share/qemu')]
    бинарно = shutil.which('qemu-system-aarch64')
    if not бинарно:
        raise SystemExit('raspi4b Подршка_вриједност QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [бинарно]


def 해상도읽기(Текст):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Текст):
        raise argparse.ArgumentTypeError('резолуција_вриједност формат_вриједност: 1920x1080')
    너비, 높이 = map(int, Текст.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Подршка_вриједност клип: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Наредба(резолуција_вриједност=(640, 480)):
    постер_вриједност = 모의기계()
    지원목록 = subprocess.check_output(постер_вриједност + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*резолуција_вриједност))
    return постер_вриједност + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(пројектовати_корен / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Покрени():
    анализатор = argparse.ArgumentParser(description='자체 Java Pi4 језгро_вриједност. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Излаз_програм.')
    анализатор.add_argument('--display', default='none', help='none 또는 gtk/sdl (хост Подршка_вриједност 필요)')
    анализатор.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Величина. 예: 1920x1080; задана_вриједност 640x480')
    анализатор.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Кључ_вриједност 입력은 UART 터미널에서 합니다.')
    анализатор.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    анализатор.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    анализатор.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Повежи_се; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    анализатор.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    анализатор.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP контрола_вриједност 포트 (데이터 50000..50007)')
    анализатор.add_argument('--guest-ip', default=None, help='QEMU NAT Напред_вриједност циљ. 기본은 ip.conf의 IP; промијенити_вриједност 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    анализатор.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 адреса. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN адреса: екстерни_вриједност веза_e05f319b')
    анализатор.add_argument('--forward', action='append', default=[], help='--network додати_унос Повежи_се: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    анализатор.add_argument('--pip', action='store_true', help='PyPI извор_стабло пакет 중계 Покрени (--network 필요, MicroPython 호환 소스만)')
    анализатор.add_argument('--pip-port', type=int, default=8027, help='пакет 중계의 localhost TCP 포트')
    анализатор.add_argument('--pip-cache', type=Path, default=пројектовати_корен/'build/pip-cache')
    анализатор.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    аргумент_низ = анализатор.parse_args()
    if аргумент_низ.remote:
        аргумент_низ.network=True
        аргумент_низ.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; лозинка_вриједност: python3 Алатке/удаљен_Поставке.py show'.format(аргумент_низ.network_host,аргумент_низ.network_host),flush=True)
    if аргумент_низ.pip and not аргумент_низ.network: анализатор.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= аргумент_низ.pip_port <= 65535: анализатор.error('--pip-port 범위는 1~65535입니다.')
    if аргумент_низ.forward and not аргумент_низ.network: анализатор.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ресурс_вриједност:
        if аргумент_низ.pip:
            from 꾸러미중계 import 꾸러미중계
            ресурс_вриједност.enter_context(꾸러미중계(аргумент_низ.pip_port, аргумент_низ.pip_cache, аргумент_низ.pip_offline))
            print('пакет 중계: 127.0.0.1:' + str(аргумент_низ.pip_port), flush=True)
        Изврши(аргумент_низ)


def Изврши(аргумент_низ):
    if аргумент_низ.desktop:
        if аргумент_низ.vnc or аргумент_низ.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from десктоп_Приказ import низ_десктоп
        raise SystemExit(низ_десктоп(аргумент_низ.port, Мрежа=аргумент_низ.network, фајл_пренос_број_порта=аргумент_низ.ftp_port, 전달규칙들=аргумент_низ.forward, резолуција_вриједност=аргумент_низ.resolution, гост_адреса=аргумент_низ.guest_ip, хост_адреса=аргумент_низ.network_host))
    Опције = ['-display', аргумент_низ.display, '-serial', 'mon:stdio']
    if аргумент_низ.vnc:
        Опције += ['-vnc', аргумент_низ.vnc]
    if аргумент_низ.network:
        from Мрежа_мост import Мрежа_мост
        with Мрежа_мост(аргумент_низ.ftp_port, аргумент_низ.forward, гост_адреса=аргумент_низ.guest_ip, хост_адреса=аргумент_низ.network_host) as мост:
            стање_вриједност = subprocess.call(Наредба(аргумент_низ.resolution) + Опције + мост.전달인수())
            if мост.ГРЕШКА: raise SystemExit('network bridge: ' + мост.ГРЕШКА)
        raise SystemExit(стање_вриједност)
    raise SystemExit(subprocess.call(Наредба(аргумент_низ.resolution) + Опције))


if __name__ == '__main__':
    Покрени()
