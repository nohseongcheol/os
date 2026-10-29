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

արձակել_արմատ = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for Ճանապարհ in _난수파일들:
        try:
            os.unlink(Ճանապարհ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Ֆայլ:
        Ֆայլ.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Ֆայլ.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Ֆայլ.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    հոստ = արձակել_արմատ.parent / 'rpi4/build/host'
    적재기 = հոստ / 'lib/ld-musl-x86_64.so.1'
    երկուական = հոստ / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and երկուական.is_file():
        return [str(적재기), '--library-path', str(հոստ / 'usr/lib') + ':' + str(հոստ / 'lib'),
                str(երկուական), '-L', str(հոստ / 'usr/share/qemu')]
    երկուական = shutil.which('qemu-system-aarch64')
    if not երկուական:
        raise SystemExit('raspi4b Աջակցում_արժեք QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [երկուական]


def 해상도읽기(Տեքստ):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Տեքստ):
        raise argparse.ArgumentTypeError('տարլուծում_արժեք ձեւաչափ_արժեք: 1920x1080')
    너비, 높이 = map(int, Տեքստ.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Աջակցում_արժեք հոլովակ: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Հրահանգ(տարլուծում_արժեք=(640, 480)):
    խորք_արժեք = 모의기계()
    지원목록 = subprocess.check_output(խորք_արժեք + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*տարլուծում_արժեք))
    return խորք_արժեք + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(արձակել_արմատ / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Գործարկել():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 միջուկ_արժեք. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Ելք_ծրագիր.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (հոստ Աջակցում_արժեք 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Չափս. 예: 1920x1080; սկզբնադիր_արժեք 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. ստեղն_արժեք 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Միացնել; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP հսկում_արժեք 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT Առաջ_արժեք թիրախ. 기본은 ip.conf의 IP; փոխել_արժեք 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 հասցե. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN հասցե: 외부 կապ_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 Միացնել: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI աղբյուր_ծառ փաթեթ 중계 Գործարկել (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='փաթեթ 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=արձակել_արմատ/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    արգումենտ_ԶԱՆԳՎԱԾ = 인수해석기.parse_args()
    if արգումենտ_ԶԱՆԳՎԱԾ.remote:
        արգումենտ_ԶԱՆԳՎԱԾ.network=True
        արգումենտ_ԶԱՆԳՎԱԾ.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; գաղտնաբառ_արժեք: python3 Գործիքներ/հեռակա_Կարգավորումներ.py show'.format(արգումենտ_ԶԱՆԳՎԱԾ.network_host,արգումենտ_ԶԱՆԳՎԱԾ.network_host),flush=True)
    if արգումենտ_ԶԱՆԳՎԱԾ.pip and not արգումենտ_ԶԱՆԳՎԱԾ.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= արգումենտ_ԶԱՆԳՎԱԾ.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if արգումենտ_ԶԱՆԳՎԱԾ.forward and not արգումենտ_ԶԱՆԳՎԱԾ.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as միջոց_արժեք:
        if արգումենտ_ԶԱՆԳՎԱԾ.pip:
            from 꾸러미중계 import 꾸러미중계
            միջոց_արժեք.enter_context(꾸러미중계(արգումենտ_ԶԱՆԳՎԱԾ.pip_port, արգումենտ_ԶԱՆԳՎԱԾ.pip_cache, արգումենտ_ԶԱՆԳՎԱԾ.pip_offline))
            print('փաթեթ 중계: 127.0.0.1:' + str(արգումենտ_ԶԱՆԳՎԱԾ.pip_port), flush=True)
        Կատարել(արգումենտ_ԶԱՆԳՎԱԾ)


def Կատարել(արգումենտ_ԶԱՆԳՎԱԾ):
    if արգումենտ_ԶԱՆԳՎԱԾ.desktop:
        if արգումենտ_ԶԱՆԳՎԱԾ.vnc or արգումենտ_ԶԱՆԳՎԱԾ.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from սեղան_տեսք import աշխատեցնել_սեղան
        raise SystemExit(աշխատեցնել_սեղան(արգումենտ_ԶԱՆԳՎԱԾ.port, Ցանց=արգումենտ_ԶԱՆԳՎԱԾ.network, 파일전송접속번호=արգումենտ_ԶԱՆԳՎԱԾ.ftp_port, 전달규칙들=արգումենտ_ԶԱՆԳՎԱԾ.forward, տարլուծում_արժեք=արգումենտ_ԶԱՆԳՎԱԾ.resolution, հյուր_հասցե=արգումենտ_ԶԱՆԳՎԱԾ.guest_ip, հոստ_հասցե=արգումենտ_ԶԱՆԳՎԱԾ.network_host))
    Ընտրանքներ = ['-display', արգումենտ_ԶԱՆԳՎԱԾ.display, '-serial', 'mon:stdio']
    if արգումենտ_ԶԱՆԳՎԱԾ.vnc:
        Ընտրանքներ += ['-vnc', արգումենտ_ԶԱՆԳՎԱԾ.vnc]
    if արգումենտ_ԶԱՆԳՎԱԾ.network:
        from Ցանց_կամուրջ import Ցանց_կամուրջ
        with Ցանց_կամուրջ(արգումենտ_ԶԱՆԳՎԱԾ.ftp_port, արգումենտ_ԶԱՆԳՎԱԾ.forward, հյուր_հասցե=արգումենտ_ԶԱՆԳՎԱԾ.guest_ip, հոստ_հասցե=արգումենտ_ԶԱՆԳՎԱԾ.network_host) as կամուրջ:
            վիճակ_արժեք = subprocess.call(Հրահանգ(արգումենտ_ԶԱՆԳՎԱԾ.resolution) + Ընտրանքներ + կամուրջ.전달인수())
            if կամուրջ.Սխալ: raise SystemExit('network bridge: ' + կամուրջ.Սխալ)
        raise SystemExit(վիճակ_արժեք)
    raise SystemExit(subprocess.call(Հրահանգ(արգումենտ_ԶԱՆԳՎԱԾ.resolution) + Ընտրանքներ))


if __name__ == '__main__':
    Գործարկել()
