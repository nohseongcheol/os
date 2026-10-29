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
    for ụzọ_ozi in _난수파일들:
        try:
            os.unlink(ụzọ_ozi)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Faịlụ:
        Faịlụ.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Faịlụ.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Faịlụ.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    usu = 기준.parent / 'rpi4/build/host'
    적재기 = usu / 'lib/ld-musl-x86_64.so.1'
    ndìnààbụọ = usu / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and ndìnààbụọ.is_file():
        return [str(적재기), '--library-path', str(usu / 'usr/lib') + ':' + str(usu / 'lib'),
                str(ndìnààbụọ), '-L', str(usu / 'usr/share/qemu')]
    ndìnààbụọ = shutil.which('qemu-system-aarch64')
    if not ndìnààbụọ:
        raise SystemExit('raspi4b nkwado_valuu QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ndìnààbụọ]


def 해상도읽기(SMS):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', SMS):
        raise argparse.ArgumentTypeError('ụcha_ngosịpụta_valuu hàzie_valuu: 1920x1080')
    너비, 높이 = map(int, SMS.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('nkwado_valuu ntipanye: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Ntiiwu(ụcha_ngosịpụta_valuu=(640, 480)):
    Bakgraụnd_valuu = 모의기계()
    지원목록 = subprocess.check_output(Bakgraụnd_valuu + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*ụcha_ngosịpụta_valuu))
    return Bakgraụnd_valuu + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Bido():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 mkpụrụobī_kọmpùta_valuu. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 pụọ_app.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (usu nkwado_valuu 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Ụhara. 예: 1920x1080; Ngwa_ihe_dịadị 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC ngwaike_pọọt 5902. ọtụgwo_valuu 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC ngwaike_pọọt')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Banye; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP njizi_valuu ngwaike_pọọt (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT zìgaā_valuu ebenlereanya. 기본은 ip.conf의 IP; gbanwèe_valuu 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 àdreèsì. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN àdreèsì: 외부 njikọ_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 Banye: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI ebensìbịa_èsèrèsè_osisi ngwungwu 중계 Bido (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='ngwungwu 중계의 localhost TCP ngwaike_pọọt')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    agụment_MKPOKỌTA = 인수해석기.parse_args()
    if agụment_MKPOKỌTA.remote:
        agụment_MKPOKỌTA.network=True
        agụment_MKPOKỌTA.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; okwuntughe_valuu: python3 Ngwaọrụ/ebe_dị̀anyā_Mwube.py show'.format(agụment_MKPOKỌTA.network_host,agụment_MKPOKỌTA.network_host),flush=True)
    if agụment_MKPOKỌTA.pip and not agụment_MKPOKỌTA.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= agụment_MKPOKỌTA.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if agụment_MKPOKỌTA.forward and not agụment_MKPOKỌTA.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as njìàrụọrụ_valuu:
        if agụment_MKPOKỌTA.pip:
            from 꾸러미중계 import 꾸러미중계
            njìàrụọrụ_valuu.enter_context(꾸러미중계(agụment_MKPOKỌTA.pip_port, agụment_MKPOKỌTA.pip_cache, agụment_MKPOKỌTA.pip_offline))
            print('ngwungwu 중계: 127.0.0.1:' + str(agụment_MKPOKỌTA.pip_port), flush=True)
        mee_ọrụ(agụment_MKPOKỌTA)


def mee_ọrụ(agụment_MKPOKỌTA):
    if agụment_MKPOKỌTA.desktop:
        if agụment_MKPOKỌTA.vnc or agụment_MKPOKỌTA.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from desktọpụ_lèe import mee_desktọpụ
        raise SystemExit(mee_desktọpụ(agụment_MKPOKỌTA.port, Netwọọkụ=agụment_MKPOKỌTA.network, 파일전송접속번호=agụment_MKPOKỌTA.ftp_port, 전달규칙들=agụment_MKPOKỌTA.forward, ụcha_ngosịpụta_valuu=agụment_MKPOKỌTA.resolution, 게스트주소=agụment_MKPOKỌTA.guest_ip, usu_àdreèsì=agụment_MKPOKỌTA.network_host))
    Ihenhọrọga = ['-display', agụment_MKPOKỌTA.display, '-serial', 'mon:stdio']
    if agụment_MKPOKỌTA.vnc:
        Ihenhọrọga += ['-vnc', agụment_MKPOKỌTA.vnc]
    if agụment_MKPOKỌTA.network:
        from 통신다리 import 통신다리
        with 통신다리(agụment_MKPOKỌTA.ftp_port, agụment_MKPOKỌTA.forward, 게스트주소=agụment_MKPOKỌTA.guest_ip, usu_àdreèsì=agụment_MKPOKỌTA.network_host) as 연결다리:
            ọnọdụ_valuu = subprocess.call(Ntiiwu(agụment_MKPOKỌTA.resolution) + Ihenhọrọga + 연결다리.전달인수())
            if 연결다리.mmejọ: raise SystemExit('network bridge: ' + 연결다리.mmejọ)
        raise SystemExit(ọnọdụ_valuu)
    raise SystemExit(subprocess.call(Ntiiwu(agụment_MKPOKỌTA.resolution) + Ihenhọrọga))


if __name__ == '__main__':
    Bido()
