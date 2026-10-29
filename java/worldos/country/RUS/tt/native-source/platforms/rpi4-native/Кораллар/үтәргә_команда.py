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

экранга_җибәрү_тамыр = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for Yul in _난수파일들:
        try:
            os.unlink(Yul)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Birem:
        Birem.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Birem.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Birem.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    хост = экранга_җибәрү_тамыр.parent / 'rpi4/build/host'
    적재기 = хост / 'lib/ld-musl-x86_64.so.1'
    бинар = хост / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and бинар.is_file():
        return [str(적재기), '--library-path', str(хост / 'usr/lib') + ':' + str(хост / 'lib'),
                str(бинар), '-L', str(хост / 'usr/share/qemu')]
    бинар = shutil.which('qemu-system-aarch64')
    if not бинар:
        raise SystemExit('raspi4b ярдәм_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [бинар]


def 해상도읽기(Mäten):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Mäten):
        raise argparse.ArgumentTypeError('ачыклык_VALUE формат_VALUE: 1920x1080')
    너비, 높이 = map(int, Mäten.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('ярдәм_VALUE клип: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def команда(ачыклык_VALUE=(640, 480)):
    Фон_VALUE = 모의기계()
    지원목록 = subprocess.check_output(Фон_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*ачыклык_VALUE))
    return Фон_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(экранга_җибәрү_тамыр / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def эшләтү():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 төш_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Чыгу_кушымта.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (хост ярдәм_VALUE 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 үлчәмен_үзгәртү. 예: 1920x1080; килешенгәнчә_кыйммәт 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. ачкыч_VALUE 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 ялгау; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP идарә_VALUE 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT Алга_VALUE максат_кыйммәт. 기본은 ip.conf의 IP; үзгәртү_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 адрес. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN адрес: 외부 тоташу_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 ялгау: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI чыганак_агач пакет 중계 эшләтү (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='пакет 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=экранга_җибәрү_тамыр/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    аргумент_МАССИВ = 인수해석기.parse_args()
    if аргумент_МАССИВ.remote:
        аргумент_МАССИВ.network=True
        аргумент_МАССИВ.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; серсүз_VALUE: python3 Кораллар/читтәге_Параметрлар.py show'.format(аргумент_МАССИВ.network_host,аргумент_МАССИВ.network_host),flush=True)
    if аргумент_МАССИВ.pip and not аргумент_МАССИВ.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= аргумент_МАССИВ.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if аргумент_МАССИВ.forward and not аргумент_МАССИВ.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ресурс_VALUE:
        if аргумент_МАССИВ.pip:
            from 꾸러미중계 import 꾸러미중계
            ресурс_VALUE.enter_context(꾸러미중계(аргумент_МАССИВ.pip_port, аргумент_МАССИВ.pip_cache, аргумент_МАССИВ.pip_offline))
            print('пакет 중계: 127.0.0.1:' + str(аргумент_МАССИВ.pip_port), flush=True)
        Башкару(аргумент_МАССИВ)


def Башкару(аргумент_МАССИВ):
    if аргумент_МАССИВ.desktop:
        if аргумент_МАССИВ.vnc or аргумент_МАССИВ.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from классик_карау import эшләтү_классик
        raise SystemExit(эшләтү_классик(аргумент_МАССИВ.port, Челтәр=аргумент_МАССИВ.network, 파일전송접속번호=аргумент_МАССИВ.ftp_port, 전달규칙들=аргумент_МАССИВ.forward, ачыклык_VALUE=аргумент_МАССИВ.resolution, кунак_адрес=аргумент_МАССИВ.guest_ip, хост_адрес=аргумент_МАССИВ.network_host))
    Параметрлар = ['-display', аргумент_МАССИВ.display, '-serial', 'mon:stdio']
    if аргумент_МАССИВ.vnc:
        Параметрлар += ['-vnc', аргумент_МАССИВ.vnc]
    if аргумент_МАССИВ.network:
        from Челтәр_күпер import Челтәр_күпер
        with Челтәр_күпер(аргумент_МАССИВ.ftp_port, аргумент_МАССИВ.forward, кунак_адрес=аргумент_МАССИВ.guest_ip, хост_адрес=аргумент_МАССИВ.network_host) as күпер:
            халәт_VALUE = subprocess.call(команда(аргумент_МАССИВ.resolution) + Параметрлар + күпер.전달인수())
            if күпер.Хата: raise SystemExit('network bridge: ' + күпер.Хата)
        raise SystemExit(халәт_VALUE)
    raise SystemExit(subprocess.call(команда(аргумент_МАССИВ.resolution) + Параметрлар))


if __name__ == '__main__':
    эшләтү()
