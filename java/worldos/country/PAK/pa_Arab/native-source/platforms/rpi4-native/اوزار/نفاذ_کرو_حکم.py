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
    for راہ in _난수파일들:
        try:
            os.unlink(راہ)
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
    مہمان_b78e430d = 기준.parent / 'rpi4/build/host'
    적재기 = مہمان_b78e430d / 'lib/ld-musl-x86_64.so.1'
    مثنی = مہمان_b78e430d / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and مثنی.is_file():
        return [str(적재기), '--library-path', str(مہمان_b78e430d / 'usr/lib') + ':' + str(مہمان_b78e430d / 'lib'),
                str(مثنی), '-L', str(مہمان_b78e430d / 'usr/share/qemu')]
    مثنی = shutil.which('qemu-system-aarch64')
    if not مثنی:
        raise SystemExit('raspi4b مدد_قدر QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [مثنی]


def 해상도읽기(متن):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', متن):
        raise argparse.ArgumentTypeError('جزیات_کاری_قدر وضع_قدر: 1920x1080')
    너비, 높이 = map(int, متن.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('مدد_قدر تراشہ: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def حکم(جزیات_کاری_قدر=(640, 480)):
    پس_منظر_قدر = 모의기계()
    지원목록 = subprocess.check_output(پس_منظر_قدر + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*جزیات_کاری_قدر))
    return پس_منظر_قدر + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def چلاؤ():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 کرنل_قدر. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 خارج_کرو_ایپ.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (مہمان_b78e430d مدد_قدر 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 سائز. 예: 1920x1080; طےشدہ_قدر 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. کلید_قدر 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 جڑو; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP کنٹرول_قدر 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT آگے_قدر ہدف. 기본은 ip.conf의 IP; تبدیل_کرو_قدر 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 پتا. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN پتا: 외부 کنکشن_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 جڑو: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI ماخذ_شجرہ گٹھ 중계 چلاؤ (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='گٹھ 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    دلیل_ایرے = 인수해석기.parse_args()
    if دلیل_ایرے.remote:
        دلیل_ایرے.network=True
        دلیل_ایرے.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; لفظی_کنجی_قدر: python3 اوزار/بعيد_سیٹنگاں.py show'.format(دلیل_ایرے.network_host,دلیل_ایرے.network_host),flush=True)
    if دلیل_ایرے.pip and not دلیل_ایرے.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= دلیل_ایرے.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if دلیل_ایرے.forward and not دلیل_ایرے.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ذریعہ_قدر:
        if دلیل_ایرے.pip:
            from 꾸러미중계 import 꾸러미중계
            ذریعہ_قدر.enter_context(꾸러미중계(دلیل_ایرے.pip_port, دلیل_ایرے.pip_cache, دلیل_ایرے.pip_offline))
            print('گٹھ 중계: 127.0.0.1:' + str(دلیل_ایرے.pip_port), flush=True)
        نفاذ_کرو_ٹاسک(دلیل_ایرے)


def نفاذ_کرو_ٹاسک(دلیل_ایرے):
    if دلیل_ایرے.desktop:
        if دلیل_ایرے.vnc or دلیل_ایرے.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ڈیسک_ٹاپ_منظر import چلاؤ_ڈیسک_ٹاپ
        raise SystemExit(چلاؤ_ڈیسک_ٹاپ(دلیل_ایرے.port, نیٹ_ورک=دلیل_ایرے.network, 파일전송접속번호=دلیل_ایرے.ftp_port, 전달규칙들=دلیل_ایرے.forward, جزیات_کاری_قدر=دلیل_ایرے.resolution, مہمان_پتا_4bde7f91=دلیل_ایرے.guest_ip, مہمان_پتا=دلیل_ایرے.network_host))
    اختیار = ['-display', دلیل_ایرے.display, '-serial', 'mon:stdio']
    if دلیل_ایرے.vnc:
        اختیار += ['-vnc', دلیل_ایرے.vnc]
    if دلیل_ایرے.network:
        from نیٹ_ورک_برج import نیٹ_ورک_برج
        with نیٹ_ورک_برج(دلیل_ایرے.ftp_port, دلیل_ایرے.forward, مہمان_پتا_4bde7f91=دلیل_ایرے.guest_ip, مہمان_پتا=دلیل_ایرے.network_host) as برج:
            حالت_قدر = subprocess.call(حکم(دلیل_ایرے.resolution) + اختیار + برج.전달인수())
            if برج.نقص: raise SystemExit('network bridge: ' + برج.نقص)
        raise SystemExit(حالت_قدر)
    raise SystemExit(subprocess.call(حکم(دلیل_ایرے.resolution) + اختیار))


if __name__ == '__main__':
    چلاؤ()
