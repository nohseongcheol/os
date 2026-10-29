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

gốcCâyDựÁn = Path(__file__).resolve().parents[1]
CácTệpNgẫuNhiên = []


def NgẫuNhiênDọnDẹp():
    for đườngDẫn in CácTệpNgẫuNhiên:
        try:
            os.unlink(đườngDẫn)
        except FileNotFoundError:
            pass


atexit.register(NgẫuNhiênDọnDẹp)


def cácĐốiSốNgẫuNhiênTừXa():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Tệp:
        Tệp.write(b'JKRENRG1' + os.urandom(32))
        CácTệpNgẫuNhiên.append(Tệp.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Tệp.name)]


def MáyGiảLập():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    Chủ = gốcCâyDựÁn.parent / 'rpi4/build/host'
    bộNạp = Chủ / 'lib/ld-musl-x86_64.so.1'
    nhịPhân = Chủ / 'usr/bin/qemu-system-aarch64'
    if bộNạp.is_file() and nhịPhân.is_file():
        return [str(bộNạp), '--library-path', str(Chủ / 'usr/lib') + ':' + str(Chủ / 'lib'),
                str(nhịPhân), '-L', str(Chủ / 'usr/share/qemu')]
    nhịPhân = shutil.which('qemu-system-aarch64')
    if not nhịPhân:
        raise SystemExit('raspi4b giáTrịHỗTrợ QEMU giáTrịCầnĐến. QEMU_AARCH64로 경로를 지정하세요.')
    return [nhịPhân]


def đọcĐộPhânGiải(vănBản):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', vănBản):
        raise argparse.ArgumentTypeError('giáTrịĐộPhânGiải giáTrịĐịnhDạng: 1920x1080')
    giáTrịRộng, giáTrịCao = map(int, vănBản.split('x'))
    if not (640 <= giáTrịRộng <= 1920 and 480 <= giáTrịCao <= 1080):
        raise argparse.ArgumentTypeError('giáTrịHỗTrợ cắtXén: giáTrịRộng 640~1920, giáTrịCao 480~1080')
    return giáTrịRộng, giáTrịCao


def lệnh(giáTrịĐộPhânGiải=(640, 480)):
    giáTrịNền = MáyGiảLập()
    cácTínhNăngĐượcHỗTrợ = subprocess.check_output(giáTrịNền + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in cácTínhNăngĐượcHỗTrợ:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. giáTrịMớiNhất QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    giáTrịRộng, giáTrịCao = đọcĐộPhânGiải('{}x{}'.format(*giáTrịĐộPhânGiải))
    return giáTrịNền + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(giáTrịRộng),
                   '-global', 'bcm2835-fb.yres=' + str(giáTrịCao), '-kernel',
                   str(gốcCâyDựÁn / 'build/kernel8.img'), '-no-reboot'] + cácĐốiSốNgẫuNhiênTừXa()


