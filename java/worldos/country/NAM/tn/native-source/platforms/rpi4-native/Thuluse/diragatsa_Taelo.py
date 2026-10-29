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
    for tsela in _난수파일들:
        try:
            os.unlink(tsela)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as faele:
        faele.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(faele.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(faele.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    pinagare = 기준.parent / 'rpi4/build/host'
    적재기 = pinagare / 'lib/ld-musl-x86_64.so.1'
    baenari = pinagare / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and baenari.is_file():
        return [str(적재기), '--library-path', str(pinagare / 'usr/lib') + ':' + str(pinagare / 'lib'),
                str(baenari), '-L', str(pinagare / 'usr/share/qemu')]
    baenari = shutil.which('qemu-system-aarch64')
    if not baenari:
        raise SystemExit('raspi4b Thuso_Boleng QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [baenari]


def 해상도읽기(SMS):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', SMS):
        raise argparse.ArgumentTypeError('resolušene_Boleng fometa_Boleng: 1920x1080')
    너비, 높이 = map(int, SMS.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Thuso_Boleng faelekhutshwe_ya_media: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Taelo(resolušene_Boleng=(640, 480)):
    Lemorago_Boleng = 모의기계()
    지원목록 = subprocess.check_output(Lemorago_Boleng + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*resolušene_Boleng))
    return Lemorago_Boleng + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def dirisa():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 Khenele_Boleng. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 tswaya_Tiriso.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (pinagare Thuso_Boleng 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 lekanya. 예: 1920x1080; boleng_jo_bo_rulaganyeditsweng_ruri 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. taetsi_Boleng 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Golaganya; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP taolo_Boleng 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT fetisa_Boleng_24592b8a setotwa. 기본은 ip.conf의 IP; fetola_Boleng 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 aterese. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN aterese: 외부 Kgolagano_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 Golaganya: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI Motswedi_sebopego_sa_tshedimosetso ngatanngwe 중계 dirisa (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='ngatanngwe 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    Thulaganyo_setlhopha = 인수해석기.parse_args()
    if Thulaganyo_setlhopha.remote:
        Thulaganyo_setlhopha.network=True
        Thulaganyo_setlhopha.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; khoututseno_Boleng: python3 Thuluse/kgakala_Diseting.py show'.format(Thulaganyo_setlhopha.network_host,Thulaganyo_setlhopha.network_host),flush=True)
    if Thulaganyo_setlhopha.pip and not Thulaganyo_setlhopha.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= Thulaganyo_setlhopha.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if Thulaganyo_setlhopha.forward and not Thulaganyo_setlhopha.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as sediriswa_Boleng:
        if Thulaganyo_setlhopha.pip:
            from 꾸러미중계 import 꾸러미중계
            sediriswa_Boleng.enter_context(꾸러미중계(Thulaganyo_setlhopha.pip_port, Thulaganyo_setlhopha.pip_cache, Thulaganyo_setlhopha.pip_offline))
            print('ngatanngwe 중계: 127.0.0.1:' + str(Thulaganyo_setlhopha.pip_port), flush=True)
        diragatsa_Tiro(Thulaganyo_setlhopha)


def diragatsa_Tiro(Thulaganyo_setlhopha):
    if Thulaganyo_setlhopha.desktop:
        if Thulaganyo_setlhopha.vnc or Thulaganyo_setlhopha.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from desekethopo_Tebego import dirisa_desekethopo
        raise SystemExit(dirisa_desekethopo(Thulaganyo_setlhopha.port, Neteweke=Thulaganyo_setlhopha.network, 파일전송접속번호=Thulaganyo_setlhopha.ftp_port, 전달규칙들=Thulaganyo_setlhopha.forward, resolušene_Boleng=Thulaganyo_setlhopha.resolution, moeng_aterese=Thulaganyo_setlhopha.guest_ip, pinagare_aterese=Thulaganyo_setlhopha.network_host))
    Diitlhophelwa = ['-display', Thulaganyo_setlhopha.display, '-serial', 'mon:stdio']
    if Thulaganyo_setlhopha.vnc:
        Diitlhophelwa += ['-vnc', Thulaganyo_setlhopha.vnc]
    if Thulaganyo_setlhopha.network:
        from Neteweke_leborogo import Neteweke_leborogo
        with Neteweke_leborogo(Thulaganyo_setlhopha.ftp_port, Thulaganyo_setlhopha.forward, moeng_aterese=Thulaganyo_setlhopha.guest_ip, pinagare_aterese=Thulaganyo_setlhopha.network_host) as leborogo:
            kemo_Boleng = subprocess.call(Taelo(Thulaganyo_setlhopha.resolution) + Diitlhophelwa + leborogo.전달인수())
            if leborogo.phoso: raise SystemExit('network bridge: ' + leborogo.phoso)
        raise SystemExit(kemo_Boleng)
    raise SystemExit(subprocess.call(Taelo(Thulaganyo_setlhopha.resolution) + Diitlhophelwa))


if __name__ == '__main__':
    dirisa()
