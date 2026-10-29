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
    for aqqut in _난수파일들:
        try:
            os.unlink(aqqut)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ini:
        ini.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(ini.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ini.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    tuttarvik = 기준.parent / 'rpi4/build/host'
    적재기 = tuttarvik / 'lib/ld-musl-x86_64.so.1'
    binary = tuttarvik / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and binary.is_file():
        return [str(적재기), '--library-path', str(tuttarvik / 'usr/lib') + ':' + str(tuttarvik / 'lib'),
                str(binary), '-L', str(tuttarvik / 'usr/share/qemu')]
    binary = shutil.which('qemu-system-aarch64')
    if not binary:
        raise SystemExit('raspi4b ikajuqsuiniq_atuutilik QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binary]


def 해상도읽기(titiqqaq):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', titiqqaq):
        raise argparse.ArgumentTypeError('saqqijaattiarninga_atuutilik aaqqisurli_atuutilik: 1920x1080')
    너비, 높이 = map(int, titiqqaq.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('ikajuqsuiniq_atuutilik Nakatigat: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def piqujijjut(saqqijaattiarninga_atuutilik=(640, 480)):
    ungataa_atuutilik = 모의기계()
    지원목록 = subprocess.check_output(ungataa_atuutilik + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*saqqijaattiarninga_atuutilik))
    return ungataa_atuutilik + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def 시작():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 kernel_atuutilik. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 taima_pilirijjut.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (tuttarvik ikajuqsuiniq_atuutilik 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 anininga. 예: 1920x1080; Aturniliuvagiiqtut 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. naqigaq_atuutilik 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 kasurli; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP aulattivik_atuutilik 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT sivummualli_atuutilik turaagaq. 기본은 ip.conf의 IP; asijjirli_atuutilik 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 turaarut. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN turaarut: 외부 kasuqsimaniq_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 kasurli: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI pivviujuq_attavigiit 꾸러미 중계 시작 (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='꾸러미 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    aturniqarnirainiq_array = 인수해석기.parse_args()
    if aturniqarnirainiq_array.remote:
        aturniqarnirainiq_array.network=True
        aturniqarnirainiq_array.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; isirut_atuutilik: python3 도구/원격설정.py show'.format(aturniqarnirainiq_array.network_host,aturniqarnirainiq_array.network_host),flush=True)
    if aturniqarnirainiq_array.pip and not aturniqarnirainiq_array.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= aturniqarnirainiq_array.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if aturniqarnirainiq_array.forward and not aturniqarnirainiq_array.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as qarasaujalirijjutiit_atuutilik:
        if aturniqarnirainiq_array.pip:
            from 꾸러미중계 import 꾸러미중계
            qarasaujalirijjutiit_atuutilik.enter_context(꾸러미중계(aturniqarnirainiq_array.pip_port, aturniqarnirainiq_array.pip_cache, aturniqarnirainiq_array.pip_offline))
            print('꾸러미 중계: 127.0.0.1:' + str(aturniqarnirainiq_array.pip_port), flush=True)
        실행하기(aturniqarnirainiq_array)


def 실행하기(aturniqarnirainiq_array):
    if aturniqarnirainiq_array.desktop:
        if aturniqarnirainiq_array.vnc or aturniqarnirainiq_array.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from igalaujaq_takussarurli import 바탕화면실행
        raise SystemExit(바탕화면실행(aturniqarnirainiq_array.port, Kasuqatigiitsimajut=aturniqarnirainiq_array.network, 파일전송접속번호=aturniqarnirainiq_array.ftp_port, 전달규칙들=aturniqarnirainiq_array.forward, saqqijaattiarninga_atuutilik=aturniqarnirainiq_array.resolution, 게스트주소=aturniqarnirainiq_array.guest_ip, tuttarvik_turaarut=aturniqarnirainiq_array.network_host))
    Qanuqtuurutit = ['-display', aturniqarnirainiq_array.display, '-serial', 'mon:stdio']
    if aturniqarnirainiq_array.vnc:
        Qanuqtuurutit += ['-vnc', aturniqarnirainiq_array.vnc]
    if aturniqarnirainiq_array.network:
        from 통신다리 import 통신다리
        with 통신다리(aturniqarnirainiq_array.ftp_port, aturniqarnirainiq_array.forward, 게스트주소=aturniqarnirainiq_array.guest_ip, tuttarvik_turaarut=aturniqarnirainiq_array.network_host) as 연결다리:
            qanuilinganiq_atuutilik = subprocess.call(piqujijjut(aturniqarnirainiq_array.resolution) + Qanuqtuurutit + 연결다리.전달인수())
            if 연결다리.tammarniq: raise SystemExit('network bridge: ' + 연결다리.tammarniq)
        raise SystemExit(qanuilinganiq_atuutilik)
    raise SystemExit(subprocess.call(piqujijjut(aturniqarnirainiq_array.resolution) + Qanuqtuurutit))


if __name__ == '__main__':
    시작()
