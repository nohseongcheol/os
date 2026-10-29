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
    for Inzira in _난수파일들:
        try:
            os.unlink(Inzira)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Idosiye:
        Idosiye.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Idosiye.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Idosiye.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    gucumbikira = 기준.parent / 'rpi4/build/host'
    적재기 = gucumbikira / 'lib/ld-musl-x86_64.so.1'
    nyabibiri = gucumbikira / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and nyabibiri.is_file():
        return [str(적재기), '--library-path', str(gucumbikira / 'usr/lib') + ':' + str(gucumbikira / 'lib'),
                str(nyabibiri), '-L', str(gucumbikira / 'usr/share/qemu')]
    nyabibiri = shutil.which('qemu-system-aarch64')
    if not nyabibiri:
        raise SystemExit('raspi4b Ubufasha_agaciro QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [nyabibiri]


def 해상도읽기(Umwandiko):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Umwandiko):
        raise argparse.ArgumentTypeError('ibonerana_agaciro imiterere_agaciro: 1920x1080')
    너비, 높이 = map(int, Umwandiko.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Ubufasha_agaciro kiripu: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Icyo_wifuza(ibonerana_agaciro=(640, 480)):
    Imbuganyuma_agaciro = 모의기계()
    지원목록 = subprocess.check_output(Imbuganyuma_agaciro + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*ibonerana_agaciro))
    return Imbuganyuma_agaciro + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def ihuriro():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 intima_agaciro. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 gusohoka_porogaramu.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (gucumbikira Ubufasha_agaciro 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Ingano. 예: 1920x1080; agaciro_gasanzweho 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. buto_agaciro 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Guhuza; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP icunga_agaciro 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT koherereza_agaciro gusimbuza_igishya. 기본은 ip.conf의 IP; guhindura_agaciro_16f64fe4 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 aderesi. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN aderesi: 외부 kwihuza_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 Guhuza: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI inkomoko_igiti ipaki 중계 ihuriro (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='ipaki 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    ingingo_ARRAY = 인수해석기.parse_args()
    if ingingo_ARRAY.remote:
        ingingo_ARRAY.network=True
        ingingo_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; ijambobanga_agaciro: python3 Ibikoresho/kure_Amagenamiterere.py show'.format(ingingo_ARRAY.network_host,ingingo_ARRAY.network_host),flush=True)
    if ingingo_ARRAY.pip and not ingingo_ARRAY.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= ingingo_ARRAY.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if ingingo_ARRAY.forward and not ingingo_ARRAY.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as umutungo_agaciro:
        if ingingo_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            umutungo_agaciro.enter_context(꾸러미중계(ingingo_ARRAY.pip_port, ingingo_ARRAY.pip_cache, ingingo_ARRAY.pip_offline))
            print('ipaki 중계: 127.0.0.1:' + str(ingingo_ARRAY.pip_port), flush=True)
        gukora_umukoro(ingingo_ARRAY)


def gukora_umukoro(ingingo_ARRAY):
    if ingingo_ARRAY.desktop:
        if ingingo_ARRAY.vnc or ingingo_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from biro_igaragaza import ihuriro_biro
        raise SystemExit(ihuriro_biro(ingingo_ARRAY.port, Urusobemiyoboro=ingingo_ARRAY.network, 파일전송접속번호=ingingo_ARRAY.ftp_port, 전달규칙들=ingingo_ARRAY.forward, ibonerana_agaciro=ingingo_ARRAY.resolution, 게스트주소=ingingo_ARRAY.guest_ip, gucumbikira_aderesi=ingingo_ARRAY.network_host))
    Amahitamo = ['-display', ingingo_ARRAY.display, '-serial', 'mon:stdio']
    if ingingo_ARRAY.vnc:
        Amahitamo += ['-vnc', ingingo_ARRAY.vnc]
    if ingingo_ARRAY.network:
        from 통신다리 import 통신다리
        with 통신다리(ingingo_ARRAY.ftp_port, ingingo_ARRAY.forward, 게스트주소=ingingo_ARRAY.guest_ip, gucumbikira_aderesi=ingingo_ARRAY.network_host) as 연결다리:
            imimerere_agaciro = subprocess.call(Icyo_wifuza(ingingo_ARRAY.resolution) + Amahitamo + 연결다리.전달인수())
            if 연결다리.IKOSA: raise SystemExit('network bridge: ' + 연결다리.IKOSA)
        raise SystemExit(imimerere_agaciro)
    raise SystemExit(subprocess.call(Icyo_wifuza(ingingo_ARRAY.resolution) + Amahitamo))


if __name__ == '__main__':
    ihuriro()
