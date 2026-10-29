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

ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for ପଥ in _난수파일들:
        try:
            os.unlink(ପଥ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ଫାଇଲ:
        ଫାଇଲ.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(ଫାଇଲ.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ଫାଇଲ.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    ଆୟୋଜକ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parent / 'rpi4/build/host'
    적재기 = ଆୟୋଜକ / 'lib/ld-musl-x86_64.so.1'
    ବାଇନାରୀ = ଆୟୋଜକ / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and ବାଇନାରୀ.is_file():
        return [str(적재기), '--library-path', str(ଆୟୋଜକ / 'usr/lib') + ':' + str(ଆୟୋଜକ / 'lib'),
                str(ବାଇନାରୀ), '-L', str(ଆୟୋଜକ / 'usr/share/qemu')]
    ବାଇନାରୀ = shutil.which('qemu-system-aarch64')
    if not ବାଇନାରୀ:
        raise SystemExit('raspi4b ସମର୍ଥନ_ମୂଲ୍ୟ QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ବାଇନାରୀ]


def 해상도읽기(ପାଠ୍ଯ):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', ପାଠ୍ଯ):
        raise argparse.ArgumentTypeError('ସ୍ପଷ୍ଟତା_ମୂଲ୍ୟ ଫର୍ମାଟ୍_ମୂଲ୍ୟ: 1920x1080')
    너비, 높이 = map(int, ପାଠ୍ଯ.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('ସମର୍ଥନ_ମୂଲ୍ୟ କ୍ଲିପ୍: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def ନିର୍ଦ୍ଦେଶ(ସ୍ପଷ୍ଟତା_ମୂଲ୍ୟ=(640, 480)):
    ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ = 모의기계()
    지원목록 = subprocess.check_output(ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*ସ୍ପଷ୍ଟତା_ମୂଲ୍ୟ))
    return ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def ଚଳାନ୍ତୁ():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 ପ୍ରସ୍ଥାନ_ଅନୁପ୍ରୟୋଗ.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (ଆୟୋଜକ ସମର୍ଥନ_ମୂଲ୍ୟ 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 ଆକାର. 예: 1920x1080; ଡିଫଲ୍ଟ_ମାନ 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC ହାର୍ଡୱେର୍_ପୋର୍ଟ 5902. କୀ_ମୂଲ୍ୟ 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC ହାର୍ଡୱେର୍_ପୋର୍ଟ')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 ସଂଯୋଗ_କରନ୍ତୁ; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP ନିୟନ୍ତ୍ରଣ_ମୂଲ୍ୟ ହାର୍ଡୱେର୍_ପୋର୍ଟ (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT ଅଗ୍ରଗାମୀ_ମୂଲ୍ୟ ଲକ୍ଷ୍ୟସ୍ଥଳ. 기본은 ip.conf의 IP; ପରିବର୍ତ୍ତନ_ମୂଲ୍ୟ 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ଠିକଣା. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ଠିକଣା: 외부 ସଂଯୋଗ_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 ସଂଯୋଗ_କରନ୍ତୁ: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI ଉତ୍ସ_ବୃକ୍ଷ ବଣ୍ଡଲ୍ 중계 ଚଳାନ୍ତୁ (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='ବଣ୍ଡଲ୍ 중계의 localhost TCP ହାର୍ଡୱେର୍_ପୋର୍ଟ')
    인수해석기.add_argument('--pip-cache', type=Path, default=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    ଯୁକ୍ତି_ଆରେ = 인수해석기.parse_args()
    if ଯୁକ୍ତି_ଆରେ.remote:
        ଯୁକ୍ତି_ଆରେ.network=True
        ଯୁକ୍ତି_ଆରେ.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; ପାସ୍_ୱାର୍ଡ୍_ମୂଲ୍ୟ: python3 ଉପକରଣସମୂହ/ଦୂରବର୍ତ୍ତୀ_ସେଟିଂସ୍.py show'.format(ଯୁକ୍ତି_ଆରେ.network_host,ଯୁକ୍ତି_ଆରେ.network_host),flush=True)
    if ଯୁକ୍ତି_ଆରେ.pip and not ଯୁକ୍ତି_ଆରେ.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= ଯୁକ୍ତି_ଆରେ.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if ଯୁକ୍ତି_ଆରେ.forward and not ଯୁକ୍ତି_ଆରେ.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ଉତ୍ସ_ମୂଲ୍ୟ:
        if ଯୁକ୍ତି_ଆରେ.pip:
            from 꾸러미중계 import 꾸러미중계
            ଉତ୍ସ_ମୂଲ୍ୟ.enter_context(꾸러미중계(ଯୁକ୍ତି_ଆରେ.pip_port, ଯୁକ୍ତି_ଆରେ.pip_cache, ଯୁକ୍ତି_ଆରେ.pip_offline))
            print('ବଣ୍ଡଲ୍ 중계: 127.0.0.1:' + str(ଯୁକ୍ତି_ଆରେ.pip_port), flush=True)
        ନିଷ୍ପାଦନ_କରନ୍ତୁ(ଯୁକ୍ତି_ଆରେ)


def ନିଷ୍ପାଦନ_କରନ୍ତୁ(ଯୁକ୍ତି_ଆରେ):
    if ଯୁକ୍ତି_ଆରେ.desktop:
        if ଯୁକ୍ତି_ଆରେ.vnc or ଯୁକ୍ତି_ଆରେ.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ଡେସ୍କଟପ୍_ଭିୟୁ import ରନ୍_ଡେସ୍କଟପ୍
        raise SystemExit(ରନ୍_ଡେସ୍କଟପ୍(ଯୁକ୍ତି_ଆରେ.port, ନେଟ୍_ୱାର୍କ୍=ଯୁକ୍ତି_ଆରେ.network, ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍=ଯୁକ୍ତି_ଆରେ.ftp_port, 전달규칙들=ଯୁକ୍ତି_ଆରେ.forward, ସ୍ପଷ୍ଟତା_ମୂଲ୍ୟ=ଯୁକ୍ତି_ଆରେ.resolution, ଅତିଥି_ଠିକଣା=ଯୁକ୍ତି_ଆରେ.guest_ip, ଆୟୋଜକ_ଠିକଣା=ଯୁକ୍ତି_ଆରେ.network_host))
    ବିକଳ୍ପ_ସମୂହ = ['-display', ଯୁକ୍ତି_ଆରେ.display, '-serial', 'mon:stdio']
    if ଯୁକ୍ତି_ଆରେ.vnc:
        ବିକଳ୍ପ_ସମୂହ += ['-vnc', ଯୁକ୍ତି_ଆରେ.vnc]
    if ଯୁକ୍ତି_ଆରେ.network:
        from ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍ import ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍
        with ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍(ଯୁକ୍ତି_ଆରେ.ftp_port, ଯୁକ୍ତି_ଆରେ.forward, ଅତିଥି_ଠିକଣା=ଯୁକ୍ତି_ଆରେ.guest_ip, ଆୟୋଜକ_ଠିକଣା=ଯୁକ୍ତି_ଆରେ.network_host) as ବ୍ରିଜ୍:
            ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 = subprocess.call(ନିର୍ଦ୍ଦେଶ(ଯୁକ୍ତି_ଆରେ.resolution) + ବିକଳ୍ପ_ସମୂହ + ବ୍ରିଜ୍.전달인수())
            if ବ୍ରିଜ୍.ତ୍ରୁଟି: raise SystemExit('network bridge: ' + ବ୍ରିଜ୍.ତ୍ରୁଟି)
        raise SystemExit(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1)
    raise SystemExit(subprocess.call(ନିର୍ଦ୍ଦେଶ(ଯୁକ୍ତି_ଆରେ.resolution) + ବିକଳ୍ପ_ସମୂହ))


if __name__ == '__main__':
    ଚଳାନ୍ତୁ()
