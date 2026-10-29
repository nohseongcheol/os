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
    for Hanyar_shiga in _난수파일들:
        try:
            os.unlink(Hanyar_shiga)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Fayil:
        Fayil.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Fayil.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Fayil.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    sauka = 기준.parent / 'rpi4/build/host'
    적재기 = sauka / 'lib/ld-musl-x86_64.so.1'
    Mai_bangare_biyu = sauka / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and Mai_bangare_biyu.is_file():
        return [str(적재기), '--library-path', str(sauka / 'usr/lib') + ':' + str(sauka / 'lib'),
                str(Mai_bangare_biyu), '-L', str(sauka / 'usr/share/qemu')]
    Mai_bangare_biyu = shutil.which('qemu-system-aarch64')
    if not Mai_bangare_biyu:
        raise SystemExit('raspi4b taimako_Daraja QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [Mai_bangare_biyu]


def 해상도읽기(SMS):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', SMS):
        raise argparse.ArgumentTypeError('Kyawon_tarkacen_hoto_Daraja zubi_Daraja: 1920x1080')
    너비, 높이 = map(int, SMS.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('taimako_Daraja darfi: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Umarni(Kyawon_tarkacen_hoto_Daraja=(640, 480)):
    Bi_bango_Daraja = 모의기계()
    지원목록 = subprocess.check_output(Bi_bango_Daraja + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*Kyawon_tarkacen_hoto_Daraja))
    return Bi_bango_Daraja + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Tafiyar_da():
    tatsar_manhaja = argparse.ArgumentParser(description='자체 Java Pi4 Kwara_Daraja. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Mafita_Shiri.')
    tatsar_manhaja.add_argument('--display', default='none', help='none 또는 gtk/sdl (sauka taimako_Daraja 필요)')
    tatsar_manhaja.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Girma. 예: 1920x1080; Tanadaddiyar_daraja 640x480')
    tatsar_manhaja.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC kayan_haɗi_na_kwamfuta_fot 5902. Makulli_Daraja 입력은 UART 터미널에서 합니다.')
    tatsar_manhaja.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    tatsar_manhaja.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC kayan_haɗi_na_kwamfuta_fot')
    tatsar_manhaja.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Haɗi; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    tatsar_manhaja.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    tatsar_manhaja.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP masarrafa_Daraja kayan_haɗi_na_kwamfuta_fot (데이터 50000..50007)')
    tatsar_manhaja.add_argument('--guest-ip', default=None, help='QEMU NAT Ingiza_Daraja tageti. 기본은 ip.conf의 IP; Canza_Daraja 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    tatsar_manhaja.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 imel. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN imel: 외부 haɗi_e05f319b')
    tatsar_manhaja.add_argument('--forward', action='append', default=[], help='--network 추가 Haɗi: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    tatsar_manhaja.add_argument('--pip', action='store_true', help='PyPI tushe_Li_irabin_tarin_bayanai dami 중계 Tafiyar_da (--network 필요, MicroPython 호환 소스만)')
    tatsar_manhaja.add_argument('--pip-port', type=int, default=8027, help='dami 중계의 localhost TCP kayan_haɗi_na_kwamfuta_fot')
    tatsar_manhaja.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    tatsar_manhaja.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    Tubalin_aiki_TSARI = tatsar_manhaja.parse_args()
    if Tubalin_aiki_TSARI.remote:
        Tubalin_aiki_TSARI.network=True
        Tubalin_aiki_TSARI.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; kalmar_sirri_Daraja: python3 Kaya/na_nesa_Saituna.py show'.format(Tubalin_aiki_TSARI.network_host,Tubalin_aiki_TSARI.network_host),flush=True)
    if Tubalin_aiki_TSARI.pip and not Tubalin_aiki_TSARI.network: tatsar_manhaja.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= Tubalin_aiki_TSARI.pip_port <= 65535: tatsar_manhaja.error('--pip-port 범위는 1~65535입니다.')
    if Tubalin_aiki_TSARI.forward and not Tubalin_aiki_TSARI.network: tatsar_manhaja.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as albarkatu_Daraja:
        if Tubalin_aiki_TSARI.pip:
            from 꾸러미중계 import 꾸러미중계
            albarkatu_Daraja.enter_context(꾸러미중계(Tubalin_aiki_TSARI.pip_port, Tubalin_aiki_TSARI.pip_cache, Tubalin_aiki_TSARI.pip_offline))
            print('dami 중계: 127.0.0.1:' + str(Tubalin_aiki_TSARI.pip_port), flush=True)
        gudanar_aiki(Tubalin_aiki_TSARI)


def gudanar_aiki(Tubalin_aiki_TSARI):
    if Tubalin_aiki_TSARI.desktop:
        if Tubalin_aiki_TSARI.vnc or Tubalin_aiki_TSARI.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from destof_s import Gudanar_da_destof
        raise SystemExit(Gudanar_da_destof(Tubalin_aiki_TSARI.port, Hanyar_sadarwa=Tubalin_aiki_TSARI.network, Fayil_Gusar_da_lambar_kafa=Tubalin_aiki_TSARI.ftp_port, 전달규칙들=Tubalin_aiki_TSARI.forward, Kyawon_tarkacen_hoto_Daraja=Tubalin_aiki_TSARI.resolution, baƙo_imel=Tubalin_aiki_TSARI.guest_ip, sauka_imel=Tubalin_aiki_TSARI.network_host))
    Zaɓuɓɓuka = ['-display', Tubalin_aiki_TSARI.display, '-serial', 'mon:stdio']
    if Tubalin_aiki_TSARI.vnc:
        Zaɓuɓɓuka += ['-vnc', Tubalin_aiki_TSARI.vnc]
    if Tubalin_aiki_TSARI.network:
        from 통신다리 import 통신다리
        with 통신다리(Tubalin_aiki_TSARI.ftp_port, Tubalin_aiki_TSARI.forward, baƙo_imel=Tubalin_aiki_TSARI.guest_ip, sauka_imel=Tubalin_aiki_TSARI.network_host) as 연결다리:
            Matsayi_Daraja = subprocess.call(Umarni(Tubalin_aiki_TSARI.resolution) + Zaɓuɓɓuka + 연결다리.전달인수())
            if 연결다리.Kuskure: raise SystemExit('network bridge: ' + 연결다리.Kuskure)
        raise SystemExit(Matsayi_Daraja)
    raise SystemExit(subprocess.call(Umarni(Tubalin_aiki_TSARI.resolution) + Zaɓuɓɓuka))


if __name__ == '__main__':
    Tafiyar_da()
