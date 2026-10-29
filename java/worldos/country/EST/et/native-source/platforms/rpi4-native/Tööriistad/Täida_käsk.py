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

Project_juur = Path(__file__).resolve().parents[1]
juhuslik_Failid = []


def _난수정리():
    for RADA in juhuslik_Failid:
        try:
            os.unlink(RADA)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Fail:
        Fail.write(b'JKRENRG1' + os.urandom(32))
        juhuslik_Failid.append(Fail.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Fail.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    host = Project_juur.parent / 'rpi4/build/host'
    laadur = host / 'lib/ld-musl-x86_64.so.1'
    binaarne = host / 'usr/bin/qemu-system-aarch64'
    if laadur.is_file() and binaarne.is_file():
        return [str(laadur), '--library-path', str(host / 'usr/lib') + ':' + str(host / 'lib'),
                str(binaarne), '-L', str(host / 'usr/share/qemu')]
    binaarne = shutil.which('qemu-system-aarch64')
    if not binaarne:
        raise SystemExit('raspi4b tugi_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [binaarne]


def 해상도읽기(Tekst):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Tekst):
        raise argparse.ArgumentTypeError('eraldusvõime_VALUE vorming_VALUE: 1920x1080')
    너비, 높이 = map(int, Tekst.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('tugi_VALUE klipp: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Käsk(eraldusvõime_VALUE=(640, 480)):
    taust_VALUE = 모의기계()
    지원목록 = subprocess.check_output(taust_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*eraldusvõime_VALUE))
    return taust_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(Project_juur / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Käivita_2():
    parser = argparse.ArgumentParser(description='oma Java Pi4 tuum_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Välju_programm.')
    parser.add_argument('--display', default='none', help='none 또는 gtk/sdl (host tugi_VALUE 필요)')
    parser.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Suurus. 예: 1920x1080; vaikeväärtus 640x480')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Võti_VALUE 입력은 UART 터미널에서 합니다.')
    parser.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    parser.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    parser.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Ühendu; --desktop과 함께 kasutus_VALUE 가능; 게스트에서 ftpd start')
    parser.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    parser.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP meede_VALUE 포트 (데이터 50000..50007)')
    parser.add_argument('--guest-ip', default=None, help='QEMU NAT Edasi_VALUE siht. 기본은 ip.conf의 IP; muutma_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    parser.add_argument('--network-host', default='127.0.0.1', help='NAT saama_VALUE ADDRESS. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ADDRESS: väline_VALUE ühendus_e05f319b')
    parser.add_argument('--forward', action='append', default=[], help='--network Lisa_kirje Ühendu: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    parser.add_argument('--pip', action='store_true', help='PyPI lähe_puu kogum 중계 Käivita_2 (--network 필요, MicroPython 호환 소스만)')
    parser.add_argument('--pip-port', type=int, default=8027, help='kogum 중계의 localhost TCP 포트')
    parser.add_argument('--pip-cache', type=Path, default=Project_juur/'build/pip-cache')
    parser.add_argument('--pip-offline', action='store_true', help='이미 받은 turustus_VALUE 파일만 제공')
    argument_ARRAY = parser.parse_args()
    if argument_ARRAY.remote:
        argument_ARRAY.network=True
        argument_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; parool_VALUE: python3 Tööriistad/kauge_Sätted.py show'.format(argument_ARRAY.network_host,argument_ARRAY.network_host),flush=True)
    if argument_ARRAY.pip and not argument_ARRAY.network: parser.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argument_ARRAY.pip_port <= 65535: parser.error('--pip-port 범위는 1~65535입니다.')
    if argument_ARRAY.forward and not argument_ARRAY.network: parser.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ressurss_VALUE:
        if argument_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            ressurss_VALUE.enter_context(꾸러미중계(argument_ARRAY.pip_port, argument_ARRAY.pip_cache, argument_ARRAY.pip_offline))
            print('kogum 중계: 127.0.0.1:' + str(argument_ARRAY.pip_port), flush=True)
        Käivita(argument_ARRAY)


def Käivita(argument_ARRAY):
    if argument_ARRAY.desktop:
        if argument_ARRAY.vnc or argument_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from töölaud_Kuva import sari_töölaud
        raise SystemExit(sari_töölaud(argument_ARRAY.port, võrk=argument_ARRAY.network, failiedastus_pordinumber=argument_ARRAY.ftp_port, 전달규칙들=argument_ARRAY.forward, eraldusvõime_VALUE=argument_ARRAY.resolution, külaline_ADDRESS=argument_ARRAY.guest_ip, host_ADDRESS=argument_ARRAY.network_host))
    Suvandid = ['-display', argument_ARRAY.display, '-serial', 'mon:stdio']
    if argument_ARRAY.vnc:
        Suvandid += ['-vnc', argument_ARRAY.vnc]
    if argument_ARRAY.network:
        from sild_3de4fe3a import sild_3de4fe3a
        with sild_3de4fe3a(argument_ARRAY.ftp_port, argument_ARRAY.forward, külaline_ADDRESS=argument_ARRAY.guest_ip, host_ADDRESS=argument_ARRAY.network_host) as sild:
            Olek_VALUE = subprocess.call(Käsk(argument_ARRAY.resolution) + Suvandid + sild.전달인수())
            if sild.VIGA: raise SystemExit('network bridge: ' + sild.VIGA)
        raise SystemExit(Olek_VALUE)
    raise SystemExit(subprocess.call(Käsk(argument_ARRAY.resolution) + Suvandid))


if __name__ == '__main__':
    Käivita_2()
