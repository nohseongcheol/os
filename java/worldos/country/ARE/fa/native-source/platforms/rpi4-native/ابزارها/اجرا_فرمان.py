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

نمایش_دادن_جذر = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for مسیر in _난수파일들:
        try:
            os.unlink(مسیر)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as پرونده:
        پرونده.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(پرونده.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(پرونده.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    میزبان = نمایش_دادن_جذر.parent / 'rpi4/build/host'
    적재기 = میزبان / 'lib/ld-musl-x86_64.so.1'
    دودویی = میزبان / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and دودویی.is_file():
        return [str(적재기), '--library-path', str(میزبان / 'usr/lib') + ':' + str(میزبان / 'lib'),
                str(دودویی), '-L', str(میزبان / 'usr/share/qemu')]
    دودویی = shutil.which('qemu-system-aarch64')
    if not دودویی:
        raise SystemExit('raspi4b پشتیبان_مقدار QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [دودویی]


def 해상도읽기(متن):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', متن):
        raise argparse.ArgumentTypeError('دقت_مقدار قالب_مقدار: 1920x1080')
    너비, 높이 = map(int, متن.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('پشتیبان_مقدار کلیپ: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def فرمان(دقت_مقدار=(640, 480)):
    زمینه_مقدار_0764f371 = 모의기계()
    지원목록 = subprocess.check_output(زمینه_مقدار_0764f371 + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*دقت_مقدار))
    return زمینه_مقدار_0764f371 + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(نمایش_دادن_جذر / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def اجرا_2():
    مفسر = argparse.ArgumentParser(description='بومی Java Pi4 هسته_مقدار. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 خروج_برنامه.')
    مفسر.add_argument('--display', default='none', help='none 또는 gtk/sdl (میزبان پشتیبان_مقدار 필요)')
    مفسر.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 اندازه. 예: 1920x1080; مقدار_پیش_فرض 640x480')
    مفسر.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. کلید_مقدار 입력은 UART 터미널에서 합니다.')
    مفسر.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    مفسر.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    مفسر.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 اتصال; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    مفسر.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    مفسر.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP کنترل_مقدار 포트 (데이터 50000..50007)')
    مفسر.add_argument('--guest-ip', default=None, help='QEMU NAT هدایت_مقدار_24592b8a هدف. 기본은 ip.conf의 IP; تغییر_مقدار 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    مفسر.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 آدرس. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN آدرس: 외부 اتصال_e05f319b')
    مفسر.add_argument('--forward', action='append', default=[], help='--network 추가 اتصال: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    مفسر.add_argument('--pip', action='store_true', help='PyPI منبع_درخت دسته_کردن 중계 اجرا_2 (--network 필요, MicroPython 호환 소스만)')
    مفسر.add_argument('--pip-port', type=int, default=8027, help='دسته_کردن 중계의 localhost TCP 포트')
    مفسر.add_argument('--pip-cache', type=Path, default=نمایش_دادن_جذر/'build/pip-cache')
    مفسر.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    آرگومان_آرايه = مفسر.parse_args()
    if آرگومان_آرايه.remote:
        آرگومان_آرايه.network=True
        آرگومان_آرايه.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; رمز_عبور_مقدار: python3 ابزارها/راه_دور_تنظیمات.py show'.format(آرگومان_آرايه.network_host,آرگومان_آرايه.network_host),flush=True)
    if آرگومان_آرايه.pip and not آرگومان_آرايه.network: مفسر.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= آرگومان_آرايه.pip_port <= 65535: مفسر.error('--pip-port 범위는 1~65535입니다.')
    if آرگومان_آرايه.forward and not آرگومان_آرايه.network: مفسر.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as منبع_مقدار:
        if آرگومان_آرايه.pip:
            from 꾸러미중계 import 꾸러미중계
            منبع_مقدار.enter_context(꾸러미중계(آرگومان_آرايه.pip_port, آرگومان_آرايه.pip_cache, آرگومان_آرايه.pip_offline))
            print('دسته_کردن 중계: 127.0.0.1:' + str(آرگومان_آرايه.pip_port), flush=True)
        اجرا(آرگومان_آرايه)


def اجرا(آرگومان_آرايه):
    if آرگومان_آرايه.desktop:
        if آرگومان_آرايه.vnc or آرگومان_آرايه.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from رایانه_نما import اجرا_رایانه
        raise SystemExit(اجرا_رایانه(آرگومان_آرايه.port, شبکه=آرگومان_آرايه.network, فایل_انتقال_شماره_درگاه=آرگومان_آرايه.ftp_port, 전달규칙들=آرگومان_آرايه.forward, دقت_مقدار=آرگومان_آرايه.resolution, مهمان_آدرس=آرگومان_آرايه.guest_ip, میزبان_آدرس=آرگومان_آرايه.network_host))
    گزینه_ها = ['-display', آرگومان_آرايه.display, '-serial', 'mon:stdio']
    if آرگومان_آرايه.vnc:
        گزینه_ها += ['-vnc', آرگومان_آرايه.vnc]
    if آرگومان_آرايه.network:
        from شبکه_پل import شبکه_پل
        with شبکه_پل(آرگومان_آرايه.ftp_port, آرگومان_آرايه.forward, مهمان_آدرس=آرگومان_آرايه.guest_ip, میزبان_آدرس=آرگومان_آرايه.network_host) as پل:
            وضعیت_مقدار = subprocess.call(فرمان(آرگومان_آرايه.resolution) + گزینه_ها + پل.전달인수())
            if پل.خطا: raise SystemExit('network bridge: ' + پل.خطا)
        raise SystemExit(وضعیت_مقدار)
    raise SystemExit(subprocess.call(فرمان(آرگومان_آرايه.resolution) + گزینه_ها))


if __name__ == '__main__':
    اجرا_2()
