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

기준 = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for 경로 in _난수파일들:
        try:
            os.unlink(경로)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Dataja:
        Dataja.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Dataja.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Dataja.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    호스트 = 기준.parent / 'rpi4/build/host'
    적재기 = 호스트 / 'lib/ld-musl-x86_64.so.1'
    실행바이너리 = 호스트 / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and 실행바이너리.is_file():
        return [str(적재기), '--library-path', str(호스트 / 'usr/lib') + ':' + str(호스트 / 'lib'),
                str(실행바이너리), '-L', str(호스트 / 'usr/share/qemu')]
    실행바이너리 = shutil.which('qemu-system-aarch64')
    if not 실행바이너리:
        raise SystemExit('raspi4b 지원 QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [실행바이너리]


def 해상도읽기(글):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', 글):
        raise argparse.ArgumentTypeError('해상도 형식: 1920x1080')
    너비, 높이 = map(int, 글.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('지원 범위: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def 명령(해상도=(640, 480)):
    바탕 = 모의기계()
    지원목록 = subprocess.check_output(바탕 + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*해상도))
    return 바탕 + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def 시작():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 커널. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 종료.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (호스트 지원 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 크기. 예: 1920x1080; 기본 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. 키 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 연결; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP 제어 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT 전달 대상. 기본은 ip.conf의 IP; 변경 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 주소. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN 주소: 외부 접속')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 연결: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI 소스 꾸러미 중계 시작 (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='꾸러미 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    인수배열 = 인수해석기.parse_args()
    if 인수배열.remote:
        인수배열.network=True
        인수배열.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; 암호: python3 도구/원격설정.py show'.format(인수배열.network_host,인수배열.network_host),flush=True)
    if 인수배열.pip and not 인수배열.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= 인수배열.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if 인수배열.forward and not 인수배열.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as 자원:
        if 인수배열.pip:
            from 꾸러미중계 import 꾸러미중계
            자원.enter_context(꾸러미중계(인수배열.pip_port, 인수배열.pip_cache, 인수배열.pip_offline))
            print('꾸러미 중계: 127.0.0.1:' + str(인수배열.pip_port), flush=True)
        Wuwjesć(인수배열)


def Wuwjesć(인수배열):
    if 인수배열.desktop:
        if 인수배열.vnc or 인수배열.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from 바탕화면 import 바탕화면실행
        raise SystemExit(바탕화면실행(인수배열.port, 통신사용=인수배열.network, 파일전송접속번호=인수배열.ftp_port, 전달규칙들=인수배열.forward, 해상도=인수배열.resolution, 게스트주소=인수배열.guest_ip, 호스트주소=인수배열.network_host))
    선택사항 = ['-display', 인수배열.display, '-serial', 'mon:stdio']
    if 인수배열.vnc:
        선택사항 += ['-vnc', 인수배열.vnc]
    if 인수배열.network:
        from 통신다리 import 통신다리
        with 통신다리(인수배열.ftp_port, 인수배열.forward, 게스트주소=인수배열.guest_ip, 호스트주소=인수배열.network_host) as 연결다리:
            상태 = subprocess.call(명령(인수배열.resolution) + 선택사항 + 연결다리.전달인수())
            if 연결다리.Zmylk: raise SystemExit('network bridge: ' + 연결다리.Zmylk)
        raise SystemExit(상태)
    raise SystemExit(subprocess.call(명령(인수배열.resolution) + 선택사항))


if __name__ == '__main__':
    시작()