def chạy():
    bộPhânTích = argparse.ArgumentParser(description='tựThân Java Pi4 giáTrịNhân. giáTrịNốiTiếp 셸은 Ctrl+A X, --desktop은 Ctrl+C로 chươngTrìnhRa.')
    bộPhânTích.add_argument('--display', default='none', help='none 또는 gtk/sdl (Chủ giáTrịHỗTrợ giáTrịCầnĐến)')
    bộPhânTích.add_argument('--resolution', type=đọcĐộPhânGiải, default=(640, 480), help='KhởiĐộng MànHình cỡ. 예: 1920x1080; giáTrịMặcĐịnh 640x480')
    bộPhânTích.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC cổngPhầnCứng 5902. giáTrịPhím 입력은 UART 터미널에서 합니다.')
    bộPhânTích.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    bộPhânTích.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC cổngPhầnCứng')
    bộPhânTích.add_argument('--network', action='store_true', help='giáTrịPhụTrợ UART SLIP와 QEMU NAT를 nốiKết; --desktop과 함께 giáTrịDùng 가능; 게스트에서 ftpd start')
    bộPhânTích.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    bộPhânTích.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP giáTrịĐiềuKhiển cổngPhầnCứng (데이터 50000..50007)')
    bộPhânTích.add_argument('--guest-ip', default=None, help='QEMU NAT giáTrịTiến giáTrịĐốiĐích. 기본은 ip.conf의 IP; đổiGiáTrị 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    bộPhânTích.add_argument('--network-host', default='127.0.0.1', help='NAT nhậnGiáTrị địaChỉ. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN địaChỉ: giáTrịBênNgoài kếtNối')
    bộPhânTích.add_argument('--forward', action='append', default=[], help='--network thêmCuốiMục nốiKết: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    bộPhânTích.add_argument('--pip', action='store_true', help='PyPI câyNguồn GóiGộp chuyểnTiếpGiáTrị chạy (--network giáTrịCầnĐến, MicroPython 호환 소스만)')
    bộPhânTích.add_argument('--pip-port', type=int, default=8027, help='GóiGộp 중계의 localhost TCP cổngPhầnCứng')
    bộPhânTích.add_argument('--pip-cache', type=Path, default=gốcCâyDựÁn/'build/pip-cache')
    bộPhânTích.add_argument('--pip-offline', action='store_true', help='이미 받은 giáTrịBảnPhânPhối 파일만 제공')
    mảngĐốiSố = bộPhânTích.parse_args()
    if mảngĐốiSố.remote:
        mảngĐốiSố.network=True
        mảngĐốiSố.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; giáTrịMậtKhẩu: python3 CôngCụ/cácThiếtLậpTừXa.py show'.format(mảngĐốiSố.network_host,mảngĐốiSố.network_host),flush=True)
    if mảngĐốiSố.pip and not mảngĐốiSố.network: bộPhânTích.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= mảngĐốiSố.pip_port <= 65535: bộPhânTích.error('--pip-port 범위는 1~65535입니다.')
    if mảngĐốiSố.forward and not mảngĐốiSố.network: bộPhânTích.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as giáTrịTàiNguyên:
        if mảngĐốiSố.pip:
            from chuyểnTiếpGóiGộp import chuyểnTiếpGóiGộp
            giáTrịTàiNguyên.enter_context(chuyểnTiếpGóiGộp(mảngĐốiSố.pip_port, mảngĐốiSố.pip_cache, mảngĐốiSố.pip_offline))
            print('GóiGộp chuyểnTiếpGiáTrị: 127.0.0.1:' + str(mảngĐốiSố.pip_port), flush=True)
        thựcThiTácVụ(mảngĐốiSố)


def thựcThiTácVụ(mảngĐốiSố):
    if mảngĐốiSố.desktop:
        if mảngĐốiSố.vnc or mảngĐốiSố.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from khungNhìnMànLàmViệc import chạyMànLàmViệc
        raise SystemExit(chạyMànLàmViệc(mảngĐốiSố.port, mạng=mảngĐốiSố.network, sốCổngChuyểnGiaoTệp=mảngĐốiSố.ftp_port, cácQuyTắcViệcChuyểnTiếp=mảngĐốiSố.forward, giáTrịĐộPhânGiải=mảngĐốiSố.resolution, địaChỉKhách=mảngĐốiSố.guest_ip, địaChỉChủ=mảngĐốiSố.network_host))
    cácTùyChọn = ['-display', mảngĐốiSố.display, '-serial', 'mon:stdio']
    if mảngĐốiSố.vnc:
        cácTùyChọn += ['-vnc', mảngĐốiSố.vnc]
    if mảngĐốiSố.network:
        from cầuNốiMạng import cầuNốiMạng
        with cầuNốiMạng(mảngĐốiSố.ftp_port, mảngĐốiSố.forward, địaChỉKhách=mảngĐốiSố.guest_ip, địaChỉChủ=mảngĐốiSố.network_host) as cầuNối:
            giáTrịTrạngThái = subprocess.call(lệnh(mảngĐốiSố.resolution) + cácTùyChọn + cầuNối.đốiSốĐãChuyểnTiếp())
            if cầuNối.lỗi: raise SystemExit('network bridge: ' + cầuNối.lỗi)
        raise SystemExit(giáTrịTrạngThái)
    raise SystemExit(subprocess.call(lệnh(mảngĐốiSố.resolution) + cácTùyChọn))


if __name__ == '__main__':
    chạy()
