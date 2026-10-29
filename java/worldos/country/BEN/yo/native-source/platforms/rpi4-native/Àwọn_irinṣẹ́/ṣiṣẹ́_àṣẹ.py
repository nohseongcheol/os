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
    for ọ̀nà in _난수파일들:
        try:
            os.unlink(ọ̀nà)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Fáìlì:
        Fáìlì.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Fáìlì.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Fáìlì.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    olùpèsè = 기준.parent / 'rpi4/build/host'
    적재기 = olùpèsè / 'lib/ld-musl-x86_64.so.1'
    abèjì = olùpèsè / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and abèjì.is_file():
        return [str(적재기), '--library-path', str(olùpèsè / 'usr/lib') + ':' + str(olùpèsè / 'lib'),
                str(abèjì), '-L', str(olùpèsè / 'usr/share/qemu')]
    abèjì = shutil.which('qemu-system-aarch64')
    if not abèjì:
        raise SystemExit('raspi4b àtìlẹ́yìn_iye QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [abèjì]


def 해상도읽기(SMS):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', SMS):
        raise argparse.ArgumentTypeError('ìmúsí_àwòrán_iye ìgúnrégé_iye: 1920x1080')
    너비, 높이 = map(int, SMS.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('àtìlẹ́yìn_iye ní_ṣókí: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Àṣẹ(ìmúsí_àwòrán_iye=(640, 480)):
    Àgbétẹ́lẹ̀_iye = 모의기계()
    지원목록 = subprocess.check_output(Àgbétẹ́lẹ̀_iye + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*ìmúsí_àwòrán_iye))
    return Àgbétẹ́lẹ̀_iye + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Rọ́ọ̀nù():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 kánẹ́ẹ̀lì_iye. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 jáde_àtòjọ_ètò.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (olùpèsè àtìlẹ́yìn_iye 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Ìwọ̀n. 예: 1920x1080; àdáwọ̀ 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC ohun_èlò_alárídìmú_ojú 5902. bọ́tìnnì_iye 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC ohun_èlò_alárídìmú_ojú')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Darapọ̀; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP ìdarí_iye ohun_èlò_alárídìmú_ojú (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT tari_sí_iye àfojúsùn. 기본은 ip.conf의 IP; ṣàyípadà_iye 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 àdírẹ́ẹ̀sì. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN àdírẹ́ẹ̀sì: 외부 Ìsomọ́_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 Darapọ̀: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI orísun_ètò_afigijúwe àkópọ̀ 중계 Rọ́ọ̀nù (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='àkópọ̀ 중계의 localhost TCP ohun_èlò_alárídìmú_ojú')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    ágúmẹ́ntì_ÀRÉÈ = 인수해석기.parse_args()
    if ágúmẹ́ntì_ÀRÉÈ.remote:
        ágúmẹ́ntì_ÀRÉÈ.network=True
        ágúmẹ́ntì_ÀRÉÈ.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; ọ̀rọ̀_aṣínà_iye: python3 Àwọn_irinṣẹ́/Ìjìnnà_Àwọn_ààtò.py show'.format(ágúmẹ́ntì_ÀRÉÈ.network_host,ágúmẹ́ntì_ÀRÉÈ.network_host),flush=True)
    if ágúmẹ́ntì_ÀRÉÈ.pip and not ágúmẹ́ntì_ÀRÉÈ.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= ágúmẹ́ntì_ÀRÉÈ.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if ágúmẹ́ntì_ÀRÉÈ.forward and not ágúmẹ́ntì_ÀRÉÈ.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ohun_àmúlò_iye:
        if ágúmẹ́ntì_ÀRÉÈ.pip:
            from 꾸러미중계 import 꾸러미중계
            ohun_àmúlò_iye.enter_context(꾸러미중계(ágúmẹ́ntì_ÀRÉÈ.pip_port, ágúmẹ́ntì_ÀRÉÈ.pip_cache, ágúmẹ́ntì_ÀRÉÈ.pip_offline))
            print('àkópọ̀ 중계: 127.0.0.1:' + str(ágúmẹ́ntì_ÀRÉÈ.pip_port), flush=True)
        ṣiṣẹ́_iṣẹ́(ágúmẹ́ntì_ÀRÉÈ)


def ṣiṣẹ́_iṣẹ́(ágúmẹ́ntì_ÀRÉÈ):
    if ágúmẹ́ntì_ÀRÉÈ.desktop:
        if ágúmẹ́ntì_ÀRÉÈ.vnc or ágúmẹ́ntì_ÀRÉÈ.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from àtẹ_iṣẹ́_wo import ṣiṣẹ́_àtẹ_iṣẹ́
        raise SystemExit(ṣiṣẹ́_àtẹ_iṣẹ́(ágúmẹ́ntì_ÀRÉÈ.port, Alásopọ̀=ágúmẹ́ntì_ÀRÉÈ.network, 파일전송접속번호=ágúmẹ́ntì_ÀRÉÈ.ftp_port, 전달규칙들=ágúmẹ́ntì_ÀRÉÈ.forward, ìmúsí_àwòrán_iye=ágúmẹ́ntì_ÀRÉÈ.resolution, àlejò_àdírẹ́ẹ̀sì=ágúmẹ́ntì_ÀRÉÈ.guest_ip, olùpèsè_àdírẹ́ẹ̀sì=ágúmẹ́ntì_ÀRÉÈ.network_host))
    Àwọn_Ẹ̀yàn = ['-display', ágúmẹ́ntì_ÀRÉÈ.display, '-serial', 'mon:stdio']
    if ágúmẹ́ntì_ÀRÉÈ.vnc:
        Àwọn_Ẹ̀yàn += ['-vnc', ágúmẹ́ntì_ÀRÉÈ.vnc]
    if ágúmẹ́ntì_ÀRÉÈ.network:
        from Alásopọ̀_afará import Alásopọ̀_afará
        with Alásopọ̀_afará(ágúmẹ́ntì_ÀRÉÈ.ftp_port, ágúmẹ́ntì_ÀRÉÈ.forward, àlejò_àdírẹ́ẹ̀sì=ágúmẹ́ntì_ÀRÉÈ.guest_ip, olùpèsè_àdírẹ́ẹ̀sì=ágúmẹ́ntì_ÀRÉÈ.network_host) as afará:
            ipò_iye = subprocess.call(Àṣẹ(ágúmẹ́ntì_ÀRÉÈ.resolution) + Àwọn_Ẹ̀yàn + afará.전달인수())
            if afará.àṣìṣe: raise SystemExit('network bridge: ' + afará.àṣìṣe)
        raise SystemExit(ipò_iye)
    raise SystemExit(subprocess.call(Àṣẹ(ágúmẹ́ntì_ÀRÉÈ.resolution) + Àwọn_Ẹ̀yàn))


if __name__ == '__main__':
    Rọ́ọ̀nù()
