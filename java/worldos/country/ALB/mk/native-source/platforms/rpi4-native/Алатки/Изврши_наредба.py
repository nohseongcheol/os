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

Project_корен = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for ПАТЕКА in _난수파일들:
        try:
            os.unlink(ПАТЕКА)
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
    вдоми = Project_корен.parent / 'rpi4/build/host'
    적재기 = вдоми / 'lib/ld-musl-x86_64.so.1'
    бинарен = вдоми / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and бинарен.is_file():
        return [str(적재기), '--library-path', str(вдоми / 'usr/lib') + ':' + str(вдоми / 'lib'),
                str(бинарен), '-L', str(вдоми / 'usr/share/qemu')]
    бинарен = shutil.which('qemu-system-aarch64')
    if not бинарен:
        raise SystemExit('raspi4b Поддршка_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [бинарен]


def 해상도읽기(Текст):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Текст):
        raise argparse.ArgumentTypeError('резолуција_VALUE формат_VALUE: 1920x1080')
    너비, 높이 = map(int, Текст.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Поддршка_VALUE клип: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Команда(резолуција_VALUE=(640, 480)):
    тапет_VALUE = 모의기계()
    지원목록 = subprocess.check_output(тапет_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*резолуција_VALUE))
    return тапет_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(Project_корен / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Изврши_2():
    анализатор = argparse.ArgumentParser(description='자체 Java Pi4 јадро_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Излез_програма.')
    анализатор.add_argument('--display', default='none', help='none 또는 gtk/sdl (вдоми Поддршка_VALUE 필요)')
    анализатор.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Големина. 예: 1920x1080; стандардна_вредност 640x480')
    анализатор.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Клуч_VALUE 입력은 UART 터미널에서 합니다.')
    анализатор.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    анализатор.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    анализатор.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Врзи_се; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    анализатор.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    анализатор.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP контрола_VALUE 포트 (데이터 50000..50007)')
    анализатор.add_argument('--guest-ip', default=None, help='QEMU NAT Напред_VALUE цел. 기본은 ip.conf의 IP; измени_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    анализатор.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 адреса. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN адреса: 외부 врска_e05f319b')
    анализатор.add_argument('--forward', action='append', default=[], help='--network 추가 Врзи_се: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    анализатор.add_argument('--pip', action='store_true', help='PyPI извор_дрво пакет 중계 Изврши_2 (--network 필요, MicroPython 호환 소스만)')
    анализатор.add_argument('--pip-port', type=int, default=8027, help='пакет 중계의 localhost TCP 포트')
    анализатор.add_argument('--pip-cache', type=Path, default=Project_корен/'build/pip-cache')
    анализатор.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    аргумент_низа = анализатор.parse_args()
    if аргумент_низа.remote:
        аргумент_низа.network=True
        аргумент_низа.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; лозинка_VALUE: python3 Алатки/далечинскo_Параметри.py show'.format(аргумент_низа.network_host,аргумент_низа.network_host),flush=True)
    if аргумент_низа.pip and not аргумент_низа.network: анализатор.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= аргумент_низа.pip_port <= 65535: анализатор.error('--pip-port 범위는 1~65535입니다.')
    if аргумент_низа.forward and not аргумент_низа.network: анализатор.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as извор_VALUE:
        if аргумент_низа.pip:
            from 꾸러미중계 import 꾸러미중계
            извор_VALUE.enter_context(꾸러미중계(аргумент_низа.pip_port, аргумент_низа.pip_cache, аргумент_низа.pip_offline))
            print('пакет 중계: 127.0.0.1:' + str(аргумент_низа.pip_port), flush=True)
        Изврши(аргумент_низа)


def Изврши(аргумент_низа):
    if аргумент_низа.desktop:
        if аргумент_низа.vnc or аргумент_низа.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from десктоп_Приказ import изврши_десктоп
        raise SystemExit(изврши_десктоп(аргумент_низа.port, Мрежа=аргумент_низа.network, датотека_пренос_број_на_порта=аргумент_низа.ftp_port, 전달규칙들=аргумент_низа.forward, резолуција_VALUE=аргумент_низа.resolution, гостин_адреса=аргумент_низа.guest_ip, вдоми_адреса=аргумент_низа.network_host))
    Опции = ['-display', аргумент_низа.display, '-serial', 'mon:stdio']
    if аргумент_низа.vnc:
        Опции += ['-vnc', аргумент_низа.vnc]
    if аргумент_низа.network:
        from Мрежа_мост import Мрежа_мост
        with Мрежа_мост(аргумент_низа.ftp_port, аргумент_низа.forward, гостин_адреса=аргумент_низа.guest_ip, вдоми_адреса=аргумент_низа.network_host) as мост:
            статус_VALUE = subprocess.call(Команда(аргумент_низа.resolution) + Опции + мост.전달인수())
            if мост.ГРЕШКА: raise SystemExit('network bridge: ' + мост.ГРЕШКА)
        raise SystemExit(статус_VALUE)
    raise SystemExit(subprocess.call(Команда(аргумент_низа.resolution) + Опции))


if __name__ == '__main__':
    Изврши_2()
