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
    for ᎠᏍᏓᏩᏛᏍᏗ in _난수파일들:
        try:
            os.unlink(ᎠᏍᏓᏩᏛᏍᏗ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ᎠᏍᏆᏂᎪᏙᏗ:
        ᎠᏍᏆᏂᎪᏙᏗ.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(ᎠᏍᏆᏂᎪᏙᏗ.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ᎠᏍᏆᏂᎪᏙᏗ.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    ᎠᏁᏢᏍᎩ = 기준.parent / 'rpi4/build/host'
    적재기 = ᎠᏁᏢᏍᎩ / 'lib/ld-musl-x86_64.so.1'
    binary = ᎠᏁᏢᏍᎩ / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and binary.is_file():
        return [str(적재기), '--library-path', str(ᎠᏁᏢᏍᎩ / 'usr/lib') + ':' + str(ᎠᏁᏢᏍᎩ / 'lib'),
                str(binary), '-L', str(ᎠᏁᏢᏍᎩ / 'usr/share/qemu')]
    binary = shutil.which('qemu-system-aarch64')
    if not binary:
        raise SystemExit('raspi4b ᎦᎫᏍᏛᏗ_ᏧᎬᏩᎶᏗᏯ QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binary]


def 해상도읽기(ᎠᎪᎵᏰᏗ):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', ᎠᎪᎵᏰᏗ):
        raise argparse.ArgumentTypeError('ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᏧᎬᏩᎶᏗᏯ ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ: 1920x1080')
    너비, 높이 = map(int, ᎠᎪᎵᏰᏗ.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('ᎦᎫᏍᏛᏗ_ᏧᎬᏩᎶᏗᏯ ᎠᎬᎭᎸᏓ_ᏗᏓᏴᎳᏛᏙᏗ: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def ᎤᏁᏤᎸᎩ(ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᏧᎬᏩᎶᏗᏯ=(640, 480)):
    ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ = 모의기계()
    지원목록 = subprocess.check_output(ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᏧᎬᏩᎶᏗᏯ))
    return ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def ᎠᎢᏎᏍᏗ():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 kernel_ᏧᎬᏩᎶᏗᏯ. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 ᎦᏅᎪᎢᏍᏗ_ᎬᏙᏗ.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (ᎠᏁᏢᏍᎩ ᎦᎫᏍᏛᏗ_ᏧᎬᏩᎶᏗᏯ 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 ᎢᎩᏓ. 예: 1920x1080; ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 ᎫᏓᎳ; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP ᎠᎯᎸᏍᏗ_ᏧᎬᏩᎶᏗᏯ 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT ᏩᎦᏛᏗᏜ_ᏧᎬᏩᎶᏗᏯ ᎠᏉᏅᏗᎢ. 기본은 ip.conf의 IP; ᎯᏁᏟᏴᎾ_ᏧᎬᏩᎶᏗᏯ 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ᎪᏪᎵ_ᏫᏗᎦᏅᏗ. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ᎪᏪᎵ_ᏫᏗᎦᏅᏗ: 외부 ᎫᏓᎸᎢ_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 ᎫᏓᎳ: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI ᎦᏟᏌᏅᎯ_ᏡᎬ ᎦᏇᏅᎯ 중계 ᎠᎢᏎᏍᏗ (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='ᎦᏇᏅᎯ 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    ᏗᏓᎦᏘᎸᏍᏗ_array = 인수해석기.parse_args()
    if ᏗᏓᎦᏘᎸᏍᏗ_array.remote:
        ᏗᏓᎦᏘᎸᏍᏗ_array.network=True
        ᏗᏓᎦᏘᎸᏍᏗ_array.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ_ᏧᎬᏩᎶᏗᏯ: python3 도구/원격설정.py show'.format(ᏗᏓᎦᏘᎸᏍᏗ_array.network_host,ᏗᏓᎦᏘᎸᏍᏗ_array.network_host),flush=True)
    if ᏗᏓᎦᏘᎸᏍᏗ_array.pip and not ᏗᏓᎦᏘᎸᏍᏗ_array.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= ᏗᏓᎦᏘᎸᏍᏗ_array.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if ᏗᏓᎦᏘᎸᏍᏗ_array.forward and not ᏗᏓᎦᏘᎸᏍᏗ_array.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ᎠᏓᏁᏢᎢ_ᏧᎬᏩᎶᏗᏯ:
        if ᏗᏓᎦᏘᎸᏍᏗ_array.pip:
            from 꾸러미중계 import 꾸러미중계
            ᎠᏓᏁᏢᎢ_ᏧᎬᏩᎶᏗᏯ.enter_context(꾸러미중계(ᏗᏓᎦᏘᎸᏍᏗ_array.pip_port, ᏗᏓᎦᏘᎸᏍᏗ_array.pip_cache, ᏗᏓᎦᏘᎸᏍᏗ_array.pip_offline))
            print('ᎦᏇᏅᎯ 중계: 127.0.0.1:' + str(ᏗᏓᎦᏘᎸᏍᏗ_array.pip_port), flush=True)
        ᎠᎴᏅᏗᏱ_ᏯᏛᏁᏗ(ᏗᏓᎦᏘᎸᏍᏗ_array)


def ᎠᎴᏅᏗᏱ_ᏯᏛᏁᏗ(ᏗᏓᎦᏘᎸᏍᏗ_array):
    if ᏗᏓᎦᏘᎸᏍᏗ_array.desktop:
        if ᏗᏓᎦᏘᎸᏍᏗ_array.vnc or ᏗᏓᎦᏘᎸᏍᏗ_array.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ᎦᏍᎩᎶᎩ_ᎦᏚ_ᎯᎪᎵᏯ import ᎠᎢᏎᏍᏗ_ᎦᏍᎩᎶᎩ_ᎦᏚ
        raise SystemExit(ᎠᎢᏎᏍᏗ_ᎦᏍᎩᎶᎩ_ᎦᏚ(ᏗᏓᎦᏘᎸᏍᏗ_array.port, ᏧᎾᏚᏓᎵ=ᏗᏓᎦᏘᎸᏍᏗ_array.network, 파일전송접속번호=ᏗᏓᎦᏘᎸᏍᏗ_array.ftp_port, 전달규칙들=ᏗᏓᎦᏘᎸᏍᏗ_array.forward, ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ_ᏧᎬᏩᎶᏗᏯ=ᏗᏓᎦᏘᎸᏍᏗ_array.resolution, ᎠᏓᏩᏛᎯᏙᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=ᏗᏓᎦᏘᎸᏍᏗ_array.guest_ip, ᎠᏁᏢᏍᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=ᏗᏓᎦᏘᎸᏍᏗ_array.network_host))
    ᎠᏑᏰᏍᏗᎢ = ['-display', ᏗᏓᎦᏘᎸᏍᏗ_array.display, '-serial', 'mon:stdio']
    if ᏗᏓᎦᏘᎸᏍᏗ_array.vnc:
        ᎠᏑᏰᏍᏗᎢ += ['-vnc', ᏗᏓᎦᏘᎸᏍᏗ_array.vnc]
    if ᏗᏓᎦᏘᎸᏍᏗ_array.network:
        from 통신다리 import 통신다리
        with 통신다리(ᏗᏓᎦᏘᎸᏍᏗ_array.ftp_port, ᏗᏓᎦᏘᎸᏍᏗ_array.forward, ᎠᏓᏩᏛᎯᏙᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=ᏗᏓᎦᏘᎸᏍᏗ_array.guest_ip, ᎠᏁᏢᏍᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ=ᏗᏓᎦᏘᎸᏍᏗ_array.network_host) as 연결다리:
            ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ = subprocess.call(ᎤᏁᏤᎸᎩ(ᏗᏓᎦᏘᎸᏍᏗ_array.resolution) + ᎠᏑᏰᏍᏗᎢ + 연결다리.전달인수())
            if 연결다리.ᎦᎵᏓᏍᏔᏅ: raise SystemExit('network bridge: ' + 연결다리.ᎦᎵᏓᏍᏔᏅ)
        raise SystemExit(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ)
    raise SystemExit(subprocess.call(ᎤᏁᏤᎸᎩ(ᏗᏓᎦᏘᎸᏍᏗ_array.resolution) + ᎠᏑᏰᏍᏗᎢ))


if __name__ == '__main__':
    ᎠᎢᏎᏍᏗ()
