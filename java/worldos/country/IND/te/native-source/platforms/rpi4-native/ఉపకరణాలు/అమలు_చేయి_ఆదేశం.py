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

ప్రొజెక్ట్_మూలం = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for పాత్ in _난수파일들:
        try:
            os.unlink(పాత్)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as దస్త్రం:
        దస్త్రం.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(దస్త్రం.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(దస్త్రం.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    హోస్ట్ = ప్రొజెక్ట్_మూలం.parent / 'rpi4/build/host'
    적재기 = హోస్ట్ / 'lib/ld-musl-x86_64.so.1'
    బైనరీ = హోస్ట్ / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and బైనరీ.is_file():
        return [str(적재기), '--library-path', str(హోస్ట్ / 'usr/lib') + ':' + str(హోస్ట్ / 'lib'),
                str(బైనరీ), '-L', str(హోస్ట్ / 'usr/share/qemu')]
    బైనరీ = shutil.which('qemu-system-aarch64')
    if not బైనరీ:
        raise SystemExit('raspi4b మద్దతు_మూల్యం QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [బైనరీ]


def 해상도읽기(పాఠ్యము):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', పాఠ్యము):
        raise argparse.ArgumentTypeError('స్పష్టత_మూల్యం ఆకృతి_మూల్యం: 1920x1080')
    너비, 높이 = map(int, పాఠ్యము.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('మద్దతు_మూల్యం క్లిప్: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def ఆదేశము(స్పష్టత_మూల్యం=(640, 480)):
    నేపథ్యం_మూల్యం = 모의기계()
    지원목록 = subprocess.check_output(నేపథ్యం_మూల్యం + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*స్పష్టత_మూల్యం))
    return నేపథ్యం_మూల్యం + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(ప్రొజెక్ట్_మూలం / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def నడుపుము():
    పార్సర్ = argparse.ArgumentParser(description='자체 Java Pi4 కెర్నల్_మూల్యం. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 నిష్క్రమణ_అనువర్తనం.')
    పార్సర్.add_argument('--display', default='none', help='none 또는 gtk/sdl (హోస్ట్ మద్దతు_మూల్యం 필요)')
    పార్సర్.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 పరిమాణం. 예: 1920x1080; స్వయంసిద్ధ_విలువ 640x480')
    పార్సర్.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. కీ_మూల్యం 입력은 UART 터미널에서 합니다.')
    పార్సర్.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    పార్సర్.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    పార్సర్.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 కనెక్టుచేయి; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    పార్సర్.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    పార్సర్.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP నియంత్రణ_మూల్యం 포트 (데이터 50000..50007)')
    పార్సర్.add_argument('--guest-ip', default=None, help='QEMU NAT ఫార్వార్డ్_మూల్యం లక్ష్యం. 기본은 ip.conf의 IP; మార్చు_మూల్యం 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    పార్సర్.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ఇమెయిల్. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ఇమెయిల్: 외부 కనెక్షన్_e05f319b')
    పార్సర్.add_argument('--forward', action='append', default=[], help='--network 추가 కనెక్టుచేయి: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    పార్సర్.add_argument('--pip', action='store_true', help='PyPI మూలం_వృక్షాకృతి బండిల్ 중계 నడుపుము (--network 필요, MicroPython 호환 소스만)')
    పార్సర్.add_argument('--pip-port', type=int, default=8027, help='బండిల్ 중계의 localhost TCP 포트')
    పార్సర్.add_argument('--pip-cache', type=Path, default=ప్రొజెక్ట్_మూలం/'build/pip-cache')
    పార్సర్.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    కారకం_శ్రేణి = పార్సర్.parse_args()
    if కారకం_శ్రేణి.remote:
        కారకం_శ్రేణి.network=True
        కారకం_శ్రేణి.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; అనుమతిపదం_మూల్యం: python3 ఉపకరణాలు/రిమోట్_సెట్టింగ్_లు.py show'.format(కారకం_శ్రేణి.network_host,కారకం_శ్రేణి.network_host),flush=True)
    if కారకం_శ్రేణి.pip and not కారకం_శ్రేణి.network: పార్సర్.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= కారకం_శ్రేణి.pip_port <= 65535: పార్సర్.error('--pip-port 범위는 1~65535입니다.')
    if కారకం_శ్రేణి.forward and not కారకం_శ్రేణి.network: పార్సర్.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as వనరు_మూల్యం:
        if కారకం_శ్రేణి.pip:
            from 꾸러미중계 import 꾸러미중계
            వనరు_మూల్యం.enter_context(꾸러미중계(కారకం_శ్రేణి.pip_port, కారకం_శ్రేణి.pip_cache, కారకం_శ్రేణి.pip_offline))
            print('బండిల్ 중계: 127.0.0.1:' + str(కారకం_శ్రేణి.pip_port), flush=True)
        అమలుపరుచు(కారకం_శ్రేణి)


def అమలుపరుచు(కారకం_శ్రేణి):
    if కారకం_శ్రేణి.desktop:
        if కారకం_శ్రేణి.vnc or కారకం_శ్రేణి.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from డెస్క్_టాప్_వీక్షణ import అమలు_చెయ్_డెస్క్_టాప్
        raise SystemExit(అమలు_చెయ్_డెస్క్_టాప్(కారకం_శ్రేణి.port, నెట్_వర్క్=కారకం_శ్రేణి.network, ఫైలు_బదిలీ_పోర్ట్_సంఖ్య=కారకం_శ్రేణి.ftp_port, 전달규칙들=కారకం_శ్రేణి.forward, స్పష్టత_మూల్యం=కారకం_శ్రేణి.resolution, అతిథి_ఇమెయిల్=కారకం_శ్రేణి.guest_ip, హోస్ట్_ఇమెయిల్=కారకం_శ్రేణి.network_host))
    ఐచ్ఛికాలు = ['-display', కారకం_శ్రేణి.display, '-serial', 'mon:stdio']
    if కారకం_శ్రేణి.vnc:
        ఐచ్ఛికాలు += ['-vnc', కారకం_శ్రేణి.vnc]
    if కారకం_శ్రేణి.network:
        from నెట్_వర్క్_బ్రిడ్జ్ import నెట్_వర్క్_బ్రిడ్జ్
        with నెట్_వర్క్_బ్రిడ్జ్(కారకం_శ్రేణి.ftp_port, కారకం_శ్రేణి.forward, అతిథి_ఇమెయిల్=కారకం_శ్రేణి.guest_ip, హోస్ట్_ఇమెయిల్=కారకం_శ్రేణి.network_host) as బ్రిడ్జ్:
            స్థితి_మూల్యం = subprocess.call(ఆదేశము(కారకం_శ్రేణి.resolution) + ఐచ్ఛికాలు + బ్రిడ్జ్.전달인수())
            if బ్రిడ్జ్.దోషం: raise SystemExit('network bridge: ' + బ్రిడ్జ్.దోషం)
        raise SystemExit(స్థితి_మూల్యం)
    raise SystemExit(subprocess.call(ఆదేశము(కారకం_శ్రేణి.resolution) + ఐచ్ఛికాలు))


if __name__ == '__main__':
    నడుపుము()
