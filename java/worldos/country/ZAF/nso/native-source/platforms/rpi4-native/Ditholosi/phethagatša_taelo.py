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
    for Tsejana in _난수파일들:
        try:
            os.unlink(Tsejana)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Faele:
        Faele.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Faele.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Faele.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    go_nea_ditirelo = 기준.parent / 'rpi4/build/host'
    적재기 = go_nea_ditirelo / 'lib/ld-musl-x86_64.so.1'
    paenari = go_nea_ditirelo / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and paenari.is_file():
        return [str(적재기), '--library-path', str(go_nea_ditirelo / 'usr/lib') + ':' + str(go_nea_ditirelo / 'lib'),
                str(paenari), '-L', str(go_nea_ditirelo / 'usr/share/qemu')]
    paenari = shutil.which('qemu-system-aarch64')
    if not paenari:
        raise SystemExit('raspi4b Thekgo_boleng QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [paenari]


def 해상도읽기(Sengwalwa):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Sengwalwa):
        raise argparse.ArgumentTypeError('sephetho_boleng fomete_boleng: 1920x1080')
    너비, 높이 = map(int, Sengwalwa.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Thekgo_boleng setsopolwa: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Taelo(sephetho_boleng=(640, 480)):
    Bokamorago_boleng = 모의기계()
    지원목록 = subprocess.check_output(Bokamorago_boleng + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*sephetho_boleng))
    return Bokamorago_boleng + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Diriša():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 khenele_boleng. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Etšwa_tirišo.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (go_nea_ditirelo Thekgo_boleng 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Bogolo. 예: 1920x1080; setsenywa_sa_tirelwa 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. khii_boleng 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Ikgokaganye; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP taolo_boleng 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT romela_pele_boleng nepo. 기본은 ip.conf의 IP; fetoša_boleng 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 atrese. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN atrese: 외부 kgokaganya_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 Ikgokaganye: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI mohlodi_mohlare sehlopha 중계 Diriša (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='sehlopha 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    akumente_arei = 인수해석기.parse_args()
    if akumente_arei.remote:
        akumente_arei.network=True
        akumente_arei.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; phasewete_boleng: python3 Ditholosi/ya_kgole_Dipeakanyo.py show'.format(akumente_arei.network_host,akumente_arei.network_host),flush=True)
    if akumente_arei.pip and not akumente_arei.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= akumente_arei.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if akumente_arei.forward and not akumente_arei.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as mothopo_boleng:
        if akumente_arei.pip:
            from 꾸러미중계 import 꾸러미중계
            mothopo_boleng.enter_context(꾸러미중계(akumente_arei.pip_port, akumente_arei.pip_cache, akumente_arei.pip_offline))
            print('sehlopha 중계: 127.0.0.1:' + str(akumente_arei.pip_port), flush=True)
        phethagatša_mošomo(akumente_arei)


def phethagatša_mošomo(akumente_arei):
    if akumente_arei.desktop:
        if akumente_arei.vnc or akumente_arei.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from teskethopo_pogelo import sepetša_teskethopo
        raise SystemExit(sepetša_teskethopo(akumente_arei.port, Netweke=akumente_arei.network, 파일전송접속번호=akumente_arei.ftp_port, 전달규칙들=akumente_arei.forward, sephetho_boleng=akumente_arei.resolution, moeng_atrese=akumente_arei.guest_ip, go_nea_ditirelo_atrese=akumente_arei.network_host))
    Dikgetho = ['-display', akumente_arei.display, '-serial', 'mon:stdio']
    if akumente_arei.vnc:
        Dikgetho += ['-vnc', akumente_arei.vnc]
    if akumente_arei.network:
        from Netweke_kgokaganyo import Netweke_kgokaganyo
        with Netweke_kgokaganyo(akumente_arei.ftp_port, akumente_arei.forward, moeng_atrese=akumente_arei.guest_ip, go_nea_ditirelo_atrese=akumente_arei.network_host) as kgokaganyo:
            boemo_boleng = subprocess.call(Taelo(akumente_arei.resolution) + Dikgetho + kgokaganyo.전달인수())
            if kgokaganyo.Phošo: raise SystemExit('network bridge: ' + kgokaganyo.Phošo)
        raise SystemExit(boemo_boleng)
    raise SystemExit(subprocess.call(Taelo(akumente_arei.resolution) + Dikgetho))


if __name__ == '__main__':
    Diriša()
