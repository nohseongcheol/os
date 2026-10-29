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

ໂຄງ_ການ_ເລກຮາກ = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for ທາງໂຄຈອນ in _난수파일들:
        try:
            os.unlink(ທາງໂຄຈອນ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ຟາຍ:
        ຟາຍ.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(ຟາຍ.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ຟາຍ.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    ໂຮສ = ໂຄງ_ການ_ເລກຮາກ.parent / 'rpi4/build/host'
    적재기 = ໂຮສ / 'lib/ld-musl-x86_64.so.1'
    ຖານ_ສອງ = ໂຮສ / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and ຖານ_ສອງ.is_file():
        return [str(적재기), '--library-path', str(ໂຮສ / 'usr/lib') + ':' + str(ໂຮສ / 'lib'),
                str(ຖານ_ສອງ), '-L', str(ໂຮສ / 'usr/share/qemu')]
    ຖານ_ສອງ = shutil.which('qemu-system-aarch64')
    if not ຖານ_ສອງ:
        raise SystemExit('raspi4b ການຮອງຮັບ_ຄ່າ QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ຖານ_ສອງ]


def 해상도읽기(ຂໍ້ຄວາມ):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', ຂໍ້ຄວາມ):
        raise argparse.ArgumentTypeError('ຄວາມລະອຽດ_ຄ່າ ຮູບແບບ_ຄ່າ_d1a42ea5: 1920x1080')
    너비, 높이 = map(int, ຂໍ້ຄວາມ.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('ການຮອງຮັບ_ຄ່າ ຄ_ລິບ: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def ຄໍາສັ່ງ_1f12b8e2(ຄວາມລະອຽດ_ຄ່າ=(640, 480)):
    ພື້ນຫຼັງ_ຄ່າ = 모의기계()
    지원목록 = subprocess.check_output(ພື້ນຫຼັງ_ຄ່າ + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*ຄວາມລະອຽດ_ຄ່າ))
    return ພື້ນຫຼັງ_ຄ່າ + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(ໂຄງ_ການ_ເລກຮາກ / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def ແລ່ນ():
    ຕົວແຍກວິເຄາະ = argparse.ArgumentParser(description='자체 Java Pi4 ແກນກາງ_ຄ່າ. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 ອອກ_ແອັບ.')
    ຕົວແຍກວິເຄາະ.add_argument('--display', default='none', help='none 또는 gtk/sdl (ໂຮສ ການຮອງຮັບ_ຄ່າ 필요)')
    ຕົວແຍກວິເຄາະ.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 ຂະ_ຫນາດ. 예: 1920x1080; ຄ່າທີ່ກໍານົດໄວ້ແລ້ວ 640x480')
    ຕົວແຍກວິເຄາະ.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. ກະແຈ_ຄ່າ 입력은 UART 터미널에서 합니다.')
    ຕົວແຍກວິເຄາະ.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    ຕົວແຍກວິເຄາະ.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    ຕົວແຍກວິເຄາະ.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 ເຊື່ອມຕໍ່; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    ຕົວແຍກວິເຄາະ.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    ຕົວແຍກວິເຄາະ.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP ຄວບຄຸມ_ຄ່າ 포트 (데이터 50000..50007)')
    ຕົວແຍກວິເຄາະ.add_argument('--guest-ip', default=None, help='QEMU NAT ສົ່ງຕໍ່_ຄ່າ ເປົ້າ_ຫມາຍ. 기본은 ip.conf의 IP; ປ່ຽນ_ແປງ_ຄ່າ 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    ຕົວແຍກວິເຄາະ.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ອີເມວ. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ອີເມວ: 외부 ການເຊື່ອມຕໍ່_e05f319b')
    ຕົວແຍກວິເຄາະ.add_argument('--forward', action='append', default=[], help='--network 추가 ເຊື່ອມຕໍ່: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    ຕົວແຍກວິເຄາະ.add_argument('--pip', action='store_true', help='PyPI ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ ຊຸດ 중계 ແລ່ນ (--network 필요, MicroPython 호환 소스만)')
    ຕົວແຍກວິເຄາະ.add_argument('--pip-port', type=int, default=8027, help='ຊຸດ 중계의 localhost TCP 포트')
    ຕົວແຍກວິເຄາະ.add_argument('--pip-cache', type=Path, default=ໂຄງ_ການ_ເລກຮາກ/'build/pip-cache')
    ຕົວແຍກວິເຄາະ.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ = ຕົວແຍກວິເຄາະ.parse_args()
    if ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.remote:
        ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.network=True
        ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; ລະຫັດຜ່ານ_ຄ່າ: python3 ເຄື່ອງມື/ທາງ_ໄກ_ການຕັ້ງຄ່າ.py show'.format(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.network_host,ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.network_host),flush=True)
    if ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.pip and not ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.network: ຕົວແຍກວິເຄາະ.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.pip_port <= 65535: ຕົວແຍກວິເຄາະ.error('--pip-port 범위는 1~65535입니다.')
    if ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.forward and not ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.network: ຕົວແຍກວິເຄາະ.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ແຫຼ່ງ_ຄ່າ:
        if ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.pip:
            from 꾸러미중계 import 꾸러미중계
            ແຫຼ່ງ_ຄ່າ.enter_context(꾸러미중계(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.pip_port, ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.pip_cache, ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.pip_offline))
            print('ຊຸດ 중계: 127.0.0.1:' + str(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.pip_port), flush=True)
        ປະ_ຕິ_ບັດ_ຫນ້າວຽກ(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ)


def ປະ_ຕິ_ບັດ_ຫນ້າວຽກ(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ):
    if ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.desktop:
        if ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.vnc or ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ເດັສທັອບ_ເບິ່ງ import ແລ່ນ_ເດັສທັອບ
        raise SystemExit(ແລ່ນ_ເດັສທັອບ(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.port, ເຄືອຂ່າຍ=ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.network, ຟາຍ_ໂອນ_ຫມາຍເລກພອດ=ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.ftp_port, 전달규칙들=ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.forward, ຄວາມລະອຽດ_ຄ່າ=ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.resolution, ແຂກ_ອີເມວ=ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.guest_ip, ໂຮສ_ອີເມວ=ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.network_host))
    ຕົວເລືອກ = ['-display', ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.display, '-serial', 'mon:stdio']
    if ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.vnc:
        ຕົວເລືອກ += ['-vnc', ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.vnc]
    if ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.network:
        from ເຄືອຂ່າຍ_ຕົວເຊື່ອມ import ເຄືອຂ່າຍ_ຕົວເຊື່ອມ
        with ເຄືອຂ່າຍ_ຕົວເຊື່ອມ(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.ftp_port, ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.forward, ແຂກ_ອີເມວ=ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.guest_ip, ໂຮສ_ອີເມວ=ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.network_host) as ຕົວເຊື່ອມ:
            ສະຖານະ_ຄ່າ = subprocess.call(ຄໍາສັ່ງ_1f12b8e2(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.resolution) + ຕົວເລືອກ + ຕົວເຊື່ອມ.전달인수())
            if ຕົວເຊື່ອມ.ຂໍ້ຜິດພາດ: raise SystemExit('network bridge: ' + ຕົວເຊື່ອມ.ຂໍ້ຜິດພາດ)
        raise SystemExit(ສະຖານະ_ຄ່າ)
    raise SystemExit(subprocess.call(ຄໍາສັ່ງ_1f12b8e2(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.resolution) + ຕົວເລືອກ))


if __name__ == '__main__':
    ແລ່ນ()
