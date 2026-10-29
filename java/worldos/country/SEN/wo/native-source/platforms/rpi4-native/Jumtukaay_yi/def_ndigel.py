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
    for Yoonu_jëmale in _난수파일들:
        try:
            os.unlink(Yoonu_jëmale)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as bara_denc:
        bara_denc.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(bara_denc.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(bara_denc.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    dalal = 기준.parent / 'rpi4/build/host'
    적재기 = dalal / 'lib/ld-musl-x86_64.so.1'
    Seexalin_ci_kaw_0_et1 = dalal / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and Seexalin_ci_kaw_0_et1.is_file():
        return [str(적재기), '--library-path', str(dalal / 'usr/lib') + ':' + str(dalal / 'lib'),
                str(Seexalin_ci_kaw_0_et1), '-L', str(dalal / 'usr/share/qemu')]
    Seexalin_ci_kaw_0_et1 = shutil.which('qemu-system-aarch64')
    if not Seexalin_ci_kaw_0_et1:
        raise SystemExit('raspi4b Ndimbal_xëyma QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [Seexalin_ci_kaw_0_et1]


def 해상도읽기(Tekst):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Tekst):
        raise argparse.ArgumentTypeError('Sottal_xëyma dayo_xëyma: 1920x1080')
    너비, 높이 = map(int, Tekst.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Ndimbal_xëyma kilip: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def ndigel(Sottal_xëyma=(640, 480)):
    Njiitlay_xëyma = 모의기계()
    지원목록 = subprocess.check_output(Njiitlay_xëyma + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*Sottal_xëyma))
    return Njiitlay_xëyma + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def daw():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 xoox_xëyma. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Génn_jëfekaay.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (dalal Ndimbal_xëyma 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 tolluwaay. 예: 1920x1080; xayma_bi_teew 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC jumtukaay_jël 5902. kër_xëyma 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC jumtukaay_jël')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 JOKKOO; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP Saytu_doxinu_ordinateur_xëyma jumtukaay_jël (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT jëmal_kanam_xëyma luñu_name. 기본은 ip.conf의 IP; soppi_xëyma_16f64fe4 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 dëkkuwaay. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN dëkkuwaay: 외부 jokkalóo_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 JOKKOO: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI Cosaan_tëralinuy_pàcc takku_xéewël 중계 daw (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='takku_xéewël 중계의 localhost TCP jumtukaay_jël')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    Tegtal_TABLO = 인수해석기.parse_args()
    if Tegtal_TABLO.remote:
        Tegtal_TABLO.network=True
        Tegtal_TABLO.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; pasu_dugg_xëyma: python3 Jumtukaay_yi/lu_soree_Jekkal_yi.py show'.format(Tegtal_TABLO.network_host,Tegtal_TABLO.network_host),flush=True)
    if Tegtal_TABLO.pip and not Tegtal_TABLO.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= Tegtal_TABLO.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if Tegtal_TABLO.forward and not Tegtal_TABLO.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as Kàttan_xëyma:
        if Tegtal_TABLO.pip:
            from 꾸러미중계 import 꾸러미중계
            Kàttan_xëyma.enter_context(꾸러미중계(Tegtal_TABLO.pip_port, Tegtal_TABLO.pip_cache, Tegtal_TABLO.pip_offline))
            print('takku_xéewël 중계: 127.0.0.1:' + str(Tegtal_TABLO.pip_port), flush=True)
        def_ligeey(Tegtal_TABLO)


def def_ligeey(Tegtal_TABLO):
    if Tegtal_TABLO.desktop:
        if Tegtal_TABLO.vnc or Tegtal_TABLO.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from Biro_wonin import daw_Biro
        raise SystemExit(daw_Biro(Tegtal_TABLO.port, mbaal=Tegtal_TABLO.network, 파일전송접속번호=Tegtal_TABLO.ftp_port, 전달규칙들=Tegtal_TABLO.forward, Sottal_xëyma=Tegtal_TABLO.resolution, gan_dëkkuwaay=Tegtal_TABLO.guest_ip, dalal_dëkkuwaay=Tegtal_TABLO.network_host))
    tànneef = ['-display', Tegtal_TABLO.display, '-serial', 'mon:stdio']
    if Tegtal_TABLO.vnc:
        tànneef += ['-vnc', Tegtal_TABLO.vnc]
    if Tegtal_TABLO.network:
        from mbaal_poŋ import mbaal_poŋ
        with mbaal_poŋ(Tegtal_TABLO.ftp_port, Tegtal_TABLO.forward, gan_dëkkuwaay=Tegtal_TABLO.guest_ip, dalal_dëkkuwaay=Tegtal_TABLO.network_host) as poŋ:
            nekkin_xëyma = subprocess.call(ndigel(Tegtal_TABLO.resolution) + tànneef + poŋ.전달인수())
            if poŋ.njumte: raise SystemExit('network bridge: ' + poŋ.njumte)
        raise SystemExit(nekkin_xëyma)
    raise SystemExit(subprocess.call(ndigel(Tegtal_TABLO.resolution) + tànneef))


if __name__ == '__main__':
    daw()
