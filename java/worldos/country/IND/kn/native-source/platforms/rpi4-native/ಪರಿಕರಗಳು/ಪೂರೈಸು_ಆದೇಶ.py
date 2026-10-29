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

ಬಿಂಬಿಸು_ಮೂಲ = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for ಮಾರ್ಗ in _난수파일들:
        try:
            os.unlink(ಮಾರ್ಗ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ಕಡತ:
        ಕಡತ.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(ಕಡತ.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ಕಡತ.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    ಹೋಸ್ಟ್ = ಬಿಂಬಿಸು_ಮೂಲ.parent / 'rpi4/build/host'
    적재기 = ಹೋಸ್ಟ್ / 'lib/ld-musl-x86_64.so.1'
    ದ್ವಿಮಾನ = ಹೋಸ್ಟ್ / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and ದ್ವಿಮಾನ.is_file():
        return [str(적재기), '--library-path', str(ಹೋಸ್ಟ್ / 'usr/lib') + ':' + str(ಹೋಸ್ಟ್ / 'lib'),
                str(ದ್ವಿಮಾನ), '-L', str(ಹೋಸ್ಟ್ / 'usr/share/qemu')]
    ದ್ವಿಮಾನ = shutil.which('qemu-system-aarch64')
    if not ದ್ವಿಮಾನ:
        raise SystemExit('raspi4b ಬೆಂಬಲ_ಮೌಲ್ಯ QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ದ್ವಿಮಾನ]


def 해상도읽기(ಪಠ್ಯ):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', ಪಠ್ಯ):
        raise argparse.ArgumentTypeError('ರಿಸೊಲ್ಯೂಶನ್_ಮೌಲ್ಯ ಸ್ವರೂಪ_ಮೌಲ್ಯ: 1920x1080')
    너비, 높이 = map(int, ಪಠ್ಯ.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('ಬೆಂಬಲ_ಮೌಲ್ಯ ಕ್ಲಿಪ್: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def ಆಜ್ಞೆ(ರಿಸೊಲ್ಯೂಶನ್_ಮೌಲ್ಯ=(640, 480)):
    ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ = 모의기계()
    지원목록 = subprocess.check_output(ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*ರಿಸೊಲ್ಯೂಶನ್_ಮೌಲ್ಯ))
    return ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(ಬಿಂಬಿಸು_ಮೂಲ / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def ಚಲಾಯಿಸು_2():
    ಪಾರ್ಸರ್ = argparse.ArgumentParser(description='자체 Java Pi4 ಕರ್ನಲ್_ಮೌಲ್ಯ. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 ನಿರ್ಗಮನ_ಅಪ್ಲಿ.')
    ಪಾರ್ಸರ್.add_argument('--display', default='none', help='none 또는 gtk/sdl (ಹೋಸ್ಟ್ ಬೆಂಬಲ_ಮೌಲ್ಯ 필요)')
    ಪಾರ್ಸರ್.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 ಗಾತ್ರ. 예: 1920x1080; ಅಕ್ಷಮ_ಬೆಲೆ 640x480')
    ಪಾರ್ಸರ್.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. ಕೀ_ಮೌಲ್ಯ 입력은 UART 터미널에서 합니다.')
    ಪಾರ್ಸರ್.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    ಪಾರ್ಸರ್.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    ಪಾರ್ಸರ್.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    ಪಾರ್ಸರ್.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    ಪಾರ್ಸರ್.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP ನಿಯಂತ್ರಣ_ಮೌಲ್ಯ 포트 (데이터 50000..50007)')
    ಪಾರ್ಸರ್.add_argument('--guest-ip', default=None, help='QEMU NAT ಮುಂದೆ_ಮೌಲ್ಯ_24592b8a ಲಕ್ಷ್ಯ. 기본은 ip.conf의 IP; ಬದಲಿಸು_ಮೌಲ್ಯ 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    ಪಾರ್ಸರ್.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ಇಮೇಲ್. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ಇಮೇಲ್: 외부 ಸಂಪರ್ಕ_e05f319b')
    ಪಾರ್ಸರ್.add_argument('--forward', action='append', default=[], help='--network 추가 ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    ಪಾರ್ಸರ್.add_argument('--pip', action='store_true', help='PyPI ಮೂಲ_ವೃಕ್ಷ ಬಂಡಲ್ 중계 ಚಲಾಯಿಸು_2 (--network 필요, MicroPython 호환 소스만)')
    ಪಾರ್ಸರ್.add_argument('--pip-port', type=int, default=8027, help='ಬಂಡಲ್ 중계의 localhost TCP 포트')
    ಪಾರ್ಸರ್.add_argument('--pip-cache', type=Path, default=ಬಿಂಬಿಸು_ಮೂಲ/'build/pip-cache')
    ಪಾರ್ಸರ್.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    ವಾದ_ಅರೇ = ಪಾರ್ಸರ್.parse_args()
    if ವಾದ_ಅರೇ.remote:
        ವಾದ_ಅರೇ.network=True
        ವಾದ_ಅರೇ.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; ಪಾಸ್_ವರ್ಡ್_ಮೌಲ್ಯ: python3 ಪರಿಕರಗಳು/ರಿಮೋಟ್_ಸೆಟ್ಟಿಂಗ್ಸ್.py show'.format(ವಾದ_ಅರೇ.network_host,ವಾದ_ಅರೇ.network_host),flush=True)
    if ವಾದ_ಅರೇ.pip and not ವಾದ_ಅರೇ.network: ಪಾರ್ಸರ್.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= ವಾದ_ಅರೇ.pip_port <= 65535: ಪಾರ್ಸರ್.error('--pip-port 범위는 1~65535입니다.')
    if ವಾದ_ಅರೇ.forward and not ವಾದ_ಅರೇ.network: ಪಾರ್ಸರ್.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ಸಂಪನ್ಮೂಲ_ಮೌಲ್ಯ:
        if ವಾದ_ಅರೇ.pip:
            from 꾸러미중계 import 꾸러미중계
            ಸಂಪನ್ಮೂಲ_ಮೌಲ್ಯ.enter_context(꾸러미중계(ವಾದ_ಅರೇ.pip_port, ವಾದ_ಅರೇ.pip_cache, ವಾದ_ಅರೇ.pip_offline))
            print('ಬಂಡಲ್ 중계: 127.0.0.1:' + str(ವಾದ_ಅರೇ.pip_port), flush=True)
        ಚಲಾಯಿಸು(ವಾದ_ಅರೇ)


def ಚಲಾಯಿಸು(ವಾದ_ಅರೇ):
    if ವಾದ_ಅರೇ.desktop:
        if ವಾದ_ಅರೇ.vnc or ವಾದ_ಅರೇ.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ಡೆಸ್ಕ್_ಟಾಪ್_ವೀಕ್ಷಣೆ import ಚಲನೆ_ಡೆಸ್ಕ್_ಟಾಪ್
        raise SystemExit(ಚಲನೆ_ಡೆಸ್ಕ್_ಟಾಪ್(ವಾದ_ಅರೇ.port, ನೆಟ್_ವರ್ಕ್=ವಾದ_ಅರೇ.network, ಫೈಲ್_ವರ್ಗಾವಣೆ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ=ವಾದ_ಅರೇ.ftp_port, 전달규칙들=ವಾದ_ಅರೇ.forward, ರಿಸೊಲ್ಯೂಶನ್_ಮೌಲ್ಯ=ವಾದ_ಅರೇ.resolution, ಅತಿಥಿ_ಇಮೇಲ್=ವಾದ_ಅರೇ.guest_ip, ಹೋಸ್ಟ್_ಇಮೇಲ್=ವಾದ_ಅರೇ.network_host))
    ಆಯ್ಕೆಗಳು = ['-display', ವಾದ_ಅರೇ.display, '-serial', 'mon:stdio']
    if ವಾದ_ಅರೇ.vnc:
        ಆಯ್ಕೆಗಳು += ['-vnc', ವಾದ_ಅರೇ.vnc]
    if ವಾದ_ಅರೇ.network:
        from ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ import ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ
        with ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ(ವಾದ_ಅರೇ.ftp_port, ವಾದ_ಅರೇ.forward, ಅತಿಥಿ_ಇಮೇಲ್=ವಾದ_ಅರೇ.guest_ip, ಹೋಸ್ಟ್_ಇಮೇಲ್=ವಾದ_ಅರೇ.network_host) as ಸೇತುವೆ:
            ಸ್ಥಿತಿ_ಮೌಲ್ಯ = subprocess.call(ಆಜ್ಞೆ(ವಾದ_ಅರೇ.resolution) + ಆಯ್ಕೆಗಳು + ಸೇತುವೆ.전달인수())
            if ಸೇತುವೆ.ದೋಷ: raise SystemExit('network bridge: ' + ಸೇತುವೆ.ದೋಷ)
        raise SystemExit(ಸ್ಥಿತಿ_ಮೌಲ್ಯ)
    raise SystemExit(subprocess.call(ಆಜ್ಞೆ(ವಾದ_ಅರೇ.resolution) + ಆಯ್ಕೆಗಳು))


if __name__ == '__main__':
    ಚಲಾಯಿಸು_2()
