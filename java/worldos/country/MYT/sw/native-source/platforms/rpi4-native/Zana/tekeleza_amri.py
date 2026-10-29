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
    for njia in _난수파일들:
        try:
            os.unlink(njia)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as faili:
        faili.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(faili.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(faili.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    mwenyeji = 기준.parent / 'rpi4/build/host'
    적재기 = mwenyeji / 'lib/ld-musl-x86_64.so.1'
    jozi = mwenyeji / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and jozi.is_file():
        return [str(적재기), '--library-path', str(mwenyeji / 'usr/lib') + ':' + str(mwenyeji / 'lib'),
                str(jozi), '-L', str(mwenyeji / 'usr/share/qemu')]
    jozi = shutil.which('qemu-system-aarch64')
    if not jozi:
        raise SystemExit('raspi4b Auni_thamani QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [jozi]


def 해상도읽기(SMS):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', SMS):
        raise argparse.ArgumentTypeError('mwonekano_thamani umbiza_thamani: 1920x1080')
    너비, 높이 = map(int, SMS.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Auni_thamani dondoo: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def amri(mwonekano_thamani=(640, 480)):
    nyuma_thamani = 모의기계()
    지원목록 = subprocess.check_output(nyuma_thamani + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*mwonekano_thamani))
    return nyuma_thamani + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def endesha():
    kichanganuzi = argparse.ArgumentParser(description='자체 Java Pi4 kiini_thamani_0611a8a8. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 toka_programu.')
    kichanganuzi.add_argument('--display', default='none', help='none 또는 gtk/sdl (mwenyeji Auni_thamani 필요)')
    kichanganuzi.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 panga_ukubwa. 예: 1920x1080; hali_ya_chaguo_msingi 640x480')
    kichanganuzi.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Kitufe_thamani 입력은 UART 터미널에서 합니다.')
    kichanganuzi.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    kichanganuzi.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    kichanganuzi.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 UNGANISHA; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    kichanganuzi.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    kichanganuzi.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP udhibiti_thamani 포트 (데이터 50000..50007)')
    kichanganuzi.add_argument('--guest-ip', default=None, help='QEMU NAT tuma_mbele_thamani lengo. 기본은 ip.conf의 IP; badilisha_thamani_16f64fe4 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    kichanganuzi.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 anwani. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN anwani: 외부 muunganisho_e05f319b')
    kichanganuzi.add_argument('--forward', action='append', default=[], help='--network 추가 UNGANISHA: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    kichanganuzi.add_argument('--pip', action='store_true', help='PyPI chanzo_mti fungasha 중계 endesha (--network 필요, MicroPython 호환 소스만)')
    kichanganuzi.add_argument('--pip-port', type=int, default=8027, help='fungasha 중계의 localhost TCP 포트')
    kichanganuzi.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    kichanganuzi.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    hoja_ARRAY = kichanganuzi.parse_args()
    if hoja_ARRAY.remote:
        hoja_ARRAY.network=True
        hoja_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; nywila_thamani: python3 Zana/kwa_mbali_Mipangilio.py show'.format(hoja_ARRAY.network_host,hoja_ARRAY.network_host),flush=True)
    if hoja_ARRAY.pip and not hoja_ARRAY.network: kichanganuzi.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= hoja_ARRAY.pip_port <= 65535: kichanganuzi.error('--pip-port 범위는 1~65535입니다.')
    if hoja_ARRAY.forward and not hoja_ARRAY.network: kichanganuzi.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as rasilimali_thamani:
        if hoja_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            rasilimali_thamani.enter_context(꾸러미중계(hoja_ARRAY.pip_port, hoja_ARRAY.pip_cache, hoja_ARRAY.pip_offline))
            print('fungasha 중계: 127.0.0.1:' + str(hoja_ARRAY.pip_port), flush=True)
        tekeleza_kazi(hoja_ARRAY)


def tekeleza_kazi(hoja_ARRAY):
    if hoja_ARRAY.desktop:
        if hoja_ARRAY.vnc or hoja_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from Eneo_kazi_Onesha import endesha_Eneo_kazi
        raise SystemExit(endesha_Eneo_kazi(hoja_ARRAY.port, Mtandao=hoja_ARRAY.network, faili_hamisha_namba_ya_kituo=hoja_ARRAY.ftp_port, 전달규칙들=hoja_ARRAY.forward, mwonekano_thamani=hoja_ARRAY.resolution, mgeni_anwani=hoja_ARRAY.guest_ip, mwenyeji_anwani=hoja_ARRAY.network_host))
    chaguo = ['-display', hoja_ARRAY.display, '-serial', 'mon:stdio']
    if hoja_ARRAY.vnc:
        chaguo += ['-vnc', hoja_ARRAY.vnc]
    if hoja_ARRAY.network:
        from Mtandao_daraja import Mtandao_daraja
        with Mtandao_daraja(hoja_ARRAY.ftp_port, hoja_ARRAY.forward, mgeni_anwani=hoja_ARRAY.guest_ip, mwenyeji_anwani=hoja_ARRAY.network_host) as daraja:
            hali_thamani = subprocess.call(amri(hoja_ARRAY.resolution) + chaguo + daraja.전달인수())
            if daraja.kosa: raise SystemExit('network bridge: ' + daraja.kosa)
        raise SystemExit(hali_thamani)
    raise SystemExit(subprocess.call(amri(hoja_ARRAY.resolution) + chaguo))


if __name__ == '__main__':
    endesha()
