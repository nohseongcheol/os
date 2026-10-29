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

기준 = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for ШЛЯХ in _난수파일들:
        try:
            os.unlink(ШЛЯХ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Файл:
        Файл.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Файл.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Файл.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    вузел = 기준.parent / 'rpi4/build/host'
    적재기 = вузел / 'lib/ld-musl-x86_64.so.1'
    дваічны = вузел / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and дваічны.is_file():
        return [str(적재기), '--library-path', str(вузел / 'usr/lib') + ':' + str(вузел / 'lib'),
                str(дваічны), '-L', str(вузел / 'usr/share/qemu')]
    дваічны = shutil.which('qemu-system-aarch64')
    if not дваічны:
        raise SystemExit('raspi4b апора_значэнне QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [дваічны]


def 해상도읽기(Тэкст):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Тэкст):
        raise argparse.ArgumentTypeError('разрознасць_значэнне фармат_значэнне: 1920x1080')
    너비, 높이 = map(int, Тэкст.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('апора_значэнне кліп: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Загад(разрознасць_значэнне=(640, 480)):
    Фон_значэнне = 모의기계()
    지원목록 = subprocess.check_output(Фон_значэнне + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*разрознасць_значэнне))
    return Фон_значэнне + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Выканаць():
    аналізатар = argparse.ArgumentParser(description='자체 Java Pi4 ядро_значэнне. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Выхад_праграма.')
    аналізатар.add_argument('--display', default='none', help='none 또는 gtk/sdl (вузел апора_значэнне 필요)')
    аналізатар.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Памер. 예: 1920x1080; значэнне_па_змаўчанні 640x480')
    аналізатар.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. клавіша_значэнне 입력은 UART 터미널에서 합니다.')
    аналізатар.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    аналізатар.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    аналізатар.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Злучыцца; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    аналізатар.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    аналізатар.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP кіраванне_значэнне 포트 (데이터 50000..50007)')
    аналізатар.add_argument('--guest-ip', default=None, help='QEMU NAT пераслаць_значэнне мэтавы_паказчык. 기본은 ip.conf의 IP; змяніць_значэнне 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    аналізатар.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 адрас. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN адрас: 외부 кантакт_e05f319b')
    аналізатар.add_argument('--forward', action='append', default=[], help='--network 추가 Злучыцца: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    аналізатар.add_argument('--pip', action='store_true', help='PyPI крыніца_дрэва пакет 중계 Выканаць (--network 필요, MicroPython 호환 소스만)')
    аналізатар.add_argument('--pip-port', type=int, default=8027, help='пакет 중계의 localhost TCP 포트')
    аналізатар.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    аналізатар.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    аргумент_масіў = аналізатар.parse_args()
    if аргумент_масіў.remote:
        аргумент_масіў.network=True
        аргумент_масіў.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; пароль_значэнне: python3 Інструменты/аддалены_Налады.py show'.format(аргумент_масіў.network_host,аргумент_масіў.network_host),flush=True)
    if аргумент_масіў.pip and not аргумент_масіў.network: аналізатар.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= аргумент_масіў.pip_port <= 65535: аналізатар.error('--pip-port 범위는 1~65535입니다.')
    if аргумент_масіў.forward and not аргумент_масіў.network: аналізатар.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as рэсурс_значэнне:
        if аргумент_масіў.pip:
            from 꾸러미중계 import 꾸러미중계
            рэсурс_значэнне.enter_context(꾸러미중계(аргумент_масіў.pip_port, аргумент_масіў.pip_cache, аргумент_масіў.pip_offline))
            print('пакет 중계: 127.0.0.1:' + str(аргумент_масіў.pip_port), flush=True)
        Выкананне(аргумент_масіў)


def Выкананне(аргумент_масіў):
    if аргумент_масіў.desktop:
        if аргумент_масіў.vnc or аргумент_масіў.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from працоўны_стол_выгляд import паток_працоўны_стол
        raise SystemExit(паток_працоўны_стол(аргумент_масіў.port, Сетка=аргумент_масіў.network, файл_перанос_нумар_порта=аргумент_масіў.ftp_port, 전달규칙들=аргумент_масіў.forward, разрознасць_значэнне=аргумент_масіў.resolution, госць_адрас=аргумент_масіў.guest_ip, вузел_адрас=аргумент_масіў.network_host))
    Параметры = ['-display', аргумент_масіў.display, '-serial', 'mon:stdio']
    if аргумент_масіў.vnc:
        Параметры += ['-vnc', аргумент_масіў.vnc]
    if аргумент_масіў.network:
        from Сетка_мост import Сетка_мост
        with Сетка_мост(аргумент_масіў.ftp_port, аргумент_масіў.forward, госць_адрас=аргумент_масіў.guest_ip, вузел_адрас=аргумент_масіў.network_host) as мост:
            стан_значэнне = subprocess.call(Загад(аргумент_масіў.resolution) + Параметры + мост.전달인수())
            if мост.ПАМЫЛКА: raise SystemExit('network bridge: ' + мост.ПАМЫЛКА)
        raise SystemExit(стан_значэнне)
    raise SystemExit(subprocess.call(Загад(аргумент_масіў.resolution) + Параметры))


if __name__ == '__main__':
    Выканаць()
