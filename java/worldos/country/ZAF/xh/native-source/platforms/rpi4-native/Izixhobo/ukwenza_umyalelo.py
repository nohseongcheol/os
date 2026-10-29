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
    for INDLELA in _난수파일들:
        try:
            os.unlink(INDLELA)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as iFayili:
        iFayili.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(iFayili.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(iFayili.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    umsingathi = 기준.parent / 'rpi4/build/host'
    적재기 = umsingathi / 'lib/ld-musl-x86_64.so.1'
    ibhayinari = umsingathi / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and ibhayinari.is_file():
        return [str(적재기), '--library-path', str(umsingathi / 'usr/lib') + ':' + str(umsingathi / 'lib'),
                str(ibhayinari), '-L', str(umsingathi / 'usr/share/qemu')]
    ibhayinari = shutil.which('qemu-system-aarch64')
    if not ibhayinari:
        raise SystemExit('raspi4b inkxaso_ixabiso QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ibhayinari]


def 해상도읽기(Umbhalo):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Umbhalo):
        raise argparse.ArgumentTypeError('isisombululo_ixabiso fomatha_ixabiso: 1920x1080')
    너비, 높이 = map(int, Umbhalo.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('inkxaso_ixabiso ikliphu: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Umyalelo(isisombululo_ixabiso=(640, 480)):
    Ngasemva_ixabiso = 모의기계()
    지원목록 = subprocess.check_output(Ngasemva_ixabiso + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*isisombululo_ixabiso))
    return Ngasemva_ixabiso + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Phumeza():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 ikheneli_ixabiso. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 phuma_inkqubo.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (umsingathi inkxaso_ixabiso 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Ubukhulu. 예: 1920x1080; ixabiso_elisisiseko 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. iqhosha_ixabiso 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Nxulumanisa; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP isilawuli_ixabiso 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT dlulisa_ixabiso ithagethi. 기본은 ip.conf의 IP; tshintsha_ixabiso 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 idilesi. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN idilesi: 외부 uqhagamshelo_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 Nxulumanisa: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI umthombo_umthi umqulu 중계 Phumeza (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='umqulu 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    isiniki_myalelo_ULUHLU = 인수해석기.parse_args()
    if isiniki_myalelo_ULUHLU.remote:
        isiniki_myalelo_ULUHLU.network=True
        isiniki_myalelo_ULUHLU.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; iphaswedi_ixabiso: python3 Izixhobo/kude_Iisetingi.py show'.format(isiniki_myalelo_ULUHLU.network_host,isiniki_myalelo_ULUHLU.network_host),flush=True)
    if isiniki_myalelo_ULUHLU.pip and not isiniki_myalelo_ULUHLU.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= isiniki_myalelo_ULUHLU.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if isiniki_myalelo_ULUHLU.forward and not isiniki_myalelo_ULUHLU.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as isixhobo_sekhompyutha_ixabiso:
        if isiniki_myalelo_ULUHLU.pip:
            from 꾸러미중계 import 꾸러미중계
            isixhobo_sekhompyutha_ixabiso.enter_context(꾸러미중계(isiniki_myalelo_ULUHLU.pip_port, isiniki_myalelo_ULUHLU.pip_cache, isiniki_myalelo_ULUHLU.pip_offline))
            print('umqulu 중계: 127.0.0.1:' + str(isiniki_myalelo_ULUHLU.pip_port), flush=True)
        ukwenza_umsebenzi(isiniki_myalelo_ULUHLU)


def ukwenza_umsebenzi(isiniki_myalelo_ULUHLU):
    if isiniki_myalelo_ULUHLU.desktop:
        if isiniki_myalelo_ULUHLU.vnc or isiniki_myalelo_ULUHLU.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from idesktophu_bona import i_run_idesktophu
        raise SystemExit(i_run_idesktophu(isiniki_myalelo_ULUHLU.port, Inethiwekhi=isiniki_myalelo_ULUHLU.network, 파일전송접속번호=isiniki_myalelo_ULUHLU.ftp_port, 전달규칙들=isiniki_myalelo_ULUHLU.forward, isisombululo_ixabiso=isiniki_myalelo_ULUHLU.resolution, undwendwe_idilesi=isiniki_myalelo_ULUHLU.guest_ip, umsingathi_idilesi=isiniki_myalelo_ULUHLU.network_host))
    uKhetho = ['-display', isiniki_myalelo_ULUHLU.display, '-serial', 'mon:stdio']
    if isiniki_myalelo_ULUHLU.vnc:
        uKhetho += ['-vnc', isiniki_myalelo_ULUHLU.vnc]
    if isiniki_myalelo_ULUHLU.network:
        from Inethiwekhi_ibhulorho import Inethiwekhi_ibhulorho
        with Inethiwekhi_ibhulorho(isiniki_myalelo_ULUHLU.ftp_port, isiniki_myalelo_ULUHLU.forward, undwendwe_idilesi=isiniki_myalelo_ULUHLU.guest_ip, umsingathi_idilesi=isiniki_myalelo_ULUHLU.network_host) as ibhulorho:
            imo_ixabiso = subprocess.call(Umyalelo(isiniki_myalelo_ULUHLU.resolution) + uKhetho + ibhulorho.전달인수())
            if ibhulorho.Impazamo: raise SystemExit('network bridge: ' + ibhulorho.Impazamo)
        raise SystemExit(imo_ixabiso)
    raise SystemExit(subprocess.call(Umyalelo(isiniki_myalelo_ULUHLU.resolution) + uKhetho))


if __name__ == '__main__':
    Phumeza()
