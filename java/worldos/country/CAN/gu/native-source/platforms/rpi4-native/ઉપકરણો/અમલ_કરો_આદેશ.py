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

પ્રોજેક્ટ_રૂટ = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for પથ in _난수파일들:
        try:
            os.unlink(પથ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ફાઈલ:
        ફાઈલ.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(ફાઈલ.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ફાઈલ.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    હોસ્ટ = પ્રોજેક્ટ_રૂટ.parent / 'rpi4/build/host'
    적재기 = હોસ્ટ / 'lib/ld-musl-x86_64.so.1'
    બાઇનરી = હોસ્ટ / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and બાઇનરી.is_file():
        return [str(적재기), '--library-path', str(હોસ્ટ / 'usr/lib') + ':' + str(હોસ્ટ / 'lib'),
                str(બાઇનરી), '-L', str(હોસ્ટ / 'usr/share/qemu')]
    બાઇનરી = shutil.which('qemu-system-aarch64')
    if not બાઇનરી:
        raise SystemExit('raspi4b સપોર્ટ_મૂલ્ય QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [બાઇનરી]


def 해상도읽기(લખાણ):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', લખાણ):
        raise argparse.ArgumentTypeError('રિઝોલ્યૂશન_મૂલ્ય સ્વરૂપ_મૂલ્ય: 1920x1080')
    너비, 높이 = map(int, લખાણ.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('સપોર્ટ_મૂલ્ય ક્લિપ: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def આદેશ(રિઝોલ્યૂશન_મૂલ્ય=(640, 480)):
    વૉલપેપર_મૂલ્ય = 모의기계()
    지원목록 = subprocess.check_output(વૉલપેપર_મૂલ્ય + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*રિઝોલ્યૂશન_મૂલ્ય))
    return વૉલપેપર_મૂલ્ય + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(પ્રોજેક્ટ_રૂટ / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def ચલાવો_2():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 કર્નેલ_મૂલ્ય. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 પ્રસ્થાન_એપ્લિકેશન.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (હોસ્ટ સપોર્ટ_મૂલ્ય 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 માપ. 예: 1920x1080; ડિફૉલ્ટ_મૂલ્ય 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC હાર્ડવેર_પૉર્ટ 5902. કી_મૂલ્ય 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC હાર્ડવેર_પૉર્ટ')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 સંપર્ક_કરો; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP નિયંત્રણ_મૂલ્ય હાર્ડવેર_પૉર્ટ (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT ફોર્વર્ડ_મૂલ્ય લક્ષ્ય. 기본은 ip.conf의 IP; પરિવર્તન_કરો_મૂલ્ય 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 સરનામું. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN સરનામું: 외부 કનેક્શન_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 સંપર્ક_કરો: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI સ્રોત_ટ્રી બન્ડલ 중계 ચલાવો_2 (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='બન્ડલ 중계의 localhost TCP હાર્ડવેર_પૉર્ટ')
    인수해석기.add_argument('--pip-cache', type=Path, default=પ્રોજેક્ટ_રૂટ/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    દલીલ_અરે = 인수해석기.parse_args()
    if દલીલ_અરે.remote:
        દલીલ_અરે.network=True
        દલીલ_અરે.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; પાસવર્ડ_મૂલ્ય: python3 ઉપકરણો/રિમોટ_સેટિંગ્સ.py show'.format(દલીલ_અરે.network_host,દલીલ_અરે.network_host),flush=True)
    if દલીલ_અરે.pip and not દલીલ_અરે.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= દલીલ_અરે.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if દલીલ_અરે.forward and not દલીલ_અરે.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as સાધન_મૂલ્ય:
        if દલીલ_અરે.pip:
            from 꾸러미중계 import 꾸러미중계
            સાધન_મૂલ્ય.enter_context(꾸러미중계(દલીલ_અરે.pip_port, દલીલ_અરે.pip_cache, દલીલ_અરે.pip_offline))
            print('બન્ડલ 중계: 127.0.0.1:' + str(દલીલ_અરે.pip_port), flush=True)
        ચલાવો(દલીલ_અરે)


def ચલાવો(દલીલ_અરે):
    if દલીલ_અરે.desktop:
        if દલીલ_અરે.vnc or દલીલ_અરે.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ડેસ્કટૉપ_જુઓ import ચલાવો_ડેસ્કટૉપ
        raise SystemExit(ચલાવો_ડેસ્કટૉપ(દલીલ_અરે.port, નેટવર્ક=દલીલ_અરે.network, ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર=દલીલ_અરે.ftp_port, 전달규칙들=દલીલ_અરે.forward, રિઝોલ્યૂશન_મૂલ્ય=દલીલ_અરે.resolution, અતિથિ_સરનામું=દલીલ_અરે.guest_ip, હોસ્ટ_સરનામું=દલીલ_અરે.network_host))
    વિકલ્પો = ['-display', દલીલ_અરે.display, '-serial', 'mon:stdio']
    if દલીલ_અરે.vnc:
        વિકલ્પો += ['-vnc', દલીલ_અરે.vnc]
    if દલીલ_અરે.network:
        from નેટવર્ક_બ્રિજ import નેટવર્ક_બ્રિજ
        with નેટવર્ક_બ્રિજ(દલીલ_અરે.ftp_port, દલીલ_અરે.forward, અતિથિ_સરનામું=દલીલ_અરે.guest_ip, હોસ્ટ_સરનામું=દલીલ_અરે.network_host) as બ્રિજ:
            સ્થિતિ_મૂલ્ય_e10195a1 = subprocess.call(આદેશ(દલીલ_અરે.resolution) + વિકલ્પો + બ્રિજ.전달인수())
            if બ્રિજ.ભૂલ: raise SystemExit('network bridge: ' + બ્રિજ.ભૂલ)
        raise SystemExit(સ્થિતિ_મૂલ્ય_e10195a1)
    raise SystemExit(subprocess.call(આદેશ(દલીલ_અરે.resolution) + વિકલ્પો))


if __name__ == '__main__':
    ચલાવો_2()
