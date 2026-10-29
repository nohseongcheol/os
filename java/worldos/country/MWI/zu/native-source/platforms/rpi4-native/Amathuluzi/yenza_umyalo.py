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
    for Indlela_2 in _난수파일들:
        try:
            os.unlink(Indlela_2)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Ihele:
        Ihele.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(Ihele.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Ihele.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    singatha = 기준.parent / 'rpi4/build/host'
    적재기 = singatha / 'lib/ld-musl-x86_64.so.1'
    unambambili = singatha / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and unambambili.is_file():
        return [str(적재기), '--library-path', str(singatha / 'usr/lib') + ':' + str(singatha / 'lib'),
                str(unambambili), '-L', str(singatha / 'usr/share/qemu')]
    unambambili = shutil.which('qemu-system-aarch64')
    if not unambambili:
        raise SystemExit('raspi4b uxhaso_inani QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [unambambili]


def 해상도읽기(Itekisi):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Itekisi):
        raise argparse.ArgumentTypeError('ukucaca_inani misa_inani: 1920x1080')
    너비, 높이 = map(int, Itekisi.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('uxhaso_inani isiqeshana: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Umlayelo(ukucaca_inani=(640, 480)):
    ngemuva_inani = 모의기계()
    지원목록 = subprocess.check_output(ngemuva_inani + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*ukucaca_inani))
    return ngemuva_inani + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Sebenzisa():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 ikhenela_inani. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 phuma_i_app.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (singatha uxhaso_inani 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Ubungako. 예: 1920x1080; inani_elimisiwe 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. inkomba_inani 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Xhumanisa; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP isilawuli_inani 포트 (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT dlulisela_phambili_inani impokophelo. 기본은 ip.conf의 IP; guqula_inani 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ikheli. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ikheli: 외부 uxhumano_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 Xhumanisa: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI umthombo_isihlahla isigaxa 중계 Sebenzisa (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='isigaxa 중계의 localhost TCP 포트')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    i_agumenti_AMALUNGU_AFANAYO = 인수해석기.parse_args()
    if i_agumenti_AMALUNGU_AFANAYO.remote:
        i_agumenti_AMALUNGU_AFANAYO.network=True
        i_agumenti_AMALUNGU_AFANAYO.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; iphasiwedi_inani: python3 Amathuluzi/kude_Amasethingi.py show'.format(i_agumenti_AMALUNGU_AFANAYO.network_host,i_agumenti_AMALUNGU_AFANAYO.network_host),flush=True)
    if i_agumenti_AMALUNGU_AFANAYO.pip and not i_agumenti_AMALUNGU_AFANAYO.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= i_agumenti_AMALUNGU_AFANAYO.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if i_agumenti_AMALUNGU_AFANAYO.forward and not i_agumenti_AMALUNGU_AFANAYO.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as insiza_inani:
        if i_agumenti_AMALUNGU_AFANAYO.pip:
            from 꾸러미중계 import 꾸러미중계
            insiza_inani.enter_context(꾸러미중계(i_agumenti_AMALUNGU_AFANAYO.pip_port, i_agumenti_AMALUNGU_AFANAYO.pip_cache, i_agumenti_AMALUNGU_AFANAYO.pip_offline))
            print('isigaxa 중계: 127.0.0.1:' + str(i_agumenti_AMALUNGU_AFANAYO.pip_port), flush=True)
        yenza_umsebenzi(i_agumenti_AMALUNGU_AFANAYO)


def yenza_umsebenzi(i_agumenti_AMALUNGU_AFANAYO):
    if i_agumenti_AMALUNGU_AFANAYO.desktop:
        if i_agumenti_AMALUNGU_AFANAYO.vnc or i_agumenti_AMALUNGU_AFANAYO.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ideskithophu_buka import sebenzisa_ideskithophu
        raise SystemExit(sebenzisa_ideskithophu(i_agumenti_AMALUNGU_AFANAYO.port, iNethiwekhi=i_agumenti_AMALUNGU_AFANAYO.network, 파일전송접속번호=i_agumenti_AMALUNGU_AFANAYO.ftp_port, 전달규칙들=i_agumenti_AMALUNGU_AFANAYO.forward, ukucaca_inani=i_agumenti_AMALUNGU_AFANAYO.resolution, isivakashi_ikheli=i_agumenti_AMALUNGU_AFANAYO.guest_ip, singatha_ikheli=i_agumenti_AMALUNGU_AFANAYO.network_host))
    Izinketho = ['-display', i_agumenti_AMALUNGU_AFANAYO.display, '-serial', 'mon:stdio']
    if i_agumenti_AMALUNGU_AFANAYO.vnc:
        Izinketho += ['-vnc', i_agumenti_AMALUNGU_AFANAYO.vnc]
    if i_agumenti_AMALUNGU_AFANAYO.network:
        from iNethiwekhi_ibhuloho import iNethiwekhi_ibhuloho
        with iNethiwekhi_ibhuloho(i_agumenti_AMALUNGU_AFANAYO.ftp_port, i_agumenti_AMALUNGU_AFANAYO.forward, isivakashi_ikheli=i_agumenti_AMALUNGU_AFANAYO.guest_ip, singatha_ikheli=i_agumenti_AMALUNGU_AFANAYO.network_host) as ibhuloho:
            isimo_inani = subprocess.call(Umlayelo(i_agumenti_AMALUNGU_AFANAYO.resolution) + Izinketho + ibhuloho.전달인수())
            if ibhuloho.Iphutha: raise SystemExit('network bridge: ' + ibhuloho.Iphutha)
        raise SystemExit(isimo_inani)
    raise SystemExit(subprocess.call(Umlayelo(i_agumenti_AMALUNGU_AFANAYO.resolution) + Izinketho))


if __name__ == '__main__':
    Sebenzisa()
