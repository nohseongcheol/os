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
    for මාර්_ගය in _난수파일들:
        try:
            os.unlink(මාර්_ගය)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ගොනු:
        ගොනු.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(ගොනු.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ගොනු.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    ධාරකය = 기준.parent / 'rpi4/build/host'
    적재기 = ධාරකය / 'lib/ld-musl-x86_64.so.1'
    ද්විමය = ධාරකය / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and ද්විමය.is_file():
        return [str(적재기), '--library-path', str(ධාරකය / 'usr/lib') + ':' + str(ධාරකය / 'lib'),
                str(ද්විමය), '-L', str(ධාරකය / 'usr/share/qemu')]
    ද්විමය = shutil.which('qemu-system-aarch64')
    if not ද්විමය:
        raise SystemExit('raspi4b සහාය_අගය QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ද්විමය]


def 해상도읽기(පෙළ):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', පෙළ):
        raise argparse.ArgumentTypeError('විභේදනය_අගය හැඩතලය_අගය: 1920x1080')
    너비, 높이 = map(int, පෙළ.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('සහාය_අගය පසුර: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def විධානය(විභේදනය_අගය=(640, 480)):
    පසුබිම_අගය = 모의기계()
    지원목록 = subprocess.check_output(පසුබිම_අගය + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*විභේදනය_අගය))
    return පසුබිම_අගය + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def ක්_රියාත්මක_කරන්න_2():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 කර්නලය_අගය. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 පිටවීම_යෙදු.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (ධාරකය සහාය_අගය 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 ප්_රමාණය. 예: 1920x1080; පෙරනිමි_අගය 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. යතුර_අගය 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 සම්බන්ද_වන්න; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP පාලකය_අගය 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT ඉදිරියට_අගය ඉලක්කය. 기본은 ip.conf의 IP; වෙනස්_කරන්න_අගය 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 යොමුව. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN යොමුව: 외부 සබැඳුම_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 සම්බන්ද_වන්න: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI මූලය_රුක පොදිය 중계 ක්_රියාත්මක_කරන්න_2 (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='පොදිය 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    විස්තාරකය_ආරා_ව = 인수해석기.parse_args()
    if විස්තාරකය_ආරා_ව.remote:
        විස්තාරකය_ආරා_ව.network=True
        විස්තාරකය_ආරා_ව.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; මුර_පදය_අගය: python3 මෙවලම්/දුරස්ථ_පසුතල.py show'.format(විස්තාරකය_ආරා_ව.network_host,විස්තාරකය_ආරා_ව.network_host),flush=True)
    if විස්තාරකය_ආරා_ව.pip and not විස්තාරකය_ආරා_ව.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= විස්තාරකය_ආරා_ව.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if විස්තාරකය_ආරා_ව.forward and not විස්තාරකය_ආරා_ව.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as සම්පත_අගය:
        if විස්තාරකය_ආරා_ව.pip:
            from 꾸러미중계 import 꾸러미중계
            සම්පත_අගය.enter_context(꾸러미중계(විස්තාරකය_ආරා_ව.pip_port, විස්තාරකය_ආරා_ව.pip_cache, විස්තාරකය_ආරා_ව.pip_offline))
            print('පොදිය 중계: 127.0.0.1:' + str(විස්තාරකය_ආරා_ව.pip_port), flush=True)
        ක්_රියාත්මක_කරන්න(විස්තාරකය_ආරා_ව)


def ක්_රියාත්මක_කරන්න(විස්තාරකය_ආරා_ව):
    if විස්තාරකය_ආරා_ව.desktop:
        if විස්තාරකය_ආරා_ව.vnc or විස්තාරකය_ආරා_ව.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from වැඩතලය_දසුන import ධාවනය_කරන්න_වැඩතලය
        raise SystemExit(ධාවනය_කරන්න_වැඩතලය(විස්තාරකය_ආරා_ව.port, ජාලය=විස්තාරකය_ආරා_ව.network, 파일전송접속번호=විස්තාරකය_ආරා_ව.ftp_port, 전달규칙들=විස්තාරකය_ආරා_ව.forward, විභේදනය_අගය=විස්තාරකය_ආරා_ව.resolution, අමුත්තා_යොමුව=විස්තාරකය_ආරා_ව.guest_ip, ධාරකය_යොමුව=විස්තාරකය_ආරා_ව.network_host))
    අභිරුචි = ['-display', විස්තාරකය_ආරා_ව.display, '-serial', 'mon:stdio']
    if විස්තාරකය_ආරා_ව.vnc:
        අභිරුචි += ['-vnc', විස්තාරකය_ආරා_ව.vnc]
    if විස්තාරකය_ආරා_ව.network:
        from ජාලය_පාලම import ජාලය_පාලම
        with ජාලය_පාලම(විස්තාරකය_ආරා_ව.ftp_port, විස්තාරකය_ආරා_ව.forward, අමුත්තා_යොමුව=විස්තාරකය_ආරා_ව.guest_ip, ධාරකය_යොමුව=විස්තාරකය_ආරා_ව.network_host) as පාලම:
            තත්වය_අගය = subprocess.call(විධානය(විස්තාරකය_ආරා_ව.resolution) + අභිරුචි + පාලම.전달인수())
            if පාලම.දෝෂය: raise SystemExit('network bridge: ' + පාලම.දෝෂය)
        raise SystemExit(තත්වය_අගය)
    raise SystemExit(subprocess.call(විධානය(විස්තාරකය_ආරා_ව.resolution) + අභිරුචි))


if __name__ == '__main__':
    ක්_රියාත්මක_කරන්න_2()
