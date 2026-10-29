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

प्रॉजॅक्ट_रूट = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for पाथ in _난수파일들:
        try:
            os.unlink(पाथ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as फायल:
        फायल.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(फायल.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(फायल.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    येजमान = प्रॉजॅक्ट_रूट.parent / 'rpi4/build/host'
    적재기 = येजमान / 'lib/ld-musl-x86_64.so.1'
    बायनरी = येजमान / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and बायनरी.is_file():
        return [str(적재기), '--library-path', str(येजमान / 'usr/lib') + ':' + str(येजमान / 'lib'),
                str(बायनरी), '-L', str(येजमान / 'usr/share/qemu')]
    बायनरी = shutil.which('qemu-system-aarch64')
    if not बायनरी:
        raise SystemExit('raspi4b तेंको_मोल QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [बायनरी]


def 해상도읽기(SMS):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', SMS):
        raise argparse.ArgumentTypeError('रिजोल्युशन_मोल स्वरूप_मोल: 1920x1080')
    너비, 높이 = map(int, SMS.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('तेंको_मोल क्लिप: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def आदेश(रिजोल्युशन_मोल=(640, 480)):
    फाटभूंय_मोल = 모의기계()
    지원목록 = subprocess.check_output(फाटभूंय_मोल + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*रिजोल्युशन_मोल))
    return फाटभूंय_मोल + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(प्रॉजॅक्ट_रूट / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def चलोवप():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 कर्नेल_मोल. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 प्रस्थान_करचें_एप्लिकेशन.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (येजमान तेंको_मोल 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 आवाठ. 예: 1920x1080; डिफॉल्ट_मोल 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC हार्डवॅर_पोर्ट 5902. की_मोल 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC हार्डवॅर_पोर्ट')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 कनॅक्ट; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP नियंत्रण_मोल हार्डवॅर_पोर्ट (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT फॉर्वर्ड_मोल लक्ष्य. 기본은 ip.conf의 IP; बदलचें_मोल 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 नामो. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN नामो: 외부 कनॅक्शन_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 कनॅक्ट: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI स्त्रोत_ट्री रास 중계 चलोवप (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='रास 중계의 localhost TCP हार्डवॅर_पोर्ट')
    인수해석기.add_argument('--pip-cache', type=Path, default=प्रॉजॅक्ट_रूट/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    युक्तीवाद_क्रम = 인수해석기.parse_args()
    if युक्तीवाद_क्रम.remote:
        युक्तीवाद_क्रम.network=True
        युक्तीवाद_क्रम.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; पासवर्ड_मोल: python3 साधनां/दुर्मीळ_मांडावळी.py show'.format(युक्तीवाद_क्रम.network_host,युक्तीवाद_क्रम.network_host),flush=True)
    if युक्तीवाद_क्रम.pip and not युक्तीवाद_क्रम.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= युक्तीवाद_क्रम.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if युक्तीवाद_क्रम.forward and not युक्तीवाद_क्रम.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as साधनसामुग्री_मोल:
        if युक्तीवाद_क्रम.pip:
            from 꾸러미중계 import 꾸러미중계
            साधनसामुग्री_मोल.enter_context(꾸러미중계(युक्तीवाद_क्रम.pip_port, युक्तीवाद_क्रम.pip_cache, युक्तीवाद_क्रम.pip_offline))
            print('रास 중계: 127.0.0.1:' + str(युक्तीवाद_क्रम.pip_port), flush=True)
        पाळो_दिवचो_कार्य(युक्तीवाद_क्रम)


def पाळो_दिवचो_कार्य(युक्तीवाद_क्रम):
    if युक्तीवाद_क्रम.desktop:
        if युक्तीवाद_क्रम.vnc or युक्तीवाद_क्रम.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from डॅस्कटॉप_दृश्य import चलोवप_डॅस्कटॉप
        raise SystemExit(चलोवप_डॅस्कटॉप(युक्तीवाद_क्रम.port, नॅटवर्क=युक्तीवाद_क्रम.network, 파일전송접속번호=युक्तीवाद_क्रम.ftp_port, 전달규칙들=युक्तीवाद_क्रम.forward, रिजोल्युशन_मोल=युक्तीवाद_क्रम.resolution, सोयरो_नामो=युक्तीवाद_क्रम.guest_ip, येजमान_नामो=युक्तीवाद_क्रम.network_host))
    पर्याय = ['-display', युक्तीवाद_क्रम.display, '-serial', 'mon:stdio']
    if युक्तीवाद_क्रम.vnc:
        पर्याय += ['-vnc', युक्तीवाद_क्रम.vnc]
    if युक्तीवाद_क्रम.network:
        from नॅटवर्क_ब्रिज import नॅटवर्क_ब्रिज
        with नॅटवर्क_ब्रिज(युक्तीवाद_क्रम.ftp_port, युक्तीवाद_क्रम.forward, सोयरो_नामो=युक्तीवाद_क्रम.guest_ip, येजमान_नामो=युक्तीवाद_क्रम.network_host) as ब्रिज:
            स्थिती_मोल_e10195a1 = subprocess.call(आदेश(युक्तीवाद_क्रम.resolution) + पर्याय + ब्रिज.전달인수())
            if ब्रिज.चूक: raise SystemExit('network bridge: ' + ब्रिज.चूक)
        raise SystemExit(स्थिती_मोल_e10195a1)
    raise SystemExit(subprocess.call(आदेश(युक्तीवाद_क्रम.resolution) + पर्याय))


if __name__ == '__main__':
    चलोवप()
