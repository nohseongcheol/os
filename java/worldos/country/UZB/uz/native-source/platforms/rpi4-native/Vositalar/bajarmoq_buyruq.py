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

Project_ildiz = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for yo_l in _난수파일들:
        try:
            os.unlink(yo_l)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Fayl:
        Fayl.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Fayl.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Fayl.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    tashkilotchi = Project_ildiz.parent / 'rpi4/build/host'
    적재기 = tashkilotchi / 'lib/ld-musl-x86_64.so.1'
    binar = tashkilotchi / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and binar.is_file():
        return [str(적재기), '--library-path', str(tashkilotchi / 'usr/lib') + ':' + str(tashkilotchi / 'lib'),
                str(binar), '-L', str(tashkilotchi / 'usr/share/qemu')]
    binar = shutil.which('qemu-system-aarch64')
    if not binar:
        raise SystemExit('raspi4b madad_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binar]


def 해상도읽기(Matn):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Matn):
        raise argparse.ArgumentTypeError('ruxsat_VALUE format_VALUE: 1920x1080')
    너비, 높이 = map(int, Matn.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('madad_VALUE klip: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Buyruq(ruxsat_VALUE=(640, 480)):
    Fon_VALUE = 모의기계()
    지원목록 = subprocess.check_output(Fon_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*ruxsat_VALUE))
    return Fon_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(Project_ildiz / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Bajarish():
    parser = argparse.ArgumentParser(description='자체 Java Pi4 o_zak_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Chiqish_ilova.')
    parser.add_argument('--display', default='none', help='none 또는 gtk/sdl (tashkilotchi madad_VALUE 필요)')
    parser.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Hajmi. 예: 1920x1080; sukut_bo_yicha_qiymat 640x480')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Kalit_VALUE 입력은 UART 터미널에서 합니다.')
    parser.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    parser.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    parser.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Ulanish; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    parser.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    parser.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP boshqaruv_VALUE 포트 (데이터 50000..50007)')
    parser.add_argument('--guest-ip', default=None, help='QEMU NAT Oldinga_VALUE nishon. 기본은 ip.conf의 IP; o_zgartirmoq_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    parser.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 manzil. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN manzil: 외부 aloqa_e05f319b')
    parser.add_argument('--forward', action='append', default=[], help='--network 추가 Ulanish: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    parser.add_argument('--pip', action='store_true', help='PyPI manba_daraxt to_plam 중계 Bajarish (--network 필요, MicroPython 호환 소스만)')
    parser.add_argument('--pip-port', type=int, default=8027, help='to_plam 중계의 localhost TCP 포트')
    parser.add_argument('--pip-cache', type=Path, default=Project_ildiz/'build/pip-cache')
    parser.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    dalil_ARRAY = parser.parse_args()
    if dalil_ARRAY.remote:
        dalil_ARRAY.network=True
        dalil_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; parol_VALUE: python3 Vositalar/masofaviy_Sozlamalar.py show'.format(dalil_ARRAY.network_host,dalil_ARRAY.network_host),flush=True)
    if dalil_ARRAY.pip and not dalil_ARRAY.network: parser.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= dalil_ARRAY.pip_port <= 65535: parser.error('--pip-port 범위는 1~65535입니다.')
    if dalil_ARRAY.forward and not dalil_ARRAY.network: parser.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as resurs_VALUE:
        if dalil_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            resurs_VALUE.enter_context(꾸러미중계(dalil_ARRAY.pip_port, dalil_ARRAY.pip_cache, dalil_ARRAY.pip_offline))
            print('to_plam 중계: 127.0.0.1:' + str(dalil_ARRAY.pip_port), flush=True)
        Ishga_tushirish(dalil_ARRAY)


def Ishga_tushirish(dalil_ARRAY):
    if dalil_ARRAY.desktop:
        if dalil_ARRAY.vnc or dalil_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ishchi_stol_ko_rinish import ishlash_ishchi_stol
        raise SystemExit(ishlash_ishchi_stol(dalil_ARRAY.port, Tarmoq=dalil_ARRAY.network, 파일전송접속번호=dalil_ARRAY.ftp_port, 전달규칙들=dalil_ARRAY.forward, ruxsat_VALUE=dalil_ARRAY.resolution, mehmon_manzil=dalil_ARRAY.guest_ip, tashkilotchi_manzil=dalil_ARRAY.network_host))
    Opsiyalar = ['-display', dalil_ARRAY.display, '-serial', 'mon:stdio']
    if dalil_ARRAY.vnc:
        Opsiyalar += ['-vnc', dalil_ARRAY.vnc]
    if dalil_ARRAY.network:
        from 통신다리 import 통신다리
        with 통신다리(dalil_ARRAY.ftp_port, dalil_ARRAY.forward, mehmon_manzil=dalil_ARRAY.guest_ip, tashkilotchi_manzil=dalil_ARRAY.network_host) as 연결다리:
            holat_VALUE_e10195a1 = subprocess.call(Buyruq(dalil_ARRAY.resolution) + Opsiyalar + 연결다리.전달인수())
            if 연결다리.Xato: raise SystemExit('network bridge: ' + 연결다리.Xato)
        raise SystemExit(holat_VALUE_e10195a1)
    raise SystemExit(subprocess.call(Buyruq(dalil_ARRAY.resolution) + Opsiyalar))


if __name__ == '__main__':
    Bajarish()
