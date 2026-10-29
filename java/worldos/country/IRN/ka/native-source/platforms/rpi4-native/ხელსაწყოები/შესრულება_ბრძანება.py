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

პროეცირება_ფესვი = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for გეზი in _난수파일들:
        try:
            os.unlink(გეზი)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ფაილი:
        ფაილი.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(ფაილი.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ფაილი.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    მასპინძელი = პროეცირება_ფესვი.parent / 'rpi4/build/host'
    적재기 = მასპინძელი / 'lib/ld-musl-x86_64.so.1'
    ორობითი = მასპინძელი / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and ორობითი.is_file():
        return [str(적재기), '--library-path', str(მასპინძელი / 'usr/lib') + ':' + str(მასპინძელი / 'lib'),
                str(ორობითი), '-L', str(მასპინძელი / 'usr/share/qemu')]
    ორობითი = shutil.which('qemu-system-aarch64')
    if not ორობითი:
        raise SystemExit('raspi4b მხარდაჭერა_მნიშვნელობა QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ორობითი]


def 해상도읽기(ტექსტი):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', ტექსტი):
        raise argparse.ArgumentTypeError('გარჩევადობა_მნიშვნელობა ფორმატი_მნიშვნელობა: 1920x1080')
    너비, 높이 = map(int, ტექსტი.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('მხარდაჭერა_მნიშვნელობა კლიპი: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def ბრძანება(გარჩევადობა_მნიშვნელობა=(640, 480)):
    ფონი_მნიშვნელობა = 모의기계()
    지원목록 = subprocess.check_output(ფონი_მნიშვნელობა + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*გარჩევადობა_მნიშვნელობა))
    return ფონი_მნიშვნელობა + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(პროეცირება_ფესვი / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def გაშვება():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 ბირთვი_მნიშვნელობა. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 გასვლა_აპი.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (მასპინძელი მხარდაჭერა_მნიშვნელობა 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 ზომა. 예: 1920x1080; ნაგულისხმევი_მნიშვნელობა 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. კლავიში_მნიშვნელობა 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 დაკავშირება; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP მართვა_მნიშვნელობა 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT გადაგზავნა_მნიშვნელობა მიზანი. 기본은 ip.conf의 IP; შეცვლა_მნიშვნელობა 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 მისამართი. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN მისამართი: 외부 კავშირი_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 დაკავშირება: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI წყარო_ხე შეკვრა 중계 გაშვება (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='შეკვრა 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=პროეცირება_ფესვი/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    არგუმენტი_მასივი = 인수해석기.parse_args()
    if არგუმენტი_მასივი.remote:
        არგუმენტი_მასივი.network=True
        არგუმენტი_მასივი.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; პაროლი_მნიშვნელობა: python3 ხელსაწყოები/დისტანციური_პარამეტრები.py show'.format(არგუმენტი_მასივი.network_host,არგუმენტი_მასივი.network_host),flush=True)
    if არგუმენტი_მასივი.pip and not არგუმენტი_მასივი.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= არგუმენტი_მასივი.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if არგუმენტი_მასივი.forward and not არგუმენტი_მასივი.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as რესურსი_მნიშვნელობა:
        if არგუმენტი_მასივი.pip:
            from 꾸러미중계 import 꾸러미중계
            რესურსი_მნიშვნელობა.enter_context(꾸러미중계(არგუმენტი_მასივი.pip_port, არგუმენტი_მასივი.pip_cache, არგუმენტი_მასივი.pip_offline))
            print('შეკვრა 중계: 127.0.0.1:' + str(არგუმენტი_მასივი.pip_port), flush=True)
        შესრულება(არგუმენტი_მასივი)


def შესრულება(არგუმენტი_მასივი):
    if არგუმენტი_მასივი.desktop:
        if არგუმენტი_მასივი.vnc or არგუმენტი_მასივი.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from სამუშაო_დაფა_ხედი import სერია_სამუშაო_დაფა
        raise SystemExit(სერია_სამუშაო_დაფა(არგუმენტი_მასივი.port, ქსელი=არგუმენტი_მასივი.network, 파일전송접속번호=არგუმენტი_მასივი.ftp_port, 전달규칙들=არგუმენტი_მასივი.forward, გარჩევადობა_მნიშვნელობა=არგუმენტი_მასივი.resolution, სტუმარი_მისამართი=არგუმენტი_მასივი.guest_ip, მასპინძელი_მისამართი=არგუმენტი_მასივი.network_host))
    ვარიანტები = ['-display', არგუმენტი_მასივი.display, '-serial', 'mon:stdio']
    if არგუმენტი_მასივი.vnc:
        ვარიანტები += ['-vnc', არგუმენტი_მასივი.vnc]
    if არგუმენტი_მასივი.network:
        from ქსელი_ხიდი import ქსელი_ხიდი
        with ქსელი_ხიდი(არგუმენტი_მასივი.ftp_port, არგუმენტი_მასივი.forward, სტუმარი_მისამართი=არგუმენტი_მასივი.guest_ip, მასპინძელი_მისამართი=არგუმენტი_მასივი.network_host) as ხიდი:
            სტატუსი_მნიშვნელობა = subprocess.call(ბრძანება(არგუმენტი_მასივი.resolution) + ვარიანტები + ხიდი.전달인수())
            if ხიდი.შეცდომა: raise SystemExit('network bridge: ' + ხიდი.შეცდომა)
        raise SystemExit(სტატუსი_მნიშვნელობა)
    raise SystemExit(subprocess.call(ბრძანება(არგუმენტი_მასივი.resolution) + ვარიანტები))


if __name__ == '__main__':
    გაშვება()
