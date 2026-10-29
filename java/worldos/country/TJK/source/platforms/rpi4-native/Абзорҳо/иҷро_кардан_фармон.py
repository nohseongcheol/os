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
    for масир in _난수파일들:
        try:
            os.unlink(масир)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Файл:
        Файл.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Файл.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Файл.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    мизбон = 기준.parent / 'rpi4/build/host'
    적재기 = мизбон / 'lib/ld-musl-x86_64.so.1'
    дуӣ = мизбон / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and дуӣ.is_file():
        return [str(적재기), '--library-path', str(мизбон / 'usr/lib') + ':' + str(мизбон / 'lib'),
                str(дуӣ), '-L', str(мизбон / 'usr/share/qemu')]
    дуӣ = shutil.which('qemu-system-aarch64')
    if not дуӣ:
        raise SystemExit('raspi4b Дастгирӣ_қимат QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [дуӣ]


def 해상도읽기(Матн):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Матн):
        raise argparse.ArgumentTypeError('возеҳӣ_қимат формат_қимат: 1920x1080')
    너비, 높이 = map(int, Матн.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Дастгирӣ_қимат клип: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def фармон(возеҳӣ_қимат=(640, 480)):
    Пасзамина_қимат = 모의기계()
    지원목록 = subprocess.check_output(Пасзамина_қимат + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*возеҳӣ_қимат))
    return Пасзамина_қимат + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def порча():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 ҳаста_қимат. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Баромад_барнома.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (мизбон Дастгирӣ_қимат 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 андоза_кардан. 예: 1920x1080; қимати_пешфарз 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. калид_қимат 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 ПАЙВАСТ; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP идоракунӣ_қимат 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT бозфиристодан_қимат ҳадаф. 기본은 ip.conf의 IP; тағйир_додан_қимат 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 суроға. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN суроға: 외부 пайваст_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 ПАЙВАСТ: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI манбаъ_дарахт баста 중계 порча (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='баста 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    аргумент_қатор = 인수해석기.parse_args()
    if аргумент_қатор.remote:
        аргумент_қатор.network=True
        аргумент_қатор.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; парол_қимат: python3 Абзорҳо/дурдаст_Танзимот.py show'.format(аргумент_қатор.network_host,аргумент_қатор.network_host),flush=True)
    if аргумент_қатор.pip and not аргумент_қатор.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= аргумент_қатор.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if аргумент_қатор.forward and not аргумент_қатор.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as захира_қимат:
        if аргумент_қатор.pip:
            from 꾸러미중계 import 꾸러미중계
            захира_қимат.enter_context(꾸러미중계(аргумент_қатор.pip_port, аргумент_қатор.pip_cache, аргумент_қатор.pip_offline))
            print('баста 중계: 127.0.0.1:' + str(аргумент_қатор.pip_port), flush=True)
        Иҷро_кардан(аргумент_қатор)


def Иҷро_кардан(аргумент_қатор):
    if аргумент_қатор.desktop:
        if аргумент_қатор.vnc or аргумент_қатор.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from мизи_корӣ_намуд import порча_мизи_корӣ
        raise SystemExit(порча_мизи_корӣ(аргумент_қатор.port, Шабака=аргумент_қатор.network, 파일전송접속번호=аргумент_қатор.ftp_port, 전달규칙들=аргумент_қатор.forward, возеҳӣ_қимат=аргумент_қатор.resolution, меҳмон_суроға=аргумент_қатор.guest_ip, мизбон_суроға=аргумент_қатор.network_host))
    Имконот = ['-display', аргумент_қатор.display, '-serial', 'mon:stdio']
    if аргумент_қатор.vnc:
        Имконот += ['-vnc', аргумент_қатор.vnc]
    if аргумент_қатор.network:
        from Шабака_кӯпрук import Шабака_кӯпрук
        with Шабака_кӯпрук(аргумент_қатор.ftp_port, аргумент_қатор.forward, меҳмон_суроға=аргумент_қатор.guest_ip, мизбон_суроға=аргумент_қатор.network_host) as кӯпрук:
            вазъият_қимат = subprocess.call(фармон(аргумент_қатор.resolution) + Имконот + кӯпрук.전달인수())
            if кӯпрук.Хато: raise SystemExit('network bridge: ' + кӯпрук.Хато)
        raise SystemExit(вазъият_қимат)
    raise SystemExit(subprocess.call(фармон(аргумент_қатор.resolution) + Имконот))


if __name__ == '__main__':
    порча()
