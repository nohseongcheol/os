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

പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for വഴി in _난수파일들:
        try:
            os.unlink(വഴി)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ഫയല്:
        ഫയല്.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(ഫയല്.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ഫയല്.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    ഹോസ്റ്റ് = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parent / 'rpi4/build/host'
    적재기 = ഹോസ്റ്റ് / 'lib/ld-musl-x86_64.so.1'
    బైనరీ = ഹോസ്റ്റ് / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and బైనరీ.is_file():
        return [str(적재기), '--library-path', str(ഹോസ്റ്റ് / 'usr/lib') + ':' + str(ഹോസ്റ്റ് / 'lib'),
                str(బైనరీ), '-L', str(ഹോസ്റ്റ് / 'usr/share/qemu')]
    బైనరీ = shutil.which('qemu-system-aarch64')
    if not బైనరీ:
        raise SystemExit('raspi4b പിന്തുണ_മൂല്യം QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [బైనరీ]


def 해상도읽기(പദാവലി):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', പദാവലി):
        raise argparse.ArgumentTypeError('റെസലൂഷന്_മൂല്യം ఫార్మాట్_മൂല്യം: 1920x1080')
    너비, 높이 = map(int, പദാവലി.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('പിന്തുണ_മൂല്യം ക്ലിപ്പ്: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def ആജ്ഞ(റെസലൂഷന്_മൂല്യം=(640, 480)):
    నేపథ్యం_മൂല്യം = 모의기계()
    지원목록 = subprocess.check_output(నేపథ్యం_മൂല്യം + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*റെസലൂഷന്_മൂല്യം))
    return నేపథ్యం_മൂല്യം + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def നടപ്പിലാക്കുക():
    പാഴ്_സർ = argparse.ArgumentParser(description='자체 Java Pi4 കെര്_ണല്_മൂല്യം. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 പുറത്തുകടക്കൽ_പ്രോഗ്രാം.')
    പാഴ്_സർ.add_argument('--display', default='none', help='none 또는 gtk/sdl (ഹോസ്റ്റ് പിന്തുണ_മൂല്യം 필요)')
    പാഴ്_സർ.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 വലിപ്പം. 예: 1920x1080; സ്ഥിരസ്ഥിതി_മൂല്യം 640x480')
    പാഴ്_സർ.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. കീ_മൂല്യം 입력은 UART 터미널에서 합니다.')
    പാഴ്_സർ.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    പാഴ്_സർ.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    പാഴ്_സർ.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 കണക്ടു്_ചെയ്യുക; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    പാഴ്_സർ.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    പാഴ്_സർ.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP നിയന്ത്രണം_മൂല്യം 포트 (데이터 50000..50007)')
    പാഴ്_സർ.add_argument('--guest-ip', default=None, help='QEMU NAT ഫോർവേഡുചെയ്യുക_മൂല്യം ലക്_ഷ്യം. 기본은 ip.conf의 IP; മാറ്റികൊടുക്കുക_മൂല്യം 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    പാഴ്_സർ.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ഇമെയിൽ. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ഇമെയിൽ: 외부 കണക്ഷൻ_e05f319b')
    പാഴ്_സർ.add_argument('--forward', action='append', default=[], help='--network 추가 കണക്ടു്_ചെയ്യുക: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    പാഴ്_സർ.add_argument('--pip', action='store_true', help='PyPI ഉറവിടം_ശാഖി ബണ്ടിൽ 중계 നടപ്പിലാക്കുക (--network 필요, MicroPython 호환 소스만)')
    പാഴ്_സർ.add_argument('--pip-port', type=int, default=8027, help='ബണ്ടിൽ 중계의 localhost TCP 포트')
    പാഴ്_സർ.add_argument('--pip-cache', type=Path, default=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/pip-cache')
    പാഴ്_സർ.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    ആര്_ഗ്യുമെന്_റ്_അരേ = പാഴ്_സർ.parse_args()
    if ആര്_ഗ്യുമെന്_റ്_അരേ.remote:
        ആര്_ഗ്യുമെന്_റ്_അരേ.network=True
        ആര്_ഗ്യുമെന്_റ്_അരേ.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; പാസ്_വേഡ്_മൂല്യം: python3 ഉപകരണങ്ങൾ/വിദൂര_ക്രമീകരണം.py show'.format(ആര്_ഗ്യുമെന്_റ്_അരേ.network_host,ആര്_ഗ്യുമെന്_റ്_അരേ.network_host),flush=True)
    if ആര്_ഗ്യുമെന്_റ്_അരേ.pip and not ആര്_ഗ്യുമെന്_റ്_അരേ.network: പാഴ്_സർ.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= ആര്_ഗ്യുമെന്_റ്_അരേ.pip_port <= 65535: പാഴ്_സർ.error('--pip-port 범위는 1~65535입니다.')
    if ആര്_ഗ്യുമെന്_റ്_അരേ.forward and not ആര്_ഗ്യുമെന്_റ്_അരേ.network: പാഴ്_സർ.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ഉറവിടം_മൂല്യം:
        if ആര്_ഗ്യുമെന്_റ്_അരേ.pip:
            from 꾸러미중계 import 꾸러미중계
            ഉറവിടം_മൂല്യം.enter_context(꾸러미중계(ആര്_ഗ്യുമെന്_റ്_അരേ.pip_port, ആര്_ഗ്യുമെന്_റ്_അരേ.pip_cache, ആര്_ഗ്യുമെന്_റ്_അരേ.pip_offline))
            print('ബണ്ടിൽ 중계: 127.0.0.1:' + str(ആര്_ഗ്യുമെന്_റ്_അരേ.pip_port), flush=True)
        പ്രവര്_ത്തിപ്പിയ്ക്കുക(ആര്_ഗ്യുമെന്_റ്_അരേ)


def പ്രവര്_ത്തിപ്പിയ്ക്കുക(ആര്_ഗ്യുമെന്_റ്_അരേ):
    if ആര്_ഗ്യുമെന്_റ്_അരേ.desktop:
        if ആര്_ഗ്യുമെന്_റ്_അരേ.vnc or ആര്_ഗ്യുമെന്_റ്_അരേ.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ഡെസ്ക്ടോപ്പ്_കാഴ്ച import റണ്_ഡെസ്ക്ടോപ്പ്
        raise SystemExit(റണ്_ഡെസ്ക്ടോപ്പ്(ആര്_ഗ്യുമെന്_റ്_അരേ.port, നെറ്റ്_വർക്ക്=ആര്_ഗ്യുമെന്_റ്_അരേ.network, ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര്=ആര്_ഗ്യുമെന്_റ്_അരേ.ftp_port, 전달규칙들=ആര്_ഗ്യുമെന്_റ്_അരേ.forward, റെസലൂഷന്_മൂല്യം=ആര്_ഗ്യുമെന്_റ്_അരേ.resolution, അതിഥി_ഇമെയിൽ=ആര്_ഗ്യുമെന്_റ്_അരേ.guest_ip, ഹോസ്റ്റ്_ഇമെയിൽ=ആര്_ഗ്യുമെന്_റ്_അരേ.network_host))
    ഐച്ഛികങ്ങള് = ['-display', ആര്_ഗ്യുമെന്_റ്_അരേ.display, '-serial', 'mon:stdio']
    if ആര്_ഗ്യുമെന്_റ്_അരേ.vnc:
        ഐച്ഛികങ്ങള് += ['-vnc', ആര്_ഗ്യുമെന്_റ്_അരേ.vnc]
    if ആര്_ഗ്യുമെന്_റ്_അരേ.network:
        from നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ് import നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്
        with നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്(ആര്_ഗ്യുമെന്_റ്_അരേ.ftp_port, ആര്_ഗ്യുമെന്_റ്_അരേ.forward, അതിഥി_ഇമെയിൽ=ആര്_ഗ്യുമെന്_റ്_അരേ.guest_ip, ഹോസ്റ്റ്_ഇമെയിൽ=ആര്_ഗ്യുമെന്_റ്_അരേ.network_host) as ബ്രിഡ്_ജ്:
            അവസ്ഥ_മൂല്യം = subprocess.call(ആജ്ഞ(ആര്_ഗ്യുമെന്_റ്_അരേ.resolution) + ഐച്ഛികങ്ങള് + ബ്രിഡ്_ജ്.전달인수())
            if ബ്രിഡ്_ജ്.പിശക്: raise SystemExit('network bridge: ' + ബ്രിഡ്_ജ്.പിശക്)
        raise SystemExit(അവസ്ഥ_മൂല്യം)
    raise SystemExit(subprocess.call(ആജ്ഞ(ആര്_ഗ്യുമെന്_റ്_അരേ.resolution) + ഐച്ഛികങ്ങള്))


if __name__ == '__main__':
    നടപ്പിലാക്കുക()
