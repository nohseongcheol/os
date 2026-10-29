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

परियोजना_रूट = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for मार्ग in _난수파일들:
        try:
            os.unlink(मार्ग)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as फाइल:
        फाइल.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(फाइल.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(फाइल.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    होस्ट = परियोजना_रूट.parent / 'rpi4/build/host'
    적재기 = होस्ट / 'lib/ld-musl-x86_64.so.1'
    बाइनेरी = होस्ट / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and बाइनेरी.is_file():
        return [str(적재기), '--library-path', str(होस्ट / 'usr/lib') + ':' + str(होस्ट / 'lib'),
                str(बाइनेरी), '-L', str(होस्ट / 'usr/share/qemu')]
    बाइनेरी = shutil.which('qemu-system-aarch64')
    if not बाइनेरी:
        raise SystemExit('raspi4b समर्थन_मान QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [बाइनेरी]


def 해상도읽기(पाठ):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', पाठ):
        raise argparse.ArgumentTypeError('रिजोल्यूशन_मान ढाँचा_मान: 1920x1080')
    너비, 높이 = map(int, पाठ.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('समर्थन_मान क्लिप: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def आदेश(रिजोल्यूशन_मान=(640, 480)):
    वालपेपर_मान = 모의기계()
    지원목록 = subprocess.check_output(वालपेपर_मान + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*रिजोल्यूशन_मान))
    return वालपेपर_मान + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(परियोजना_रूट / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def चलाउनुहोस्():
    인수해석기 = argparse.ArgumentParser(description='निज Java Pi4 कर्णेल_मान. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 बाहिर_जानुहोस्_अनुप्रयोग.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (होस्ट समर्थन_मान 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 आकार. 예: 1920x1080; पूर्वनिर्धारित_मान 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC हार्डवेयर_पोर्ट 5902. कुञ्जी_मान 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC हार्डवेयर_पोर्ट')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 जडान; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP नियन्त्रण_मान हार्डवेयर_पोर्ट (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT फरवार्ड_मान लक्ष्य. 기본은 ip.conf의 IP; परिवर्तन_मान 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ठेगाना. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ठेगाना: 외부 जडान_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 जडान: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI स्रोत_वृक्ष पोको 중계 चलाउनुहोस् (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='पोको 중계의 localhost TCP हार्डवेयर_पोर्ट')
    인수해석기.add_argument('--pip-cache', type=Path, default=परियोजना_रूट/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    तर्क_विन्यास = 인수해석기.parse_args()
    if तर्क_विन्यास.remote:
        तर्क_विन्यास.network=True
        तर्क_विन्यास.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; पासवर्ड_मान: python3 उपकरणहरू/दूर_सेटिङहरू.py show'.format(तर्क_विन्यास.network_host,तर्क_विन्यास.network_host),flush=True)
    if तर्क_विन्यास.pip and not तर्क_विन्यास.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= तर्क_विन्यास.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if तर्क_विन्यास.forward and not तर्क_विन्यास.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as स्रोत_मान:
        if तर्क_विन्यास.pip:
            from 꾸러미중계 import 꾸러미중계
            स्रोत_मान.enter_context(꾸러미중계(तर्क_विन्यास.pip_port, तर्क_विन्यास.pip_cache, तर्क_विन्यास.pip_offline))
            print('पोको 중계: 127.0.0.1:' + str(तर्क_विन्यास.pip_port), flush=True)
        कार्यान्वयन_गर्नुहोस्(तर्क_विन्यास)


def कार्यान्वयन_गर्नुहोस्(तर्क_विन्यास):
    if तर्क_विन्यास.desktop:
        if तर्क_विन्यास.vnc or तर्क_विन्यास.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from डेस्कटप_दृश्य import चलाउनुहोस्_डेस्कटप
        raise SystemExit(चलाउनुहोस्_डेस्कटप(तर्क_विन्यास.port, सञ्जाल=तर्क_विन्यास.network, 파일전송접속번호=तर्क_विन्यास.ftp_port, 전달규칙들=तर्क_विन्यास.forward, रिजोल्यूशन_मान=तर्क_विन्यास.resolution, अतिथि_ठेगाना=तर्क_विन्यास.guest_ip, होस्ट_ठेगाना=तर्क_विन्यास.network_host))
    विकल्पहरु = ['-display', तर्क_विन्यास.display, '-serial', 'mon:stdio']
    if तर्क_विन्यास.vnc:
        विकल्पहरु += ['-vnc', तर्क_विन्यास.vnc]
    if तर्क_विन्यास.network:
        from सञ्जाल_ब्रिज import सञ्जाल_ब्रिज
        with सञ्जाल_ब्रिज(तर्क_विन्यास.ftp_port, तर्क_विन्यास.forward, अतिथि_ठेगाना=तर्क_विन्यास.guest_ip, होस्ट_ठेगाना=तर्क_विन्यास.network_host) as ब्रिज:
            स्थिति_मान = subprocess.call(आदेश(तर्क_विन्यास.resolution) + विकल्पहरु + ब्रिज.전달인수())
            if ब्रिज.त्रुटि: raise SystemExit('network bridge: ' + ब्रिज.त्रुटि)
        raise SystemExit(स्थिति_मान)
    raise SystemExit(subprocess.call(आदेश(तर्क_विन्यास.resolution) + विकल्पहरु))


if __name__ == '__main__':
    चलाउनुहोस्()
