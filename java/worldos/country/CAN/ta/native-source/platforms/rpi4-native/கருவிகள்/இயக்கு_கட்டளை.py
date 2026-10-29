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

திட்டப்பணி_மூலம் = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for பாதை_2 in _난수파일들:
        try:
            os.unlink(பாதை_2)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as கோப்பின்_பெயர்:
        கோப்பின்_பெயர்.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(கோப்பின்_பெயர்.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(கோப்பின்_பெயர்.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    ஓம்பு = திட்டப்பணி_மூலம்.parent / 'rpi4/build/host'
    적재기 = ஓம்பு / 'lib/ld-musl-x86_64.so.1'
    பைனரி = ஓம்பு / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and பைனரி.is_file():
        return [str(적재기), '--library-path', str(ஓம்பு / 'usr/lib') + ':' + str(ஓம்பு / 'lib'),
                str(பைனரி), '-L', str(ஓம்பு / 'usr/share/qemu')]
    பைனரி = shutil.which('qemu-system-aarch64')
    if not பைனரி:
        raise SystemExit('raspi4b ஆதரவு_மதிப்பு QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [பைனரி]


def 해상도읽기(உரை):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', உரை):
        raise argparse.ArgumentTypeError('தெளிவுத்திறன்_மதிப்பு வடிவமை_மதிப்பு: 1920x1080')
    너비, 높이 = map(int, உரை.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('ஆதரவு_மதிப்பு கிளிப்: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def கட்டளை(தெளிவுத்திறன்_மதிப்பு=(640, 480)):
    பின்புல_மதிப்பு = 모의기계()
    지원목록 = subprocess.check_output(பின்புல_மதிப்பு + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*தெளிவுத்திறன்_மதிப்பு))
    return பின்புல_மதிப்பு + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(திட்டப்பணி_மூலம் / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def செயல்படுத்துக():
    பார்சர் = argparse.ArgumentParser(description='자체 Java Pi4 கரு_மதிப்பு. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 முடிவு_நிரல்.')
    பார்சர்.add_argument('--display', default='none', help='none 또는 gtk/sdl (ஓம்பு ஆதரவு_மதிப்பு 필요)')
    பார்சர்.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 அளவு. 예: 1920x1080; இயல்புநிலை_மதிப்பு 640x480')
    பார்சர்.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. சாவி_மதிப்பு 입력은 UART 터미널에서 합니다.')
    பார்சர்.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    பார்சர்.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    பார்சர்.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 இணைக்க; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    பார்சர்.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    பார்சர்.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP கட்டுப்பாடு_மதிப்பு 포트 (데이터 50000..50007)')
    பார்சர்.add_argument('--guest-ip', default=None, help='QEMU NAT பகிர்_மதிப்பு இலக்கு. 기본은 ip.conf의 IP; மாற்று_மதிப்பு_16f64fe4 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    பார்சர்.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 முகவரி. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN முகவரி: 외부 இணைப்பு_e05f319b')
    பார்சர்.add_argument('--forward', action='append', default=[], help='--network 추가 இணைக்க: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    பார்சர்.add_argument('--pip', action='store_true', help='PyPI மூலம்_மரம் மூட்டை 중계 செயல்படுத்துக (--network 필요, MicroPython 호환 소스만)')
    பார்சர்.add_argument('--pip-port', type=int, default=8027, help='மூட்டை 중계의 localhost TCP 포트')
    பார்சர்.add_argument('--pip-cache', type=Path, default=திட்டப்பணி_மூலம்/'build/pip-cache')
    பார்சர்.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    மதிப்புரு_கோவை = பார்சர்.parse_args()
    if மதிப்புரு_கோவை.remote:
        மதிப்புரு_கோவை.network=True
        மதிப்புரு_கோவை.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; கடவுச்சொல்_மதிப்பு: python3 கருவிகள்/தொலைநிலை_அமைப்புகள்.py show'.format(மதிப்புரு_கோவை.network_host,மதிப்புரு_கோவை.network_host),flush=True)
    if மதிப்புரு_கோவை.pip and not மதிப்புரு_கோவை.network: பார்சர்.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= மதிப்புரு_கோவை.pip_port <= 65535: பார்சர்.error('--pip-port 범위는 1~65535입니다.')
    if மதிப்புரு_கோவை.forward and not மதிப்புரு_கோவை.network: பார்சர்.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as வளம்_மதிப்பு:
        if மதிப்புரு_கோவை.pip:
            from 꾸러미중계 import 꾸러미중계
            வளம்_மதிப்பு.enter_context(꾸러미중계(மதிப்புரு_கோவை.pip_port, மதிப்புரு_கோவை.pip_cache, மதிப்புரு_கோவை.pip_offline))
            print('மூட்டை 중계: 127.0.0.1:' + str(மதிப்புரு_கோவை.pip_port), flush=True)
        செயற்படுத்துக(மதிப்புரு_கோவை)


def செயற்படுத்துக(மதிப்புரு_கோவை):
    if மதிப்புரு_கோவை.desktop:
        if மதிப்புரு_கோவை.vnc or மதிப்புரு_கோவை.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from டெஸ்க்டாப்_காட்சி import இயக்கு_டெஸ்க்டாப்
        raise SystemExit(இயக்கு_டெஸ்க்டாப்(மதிப்புரு_கோவை.port, பிணையம்=மதிப்புரு_கோவை.network, கோப்பு_இடமாற்று_முனைய_எண்=மதிப்புரு_கோவை.ftp_port, 전달규칙들=மதிப்புரு_கோவை.forward, தெளிவுத்திறன்_மதிப்பு=மதிப்புரு_கோவை.resolution, விருந்தினர்_முகவரி=மதிப்புரு_கோவை.guest_ip, ஓம்பு_முகவரி=மதிப்புரு_கோவை.network_host))
    விருப்பங்கள் = ['-display', மதிப்புரு_கோவை.display, '-serial', 'mon:stdio']
    if மதிப்புரு_கோவை.vnc:
        விருப்பங்கள் += ['-vnc', மதிப்புரு_கோவை.vnc]
    if மதிப்புரு_கோவை.network:
        from பிணையம்_பிரிட்ஜ் import பிணையம்_பிரிட்ஜ்
        with பிணையம்_பிரிட்ஜ்(மதிப்புரு_கோவை.ftp_port, மதிப்புரு_கோவை.forward, விருந்தினர்_முகவரி=மதிப்புரு_கோவை.guest_ip, ஓம்பு_முகவரி=மதிப்புரு_கோவை.network_host) as பிரிட்ஜ்:
            நிலை_மதிப்பு_e10195a1 = subprocess.call(கட்டளை(மதிப்புரு_கோவை.resolution) + விருப்பங்கள் + பிரிட்ஜ்.전달인수())
            if பிரிட்ஜ்.பிழை: raise SystemExit('network bridge: ' + பிரிட்ஜ்.பிழை)
        raise SystemExit(நிலை_மதிப்பு_e10195a1)
    raise SystemExit(subprocess.call(கட்டளை(மதிப்புரு_கோவை.resolution) + விருப்பங்கள்))


if __name__ == '__main__':
    செயல்படுத்துக()
