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

प्रोजेक्ट_करें_मूल = Path(__file__).resolve().parents[1]
यादृच्_छिक_फ़ाइलें = []


def _난수정리():
    for पथ in यादृच्_छिक_फ़ाइलें:
        try:
            os.unlink(पथ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as संचिका:
        संचिका.write(b'JKRENRG1' + os.urandom(32))
        यादृच्_छिक_फ़ाइलें.append(संचिका.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(संचिका.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    आयोजक = प्रोजेक्ट_करें_मूल.parent / 'rpi4/build/host'
    लोडर = आयोजक / 'lib/ld-musl-x86_64.so.1'
    बाइनरी = आयोजक / 'usr/bin/qemu-system-aarch64'
    if लोडर.is_file() and बाइनरी.is_file():
        return [str(लोडर), '--library-path', str(आयोजक / 'usr/lib') + ':' + str(आयोजक / 'lib'),
                str(बाइनरी), '-L', str(आयोजक / 'usr/share/qemu')]
    बाइनरी = shutil.which('qemu-system-aarch64')
    if not बाइनरी:
        raise SystemExit('raspi4b समर्थन_मान QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [बाइनरी]


def पढें_रिज़ॉल्यूशन(पाठ):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', पाठ):
        raise argparse.ArgumentTypeError('रिज़ॉल्यूशन_मान फॉर्मैट_मान: 1920x1080')
    너비, 높이 = map(int, पाठ.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('समर्थन_मान क्लिप: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def आदेश(रिज़ॉल्यूशन_मान=(640, 480)):
    वॉलपेपर_मान = 모의기계()
    지원목록 = subprocess.check_output(वॉलपेपर_मान + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = पढें_रिज़ॉल्यूशन('{}x{}'.format(*रिज़ॉल्यूशन_मान))
    return वॉलपेपर_मान + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(प्रोजेक्ट_करें_मूल / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def चलाएँ():
    पार्सर = argparse.ArgumentParser(description='निज Java Pi4 कर्नेल_मान. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 निर्गमन_ऐप.')
    पार्सर.add_argument('--display', default='none', help='none 또는 gtk/sdl (आयोजक समर्थन_मान 필요)')
    पार्सर.add_argument('--resolution', type=पढें_रिज़ॉल्यूशन, default=(640, 480), help='부팅 화면 आकार. 예: 1920x1080; डिफ़ॉल्ट_मान 640x480')
    पार्सर.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. कुंजी_मान 입력은 UART 터미널에서 합니다.')
    पार्सर.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    पार्सर.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    पार्सर.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 जोड़ना; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    पार्सर.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    पार्सर.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP नियंत्रण_मान 포트 (데이터 50000..50007)')
    पार्सर.add_argument('--guest-ip', default=None, help='QEMU NAT आगे_मान लक्ष्य. 기본은 ip.conf의 IP; परिवर्तित_करें_मान 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    पार्सर.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 पता. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN पता: बाहरी_मान कनेक्शन_e05f319b')
    पार्सर.add_argument('--forward', action='append', default=[], help='--network जोड़ें_एन्ट्री जोड़ना: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    पार्सर.add_argument('--pip', action='store_true', help='PyPI स्रोत_ट्री बंडल 중계 चलाएँ (--network 필요, MicroPython 호환 소스만)')
    पार्सर.add_argument('--pip-port', type=int, default=8027, help='बंडल 중계의 localhost TCP 포트')
    पार्सर.add_argument('--pip-cache', type=Path, default=प्रोजेक्ट_करें_मूल/'build/pip-cache')
    पार्सर.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    तर्क_सरणी = पार्सर.parse_args()
    if तर्क_सरणी.remote:
        तर्क_सरणी.network=True
        तर्क_सरणी.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; पासवर्ड_मान: python3 उपकरण/दूरस्थ_सेटिंग.py show'.format(तर्क_सरणी.network_host,तर्क_सरणी.network_host),flush=True)
    if तर्क_सरणी.pip and not तर्क_सरणी.network: पार्सर.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= तर्क_सरणी.pip_port <= 65535: पार्सर.error('--pip-port 범위는 1~65535입니다.')
    if तर्क_सरणी.forward and not तर्क_सरणी.network: पार्सर.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as संसाधन_मान:
        if तर्क_सरणी.pip:
            from 꾸러미중계 import 꾸러미중계
            संसाधन_मान.enter_context(꾸러미중계(तर्क_सरणी.pip_port, तर्क_सरणी.pip_cache, तर्क_सरणी.pip_offline))
            print('बंडल 중계: 127.0.0.1:' + str(तर्क_सरणी.pip_port), flush=True)
        निष्पादन(तर्क_सरणी)


def निष्पादन(तर्क_सरणी):
    if तर्क_सरणी.desktop:
        if तर्क_सरणी.vnc or तर्क_सरणी.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from डेस्कटॉप_दृश्य import चलाएँ_डेस्कटॉप
        raise SystemExit(चलाएँ_डेस्कटॉप(तर्क_सरणी.port, नेटवर्क=तर्क_सरणी.network, फ़ाइल_स्थानांतरण_पोर्ट_संख्या=तर्क_सरणी.ftp_port, 전달규칙들=तर्क_सरणी.forward, रिज़ॉल्यूशन_मान=तर्क_सरणी.resolution, अतिथि_पता=तर्क_सरणी.guest_ip, आयोजक_पता=तर्क_सरणी.network_host))
    विकल्प = ['-display', तर्क_सरणी.display, '-serial', 'mon:stdio']
    if तर्क_सरणी.vnc:
        विकल्प += ['-vnc', तर्क_सरणी.vnc]
    if तर्क_सरणी.network:
        from ब्रिज_3de4fe3a import ब्रिज_3de4fe3a
        with ब्रिज_3de4fe3a(तर्क_सरणी.ftp_port, तर्क_सरणी.forward, अतिथि_पता=तर्क_सरणी.guest_ip, आयोजक_पता=तर्क_सरणी.network_host) as ब्रिज:
            अवस्था_मान = subprocess.call(आदेश(तर्क_सरणी.resolution) + विकल्प + ब्रिज.전달인수())
            if ब्रिज.त्रुटि: raise SystemExit('network bridge: ' + ब्रिज.त्रुटि)
        raise SystemExit(अवस्था_मान)
    raise SystemExit(subprocess.call(आदेश(तर्क_सरणी.resolution) + विकल्प))


if __name__ == '__main__':
    चलाएँ()
