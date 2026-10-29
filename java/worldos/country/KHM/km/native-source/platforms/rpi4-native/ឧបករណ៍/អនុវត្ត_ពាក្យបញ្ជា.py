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

បញ្ចាំង_ឬស = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for ផ្លូវ in _난수파일들:
        try:
            os.unlink(ផ្លូវ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ឯកសារ:
        ឯកសារ.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(ឯកសារ.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ឯកសារ.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    ហូស = បញ្ចាំង_ឬស.parent / 'rpi4/build/host'
    적재기 = ហូស / 'lib/ld-musl-x86_64.so.1'
    គោលពីរ = ហូស / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and គោលពីរ.is_file():
        return [str(적재기), '--library-path', str(ហូស / 'usr/lib') + ':' + str(ហូស / 'lib'),
                str(គោលពីរ), '-L', str(ហូស / 'usr/share/qemu')]
    គោលពីរ = shutil.which('qemu-system-aarch64')
    if not គោលពីរ:
        raise SystemExit('raspi4b ទម្រ_តំលៃ QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [គោលពីរ]


def 해상도읽기(អត្ថបទ):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', អត្ថបទ):
        raise argparse.ArgumentTypeError('គុណភាព_បង្ហាញ_តំលៃ ទំរង់_តំលៃ: 1920x1080')
    너비, 높이 = map(int, អត្ថបទ.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('ទម្រ_តំលៃ មេឌៀខ្លីៗ: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def ពាក្យ_បញ្ជា(គុណភាព_បង្ហាញ_តំលៃ=(640, 480)):
    គំរូដែសថប_តំលៃ = 모의기계()
    지원목록 = subprocess.check_output(គំរូដែសថប_តំលៃ + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*គុណភាព_បង្ហាញ_តំលៃ))
    return គំរូដែសថប_តំលៃ + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(បញ្ចាំង_ឬស / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def រត់():
    មុខងារ_ញែក = argparse.ArgumentParser(description='자체 Java Pi4 ខឺណេល_តំលៃ. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 ចេញ_កម្មវិធី.')
    មុខងារ_ញែក.add_argument('--display', default='none', help='none 또는 gtk/sdl (ហូស ទម្រ_តំលៃ 필요)')
    មុខងារ_ញែក.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 ដាក់ទំហំ. 예: 1920x1080; តំលៃស្វ័យប្រវត្តិ 640x480')
    មុខងារ_ញែក.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. ឃី_តំលៃ 입력은 UART 터미널에서 합니다.')
    មុខងារ_ញែក.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    មុខងារ_ញែក.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    មុខងារ_ញែក.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 ភ្ជាប់; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    មុខងារ_ញែក.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    មុខងារ_ញែក.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP អង្គបញ្ជា_តំលៃ 포트 (데이터 50000..50007)')
    មុខងារ_ញែក.add_argument('--guest-ip', default=None, help='QEMU NAT បញ្ជូនបន្ត_តំលៃ គោលដៅ. 기본은 ip.conf의 IP; កែប្រែ_តំលៃ 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    មុខងារ_ញែក.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 អ៊ីម៉ែល. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN អ៊ីម៉ែល: 외부 ការភ្ជាប់_e05f319b')
    មុខងារ_ញែក.add_argument('--forward', action='append', default=[], help='--network 추가 ភ្ជាប់: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    មុខងារ_ញែក.add_argument('--pip', action='store_true', help='PyPI ប្រភព_មែកធាង បាច់ 중계 រត់ (--network 필요, MicroPython 호환 소스만)')
    មុខងារ_ញែក.add_argument('--pip-port', type=int, default=8027, help='បាច់ 중계의 localhost TCP 포트')
    មុខងារ_ញែក.add_argument('--pip-cache', type=Path, default=បញ្ចាំង_ឬស/'build/pip-cache')
    មុខងារ_ញែក.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    អាគុយម៉ង់_អារេ = មុខងារ_ញែក.parse_args()
    if អាគុយម៉ង់_អារេ.remote:
        អាគុយម៉ង់_អារេ.network=True
        អាគុយម៉ង់_អារេ.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; លេខសម្ងាត់_តំលៃ: python3 ឧបករណ៍/ពីចម្ងាយ_ការកំណត់.py show'.format(អាគុយម៉ង់_អារេ.network_host,អាគុយម៉ង់_អារេ.network_host),flush=True)
    if អាគុយម៉ង់_អារេ.pip and not អាគុយម៉ង់_អារេ.network: មុខងារ_ញែក.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= អាគុយម៉ង់_អារេ.pip_port <= 65535: មុខងារ_ញែក.error('--pip-port 범위는 1~65535입니다.')
    if អាគុយម៉ង់_អារេ.forward and not អាគុយម៉ង់_អារេ.network: មុខងារ_ញែក.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ធនធាន_តំលៃ:
        if អាគុយម៉ង់_អារេ.pip:
            from 꾸러미중계 import 꾸러미중계
            ធនធាន_តំលៃ.enter_context(꾸러미중계(អាគុយម៉ង់_អារេ.pip_port, អាគុយម៉ង់_អារេ.pip_cache, អាគុយម៉ង់_អារេ.pip_offline))
            print('បាច់ 중계: 127.0.0.1:' + str(អាគុយម៉ង់_អារេ.pip_port), flush=True)
        ប្រតិបត្តិ(អាគុយម៉ង់_អារេ)


def ប្រតិបត្តិ(អាគុយម៉ង់_អារេ):
    if អាគុយម៉ង់_អារេ.desktop:
        if អាគុយម៉ង់_អារេ.vnc or អាគុយម៉ង់_អារេ.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ដែសថប_ការមើល import ដំណើរការ_ដែសថប
        raise SystemExit(ដំណើរការ_ដែសថប(អាគុយម៉ង់_អារេ.port, ណិតវឺក=អាគុយម៉ង់_អារេ.network, ឯកសារ_ផ្ទេរ_លេខរន្ធ=អាគុយម៉ង់_អារេ.ftp_port, 전달규칙들=អាគុយម៉ង់_អារេ.forward, គុណភាព_បង្ហាញ_តំលៃ=អាគុយម៉ង់_អារេ.resolution, ភ្ញៀវ_អ៊ីម៉ែល=អាគុយម៉ង់_អារេ.guest_ip, ហូស_អ៊ីម៉ែល=អាគុយម៉ង់_អារេ.network_host))
    ជំរើស = ['-display', អាគុយម៉ង់_អារេ.display, '-serial', 'mon:stdio']
    if អាគុយម៉ង់_អារេ.vnc:
        ជំរើស += ['-vnc', អាគុយម៉ង់_អារេ.vnc]
    if អាគុយម៉ង់_អារេ.network:
        from 통신다리 import 통신다리
        with 통신다리(អាគុយម៉ង់_អារេ.ftp_port, អាគុយម៉ង់_អារេ.forward, ភ្ញៀវ_អ៊ីម៉ែល=អាគុយម៉ង់_អារេ.guest_ip, ហូស_អ៊ីម៉ែល=អាគុយម៉ង់_អារេ.network_host) as 연결다리:
            ភាព_តំលៃ = subprocess.call(ពាក្យ_បញ្ជា(អាគុយម៉ង់_អារេ.resolution) + ជំរើស + 연결다리.전달인수())
            if 연결다리.កំហុស: raise SystemExit('network bridge: ' + 연결다리.កំហុស)
        raise SystemExit(ភាព_តំលៃ)
    raise SystemExit(subprocess.call(ពាក្យ_បញ្ជា(អាគុយម៉ង់_អារេ.resolution) + ជំរើស))


if __name__ == '__main__':
    រត់()
