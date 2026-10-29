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

проект_корен = Path(__file__).resolve().parents[1]
случаен_Файлове = []


def _난수정리():
    for ПЪТ in случаен_Файлове:
        try:
            os.unlink(ПЪТ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Файл:
        Файл.write(b'JKRENRG1' + os.urandom(32))
        случаен_Файлове.append(Файл.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Файл.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    хост = проект_корен.parent / 'rpi4/build/host'
    зареждаща_служебна_програма = хост / 'lib/ld-musl-x86_64.so.1'
    двоичен = хост / 'usr/bin/qemu-system-aarch64'
    if зареждаща_служебна_програма.is_file() and двоичен.is_file():
        return [str(зареждаща_служебна_програма), '--library-path', str(хост / 'usr/lib') + ':' + str(хост / 'lib'),
                str(двоичен), '-L', str(хост / 'usr/share/qemu')]
    двоичен = shutil.which('qemu-system-aarch64')
    if not двоичен:
        raise SystemExit('raspi4b Поддръжка_стойност QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [двоичен]


def 해상도읽기(Текст):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Текст):
        raise argparse.ArgumentTypeError('разделителна_способност_стойност формат_стойност: 1920x1080')
    너비, 높이 = map(int, Текст.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Поддръжка_стойност клип: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Команда(разделителна_способност_стойност=(640, 480)):
    Фон_стойност = 모의기계()
    지원목록 = subprocess.check_output(Фон_стойност + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*разделителна_способност_стойност))
    return Фон_стойност + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(проект_корен / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Стартиране():
    анализатор = argparse.ArgumentParser(description='자체 Java Pi4 ядро_стойност. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Изход_програма.')
    анализатор.add_argument('--display', default='none', help='none 또는 gtk/sdl (хост Поддръжка_стойност 필요)')
    анализатор.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Размер. 예: 1920x1080; стойност_по_подразбиране 640x480')
    анализатор.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Ключ_стойност 입력은 UART 터미널에서 합니다.')
    анализатор.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    анализатор.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    анализатор.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Свързване; --desktop과 함께 използвам_стойност 가능; 게스트에서 ftpd start')
    анализатор.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    анализатор.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP контрол_стойност 포트 (데이터 50000..50007)')
    анализатор.add_argument('--guest-ip', default=None, help='QEMU NAT Напред_стойност цел. 기본은 ip.conf의 IP; променям_стойност 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    анализатор.add_argument('--network-host', default='127.0.0.1', help='NAT получавам_стойност_cef4d8ab адрес. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN адрес: външен_стойност връзка_e05f319b')
    анализатор.add_argument('--forward', action='append', default=[], help='--network добавям_запис Свързване: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    анализатор.add_argument('--pip', action='store_true', help='PyPI източник_дърво пакет 중계 Стартиране (--network 필요, MicroPython 호환 소스만)')
    анализатор.add_argument('--pip-port', type=int, default=8027, help='пакет 중계의 localhost TCP 포트')
    анализатор.add_argument('--pip-cache', type=Path, default=проект_корен/'build/pip-cache')
    анализатор.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    аргумент_масив = анализатор.parse_args()
    if аргумент_масив.remote:
        аргумент_масив.network=True
        аргумент_масив.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; парола_стойност: python3 Инструменти/отдалечен_Настройки.py show'.format(аргумент_масив.network_host,аргумент_масив.network_host),flush=True)
    if аргумент_масив.pip and not аргумент_масив.network: анализатор.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= аргумент_масив.pip_port <= 65535: анализатор.error('--pip-port 범위는 1~65535입니다.')
    if аргумент_масив.forward and not аргумент_масив.network: анализатор.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ресурс_стойност:
        if аргумент_масив.pip:
            from 꾸러미중계 import 꾸러미중계
            ресурс_стойност.enter_context(꾸러미중계(аргумент_масив.pip_port, аргумент_масив.pip_cache, аргумент_масив.pip_offline))
            print('пакет 중계: 127.0.0.1:' + str(аргумент_масив.pip_port), flush=True)
        Изпълнение(аргумент_масив)


def Изпълнение(аргумент_масив):
    if аргумент_масив.desktop:
        if аргумент_масив.vnc or аргумент_масив.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from десктоп_Изглед import изпълнение_десктоп
        raise SystemExit(изпълнение_десктоп(аргумент_масив.port, мрежа=аргумент_масив.network, прехвърляне_на_файл_номер_на_порт=аргумент_масив.ftp_port, 전달규칙들=аргумент_масив.forward, разделителна_способност_стойност=аргумент_масив.resolution, гост_адрес=аргумент_масив.guest_ip, хост_адрес=аргумент_масив.network_host))
    Опции = ['-display', аргумент_масив.display, '-serial', 'mon:stdio']
    if аргумент_масив.vnc:
        Опции += ['-vnc', аргумент_масив.vnc]
    if аргумент_масив.network:
        from мост_3de4fe3a import мост_3de4fe3a
        with мост_3de4fe3a(аргумент_масив.ftp_port, аргумент_масив.forward, гост_адрес=аргумент_масив.guest_ip, хост_адрес=аргумент_масив.network_host) as мост:
            Състояние_стойност = subprocess.call(Команда(аргумент_масив.resolution) + Опции + мост.전달인수())
            if мост.ГРЕШКА: raise SystemExit('network bridge: ' + мост.ГРЕШКА)
        raise SystemExit(Състояние_стойност)
    raise SystemExit(subprocess.call(Команда(аргумент_масив.resolution) + Опции))


if __name__ == '__main__':
    Стартиране()
