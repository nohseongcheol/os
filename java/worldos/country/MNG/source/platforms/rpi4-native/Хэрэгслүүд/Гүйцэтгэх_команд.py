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
    for ЗАМ in _난수파일들:
        try:
            os.unlink(ЗАМ)
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
    хост = 기준.parent / 'rpi4/build/host'
    적재기 = хост / 'lib/ld-musl-x86_64.so.1'
    хоёрт = хост / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and хоёрт.is_file():
        return [str(적재기), '--library-path', str(хост / 'usr/lib') + ':' + str(хост / 'lib'),
                str(хоёрт), '-L', str(хост / 'usr/share/qemu')]
    хоёрт = shutil.which('qemu-system-aarch64')
    if not хоёрт:
        raise SystemExit('raspi4b тусламж_утга QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [хоёрт]


def 해상도읽기(Бичвэр):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Бичвэр):
        raise argparse.ArgumentTypeError('нягтрал_утга формат_утга: 1920x1080')
    너비, 높이 = map(int, Бичвэр.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('тусламж_утга клип: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Тушаал(нягтрал_утга=(640, 480)):
    Дэвсгэр_утга = 모의기계()
    지원목록 = subprocess.check_output(Дэвсгэр_утга + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*нягтрал_утга))
    return Дэвсгэр_утга + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Ажиллуулах():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 кернел_утга. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Гарах_програм.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (хост тусламж_утга 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Хэмжээ. 예: 1920x1080; өгөгдмөл_утга 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. түлхүүр_утга 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Холбох; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP хяналт_утга 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT цааш_илгээх_утга зорилго. 기본은 ip.conf의 IP; өөрчлөх_утга 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 хаяг. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN хаяг: 외부 холболт_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 Холбох: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI эх_мод багц 중계 Ажиллуулах (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='багц 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    аргумент_олонлог = 인수해석기.parse_args()
    if аргумент_олонлог.remote:
        аргумент_олонлог.network=True
        аргумент_олонлог.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; нууц_үг_утга: python3 Хэрэгслүүд/алсын_Тохиргоо.py show'.format(аргумент_олонлог.network_host,аргумент_олонлог.network_host),flush=True)
    if аргумент_олонлог.pip and not аргумент_олонлог.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= аргумент_олонлог.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if аргумент_олонлог.forward and not аргумент_олонлог.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as хэрэгсэл_утга:
        if аргумент_олонлог.pip:
            from 꾸러미중계 import 꾸러미중계
            хэрэгсэл_утга.enter_context(꾸러미중계(аргумент_олонлог.pip_port, аргумент_олонлог.pip_cache, аргумент_олонлог.pip_offline))
            print('багц 중계: 127.0.0.1:' + str(аргумент_олонлог.pip_port), flush=True)
        Гүйцэтгэх_даалгавар(аргумент_олонлог)


def Гүйцэтгэх_даалгавар(аргумент_олонлог):
    if аргумент_олонлог.desktop:
        if аргумент_олонлог.vnc or аргумент_олонлог.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from дэлгэц_харах import ажиллах_дэлгэц
        raise SystemExit(ажиллах_дэлгэц(аргумент_олонлог.port, Сүлжээ=аргумент_олонлог.network, 파일전송접속번호=аргумент_олонлог.ftp_port, 전달규칙들=аргумент_олонлог.forward, нягтрал_утга=аргумент_олонлог.resolution, 게스트주소=аргумент_олонлог.guest_ip, хост_хаяг=аргумент_олонлог.network_host))
    Сонголтууд = ['-display', аргумент_олонлог.display, '-serial', 'mon:stdio']
    if аргумент_олонлог.vnc:
        Сонголтууд += ['-vnc', аргумент_олонлог.vnc]
    if аргумент_олонлог.network:
        from 통신다리 import 통신다리
        with 통신다리(аргумент_олонлог.ftp_port, аргумент_олонлог.forward, 게스트주소=аргумент_олонлог.guest_ip, хост_хаяг=аргумент_олонлог.network_host) as 연결다리:
            төлөв_утга = subprocess.call(Тушаал(аргумент_олонлог.resolution) + Сонголтууд + 연결다리.전달인수())
            if 연결다리.Алдаа: raise SystemExit('network bridge: ' + 연결다리.Алдаа)
        raise SystemExit(төлөв_утга)
    raise SystemExit(subprocess.call(Тушаал(аргумент_олонлог.resolution) + Сонголтууд))


if __name__ == '__main__':
    Ажиллуулах()
