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

ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for ਮਾਰਗ in _난수파일들:
        try:
            os.unlink(ਮਾਰਗ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ਫਾਇਲ:
        ਫਾਇਲ.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(ਫਾਇਲ.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ਫਾਇਲ.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    ਹੋਸਟ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parent / 'rpi4/build/host'
    적재기 = ਹੋਸਟ / 'lib/ld-musl-x86_64.so.1'
    ਜੋੜੇਦਾਰ = ਹੋਸਟ / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and ਜੋੜੇਦਾਰ.is_file():
        return [str(적재기), '--library-path', str(ਹੋਸਟ / 'usr/lib') + ':' + str(ਹੋਸਟ / 'lib'),
                str(ਜੋੜੇਦਾਰ), '-L', str(ਹੋਸਟ / 'usr/share/qemu')]
    ਜੋੜੇਦਾਰ = shutil.which('qemu-system-aarch64')
    if not ਜੋੜੇਦਾਰ:
        raise SystemExit('raspi4b ਸਮਰਥਨ_ਕੀਮਤ QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ਜੋੜੇਦਾਰ]


def 해상도읽기(ਟੈਕਸਟ):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', ਟੈਕਸਟ):
        raise argparse.ArgumentTypeError('ਰੂਪਾਂਤਰ_ਕੀਮਤ ਸਰੂਪ_ਕੀਮਤ: 1920x1080')
    너비, 높이 = map(int, ਟੈਕਸਟ.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('ਸਮਰਥਨ_ਕੀਮਤ ਕਲਿਪ: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def ਕਮਾਂਡ(ਰੂਪਾਂਤਰ_ਕੀਮਤ=(640, 480)):
    ਪਿਛੋਕੜ_ਕੀਮਤ = 모의기계()
    지원목록 = subprocess.check_output(ਪਿਛੋਕੜ_ਕੀਮਤ + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*ਰੂਪਾਂਤਰ_ਕੀਮਤ))
    return ਪਿਛੋਕੜ_ਕੀਮਤ + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def ਚਲਾਓ_2():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 ਨਿਕਾਸ_ਐਪਲੀਕੇਸ਼.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (ਹੋਸਟ ਸਮਰਥਨ_ਕੀਮਤ 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 ਆਕਾਰ. 예: 1920x1080; ਡਿਫੌਲਟ_ਵੈਲਯੂ 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. ਕੀ_ਕੀਮਤ 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 ਕੁਨੈਕਸ਼ਨ_ਕਰੋ; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP ਨਿਯੰਤਰਣ_ਕੀਮਤ 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT ਫਾਰਵਰਡ_ਕੀਮਤ ਟੀਚਾ. 기본은 ip.conf의 IP; ਬਦਲੋ_ਕੀਮਤ 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ਪਤਾ. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ਪਤਾ: 외부 ਸਬੰਧ_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 ਕੁਨੈਕਸ਼ਨ_ਕਰੋ: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI ਸਰੋਤ_ਟ੍ਰੀ ਬੰਡਲ 중계 ਚਲਾਓ_2 (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='ਬੰਡਲ 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ = 인수해석기.parse_args()
    if ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.remote:
        ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.network=True
        ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; ਪਾਸਵਰਡ_ਕੀਮਤ: python3 ਸਾਧਨ/ਰਿਮੋਟ_ਸੈਟਿੰਗਾਂ.py show'.format(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.network_host,ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.network_host),flush=True)
    if ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.pip and not ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.forward and not ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ਸੰਸਾਧਨ_ਕੀਮਤ:
        if ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.pip:
            from 꾸러미중계 import 꾸러미중계
            ਸੰਸਾਧਨ_ਕੀਮਤ.enter_context(꾸러미중계(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.pip_port, ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.pip_cache, ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.pip_offline))
            print('ਬੰਡਲ 중계: 127.0.0.1:' + str(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.pip_port), flush=True)
        ਚਲਾਓ(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ)


def ਚਲਾਓ(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ):
    if ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.desktop:
        if ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.vnc or ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ਡੈਸਕਟੌਪ_ਦ੍ਰਿਸ਼ import ਚਲਾਉ_ਡੈਸਕਟੌਪ
        raise SystemExit(ਚਲਾਉ_ਡੈਸਕਟੌਪ(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.port, ਨੈਟਵਰਕ=ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.network, 파일전송접속번호=ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.ftp_port, 전달규칙들=ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.forward, ਰੂਪਾਂਤਰ_ਕੀਮਤ=ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.resolution, ਗੈਸਟ_ਪਤਾ=ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.guest_ip, ਹੋਸਟ_ਪਤਾ=ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.network_host))
    ਚੋਣਾਂ = ['-display', ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.display, '-serial', 'mon:stdio']
    if ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.vnc:
        ਚੋਣਾਂ += ['-vnc', ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.vnc]
    if ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.network:
        from ਨੈਟਵਰਕ_ਬਰਿਜ import ਨੈਟਵਰਕ_ਬਰਿਜ
        with ਨੈਟਵਰਕ_ਬਰਿਜ(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.ftp_port, ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.forward, ਗੈਸਟ_ਪਤਾ=ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.guest_ip, ਹੋਸਟ_ਪਤਾ=ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.network_host) as ਬਰਿਜ:
            ਸਥਿਤੀ_ਕੀਮਤ = subprocess.call(ਕਮਾਂਡ(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.resolution) + ਚੋਣਾਂ + ਬਰਿਜ.전달인수())
            if ਬਰਿਜ.ਗਲਤੀ: raise SystemExit('network bridge: ' + ਬਰਿਜ.ਗਲਤੀ)
        raise SystemExit(ਸਥਿਤੀ_ਕੀਮਤ)
    raise SystemExit(subprocess.call(ਕਮਾਂਡ(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.resolution) + ਚੋਣਾਂ))


if __name__ == '__main__':
    ਚਲਾਓ_2()
