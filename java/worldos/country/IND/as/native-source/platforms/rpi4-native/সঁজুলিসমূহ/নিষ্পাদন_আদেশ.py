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
    for পথ in _난수파일들:
        try:
            os.unlink(পথ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as নথিপত্ৰ:
        নথিপত্ৰ.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(নথিপত্ৰ.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(নথিপত্ৰ.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    হ_ষ্ট = 기준.parent / 'rpi4/build/host'
    적재기 = হ_ষ্ট / 'lib/ld-musl-x86_64.so.1'
    বাইনেৰি = হ_ষ্ট / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and বাইনেৰি.is_file():
        return [str(적재기), '--library-path', str(হ_ষ্ট / 'usr/lib') + ':' + str(হ_ষ্ট / 'lib'),
                str(বাইনেৰি), '-L', str(হ_ষ্ট / 'usr/share/qemu')]
    বাইনেৰি = shutil.which('qemu-system-aarch64')
    if not বাইনেৰি:
        raise SystemExit('raspi4b সমর্থন_মান QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [বাইনেৰি]


def 해상도읽기(টেক্সট):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', টেক্সট):
        raise argparse.ArgumentTypeError('প্রতিচ্ছায়া_মান সজ্জা_মান: 1920x1080')
    너비, 높이 = map(int, টেক্সট.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('সমর্থন_মান ক্লিপ: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def কমান্ড(প্রতিচ্ছায়া_মান=(640, 480)):
    পটভূমি_মান = 모의기계()
    지원목록 = subprocess.check_output(পটভূমি_মান + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*প্রতিচ্ছায়া_মান))
    return পটভূমি_মান + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def সঞ্চালন():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 কাৰ্ণেল_মান. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 প্ৰস্থান_এপ্প্.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (হ_ষ্ট সমর্থন_মান 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 মাপ. 예: 1920x1080; ডিফ_ল্ট_মান 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. কী_মান 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 সংযোগ_স্থাপনা; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP নিয়ন্ত্রণ_মান 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT অগ্ৰসৰ_মান লক্ষ্য. 기본은 ip.conf의 IP; পৰিবৰ্তন_কৰক_মান 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ঠিকনা. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ঠিকনা: 외부 সংযোগ_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 সংযোগ_স্থাপনা: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI উৎস_ট্ৰি বাণ্ডল 중계 সঞ্চালন (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='বাণ্ডল 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    যুক্তি_শৃঙ্খলা = 인수해석기.parse_args()
    if যুক্তি_শৃঙ্খলা.remote:
        যুক্তি_শৃঙ্খলা.network=True
        যুক্তি_শৃঙ্খলা.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; পাছৱৰ্ড_মান: python3 সঁজুলিসমূহ/দূৰবৰ্তী_ছেটিংছ.py show'.format(যুক্তি_শৃঙ্খলা.network_host,যুক্তি_শৃঙ্খলা.network_host),flush=True)
    if যুক্তি_শৃঙ্খলা.pip and not যুক্তি_শৃঙ্খলা.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= যুক্তি_শৃঙ্খলা.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if যুক্তি_শৃঙ্খলা.forward and not যুক্তি_শৃঙ্খলা.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as সম্পদ_মান:
        if যুক্তি_শৃঙ্খলা.pip:
            from 꾸러미중계 import 꾸러미중계
            সম্পদ_মান.enter_context(꾸러미중계(যুক্তি_শৃঙ্খলা.pip_port, যুক্তি_শৃঙ্খলা.pip_cache, যুক্তি_শৃঙ্খলা.pip_offline))
            print('বাণ্ডল 중계: 127.0.0.1:' + str(যুক্তি_শৃঙ্খলা.pip_port), flush=True)
        চলাওক(যুক্তি_শৃঙ্খলা)


def চলাওক(যুক্তি_শৃঙ্খলা):
    if যুক্তি_শৃঙ্খলা.desktop:
        if যুক্তি_শৃঙ্খলা.vnc or যুক্তি_শৃঙ্খলা.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ডেস্কটপ_দর্শন import চলন_ডেস্কটপ
        raise SystemExit(চলন_ডেস্কটপ(যুক্তি_শৃঙ্খলা.port, নেটৱৰ্ক=যুক্তি_শৃঙ্খলা.network, 파일전송접속번호=যুক্তি_শৃঙ্খলা.ftp_port, 전달규칙들=যুক্তি_শৃঙ্খলা.forward, প্রতিচ্ছায়া_মান=যুক্তি_শৃঙ্খলা.resolution, অতিথি_ঠিকনা=যুক্তি_শৃঙ্খলা.guest_ip, হ_ষ্ট_ঠিকনা=যুক্তি_শৃঙ্খলা.network_host))
    বিকল্প = ['-display', যুক্তি_শৃঙ্খলা.display, '-serial', 'mon:stdio']
    if যুক্তি_শৃঙ্খলা.vnc:
        বিকল্প += ['-vnc', যুক্তি_শৃঙ্খলা.vnc]
    if যুক্তি_শৃঙ্খলা.network:
        from নেটৱৰ্ক_ব্ৰীজ import নেটৱৰ্ক_ব্ৰীজ
        with নেটৱৰ্ক_ব্ৰীজ(যুক্তি_শৃঙ্খলা.ftp_port, যুক্তি_শৃঙ্খলা.forward, অতিথি_ঠিকনা=যুক্তি_শৃঙ্খলা.guest_ip, হ_ষ্ট_ঠিকনা=যুক্তি_শৃঙ্খলা.network_host) as ব্ৰীজ:
            অৱস্থা_মান = subprocess.call(কমান্ড(যুক্তি_শৃঙ্খলা.resolution) + বিকল্প + ব্ৰীজ.전달인수())
            if ব্ৰীজ.ত্ৰুটি: raise SystemExit('network bridge: ' + ব্ৰীজ.ত্ৰুটি)
        raise SystemExit(অৱস্থা_মান)
    raise SystemExit(subprocess.call(কমান্ড(যুক্তি_শৃঙ্খলা.resolution) + বিকল্প))


if __name__ == '__main__':
    সঞ্চালন()
