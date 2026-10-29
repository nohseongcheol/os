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

задача_корень = Path(__file__).resolve().parents[1]
случайный_Файлы = []


def _난수정리():
    for путь in случайный_Файлы:
        try:
            os.unlink(путь)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as файл:
        файл.write(b'JKRENRG1' + os.urandom(32))
        случайный_Файлы.append(файл.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(файл.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    узел = задача_корень.parent / 'rpi4/build/host'
    загрузчик = узел / 'lib/ld-musl-x86_64.so.1'
    binary = узел / 'usr/bin/qemu-system-aarch64'
    if загрузчик.is_file() and binary.is_file():
        return [str(загрузчик), '--library-path', str(узел / 'usr/lib') + ':' + str(узел / 'lib'),
                str(binary), '-L', str(узел / 'usr/share/qemu')]
    binary = shutil.which('qemu-system-aarch64')
    if not binary:
        raise SystemExit('raspi4b опора_ЗНАЧЕН QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binary]


def чтение_разрешение(текст):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', текст):
        raise argparse.ArgumentTypeError('разрешение_ЗНАЧЕН формат_ЗНАЧЕН: 1920x1080')
    너비, 높이 = map(int, текст.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('опора_ЗНАЧЕН клип: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def команда(разрешение_ЗНАЧЕН=(640, 480)):
    фон_ЗНАЧЕН = 모의기계()
    지원목록 = subprocess.check_output(фон_ЗНАЧЕН + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = чтение_разрешение('{}x{}'.format(*разрешение_ЗНАЧЕН))
    return фон_ЗНАЧЕН + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(задача_корень / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def запустить():
    анализатор = argparse.ArgumentParser(description='свой Java Pi4 ядро_ЗНАЧЕН. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Выход_программа.')
    анализатор.add_argument('--display', default='none', help='none 또는 gtk/sdl (узел опора_ЗНАЧЕН 필요)')
    анализатор.add_argument('--resolution', type=чтение_разрешение, default=(640, 480), help='запуск_машины экран Размер. 예: 1920x1080; значение_по_умолчанию 640x480')
    анализатор.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC аппаратный_порт 5902. Ключ_ЗНАЧЕН 입력은 UART 터미널에서 합니다.')
    анализатор.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    анализатор.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC аппаратный_порт')
    анализатор.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Подключить; --desktop과 함께 использовать_ЗНАЧЕН 가능; 게스트에서 ftpd start')
    анализатор.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    анализатор.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP управление_ЗНАЧЕН аппаратный_порт (데이터 50000..50007)')
    анализатор.add_argument('--guest-ip', default=None, help='QEMU NAT вперед_ЗНАЧЕН целевое_значение. 기본은 ip.conf의 IP; изменить_ЗНАЧЕН 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    анализатор.add_argument('--network-host', default='127.0.0.1', help='NAT получить_ЗНАЧЕН АДРЕС. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN АДРЕС: внешний_ЗНАЧЕН контакт_e05f319b')
    анализатор.add_argument('--forward', action='append', default=[], help='--network добавить_ввод Подключить: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    анализатор.add_argument('--pip', action='store_true', help='PyPI источник_дерево пакет Ретрансляция_ЗНАЧЕН запустить (--network 필요, MicroPython 호환 소스만)')
    анализатор.add_argument('--pip-port', type=int, default=8027, help='пакет 중계의 localhost TCP аппаратный_порт')
    анализатор.add_argument('--pip-cache', type=Path, default=задача_корень/'build/pip-cache')
    анализатор.add_argument('--pip-offline', action='store_true', help='이미 받은 распределение_ЗНАЧЕН 파일만 제공')
    аргумент_МАССИВ = анализатор.parse_args()
    if аргумент_МАССИВ.remote:
        аргумент_МАССИВ.network=True
        аргумент_МАССИВ.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; пароль_ЗНАЧЕН: python3 инструменты/удаленный_Настройки.py show'.format(аргумент_МАССИВ.network_host,аргумент_МАССИВ.network_host),flush=True)
    if аргумент_МАССИВ.pip and not аргумент_МАССИВ.network: анализатор.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= аргумент_МАССИВ.pip_port <= 65535: анализатор.error('--pip-port 범위는 1~65535입니다.')
    if аргумент_МАССИВ.forward and not аргумент_МАССИВ.network: анализатор.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ресурс_ЗНАЧЕН:
        if аргумент_МАССИВ.pip:
            from пакет_Ретрансляция import пакет_Ретрансляция
            ресурс_ЗНАЧЕН.enter_context(пакет_Ретрансляция(аргумент_МАССИВ.pip_port, аргумент_МАССИВ.pip_cache, аргумент_МАССИВ.pip_offline))
            print('пакет Ретрансляция_ЗНАЧЕН: 127.0.0.1:' + str(аргумент_МАССИВ.pip_port), flush=True)
        Выполнить(аргумент_МАССИВ)


def Выполнить(аргумент_МАССИВ):
    if аргумент_МАССИВ.desktop:
        if аргумент_МАССИВ.vnc or аргумент_МАССИВ.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from компьютер_Вид import выполнить_компьютер
        raise SystemExit(выполнить_компьютер(аргумент_МАССИВ.port, сеть=аргумент_МАССИВ.network, передача_файла_номер_порта=аргумент_МАССИВ.ftp_port, 전달규칙들=аргумент_МАССИВ.forward, разрешение_ЗНАЧЕН=аргумент_МАССИВ.resolution, гость_АДРЕС=аргумент_МАССИВ.guest_ip, адрес_узла=аргумент_МАССИВ.network_host))
    Параметры = ['-display', аргумент_МАССИВ.display, '-serial', 'mon:stdio']
    if аргумент_МАССИВ.vnc:
        Параметры += ['-vnc', аргумент_МАССИВ.vnc]
    if аргумент_МАССИВ.network:
        from мост_3de4fe3a import мост_3de4fe3a
        with мост_3de4fe3a(аргумент_МАССИВ.ftp_port, аргумент_МАССИВ.forward, гость_АДРЕС=аргумент_МАССИВ.guest_ip, адрес_узла=аргумент_МАССИВ.network_host) as мост:
            Состояние_ЗНАЧЕН = subprocess.call(команда(аргумент_МАССИВ.resolution) + Параметры + мост.전달인수())
            if мост.ошибка: raise SystemExit('network bridge: ' + мост.ошибка)
        raise SystemExit(Состояние_ЗНАЧЕН)
    raise SystemExit(subprocess.call(команда(аргумент_МАССИВ.resolution) + Параметры))


if __name__ == '__main__':
    запустить()
