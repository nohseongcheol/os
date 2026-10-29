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

לשקף_בסיס = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for נתיב in _난수파일들:
        try:
            os.unlink(נתיב)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as קובץ:
        קובץ.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(קובץ.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(קובץ.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    ארח = לשקף_בסיס.parent / 'rpi4/build/host'
    מטען = ארח / 'lib/ld-musl-x86_64.so.1'
    בינארי = ארח / 'usr/bin/qemu-system-aarch64'
    if מטען.is_file() and בינארי.is_file():
        return [str(מטען), '--library-path', str(ארח / 'usr/lib') + ':' + str(ארח / 'lib'),
                str(בינארי), '-L', str(ארח / 'usr/share/qemu')]
    בינארי = shutil.which('qemu-system-aarch64')
    if not בינארי:
        raise SystemExit('raspi4b תמך_ערך QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [בינארי]


def 해상도읽기(טקסט):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', טקסט):
        raise argparse.ArgumentTypeError('רזולוציה_ערך לעצב_ערך: 1920x1080')
    너비, גובה_ערך = map(int, טקסט.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= גובה_ערך <= 1080):
        raise argparse.ArgumentTypeError('תמך_ערך לגזור: 너비 640~1920, גובה_ערך 480~1080')
    return 너비, גובה_ערך


def פקודה(רזולוציה_ערך=(640, 480)):
    טפט_ערך = 모의기계()
    지원목록 = subprocess.check_output(טפט_ערך + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, גובה_ערך = 해상도읽기('{}x{}'.format(*רזולוציה_ערך))
    return טפט_ערך + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(גובה_ערך), '-kernel',
                   str(לשקף_בסיס / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def הפעלה():
    מנתח = argparse.ArgumentParser(description='עצמי Java Pi4 ליבה_ערך. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 יציאה_תוכנית.')
    מנתח.add_argument('--display', default='none', help='none 또는 gtk/sdl (ארח תמך_ערך 필요)')
    מנתח.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 גודל. 예: 1920x1080; ערך_ברירת_מחדל 640x480')
    מנתח.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC חומרה_הסב 5902. מקש_ערך 입력은 UART 터미널에서 합니다.')
    מנתח.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    מנתח.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC חומרה_הסב')
    מנתח.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 חיבור; --desktop과 함께 שימוש_ערך 가능; 게스트에서 ftpd start')
    מנתח.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    מנתח.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP פקד_ערך חומרה_הסב (데이터 50000..50007)')
    מנתח.add_argument('--guest-ip', default=None, help='QEMU NAT העבר_ערך_24592b8a יעד. 기본은 ip.conf의 IP; שנה_ערך 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    מנתח.add_argument('--network-host', default='127.0.0.1', help='NAT לקבל_ערך_cef4d8ab למען. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN למען: חיצוני_ערך קשר_e05f319b')
    מנתח.add_argument('--forward', action='append', default=[], help='--network צירוף_ערך_b73accca חיבור: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    מנתח.add_argument('--pip', action='store_true', help='PyPI מקור_עץ חבילה 중계 הפעלה (--network 필요, MicroPython 호환 소스만)')
    מנתח.add_argument('--pip-port', type=int, default=8027, help='חבילה 중계의 localhost TCP חומרה_הסב')
    מנתח.add_argument('--pip-cache', type=Path, default=לשקף_בסיס/'build/pip-cache')
    מנתח.add_argument('--pip-offline', action='store_true', help='이미 받은 הפצה_ערך 파일만 제공')
    ארגומנט_מערך = מנתח.parse_args()
    if ארגומנט_מערך.remote:
        ארגומנט_מערך.network=True
        ארגומנט_מערך.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; סיסמה_ערך: python3 כלים/מרוחק_הגדרות.py show'.format(ארגומנט_מערך.network_host,ארגומנט_מערך.network_host),flush=True)
    if ארגומנט_מערך.pip and not ארגומנט_מערך.network: מנתח.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= ארגומנט_מערך.pip_port <= 65535: מנתח.error('--pip-port 범위는 1~65535입니다.')
    if ארגומנט_מערך.forward and not ארגומנט_מערך.network: מנתח.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as משאב_ערך:
        if ארגומנט_מערך.pip:
            from 꾸러미중계 import 꾸러미중계
            משאב_ערך.enter_context(꾸러미중계(ארגומנט_מערך.pip_port, ארגומנט_מערך.pip_cache, ארגומנט_מערך.pip_offline))
            print('חבילה 중계: 127.0.0.1:' + str(ארגומנט_מערך.pip_port), flush=True)
        בצע(ארגומנט_מערך)


def בצע(ארגומנט_מערך):
    if ארגומנט_מערך.desktop:
        if ארגומנט_מערך.vnc or ארגומנט_מערך.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from מחשב_שולחני_הצג import להפעיל_מחשב_שולחני
        raise SystemExit(להפעיל_מחשב_שולחני(ארגומנט_מערך.port, רשת=ארגומנט_מערך.network, העברת_קבצים_מספר_יציאה=ארגומנט_מערך.ftp_port, 전달규칙들=ארגומנט_מערך.forward, רזולוציה_ערך=ארגומנט_מערך.resolution, אורח_למען=ארגומנט_מערך.guest_ip, ארח_למען=ארגומנט_מערך.network_host))
    אפשרויות = ['-display', ארגומנט_מערך.display, '-serial', 'mon:stdio']
    if ארגומנט_מערך.vnc:
        אפשרויות += ['-vnc', ארגומנט_מערך.vnc]
    if ארגומנט_מערך.network:
        from גשר_3de4fe3a import גשר_3de4fe3a
        with גשר_3de4fe3a(ארגומנט_מערך.ftp_port, ארגומנט_מערך.forward, אורח_למען=ארגומנט_מערך.guest_ip, ארח_למען=ארגומנט_מערך.network_host) as גשר:
            מצב_ערך = subprocess.call(פקודה(ארגומנט_מערך.resolution) + אפשרויות + גשר.전달인수())
            if גשר.שגיאה: raise SystemExit('network bridge: ' + גשר.שגיאה)
        raise SystemExit(מצב_ערך)
    raise SystemExit(subprocess.call(פקודה(ארגומנט_מערך.resolution) + אפשרויות))


if __name__ == '__main__':
    הפעלה()
