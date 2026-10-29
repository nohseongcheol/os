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

Tugas_akar = Path(__file__).resolve().parents[1]
acak_File = []


def _난수정리():
    for jalur in acak_File:
        try:
            os.unlink(jalur)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as berkas:
        berkas.write(b'JKRENRG1' + os.urandom(32))
        acak_File.append(berkas.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(berkas.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    host = Tugas_akar.parent / 'rpi4/build/host'
    적재기 = host / 'lib/ld-musl-x86_64.so.1'
    biner = host / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and biner.is_file():
        return [str(적재기), '--library-path', str(host / 'usr/lib') + ':' + str(host / 'lib'),
                str(biner), '-L', str(host / 'usr/share/qemu')]
    biner = shutil.which('qemu-system-aarch64')
    if not biner:
        raise SystemExit('raspi4b dukung_VALUE QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [biner]


def 해상도읽기(teks):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', teks):
        raise argparse.ArgumentTypeError('resolusi_VALUE format_VALUE: 1920x1080')
    너비, 높이 = map(int, teks.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('dukung_VALUE klip: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def perintah(resolusi_VALUE=(640, 480)):
    wallpaper_VALUE = 모의기계()
    지원목록 = subprocess.check_output(wallpaper_VALUE + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*resolusi_VALUE))
    return wallpaper_VALUE + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(Tugas_akar / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def jalankan():
    parser = argparse.ArgumentParser(description='Asli Java Pi4 kernel_VALUE. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Keluar_apl.')
    parser.add_argument('--display', default='none', help='none 또는 gtk/sdl (host dukung_VALUE 필요)')
    parser.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='awal_mesin 화면 Ukuran. 예: 1920x1080; nilai_default 640x480')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Kunci_VALUE 입력은 UART 터미널에서 합니다.')
    parser.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    parser.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    parser.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Sambung; --desktop과 함께 gunakan_VALUE 가능; 게스트에서 ftpd start')
    parser.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    parser.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP kontrol_VALUE 포트 (데이터 50000..50007)')
    parser.add_argument('--guest-ip', default=None, help='QEMU NAT Maju_VALUE target. 기본은 ip.conf의 IP; ubah_VALUE 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    parser.add_argument('--network-host', default='127.0.0.1', help='NAT terima_VALUE surel. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN surel: eksternal_VALUE koneksi_e05f319b')
    parser.add_argument('--forward', action='append', default=[], help='--network tambah_entri Sambung: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    parser.add_argument('--pip', action='store_true', help='PyPI sumber_pohon paket 중계 jalankan (--network 필요, MicroPython 호환 소스만)')
    parser.add_argument('--pip-port', type=int, default=8027, help='paket 중계의 localhost TCP 포트')
    parser.add_argument('--pip-cache', type=Path, default=Tugas_akar/'build/pip-cache')
    parser.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    argumen_ARRAY = parser.parse_args()
    if argumen_ARRAY.remote:
        argumen_ARRAY.network=True
        argumen_ARRAY.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; sandi_VALUE: python3 alat/jarak_jauh_Pengaturan.py show'.format(argumen_ARRAY.network_host,argumen_ARRAY.network_host),flush=True)
    if argumen_ARRAY.pip and not argumen_ARRAY.network: parser.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argumen_ARRAY.pip_port <= 65535: parser.error('--pip-port 범위는 1~65535입니다.')
    if argumen_ARRAY.forward and not argumen_ARRAY.network: parser.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as sumber_daya_VALUE:
        if argumen_ARRAY.pip:
            from 꾸러미중계 import 꾸러미중계
            sumber_daya_VALUE.enter_context(꾸러미중계(argumen_ARRAY.pip_port, argumen_ARRAY.pip_cache, argumen_ARRAY.pip_offline))
            print('paket 중계: 127.0.0.1:' + str(argumen_ARRAY.pip_port), flush=True)
        Eksekusi(argumen_ARRAY)


def Eksekusi(argumen_ARRAY):
    if argumen_ARRAY.desktop:
        if argumen_ARRAY.vnc or argumen_ARRAY.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from desktop_Tampilan import eksekusi_desktop
        raise SystemExit(eksekusi_desktop(argumen_ARRAY.port, jaringan=argumen_ARRAY.network, transfer_file_nomor_port=argumen_ARRAY.ftp_port, 전달규칙들=argumen_ARRAY.forward, resolusi_VALUE=argumen_ARRAY.resolution, tamu_surel=argumen_ARRAY.guest_ip, host_surel=argumen_ARRAY.network_host))
    Opsi = ['-display', argumen_ARRAY.display, '-serial', 'mon:stdio']
    if argumen_ARRAY.vnc:
        Opsi += ['-vnc', argumen_ARRAY.vnc]
    if argumen_ARRAY.network:
        from jaringan_bridge import jaringan_bridge
        with jaringan_bridge(argumen_ARRAY.ftp_port, argumen_ARRAY.forward, tamu_surel=argumen_ARRAY.guest_ip, host_surel=argumen_ARRAY.network_host) as bridge:
            Status_VALUE = subprocess.call(perintah(argumen_ARRAY.resolution) + Opsi + bridge.전달인수())
            if bridge.galat: raise SystemExit('network bridge: ' + bridge.galat)
        raise SystemExit(Status_VALUE)
    raise SystemExit(subprocess.call(perintah(argumen_ARRAY.resolution) + Opsi))


if __name__ == '__main__':
    jalankan()
