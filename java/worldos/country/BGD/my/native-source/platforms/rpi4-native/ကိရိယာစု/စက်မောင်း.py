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

စီမံကိန်းအမြစ် = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for လမ်း in _난수파일들:
        try:
            os.unlink(လမ်း)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ဖိုင်:
        ဖိုင်.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(ဖိုင်.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ဖိုင်.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    အိမ်ရှင် = စီမံကိန်းအမြစ်.parent / 'rpi4/build/host'
    တင်သွင်းသူ = အိမ်ရှင် / 'lib/ld-musl-x86_64.so.1'
    ဒွိစနစ် = အိမ်ရှင် / 'usr/bin/qemu-system-aarch64'
    if တင်သွင်းသူ.is_file() and ဒွိစနစ်.is_file():
        return [str(တင်သွင်းသူ), '--library-path', str(အိမ်ရှင် / 'usr/lib') + ':' + str(အိမ်ရှင် / 'lib'),
                str(ဒွိစနစ်), '-L', str(အိမ်ရှင် / 'usr/share/qemu')]
    ဒွိစနစ် = shutil.which('qemu-system-aarch64')
    if not ဒွိစနစ်:
        raise SystemExit('raspi4b ထောက်ပံ့မှုတန်ဖိုး QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ဒွိစနစ်]


def ကြည်လင်ပြတ်သားမှုဖတ်(စာသား):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', စာသား):
        raise argparse.ArgumentTypeError('ကြည်လင်ပြတ်သားမှုတန်ဖိုး ပုံစံတန်ဖိုး: 1920x1080')
    အနံတန်ဖိုး, အမြင့်တန်ဖိုး = map(int, စာသား.split('x'))
    if not (640 <= အနံတန်ဖိုး <= 1920 and 480 <= အမြင့်တန်ဖိုး <= 1080):
        raise argparse.ArgumentTypeError('ထောက်ပံ့မှုတန်ဖိုး ဖြတ်နယ်ပယ်: အနံတန်ဖိုး 640~1920, အမြင့်တန်ဖိုး 480~1080')
    return အနံတန်ဖိုး, အမြင့်တန်ဖိုး


def အမိန့်(ကြည်လင်ပြတ်သားမှုတန်ဖိုး=(640, 480)):
    နောက်ခံတန်ဖိုး = 모의기계()
    지원목록 = subprocess.check_output(နောက်ခံတန်ဖိုး + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    အနံတန်ဖိုး, အမြင့်တန်ဖိုး = ကြည်လင်ပြတ်သားမှုဖတ်('{}x{}'.format(*ကြည်လင်ပြတ်သားမှုတန်ဖိုး))
    return နောက်ခံတန်ဖိုး + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(အနံတန်ဖိုး),
                   '-global', 'bcm2835-fb.yres=' + str(အမြင့်တန်ဖိုး), '-kernel',
                   str(စီမံကိန်းအမြစ် / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def လုပ်ဆောင်():
    인수해석기 = argparse.ArgumentParser(description='ကိုယ်ပိုင် Java Pi4 အူတိုင်တန်ဖိုး. အစဉ်ဆက်တန်ဖိုး 셸은 Ctrl+A X, --desktop은 Ctrl+C로 ထွက်ပရိုဂရမ်.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (အိမ်ရှင် ထောက်ပံ့မှုတန်ဖိုး 필요)')
    인수해석기.add_argument('--resolution', type=ကြည်လင်ပြတ်သားမှုဖတ်, default=(640, 480), help='စက်တင် မျက်နှာပြင် အရွယ်. 예: 1920x1080; မူလသတ်မှတ်တန်ဖိုး 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC စက်ပစ္စည်းဆက်သွယ်ပေါက် 5902. သော့တန်ဖိုး 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC စက်ပစ္စည်းဆက်သွယ်ပေါက်')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 ချိတ်ဆက်; --desktop과 함께 သုံးစွဲမှု 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP ထိန်းချုပ်တန်ဖိုး စက်ပစ္စည်းဆက်သွယ်ပေါက် (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT ဆက်ပို့တန်ဖိုး ဦးတည်ချက်တန်ဖိုး. 기본은 ip.conf의 IP; တန်ဖိုးပြောင်း 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT တန်ဖိုးလက်ခံရယူ လိပ်စာ. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN လိပ်စာ: ပြင်ပတန်ဖိုး ချိတ်ဆက်မှု')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network အချက်နောက်တွဲ ချိတ်ဆက်: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ အထုပ် 중계 လုပ်ဆောင် (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='အထုပ် 중계의 localhost TCP စက်ပစ္စည်းဆက်သွယ်ပေါက်')
    인수해석기.add_argument('--pip-cache', type=Path, default=စီမံကိန်းအမြစ်/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 ဖြန့်ချိမှုတန်ဖိုး 파일만 제공')
    ပေးအချက်အခင်းအကျင်း = 인수해석기.parse_args()
    if ပေးအချက်အခင်းအကျင်း.remote:
        ပေးအချက်အခင်းအကျင်း.network=True
        ပေးအချက်အခင်းအကျင်း.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; စကားဝှက်တန်ဖိုး: python3 ကိရိယာစု/အဝေးသတ်မှတ်ချက်.py show'.format(ပေးအချက်အခင်းအကျင်း.network_host,ပေးအချက်အခင်းအကျင်း.network_host),flush=True)
    if ပေးအချက်အခင်းအကျင်း.pip and not ပေးအချက်အခင်းအကျင်း.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= ပေးအချက်အခင်းအကျင်း.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if ပေးအချက်အခင်းအကျင်း.forward and not ပေးအချက်အခင်းအကျင်း.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as အရင်းအမြစ်တန်ဖိုး:
        if ပေးအချက်အခင်းအကျင်း.pip:
            from 꾸러미중계 import 꾸러미중계
            အရင်းအမြစ်တန်ဖိုး.enter_context(꾸러미중계(ပေးအချက်အခင်းအကျင်း.pip_port, ပေးအချက်အခင်းအကျင်း.pip_cache, ပေးအချက်အခင်းအကျင်း.pip_offline))
            print('အထုပ် 중계: 127.0.0.1:' + str(ပေးအချက်အခင်းအကျင်း.pip_port), flush=True)
        အလုပ်လုပ်ဆောင်(ပေးအချက်အခင်းအကျင်း)


def အလုပ်လုပ်ဆောင်(ပေးအချက်အခင်းအကျင်း):
    if ပေးအချက်အခင်းအကျင်း.desktop:
        if ပေးအချက်အခင်းအကျင်း.vnc or ပေးအချက်အခင်းအကျင်း.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from အလုပ်မျက်နှာပြင်ရှုမြင်ရာ import အလုပ်မျက်နှာပြင်စက်မောင်း
        raise SystemExit(အလုပ်မျက်နှာပြင်စက်မောင်း(ပေးအချက်အခင်းအကျင်း.port, ကွန်ရက်သုံးမှု=ပေးအချက်အခင်းအကျင်း.network, ဖိုင်လွှဲပြောင်းဆက်သွယ်ပေါက်ကိန်း=ပေးအချက်အခင်းအကျင်း.ftp_port, 전달규칙들=ပေးအချက်အခင်းအကျင်း.forward, ကြည်လင်ပြတ်သားမှုတန်ဖိုး=ပေးအချက်အခင်းအကျင်း.resolution, ဧည့်သည်လိပ်စာ=ပေးအချက်အခင်းအကျင်း.guest_ip, အိမ်ရှင်လိပ်စာ=ပေးအချက်အခင်းအကျင်း.network_host))
    선택사항 = ['-display', ပေးအချက်အခင်းအကျင်း.display, '-serial', 'mon:stdio']
    if ပေးအချက်အခင်းအကျင်း.vnc:
        선택사항 += ['-vnc', ပေးအချက်အခင်းအကျင်း.vnc]
    if ပေးအချက်အခင်းအကျင်း.network:
        from ကွန်ရက်တံတား import ကွန်ရက်တံတား
        with ကွန်ရက်တံတား(ပေးအချက်အခင်းအကျင်း.ftp_port, ပေးအချက်အခင်းအကျင်း.forward, ဧည့်သည်လိပ်စာ=ပေးအချက်အခင်းအကျင်း.guest_ip, အိမ်ရှင်လိပ်စာ=ပေးအချက်အခင်းအကျင်း.network_host) as တံတား:
            အခြေအနေတန်ဖိုး = subprocess.call(အမိန့်(ပေးအချက်အခင်းအကျင်း.resolution) + 선택사항 + တံတား.전달인수())
            if တံတား.အမှား: raise SystemExit('network bridge: ' + တံတား.အမှား)
        raise SystemExit(အခြေအနေတန်ဖိုး)
    raise SystemExit(subprocess.call(အမိန့်(ပေးအချက်အခင်းအကျင်း.resolution) + 선택사항))


if __name__ == '__main__':
    လုပ်ဆောင်()
