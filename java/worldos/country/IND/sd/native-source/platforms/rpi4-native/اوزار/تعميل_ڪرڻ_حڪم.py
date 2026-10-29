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
    for راههه in _난수파일들:
        try:
            os.unlink(راههه)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as فائل:
        فائل.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(فائل.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(فائل.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    مهمان = 기준.parent / 'rpi4/build/host'
    적재기 = مهمان / 'lib/ld-musl-x86_64.so.1'
    ٻٽو = مهمان / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and ٻٽو.is_file():
        return [str(적재기), '--library-path', str(مهمان / 'usr/lib') + ':' + str(مهمان / 'lib'),
                str(ٻٽو), '-L', str(مهمان / 'usr/share/qemu')]
    ٻٽو = shutil.which('qemu-system-aarch64')
    if not ٻٽو:
        raise SystemExit('raspi4b معاونت_قدر QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ٻٽو]


def 해상도읽기(متن):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', متن):
        raise argparse.ArgumentTypeError('جزيت_ڪاري_قدر وضع_قدر: 1920x1080')
    너비, 높이 = map(int, متن.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('معاونت_قدر تراشه: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def حڪم(جزيت_ڪاري_قدر=(640, 480)):
    پس_منظر_قدر = 모의기계()
    지원목록 = subprocess.check_output(پس_منظر_قدر + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*جزيت_ڪاري_قدر))
    return پس_منظر_قدر + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def هلائڻ():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 ڪرنل_قدر. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 خارج_ڪريو_ائپ.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (مهمان معاونت_قدر 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 سائيز. 예: 1920x1080; طئي_ٿيل_ملهه 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. ڪليد_قدر 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 ڪنيڪٽ; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP ڪنٽرول_قدر 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT اڳيان_قدر هدف. 기본은 ip.conf의 IP; تبديل_ڪريو_قدر 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 پتو. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN پتو: 외부 ڪنيڪشن_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 ڪنيڪٽ: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI ماخذ_شجرو بنڊل 중계 هلائڻ (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='بنڊل 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    دليل_ترتيب = 인수해석기.parse_args()
    if دليل_ترتيب.remote:
        دليل_ترتيب.network=True
        دليل_ترتيب.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; پاس_ورڊ_قدر: python3 اوزار/بعيد_سيٽنگون.py show'.format(دليل_ترتيب.network_host,دليل_ترتيب.network_host),flush=True)
    if دليل_ترتيب.pip and not دليل_ترتيب.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= دليل_ترتيب.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if دليل_ترتيب.forward and not دليل_ترتيب.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ذريعو_قدر:
        if دليل_ترتيب.pip:
            from 꾸러미중계 import 꾸러미중계
            ذريعو_قدر.enter_context(꾸러미중계(دليل_ترتيب.pip_port, دليل_ترتيب.pip_cache, دليل_ترتيب.pip_offline))
            print('بنڊل 중계: 127.0.0.1:' + str(دليل_ترتيب.pip_port), flush=True)
        تعميل_ڪرڻ_ٽاسڪ(دليل_ترتيب)


def تعميل_ڪرڻ_ٽاسڪ(دليل_ترتيب):
    if دليل_ترتيب.desktop:
        if دليل_ترتيب.vnc or دليل_ترتيب.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ڊيسڪٽاپ_منظر import هلائڻ_ڊيسڪٽاپ
        raise SystemExit(هلائڻ_ڊيسڪٽاپ(دليل_ترتيب.port, نيٽ_ورڪ=دليل_ترتيب.network, 파일전송접속번호=دليل_ترتيب.ftp_port, 전달규칙들=دليل_ترتيب.forward, جزيت_ڪاري_قدر=دليل_ترتيب.resolution, 게스트주소=دليل_ترتيب.guest_ip, مهمان_پتو=دليل_ترتيب.network_host))
    اختيار = ['-display', دليل_ترتيب.display, '-serial', 'mon:stdio']
    if دليل_ترتيب.vnc:
        اختيار += ['-vnc', دليل_ترتيب.vnc]
    if دليل_ترتيب.network:
        from 통신다리 import 통신다리
        with 통신다리(دليل_ترتيب.ftp_port, دليل_ترتيب.forward, 게스트주소=دليل_ترتيب.guest_ip, مهمان_پتو=دليل_ترتيب.network_host) as 연결다리:
            حالت_قدر = subprocess.call(حڪم(دليل_ترتيب.resolution) + اختيار + 연결다리.전달인수())
            if 연결다리.نقص: raise SystemExit('network bridge: ' + 연결다리.نقص)
        raise SystemExit(حالت_قدر)
    raise SystemExit(subprocess.call(حڪم(دليل_ترتيب.resolution) + اختيار))


if __name__ == '__main__':
    هلائڻ()
