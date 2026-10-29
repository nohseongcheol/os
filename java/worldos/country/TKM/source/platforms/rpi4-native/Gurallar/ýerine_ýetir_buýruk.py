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
    for Ýol in _난수파일들:
        try:
            os.unlink(Ýol)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Faýl:
        Faýl.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Faýl.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Faýl.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    esasy = 기준.parent / 'rpi4/build/host'
    적재기 = esasy / 'lib/ld-musl-x86_64.so.1'
    ikilik = esasy / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and ikilik.is_file():
        return [str(적재기), '--library-path', str(esasy / 'usr/lib') + ':' + str(esasy / 'lib'),
                str(ikilik), '-L', str(esasy / 'usr/share/qemu')]
    ikilik = shutil.which('qemu-system-aarch64')
    if not ikilik:
        raise SystemExit('raspi4b Goldaw_baha QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ikilik]


def 해상도읽기(Metin):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Metin):
        raise argparse.ArgumentTypeError('çözgüt_baha format_baha: 1920x1080')
    너비, 높이 = map(int, Metin.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Goldaw_baha klip: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def buýruk(çözgüt_baha=(640, 480)):
    Fon_baha = 모의기계()
    지원목록 = subprocess.check_output(Fon_baha + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*çözgüt_baha))
    return Fon_baha + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Bitir():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 ýadro_baha. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 çyk_programma.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (esasy Goldaw_baha 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Ululyk. 예: 1920x1080; öňünden_kabul_edilen_baha 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. açar_baha 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Birikme; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP dolandyryş_baha 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT ugrukdyr_baha niýet. 기본은 ip.conf의 IP; üýtget_baha 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 salgy. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN salgy: 외부 birikme_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 Birikme: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI gor_agaç toplum 중계 Bitir (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='toplum 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    argument_ARRAY = 인수해석기.parse_args()
    if argument_ARRAY.remote:
        argument_ARRAY.network=True
        argument_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; parol_baha: python3 Gurallar/uzakdan_Sazlamalar.py show'.format(argument_ARRAY.network_host,argument_ARRAY.network_host),flush=True)
    if argument_ARRAY.pip and not argument_ARRAY.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argument_ARRAY.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if argument_ARRAY.forward and not argument_ARRAY.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as gor_baha:
        if argument_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            gor_baha.enter_context(꾸러미중계(argument_ARRAY.pip_port, argument_ARRAY.pip_cache, argument_ARRAY.pip_offline))
            print('toplum 중계: 127.0.0.1:' + str(argument_ARRAY.pip_port), flush=True)
        ýerine_ýetir_tabşyryk(argument_ARRAY)


def ýerine_ýetir_tabşyryk(argument_ARRAY):
    if argument_ARRAY.desktop:
        if argument_ARRAY.vnc or argument_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from iş_stoly_görkez import işe_goýber_iş_stoly
        raise SystemExit(işe_goýber_iş_stoly(argument_ARRAY.port, Tor=argument_ARRAY.network, 파일전송접속번호=argument_ARRAY.ftp_port, 전달규칙들=argument_ARRAY.forward, çözgüt_baha=argument_ARRAY.resolution, 게스트주소=argument_ARRAY.guest_ip, esasy_salgy=argument_ARRAY.network_host))
    Opsiýalar = ['-display', argument_ARRAY.display, '-serial', 'mon:stdio']
    if argument_ARRAY.vnc:
        Opsiýalar += ['-vnc', argument_ARRAY.vnc]
    if argument_ARRAY.network:
        from 통신다리 import 통신다리
        with 통신다리(argument_ARRAY.ftp_port, argument_ARRAY.forward, 게스트주소=argument_ARRAY.guest_ip, esasy_salgy=argument_ARRAY.network_host) as 연결다리:
            ýagdaý_baha = subprocess.call(buýruk(argument_ARRAY.resolution) + Opsiýalar + 연결다리.전달인수())
            if 연결다리.Hata: raise SystemExit('network bridge: ' + 연결다리.Hata)
        raise SystemExit(ýagdaý_baha)
    raise SystemExit(subprocess.call(buýruk(argument_ARRAY.resolution) + Opsiýalar))


if __name__ == '__main__':
    Bitir()
