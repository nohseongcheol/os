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

Дії_корінь = Path(__file__).resolve().parents[1]
випадковий_Файли = []


def _난수정리():
    for шлях in випадковий_Файли:
        try:
            os.unlink(шлях)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as файл:
        файл.write(b'JKRENRG1' + os.urandom(32))
        випадковий_Файли.append(файл.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(файл.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    хост = Дії_корінь.parent / 'rpi4/build/host'
    завантажувач = хост / 'lib/ld-musl-x86_64.so.1'
    бінарний = хост / 'usr/bin/qemu-system-aarch64'
    if завантажувач.is_file() and бінарний.is_file():
        return [str(завантажувач), '--library-path', str(хост / 'usr/lib') + ':' + str(хост / 'lib'),
                str(бінарний), '-L', str(хост / 'usr/share/qemu')]
    бінарний = shutil.which('qemu-system-aarch64')
    if not бінарний:
        raise SystemExit('raspi4b опора_значення QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [бінарний]


def 해상도읽기(текст):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', текст):
        raise argparse.ArgumentTypeError('роздільна_здатність_значення формат_значення: 1920x1080')
    너비, 높이 = map(int, текст.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('опора_значення кліп: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def команда(роздільна_здатність_значення=(640, 480)):
    Фон_значення = 모의기계()
    지원목록 = subprocess.check_output(Фон_значення + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*роздільна_здатність_значення))
    return Фон_значення + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(Дії_корінь / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def запустити():
    аналізатор = argparse.ArgumentParser(description='своє Java Pi4 ядро_значення. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Вийти_програма.')
    аналізатор.add_argument('--display', default='none', help='none 또는 gtk/sdl (хост опора_значення 필요)')
    аналізатор.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='запуск_машини 화면 Розмір. 예: 1920x1080; стандартне_значення 640x480')
    аналізатор.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC обладнання_порт 5902. Ключ_значення 입력은 UART 터미널에서 합니다.')
    аналізатор.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    аналізатор.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC обладнання_порт')
    аналізатор.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 З_єднання; --desktop과 함께 використання_значення 가능; 게스트에서 ftpd start')
    аналізатор.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    аналізатор.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP керування_значення обладнання_порт (데이터 50000..50007)')
    аналізатор.add_argument('--guest-ip', default=None, help='QEMU NAT Уперед_значення мета. 기본은 ip.conf의 IP; змінювати_значення 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    аналізатор.add_argument('--network-host', default='127.0.0.1', help='NAT отримувати_значення_cef4d8ab Адреса. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN Адреса: зовнішній_значення зв_язок_e05f319b')
    аналізатор.add_argument('--forward', action='append', default=[], help='--network додавати_запис З_єднання: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    аналізатор.add_argument('--pip', action='store_true', help='PyPI джерело_дерево набір 중계 запустити (--network 필요, MicroPython 호환 소스만)')
    аналізатор.add_argument('--pip-port', type=int, default=8027, help='набір 중계의 localhost TCP обладнання_порт')
    аналізатор.add_argument('--pip-cache', type=Path, default=Дії_корінь/'build/pip-cache')
    аналізатор.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    аргумент_масив = аналізатор.parse_args()
    if аргумент_масив.remote:
        аргумент_масив.network=True
        аргумент_масив.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; пароль_значення: python3 інструменти/віддалений_Настройки.py show'.format(аргумент_масив.network_host,аргумент_масив.network_host),flush=True)
    if аргумент_масив.pip and not аргумент_масив.network: аналізатор.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= аргумент_масив.pip_port <= 65535: аналізатор.error('--pip-port 범위는 1~65535입니다.')
    if аргумент_масив.forward and not аргумент_масив.network: аналізатор.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ресурс_значення:
        if аргумент_масив.pip:
            from 꾸러미중계 import 꾸러미중계
            ресурс_значення.enter_context(꾸러미중계(аргумент_масив.pip_port, аргумент_масив.pip_cache, аргумент_масив.pip_offline))
            print('набір 중계: 127.0.0.1:' + str(аргумент_масив.pip_port), flush=True)
        Виконати(аргумент_масив)


def Виконати(аргумент_масив):
    if аргумент_масив.desktop:
        if аргумент_масив.vnc or аргумент_масив.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from настільний_Вигляд import запускати_настільний
        raise SystemExit(запускати_настільний(аргумент_масив.port, мережа=аргумент_масив.network, передавання_файлу_номер_порту=аргумент_масив.ftp_port, 전달규칙들=аргумент_масив.forward, роздільна_здатність_значення=аргумент_масив.resolution, гість_адреса=аргумент_масив.guest_ip, хост_адреса=аргумент_масив.network_host))
    Параметри = ['-display', аргумент_масив.display, '-serial', 'mon:stdio']
    if аргумент_масив.vnc:
        Параметри += ['-vnc', аргумент_масив.vnc]
    if аргумент_масив.network:
        from міст_3de4fe3a import міст_3de4fe3a
        with міст_3de4fe3a(аргумент_масив.ftp_port, аргумент_масив.forward, гість_адреса=аргумент_масив.guest_ip, хост_адреса=аргумент_масив.network_host) as міст:
            Стан_значення = subprocess.call(команда(аргумент_масив.resolution) + Параметри + міст.전달인수())
            if міст.ПОМИЛКА: raise SystemExit('network bridge: ' + міст.ПОМИЛКА)
        raise SystemExit(Стан_значення)
    raise SystemExit(subprocess.call(команда(аргумент_масив.resolution) + Параметри))


if __name__ == '__main__':
    запустити()
