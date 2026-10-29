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

প্রকল্প_মূল = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for পথ_2 in _난수파일들:
        try:
            os.unlink(পথ_2)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as নথির_নাম:
        নথির_নাম.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(নথির_নাম.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(নথির_নাম.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    হোস্ট = প্রকল্প_মূল.parent / 'rpi4/build/host'
    적재기 = হোস্ট / 'lib/ld-musl-x86_64.so.1'
    বাইনারি = হোস্ট / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and বাইনারি.is_file():
        return [str(적재기), '--library-path', str(হোস্ট / 'usr/lib') + ':' + str(হোস্ট / 'lib'),
                str(বাইনারি), '-L', str(হোস্ট / 'usr/share/qemu')]
    বাইনারি = shutil.which('qemu-system-aarch64')
    if not বাইনারি:
        raise SystemExit('raspi4b সমর্থন_মান QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [বাইনারি]


def 해상도읽기(পাঠ):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', পাঠ):
        raise argparse.ArgumentTypeError('রেজোলিউশন_মান বিন্যাস_মান: 1920x1080')
    너비, 높이 = map(int, পাঠ.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('সমর্থন_মান ক্লিপ: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def আদেশ(রেজোলিউশন_মান=(640, 480)):
    পটভূমি_মান = 모의기계()
    지원목록 = subprocess.check_output(পটভূমি_মান + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*রেজোলিউশন_মান))
    return পটভূমি_মান + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(প্রকল্প_মূল / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def চালনা():
    পার্সার = argparse.ArgumentParser(description='নিজ Java Pi4 কারনেল_মান. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 প্রস্থান_অ্যাপ.')
    পার্সার.add_argument('--display', default='none', help='none 또는 gtk/sdl (হোস্ট সমর্থন_মান 필요)')
    পার্সার.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 আকার. 예: 1920x1080; অমনোনীত_মান 640x480')
    পার্সার.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC হার্ডওয়্যার_পোর্ট 5902. কী_মান 입력은 UART 터미널에서 합니다.')
    পার্সার.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    পার্সার.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC হার্ডওয়্যার_পোর্ট')
    পার্সার.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 সংযোগ_স্থাপনা; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    পার্সার.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    পার্সার.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP নিয়ন্ত্রণ_মান হার্ডওয়্যার_পোর্ট (데이터 50000..50007)')
    পার্সার.add_argument('--guest-ip', default=None, help='QEMU NAT ফরোয়ার্ড_মান লক্ষ্য. 기본은 ip.conf의 IP; পরিবর্তন_করা_মান 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    পার্সার.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ইমেইল. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ইমেইল: 외부 সংযোগ_e05f319b')
    পার্সার.add_argument('--forward', action='append', default=[], help='--network 추가 সংযোগ_স্থাপনা: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    পার্সার.add_argument('--pip', action='store_true', help='PyPI উত্স_ট্রী পাঁজা 중계 চালনা (--network 필요, MicroPython 호환 소스만)')
    পার্সার.add_argument('--pip-port', type=int, default=8027, help='পাঁজা 중계의 localhost TCP হার্ডওয়্যার_পোর্ট')
    পার্সার.add_argument('--pip-cache', type=Path, default=প্রকল্প_মূল/'build/pip-cache')
    পার্সার.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    যুক্তি_অ্যারে = পার্সার.parse_args()
    if যুক্তি_অ্যারে.remote:
        যুক্তি_অ্যারে.network=True
        যুক্তি_অ্যারে.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; পাসওয়ার্ড_মান: python3 সরঞ্জামগুলি/দূরবর্তী_সেটিংস.py show'.format(যুক্তি_অ্যারে.network_host,যুক্তি_অ্যারে.network_host),flush=True)
    if যুক্তি_অ্যারে.pip and not যুক্তি_অ্যারে.network: পার্সার.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= যুক্তি_অ্যারে.pip_port <= 65535: পার্সার.error('--pip-port 범위는 1~65535입니다.')
    if যুক্তি_অ্যারে.forward and not যুক্তি_অ্যারে.network: পার্সার.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as রিসোর্স_মান:
        if যুক্তি_অ্যারে.pip:
            from 꾸러미중계 import 꾸러미중계
            রিসোর্স_মান.enter_context(꾸러미중계(যুক্তি_অ্যারে.pip_port, যুক্তি_অ্যারে.pip_cache, যুক্তি_অ্যারে.pip_offline))
            print('পাঁজা 중계: 127.0.0.1:' + str(যুক্তি_অ্যারে.pip_port), flush=True)
        চালানো(যুক্তি_অ্যারে)


def চালানো(যুক্তি_অ্যারে):
    if যুক্তি_অ্যারে.desktop:
        if যুক্তি_অ্যারে.vnc or যুক্তি_অ্যারে.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ডেস্কটপ_ভিউ import রান_ডেস্কটপ
        raise SystemExit(রান_ডেস্কটপ(যুক্তি_অ্যারে.port, নেটওয়ার্ক_9b2e3222=যুক্তি_অ্যারে.network, ফাইল_স্থানান্তর_পোর্ট_নম্বর=যুক্তি_অ্যারে.ftp_port, 전달규칙들=যুক্তি_অ্যারে.forward, রেজোলিউশন_মান=যুক্তি_অ্যারে.resolution, অতিথি_ইমেইল=যুক্তি_অ্যারে.guest_ip, হোস্ট_ইমেইল=যুক্তি_অ্যারে.network_host))
    পছন্দ = ['-display', যুক্তি_অ্যারে.display, '-serial', 'mon:stdio']
    if যুক্তি_অ্যারে.vnc:
        পছন্দ += ['-vnc', যুক্তি_অ্যারে.vnc]
    if যুক্তি_অ্যারে.network:
        from নেটওয়ার্ক_ব্রিজ import নেটওয়ার্ক_ব্রিজ
        with নেটওয়ার্ক_ব্রিজ(যুক্তি_অ্যারে.ftp_port, যুক্তি_অ্যারে.forward, অতিথি_ইমেইল=যুক্তি_অ্যারে.guest_ip, হোস্ট_ইমেইল=যুক্তি_অ্যারে.network_host) as ব্রিজ:
            অবস্হা_মান = subprocess.call(আদেশ(যুক্তি_অ্যারে.resolution) + পছন্দ + ব্রিজ.전달인수())
            if ব্রিজ.ত্রুটি: raise SystemExit('network bridge: ' + ব্রিজ.ত্রুটি)
        raise SystemExit(অবস্হা_মান)
    raise SystemExit(subprocess.call(আদেশ(যুক্তি_অ্যারে.resolution) + পছন্দ))


if __name__ == '__main__':
    চালনা()
