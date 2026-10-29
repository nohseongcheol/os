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

แสดง_ราก = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for เส้นทาง in _난수파일들:
        try:
            os.unlink(เส้นทาง)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as แฟ้ม:
        แฟ้ม.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(แฟ้ม.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(แฟ้ม.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    โฮสต์ = แสดง_ราก.parent / 'rpi4/build/host'
    ตัวโหลด = โฮสต์ / 'lib/ld-musl-x86_64.so.1'
    ไบนารี = โฮสต์ / 'usr/bin/qemu-system-aarch64'
    if ตัวโหลด.is_file() and ไบนารี.is_file():
        return [str(ตัวโหลด), '--library-path', str(โฮสต์ / 'usr/lib') + ':' + str(โฮสต์ / 'lib'),
                str(ไบนารี), '-L', str(โฮสต์ / 'usr/share/qemu')]
    ไบนารี = shutil.which('qemu-system-aarch64')
    if not ไบนารี:
        raise SystemExit('raspi4b สนับสนุน_ค่า QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ไบนารี]


def 해상도읽기(ข้อความ):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', ข้อความ):
        raise argparse.ArgumentTypeError('ความละเอียด_ค่า รูปแบบ_ค่า_d1a42ea5: 1920x1080')
    너비, 높이 = map(int, ข้อความ.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('สนับสนุน_ค่า คลิป: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def คําสั่ง(ความละเอียด_ค่า=(640, 480)):
    พื้นหลัง_ค่า = 모의기계()
    지원목록 = subprocess.check_output(พื้นหลัง_ค่า + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*ความละเอียด_ค่า))
    return พื้นหลัง_ค่า + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(แสดง_ราก / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def เรียกใช้งาน():
    ตัวแยกวิเคราะห์ = argparse.ArgumentParser(description='เอง Java Pi4 เคอร์เนล_ค่า. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 ออก_แอป.')
    ตัวแยกวิเคราะห์.add_argument('--display', default='none', help='none 또는 gtk/sdl (โฮสต์ สนับสนุน_ค่า 필요)')
    ตัวแยกวิเคราะห์.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 ขนาด. 예: 1920x1080; ค่าเริ่มต้น 640x480')
    ตัวแยกวิเคราะห์.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC ฮาร์ดแวร์_แปลง 5902. คีย์_ค่า 입력은 UART 터미널에서 합니다.')
    ตัวแยกวิเคราะห์.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    ตัวแยกวิเคราะห์.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC ฮาร์ดแวร์_แปลง')
    ตัวแยกวิเคราะห์.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 เชื่อมต่อ; --desktop과 함께 ใช้_ค่า 가능; 게스트에서 ftpd start')
    ตัวแยกวิเคราะห์.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    ตัวแยกวิเคราะห์.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP ควบคุม_ค่า ฮาร์ดแวร์_แปลง (데이터 50000..50007)')
    ตัวแยกวิเคราะห์.add_argument('--guest-ip', default=None, help='QEMU NAT ส่งต่อ_ค่า_24592b8a เป้าหมาย. 기본은 ip.conf의 IP; เปลี่ยนแปลง_ค่า 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    ตัวแยกวิเคราะห์.add_argument('--network-host', default='127.0.0.1', help='NAT รับ_ค่า อีเมล. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN อีเมล: ภายนอก_ค่า เพื่อน_e05f319b')
    ตัวแยกวิเคราะห์.add_argument('--forward', action='append', default=[], help='--network ผนวก_รายการ เชื่อมต่อ: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    ตัวแยกวิเคราะห์.add_argument('--pip', action='store_true', help='PyPI แหล่ง_ทรี รวม 중계 เรียกใช้งาน (--network 필요, MicroPython 호환 소스만)')
    ตัวแยกวิเคราะห์.add_argument('--pip-port', type=int, default=8027, help='รวม 중계의 localhost TCP ฮาร์ดแวร์_แปลง')
    ตัวแยกวิเคราะห์.add_argument('--pip-cache', type=Path, default=แสดง_ราก/'build/pip-cache')
    ตัวแยกวิเคราะห์.add_argument('--pip-offline', action='store_true', help='이미 받은 การกระจาย_ค่า 파일만 제공')
    อาร์กิวเมนต์_อาร์เรย์ = ตัวแยกวิเคราะห์.parse_args()
    if อาร์กิวเมนต์_อาร์เรย์.remote:
        อาร์กิวเมนต์_อาร์เรย์.network=True
        อาร์กิวเมนต์_อาร์เรย์.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; รหัสผ่าน_ค่า: python3 เครื่องมือ/ระยะไกล_การตั้งค่า.py show'.format(อาร์กิวเมนต์_อาร์เรย์.network_host,อาร์กิวเมนต์_อาร์เรย์.network_host),flush=True)
    if อาร์กิวเมนต์_อาร์เรย์.pip and not อาร์กิวเมนต์_อาร์เรย์.network: ตัวแยกวิเคราะห์.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= อาร์กิวเมนต์_อาร์เรย์.pip_port <= 65535: ตัวแยกวิเคราะห์.error('--pip-port 범위는 1~65535입니다.')
    if อาร์กิวเมนต์_อาร์เรย์.forward and not อาร์กิวเมนต์_อาร์เรย์.network: ตัวแยกวิเคราะห์.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ทรัพยากร_ค่า:
        if อาร์กิวเมนต์_อาร์เรย์.pip:
            from 꾸러미중계 import 꾸러미중계
            ทรัพยากร_ค่า.enter_context(꾸러미중계(อาร์กิวเมนต์_อาร์เรย์.pip_port, อาร์กิวเมนต์_อาร์เรย์.pip_cache, อาร์กิวเมนต์_อาร์เรย์.pip_offline))
            print('รวม 중계: 127.0.0.1:' + str(อาร์กิวเมนต์_อาร์เรย์.pip_port), flush=True)
        เรียกทํางาน(อาร์กิวเมนต์_อาร์เรย์)


def เรียกทํางาน(อาร์กิวเมนต์_อาร์เรย์):
    if อาร์กิวเมนต์_อาร์เรย์.desktop:
        if อาร์กิวเมนต์_อาร์เรย์.vnc or อาร์กิวเมนต์_อาร์เรย์.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from เดสก์ท็อป_ดู import ใช้งาน_เดสก์ท็อป
        raise SystemExit(ใช้งาน_เดสก์ท็อป(อาร์กิวเมนต์_อาร์เรย์.port, เครือข่าย_9b2e3222=อาร์กิวเมนต์_อาร์เรย์.network, การถ่ายโอนแฟ้ม_หมายเลขพอร์ต=อาร์กิวเมนต์_อาร์เรย์.ftp_port, 전달규칙들=อาร์กิวเมนต์_อาร์เรย์.forward, ความละเอียด_ค่า=อาร์กิวเมนต์_อาร์เรย์.resolution, ผู้เยี่ยมชม_อีเมล=อาร์กิวเมนต์_อาร์เรย์.guest_ip, โฮสต์_อีเมล=อาร์กิวเมนต์_อาร์เรย์.network_host))
    ตัวเลือก = ['-display', อาร์กิวเมนต์_อาร์เรย์.display, '-serial', 'mon:stdio']
    if อาร์กิวเมนต์_อาร์เรย์.vnc:
        ตัวเลือก += ['-vnc', อาร์กิวเมนต์_อาร์เรย์.vnc]
    if อาร์กิวเมนต์_อาร์เรย์.network:
        from บริดจ์_3de4fe3a import บริดจ์_3de4fe3a
        with บริดจ์_3de4fe3a(อาร์กิวเมนต์_อาร์เรย์.ftp_port, อาร์กิวเมนต์_อาร์เรย์.forward, ผู้เยี่ยมชม_อีเมล=อาร์กิวเมนต์_อาร์เรย์.guest_ip, โฮสต์_อีเมล=อาร์กิวเมนต์_อาร์เรย์.network_host) as บริดจ์:
            สถานะ_ค่า = subprocess.call(คําสั่ง(อาร์กิวเมนต์_อาร์เรย์.resolution) + ตัวเลือก + บริดจ์.전달인수())
            if บริดจ์.ข้อผิดพลาด: raise SystemExit('network bridge: ' + บริดจ์.ข้อผิดพลาด)
        raise SystemExit(สถานะ_ค่า)
    raise SystemExit(subprocess.call(คําสั่ง(อาร์กิวเมนต์_อาร์เรย์.resolution) + ตัวเลือก))


if __name__ == '__main__':
    เรียกใช้งาน()
