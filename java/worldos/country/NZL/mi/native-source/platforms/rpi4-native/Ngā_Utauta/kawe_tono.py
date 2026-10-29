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

whakaatu_pūtake = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for ara in _난수파일들:
        try:
            os.unlink(ara)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Kōnae:
        Kōnae.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Kōnae.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Kōnae.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    taurima = whakaatu_pūtake.parent / 'rpi4/build/host'
    적재기 = taurima / 'lib/ld-musl-x86_64.so.1'
    ā_rua = taurima / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and ā_rua.is_file():
        return [str(적재기), '--library-path', str(taurima / 'usr/lib') + ':' + str(taurima / 'lib'),
                str(ā_rua), '-L', str(taurima / 'usr/share/qemu')]
    ā_rua = shutil.which('qemu-system-aarch64')
    if not ā_rua:
        raise SystemExit('raspi4b Tautoko_uara QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ā_rua]


def 해상도읽기(Ngā_kupu):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Ngā_kupu):
        raise argparse.ArgumentTypeError('taumira_uara hōputu_uara: 1920x1080')
    너비, 높이 = map(int, Ngā_kupu.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Tautoko_uara topenga: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def tono(taumira_uara=(640, 480)):
    Papamuri_uara = 모의기계()
    지원목록 = subprocess.check_output(Papamuri_uara + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*taumira_uara))
    return Papamuri_uara + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(whakaatu_pūtake / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def whakahaere():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 kākano_uara_0611a8a8. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Putaatu_kaupapa.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (taurima Tautoko_uara 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 rahi. 예: 1920x1080; uara_taunoa 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. kī_uara 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 TŪHONO; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP mana_uara 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT Whakamua_uara ūnga. 기본은 ip.conf의 IP; huri_uara 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ADDRESS. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ADDRESS: 외부 hononga_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 TŪHONO: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI pūtake_rākau pūpū 중계 whakahaere (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='pūpū 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=whakaatu_pūtake/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    tohenga_HUĀNGA = 인수해석기.parse_args()
    if tohenga_HUĀNGA.remote:
        tohenga_HUĀNGA.network=True
        tohenga_HUĀNGA.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; kupuhipa_uara: python3 Ngā_Utauta/mamao_Ngā_Tautuhinga.py show'.format(tohenga_HUĀNGA.network_host,tohenga_HUĀNGA.network_host),flush=True)
    if tohenga_HUĀNGA.pip and not tohenga_HUĀNGA.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= tohenga_HUĀNGA.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if tohenga_HUĀNGA.forward and not tohenga_HUĀNGA.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as rauemi_uara:
        if tohenga_HUĀNGA.pip:
            from 꾸러미중계 import 꾸러미중계
            rauemi_uara.enter_context(꾸러미중계(tohenga_HUĀNGA.pip_port, tohenga_HUĀNGA.pip_cache, tohenga_HUĀNGA.pip_offline))
            print('pūpū 중계: 127.0.0.1:' + str(tohenga_HUĀNGA.pip_port), flush=True)
        kawe_tūmahi(tohenga_HUĀNGA)


def kawe_tūmahi(tohenga_HUĀNGA):
    if tohenga_HUĀNGA.desktop:
        if tohenga_HUĀNGA.vnc or tohenga_HUĀNGA.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from papamahi_tiro import whakahaere_papamahi
        raise SystemExit(whakahaere_papamahi(tohenga_HUĀNGA.port, whatunga=tohenga_HUĀNGA.network, 파일전송접속번호=tohenga_HUĀNGA.ftp_port, 전달규칙들=tohenga_HUĀNGA.forward, taumira_uara=tohenga_HUĀNGA.resolution, manuhiri_ADDRESS=tohenga_HUĀNGA.guest_ip, taurima_ADDRESS=tohenga_HUĀNGA.network_host))
    Kōwhiringa = ['-display', tohenga_HUĀNGA.display, '-serial', 'mon:stdio']
    if tohenga_HUĀNGA.vnc:
        Kōwhiringa += ['-vnc', tohenga_HUĀNGA.vnc]
    if tohenga_HUĀNGA.network:
        from whatunga_arawhata import whatunga_arawhata
        with whatunga_arawhata(tohenga_HUĀNGA.ftp_port, tohenga_HUĀNGA.forward, manuhiri_ADDRESS=tohenga_HUĀNGA.guest_ip, taurima_ADDRESS=tohenga_HUĀNGA.network_host) as arawhata:
            tūnga_uara = subprocess.call(tono(tohenga_HUĀNGA.resolution) + Kōwhiringa + arawhata.전달인수())
            if arawhata.Pōhēhē: raise SystemExit('network bridge: ' + arawhata.Pōhēhē)
        raise SystemExit(tūnga_uara)
    raise SystemExit(subprocess.call(tono(tohenga_HUĀNGA.resolution) + Kōwhiringa))


if __name__ == '__main__':
    whakahaere()
