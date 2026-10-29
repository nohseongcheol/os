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
    for گوزەر in _난수파일들:
        try:
            os.unlink(گوزەر)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as فایل:
        فایل.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(فایل.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(فایل.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    جێدەر = 기준.parent / 'rpi4/build/host'
    적재기 = جێدەر / 'lib/ld-musl-x86_64.so.1'
    دوانەیی = جێدەر / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and دوانەیی.is_file():
        return [str(적재기), '--library-path', str(جێدەر / 'usr/lib') + ':' + str(جێدەر / 'lib'),
                str(دوانەیی), '-L', str(جێدەر / 'usr/share/qemu')]
    دوانەیی = shutil.which('qemu-system-aarch64')
    if not دوانەیی:
        raise SystemExit('raspi4b پشتیوانی_نرخ QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [دوانەیی]


def 해상도읽기(دەق):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', دەق):
        raise argparse.ArgumentTypeError('وردبینی_نرخ بیچم_نرخ: 1920x1080')
    너비, 높이 = map(int, دەق.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('پشتیوانی_نرخ کلیپ: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def فەرمان(وردبینی_نرخ=(640, 480)):
    بن_زمینه_نرخ = 모의기계()
    지원목록 = subprocess.check_output(بن_زمینه_نرخ + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*وردبینی_نرخ))
    return بن_زمینه_نرخ + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def ڕادان():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 کوورەک_نرخ. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 بزربوون_بەرنامە.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (جێدەر پشتیوانی_نرخ 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 گۆڕینی_ئەندازە. 예: 1920x1080; بەهای_گریمانە 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. کلیل_نرخ 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 لكاندن; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP کۆنترۆڵ_نرخ 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT رەوانەکردن_نرخ مەبەست. 기본은 ip.conf의 IP; گۆڕین_نرخ 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ناونیشان. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ناونیشان: 외부 گرێدان_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 لكاندن: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI ژێدەر_دار گورزە 중계 ڕادان (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='گورزە 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    ئارگیومێنت_ڕیزی_داتا = 인수해석기.parse_args()
    if ئارگیومێنت_ڕیزی_داتا.remote:
        ئارگیومێنت_ڕیزی_داتا.network=True
        ئارگیومێنت_ڕیزی_داتا.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; نهێنوشە_نرخ: python3 ئامرازەکان/دوورەدەس_ڕێكبەندەكان.py show'.format(ئارگیومێنت_ڕیزی_داتا.network_host,ئارگیومێنت_ڕیزی_داتا.network_host),flush=True)
    if ئارگیومێنت_ڕیزی_داتا.pip and not ئارگیومێنت_ڕیزی_داتا.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= ئارگیومێنت_ڕیزی_داتا.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if ئارگیومێنت_ڕیزی_داتا.forward and not ئارگیومێنت_ڕیزی_داتا.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ژێدەر_نرخ:
        if ئارگیومێنت_ڕیزی_داتا.pip:
            from 꾸러미중계 import 꾸러미중계
            ژێدەر_نرخ.enter_context(꾸러미중계(ئارگیومێنت_ڕیزی_داتا.pip_port, ئارگیومێنت_ڕیزی_داتا.pip_cache, ئارگیومێنت_ڕیزی_داتا.pip_offline))
            print('گورزە 중계: 127.0.0.1:' + str(ئارگیومێنت_ڕیزی_داتا.pip_port), flush=True)
        جێبەجێکردن_ئەرک(ئارگیومێنت_ڕیزی_داتا)


def جێبەجێکردن_ئەرک(ئارگیومێنت_ڕیزی_داتا):
    if ئارگیومێنت_ڕیزی_داتا.desktop:
        if ئارگیومێنت_ڕیزی_داتا.vnc or ئارگیومێنت_ڕیزی_داتا.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from دێسکتۆپ_دیمەن import ڕادان_دێسکتۆپ
        raise SystemExit(ڕادان_دێسکتۆپ(ئارگیومێنت_ڕیزی_داتا.port, تۆڕ=ئارگیومێنت_ڕیزی_داتا.network, 파일전송접속번호=ئارگیومێنت_ڕیزی_داتا.ftp_port, 전달규칙들=ئارگیومێنت_ڕیزی_داتا.forward, وردبینی_نرخ=ئارگیومێنت_ڕیزی_داتا.resolution, 게스트주소=ئارگیومێنت_ڕیزی_داتا.guest_ip, جێدەر_ناونیشان=ئارگیومێنت_ڕیزی_داتا.network_host))
    بەربژارەکان = ['-display', ئارگیومێنت_ڕیزی_داتا.display, '-serial', 'mon:stdio']
    if ئارگیومێنت_ڕیزی_داتا.vnc:
        بەربژارەکان += ['-vnc', ئارگیومێنت_ڕیزی_داتا.vnc]
    if ئارگیومێنت_ڕیزی_داتا.network:
        from 통신다리 import 통신다리
        with 통신다리(ئارگیومێنت_ڕیزی_داتا.ftp_port, ئارگیومێنت_ڕیزی_داتا.forward, 게스트주소=ئارگیومێنت_ڕیزی_داتا.guest_ip, جێدەر_ناونیشان=ئارگیومێنت_ڕیزی_داتا.network_host) as 연결다리:
            دۆخ_نرخ = subprocess.call(فەرمان(ئارگیومێنت_ڕیزی_داتا.resolution) + بەربژارەکان + 연결다리.전달인수())
            if 연결다리.هەڵە: raise SystemExit('network bridge: ' + 연결다리.هەڵە)
        raise SystemExit(دۆخ_نرخ)
    raise SystemExit(subprocess.call(فەرمان(ئارگیومێنت_ڕیزی_داتا.resolution) + بەربژارەکان))


if __name__ == '__main__':
    ڕادان()
