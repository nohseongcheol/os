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

Project_kök = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for Cığır in _난수파일들:
        try:
            os.unlink(Cığır)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as FAYL:
        FAYL.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(FAYL.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(FAYL.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    host = Project_kök.parent / 'rpi4/build/host'
    적재기 = host / 'lib/ld-musl-x86_64.so.1'
    ikili = host / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and ikili.is_file():
        return [str(적재기), '--library-path', str(host / 'usr/lib') + ':' + str(host / 'lib'),
                str(ikili), '-L', str(host / 'usr/share/qemu')]
    ikili = shutil.which('qemu-system-aarch64')
    if not ikili:
        raise SystemExit('raspi4b Dəstək_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ikili]


def 해상도읽기(Mətn):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Mətn):
        raise argparse.ArgumentTypeError('əksetmə_qabiliyyəti_VALUE format_VALUE: 1920x1080')
    너비, 높이 = map(int, Mətn.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Dəstək_VALUE klip: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Əmr(əksetmə_qabiliyyəti_VALUE=(640, 480)):
    Fon_VALUE = 모의기계()
    지원목록 = subprocess.check_output(Fon_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*əksetmə_qabiliyyəti_VALUE))
    return Fon_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(Project_kök / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def İcra_Et():
    parser = argparse.ArgumentParser(description='자체 Java Pi4 nüvə_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Çıxış_proqram.')
    parser.add_argument('--display', default='none', help='none 또는 gtk/sdl (host Dəstək_VALUE 필요)')
    parser.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Böyüklük. 예: 1920x1080; standart_qiymət 640x480')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Açar_VALUE 입력은 UART 터미널에서 합니다.')
    parser.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    parser.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    parser.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Bağlan; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    parser.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    parser.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP nəzarət_VALUE 포트 (데이터 50000..50007)')
    parser.add_argument('--guest-ip', default=None, help='QEMU NAT irəli_VALUE hədəf. 기본은 ip.conf의 IP; dəyişdirmək_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    parser.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ünvan. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ünvan: 외부 qoşulma_e05f319b')
    parser.add_argument('--forward', action='append', default=[], help='--network 추가 Bağlan: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    parser.add_argument('--pip', action='store_true', help='PyPI mənbə_ağac paket 중계 İcra_Et (--network 필요, MicroPython 호환 소스만)')
    parser.add_argument('--pip-port', type=int, default=8027, help='paket 중계의 localhost TCP 포트')
    parser.add_argument('--pip-cache', type=Path, default=Project_kök/'build/pip-cache')
    parser.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    arqument_ARRAY = parser.parse_args()
    if arqument_ARRAY.remote:
        arqument_ARRAY.network=True
        arqument_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; parol_VALUE: python3 Alətlər/uzaq_Parametrlər.py show'.format(arqument_ARRAY.network_host,arqument_ARRAY.network_host),flush=True)
    if arqument_ARRAY.pip and not arqument_ARRAY.network: parser.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= arqument_ARRAY.pip_port <= 65535: parser.error('--pip-port 범위는 1~65535입니다.')
    if arqument_ARRAY.forward and not arqument_ARRAY.network: parser.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as resurs_VALUE:
        if arqument_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            resurs_VALUE.enter_context(꾸러미중계(arqument_ARRAY.pip_port, arqument_ARRAY.pip_cache, arqument_ARRAY.pip_offline))
            print('paket 중계: 127.0.0.1:' + str(arqument_ARRAY.pip_port), flush=True)
        icra_etmək_tapşırıq(arqument_ARRAY)


def icra_etmək_tapşırıq(arqument_ARRAY):
    if arqument_ARRAY.desktop:
        if arqument_ARRAY.vnc or arqument_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from iş_masası_baxmaq import icra_iş_masası
        raise SystemExit(icra_iş_masası(arqument_ARRAY.port, Şəbəkə=arqument_ARRAY.network, 파일전송접속번호=arqument_ARRAY.ftp_port, 전달규칙들=arqument_ARRAY.forward, əksetmə_qabiliyyəti_VALUE=arqument_ARRAY.resolution, qonaq_ünvan=arqument_ARRAY.guest_ip, host_ünvan=arqument_ARRAY.network_host))
    Seçimlər = ['-display', arqument_ARRAY.display, '-serial', 'mon:stdio']
    if arqument_ARRAY.vnc:
        Seçimlər += ['-vnc', arqument_ARRAY.vnc]
    if arqument_ARRAY.network:
        from Şəbəkə_körpü import Şəbəkə_körpü
        with Şəbəkə_körpü(arqument_ARRAY.ftp_port, arqument_ARRAY.forward, qonaq_ünvan=arqument_ARRAY.guest_ip, host_ünvan=arqument_ARRAY.network_host) as körpü:
            vəziyyət_VALUE = subprocess.call(Əmr(arqument_ARRAY.resolution) + Seçimlər + körpü.전달인수())
            if körpü.XƏTA: raise SystemExit('network bridge: ' + körpü.XƏTA)
        raise SystemExit(vəziyyət_VALUE)
    raise SystemExit(subprocess.call(Əmr(arqument_ARRAY.resolution) + Seçimlər))


if __name__ == '__main__':
    İcra_Et()
