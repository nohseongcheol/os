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
    for ЖОЛ in _난수파일들:
        try:
            os.unlink(ЖОЛ)
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
    кабылдоо = 기준.parent / 'rpi4/build/host'
    적재기 = кабылдоо / 'lib/ld-musl-x86_64.so.1'
    экилик = кабылдоо / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and экилик.is_file():
        return [str(적재기), '--library-path', str(кабылдоо / 'usr/lib') + ':' + str(кабылдоо / 'lib'),
                str(экилик), '-L', str(кабылдоо / 'usr/share/qemu')]
    экилик = shutil.which('qemu-system-aarch64')
    if not экилик:
        raise SystemExit('raspi4b Колдоо_маани QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [экилик]


def 해상도읽기(Текст):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Текст):
        raise argparse.ArgumentTypeError('чечим_маани формат_маани: 1920x1080')
    너비, 높이 = map(int, Текст.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Колдоо_маани клип: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Команда(чечим_маани=(640, 480)):
    Фон_маани = 모의기계()
    지원목록 = subprocess.check_output(Фон_маани + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*чечим_маани))
    return Фон_маани + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Жүргүзүү():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 өзөк_маани. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Чыгуу_програм.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (кабылдоо Колдоо_маани 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Өлчөмү. 예: 1920x1080; жарыяланбаган_маани 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. ачкыч_маани 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Туташуу; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP башкаруу_маани 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT кайра_даректөө_маани максат. 기본은 ip.conf의 IP; өзгөртүү_маани 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 дарек. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN дарек: 외부 туташуу_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 Туташуу: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI башат_дарак пакет 중계 Жүргүзүү (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='пакет 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    аргумент_МАССИВ = 인수해석기.parse_args()
    if аргумент_МАССИВ.remote:
        аргумент_МАССИВ.network=True
        аргумент_МАССИВ.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; жашыруун_сөз_маани: python3 Куралдар/алыскы_Орнотуулар.py show'.format(аргумент_МАССИВ.network_host,аргумент_МАССИВ.network_host),flush=True)
    if аргумент_МАССИВ.pip and not аргумент_МАССИВ.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= аргумент_МАССИВ.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if аргумент_МАССИВ.forward and not аргумент_МАССИВ.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ресурс_маани:
        if аргумент_МАССИВ.pip:
            from 꾸러미중계 import 꾸러미중계
            ресурс_маани.enter_context(꾸러미중계(аргумент_МАССИВ.pip_port, аргумент_МАССИВ.pip_cache, аргумент_МАССИВ.pip_offline))
            print('пакет 중계: 127.0.0.1:' + str(аргумент_МАССИВ.pip_port), flush=True)
        аткаруу_маселе(аргумент_МАССИВ)


def аткаруу_маселе(аргумент_МАССИВ):
    if аргумент_МАССИВ.desktop:
        if аргумент_МАССИВ.vnc or аргумент_МАССИВ.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from иш_такта_көрүү import топтом_иш_такта
        raise SystemExit(топтом_иш_такта(аргумент_МАССИВ.port, Желе=аргумент_МАССИВ.network, 파일전송접속번호=аргумент_МАССИВ.ftp_port, 전달규칙들=аргумент_МАССИВ.forward, чечим_маани=аргумент_МАССИВ.resolution, 게스트주소=аргумент_МАССИВ.guest_ip, кабылдоо_дарек=аргумент_МАССИВ.network_host))
    Параметрлер = ['-display', аргумент_МАССИВ.display, '-serial', 'mon:stdio']
    if аргумент_МАССИВ.vnc:
        Параметрлер += ['-vnc', аргумент_МАССИВ.vnc]
    if аргумент_МАССИВ.network:
        from 통신다리 import 통신다리
        with 통신다리(аргумент_МАССИВ.ftp_port, аргумент_МАССИВ.forward, 게스트주소=аргумент_МАССИВ.guest_ip, кабылдоо_дарек=аргумент_МАССИВ.network_host) as 연결다리:
            абал_маани = subprocess.call(Команда(аргумент_МАССИВ.resolution) + Параметрлер + 연결다리.전달인수())
            if 연결다리.Ката: raise SystemExit('network bridge: ' + 연결다리.Ката)
        raise SystemExit(абал_маани)
    raise SystemExit(subprocess.call(Команда(аргумент_МАССИВ.resolution) + Параметрлер))


if __name__ == '__main__':
    Жүргүзүү()
