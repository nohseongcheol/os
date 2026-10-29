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

يعرض_جذر = Path(__file__).resolve().parents[1]
عشوائي_الملفات = []


def _난수정리():
    for مسار in عشوائي_الملفات:
        try:
            os.unlink(مسار)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ملف:
        ملف.write(b'JKRENRG1' + os.urandom(32))
        عشوائي_الملفات.append(ملف.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ملف.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    مضيف = يعرض_جذر.parent / 'rpi4/build/host'
    أداة_تحميل = مضيف / 'lib/ld-musl-x86_64.so.1'
    ثنائي = مضيف / 'usr/bin/qemu-system-aarch64'
    if أداة_تحميل.is_file() and ثنائي.is_file():
        return [str(أداة_تحميل), '--library-path', str(مضيف / 'usr/lib') + ':' + str(مضيف / 'lib'),
                str(ثنائي), '-L', str(مضيف / 'usr/share/qemu')]
    ثنائي = shutil.which('qemu-system-aarch64')
    if not ثنائي:
        raise SystemExit('raspi4b دعم_قيمة QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ثنائي]


def يقرأ_دقة(نص):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', نص):
        raise argparse.ArgumentTypeError('دقة_قيمة ينسق_قيمة: 1920x1080')
    너비, ارتفاع_قيمة = map(int, نص.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= ارتفاع_قيمة <= 1080):
        raise argparse.ArgumentTypeError('دعم_قيمة يقص: 너비 640~1920, ارتفاع_قيمة 480~1080')
    return 너비, ارتفاع_قيمة


def أمر(دقة_قيمة=(640, 480)):
    خلفية_قيمة = 모의기계()
    지원목록 = subprocess.check_output(خلفية_قيمة + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, ارتفاع_قيمة = يقرأ_دقة('{}x{}'.format(*دقة_قيمة))
    return خلفية_قيمة + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(ارتفاع_قيمة), '-kernel',
                   str(يعرض_جذر / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def تشغيل():
    المحلل = argparse.ArgumentParser(description='ذاتي Java Pi4 نواة_قيمة. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 خروج_تطبيق.')
    المحلل.add_argument('--display', default='none', help='none 또는 gtk/sdl (مضيف دعم_قيمة 필요)')
    المحلل.add_argument('--resolution', type=يقرأ_دقة, default=(640, 480), help='إقلاع_الآلة 화면 حجم. 예: 1920x1080; قيمة_افتراضية 640x480')
    المحلل.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC أجهزة_منفذ 5902. مفتاح_قيمة 입력은 UART 터미널에서 합니다.')
    المحلل.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    المحلل.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC أجهزة_منفذ')
    المحلل.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 اتصال; --desktop과 함께 يستخدم_قيمة 가능; 게스트에서 ftpd start')
    المحلل.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    المحلل.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP تحكم_قيمة أجهزة_منفذ (데이터 50000..50007)')
    المحلل.add_argument('--guest-ip', default=None, help='QEMU NAT تحويل_قيمة_24592b8a الهدف. 기본은 ip.conf의 IP; يغيّر_قيمة 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    المحلل.add_argument('--network-host', default='127.0.0.1', help='NAT يستلم_قيمة عنوان. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN عنوان: خارجي_قيمة صديق_e05f319b')
    المحلل.add_argument('--forward', action='append', default=[], help='--network إلحاق_إدخال اتصال: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    المحلل.add_argument('--pip', action='store_true', help='PyPI مصدر_شجرة يُجمع 중계 تشغيل (--network 필요, MicroPython 호환 소스만)')
    المحلل.add_argument('--pip-port', type=int, default=8027, help='يُجمع 중계의 localhost TCP أجهزة_منفذ')
    المحلل.add_argument('--pip-cache', type=Path, default=يعرض_جذر/'build/pip-cache')
    المحلل.add_argument('--pip-offline', action='store_true', help='이미 받은 توزيع_قيمة 파일만 제공')
    وسيطة_صفيف = المحلل.parse_args()
    if وسيطة_صفيف.remote:
        وسيطة_صفيف.network=True
        وسيطة_صفيف.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; رمز_الوصول_قيمة: python3 أدوات/بعيد_إعدادات.py show'.format(وسيطة_صفيف.network_host,وسيطة_صفيف.network_host),flush=True)
    if وسيطة_صفيف.pip and not وسيطة_صفيف.network: المحلل.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= وسيطة_صفيف.pip_port <= 65535: المحلل.error('--pip-port 범위는 1~65535입니다.')
    if وسيطة_صفيف.forward and not وسيطة_صفيف.network: المحلل.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as مصدر_قيمة:
        if وسيطة_صفيف.pip:
            from 꾸러미중계 import 꾸러미중계
            مصدر_قيمة.enter_context(꾸러미중계(وسيطة_صفيف.pip_port, وسيطة_صفيف.pip_cache, وسيطة_صفيف.pip_offline))
            print('يُجمع 중계: 127.0.0.1:' + str(وسيطة_صفيف.pip_port), flush=True)
        تنفيذ(وسيطة_صفيف)


def تنفيذ(وسيطة_صفيف):
    if وسيطة_صفيف.desktop:
        if وسيطة_صفيف.vnc or وسيطة_صفيف.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from سطح_مكتب_عرض import يشغّل_سطح_مكتب
        raise SystemExit(يشغّل_سطح_مكتب(وسيطة_صفيف.port, شبكة=وسيطة_صفيف.network, نقل_الملفات_رقم_المنفذ=وسيطة_صفيف.ftp_port, 전달규칙들=وسيطة_صفيف.forward, دقة_قيمة=وسيطة_صفيف.resolution, ضيف_عنوان=وسيطة_صفيف.guest_ip, مضيف_عنوان=وسيطة_صفيف.network_host))
    خيارات = ['-display', وسيطة_صفيف.display, '-serial', 'mon:stdio']
    if وسيطة_صفيف.vnc:
        خيارات += ['-vnc', وسيطة_صفيف.vnc]
    if وسيطة_صفيف.network:
        from جسر_3de4fe3a import جسر_3de4fe3a
        with جسر_3de4fe3a(وسيطة_صفيف.ftp_port, وسيطة_صفيف.forward, ضيف_عنوان=وسيطة_صفيف.guest_ip, مضيف_عنوان=وسيطة_صفيف.network_host) as جسر:
            حالة_قيمة = subprocess.call(أمر(وسيطة_صفيف.resolution) + خيارات + جسر.전달인수())
            if جسر.خطأ: raise SystemExit('network bridge: ' + جسر.خطأ)
        raise SystemExit(حالة_قيمة)
    raise SystemExit(subprocess.call(أمر(وسيطة_صفيف.resolution) + خيارات))


if __name__ == '__main__':
    تشغيل()
