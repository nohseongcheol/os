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

كۆرسىتىش_يىلتىز = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for يول in _난수파일들:
        try:
            os.unlink(يول)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ھۆججەت:
        ھۆججەت.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(ھۆججەت.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ھۆججەت.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    باقار = كۆرسىتىش_يىلتىز.parent / 'rpi4/build/host'
    적재기 = باقار / 'lib/ld-musl-x86_64.so.1'
    ئىككىلىك = باقار / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and ئىككىلىك.is_file():
        return [str(적재기), '--library-path', str(باقار / 'usr/lib') + ':' + str(باقار / 'lib'),
                str(ئىككىلىك), '-L', str(باقار / 'usr/share/qemu')]
    ئىككىلىك = shutil.which('qemu-system-aarch64')
    if not ئىككىلىك:
        raise SystemExit('raspi4b قوللاش_قىممىتى QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ئىككىلىك]


def 해상도읽기(تېكىست):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', تېكىست):
        raise argparse.ArgumentTypeError('ئېنىقلىق_قىممىتى فورمات_قىممىتى: 1920x1080')
    너비, 높이 = map(int, تېكىست.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('قوللاش_قىممىتى كەسمە: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def بۇيرۇق(ئېنىقلىق_قىممىتى=(640, 480)):
    تەگلىك_قىممىتى = 모의기계()
    지원목록 = subprocess.check_output(تەگلىك_قىممىتى + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*ئېنىقلىق_قىممىتى))
    return تەگلىك_قىممىتى + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(كۆرسىتىش_يىلتىز / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def ئىجرا_قىل_2():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 يادرو_قىممىتى. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 چىقىش_ئەپ.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (باقار قوللاش_قىممىتى 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 چوڭلۇقى. 예: 1920x1080; سۈكۈتتىكى_قىممەت 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC قاتتىق_دېتال_ئېغىز 5902. ئاچقۇچ_قىممىتى 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC قاتتىق_دېتال_ئېغىز')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 ئۇلا; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP كونترول_قىممىتى قاتتىق_دېتال_ئېغىز (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT تارقىتىش_قىممىتى_24592b8a نىشان. 기본은 ip.conf의 IP; ئۆزگەرتمەك_قىممىتى 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ئادرېس. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ئادرېس: 외부 ئۇلىنىش_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 ئۇلا: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI مەنبە_دەرەخ توپلام 중계 ئىجرا_قىل_2 (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='توپلام 중계의 localhost TCP قاتتىق_دېتال_ئېغىز')
    인수해석기.add_argument('--pip-cache', type=Path, default=كۆرسىتىش_يىلتىز/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    دەلىل_رەت = 인수해석기.parse_args()
    if دەلىل_رەت.remote:
        دەلىل_رەت.network=True
        دەلىل_رەت.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; پارول_قىممىتى: python3 قوراللار/يىراق_تەڭشەك.py show'.format(دەلىل_رەت.network_host,دەلىل_رەت.network_host),flush=True)
    if دەلىل_رەت.pip and not دەلىل_رەت.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= دەلىل_رەت.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if دەلىل_رەت.forward and not دەلىل_رەت.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as مەنبە_قىممىتى:
        if دەلىل_رەت.pip:
            from 꾸러미중계 import 꾸러미중계
            مەنبە_قىممىتى.enter_context(꾸러미중계(دەلىل_رەت.pip_port, دەلىل_رەت.pip_cache, دەلىل_رەت.pip_offline))
            print('توپلام 중계: 127.0.0.1:' + str(دەلىل_رەت.pip_port), flush=True)
        ئىجرا_قىل(دەلىل_رەت)


def ئىجرا_قىل(دەلىل_رەت):
    if دەلىل_رەت.desktop:
        if دەلىل_رەت.vnc or دەلىل_رەت.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ئۈستەليۈزى_كۆرۈنمە import قوزغىتىش_ئۈستەليۈزى
        raise SystemExit(قوزغىتىش_ئۈستەليۈزى(دەلىل_رەت.port, تور=دەلىل_رەت.network, 파일전송접속번호=دەلىل_رەت.ftp_port, 전달규칙들=دەلىل_رەت.forward, ئېنىقلىق_قىممىتى=دەلىل_رەت.resolution, مېھمان_ئادرېس=دەلىل_رەت.guest_ip, باقار_ئادرېس=دەلىل_رەت.network_host))
    تاللانمىلار = ['-display', دەلىل_رەت.display, '-serial', 'mon:stdio']
    if دەلىل_رەت.vnc:
        تاللانمىلار += ['-vnc', دەلىل_رەت.vnc]
    if دەلىل_رەت.network:
        from تور_كۆۋرۈك import تور_كۆۋرۈك
        with تور_كۆۋرۈك(دەلىل_رەت.ftp_port, دەلىل_رەت.forward, مېھمان_ئادرېس=دەلىل_رەت.guest_ip, باقار_ئادرېس=دەلىل_رەت.network_host) as كۆۋرۈك:
            ھالەت_قىممىتى = subprocess.call(بۇيرۇق(دەلىل_رەت.resolution) + تاللانمىلار + كۆۋرۈك.전달인수())
            if كۆۋرۈك.خاتالىق: raise SystemExit('network bridge: ' + كۆۋرۈك.خاتالىق)
        raise SystemExit(ھالەت_قىممىتى)
    raise SystemExit(subprocess.call(بۇيرۇق(دەلىل_رەت.resolution) + تاللانمىلار))


if __name__ == '__main__':
    ئىجرا_قىل_2()
