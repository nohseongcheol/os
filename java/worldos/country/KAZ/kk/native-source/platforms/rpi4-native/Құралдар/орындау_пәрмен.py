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

жоба_түбір = Path(__file__).resolve().parents[1]
кездейсоқ_Файлдар = []


def _난수정리():
    for Жол_2 in кездейсоқ_Файлдар:
        try:
            os.unlink(Жол_2)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Файл:
        Файл.write(b'JKRENRG1' + os.urandom(32))
        кездейсоқ_Файлдар.append(Файл.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Файл.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    орналастыру = жоба_түбір.parent / 'rpi4/build/host'
    적재기 = орналастыру / 'lib/ld-musl-x86_64.so.1'
    екілік = орналастыру / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and екілік.is_file():
        return [str(적재기), '--library-path', str(орналастыру / 'usr/lib') + ':' + str(орналастыру / 'lib'),
                str(екілік), '-L', str(орналастыру / 'usr/share/qemu')]
    екілік = shutil.which('qemu-system-aarch64')
    if not екілік:
        raise SystemExit('raspi4b тіреу_мән QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [екілік]


def 해상도읽기(Мәтін):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Мәтін):
        raise argparse.ArgumentTypeError('ажыратымдылық_мән пішім_мән: 1920x1080')
    너비, 높이 = map(int, Мәтін.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('тіреу_мән клип: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def Команда(ажыратымдылық_мән=(640, 480)):
    Фон_мән = 모의기계()
    지원목록 = subprocess.check_output(Фон_мән + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*ажыратымдылық_мән))
    return Фон_мән + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(жоба_түбір / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Орындау_2():
    талдау_құралы = argparse.ArgumentParser(description='자체 Java Pi4 ядро_мән. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Шығу_бағдарлама.')
    талдау_құралы.add_argument('--display', default='none', help='none 또는 gtk/sdl (орналастыру тіреу_мән 필요)')
    талдау_құралы.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Өлшемі. 예: 1920x1080; әдепкі_мән 640x480')
    талдау_құралы.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. Кілт_мән 입력은 UART 터미널에서 합니다.')
    талдау_құралы.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    талдау_құралы.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    талдау_құралы.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Байланысу; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    талдау_құралы.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    талдау_құралы.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP Басқару_мән 포트 (데이터 50000..50007)')
    талдау_құралы.add_argument('--guest-ip', default=None, help='QEMU NAT Алға_мән мақсатты_мән. 기본은 ip.conf의 IP; өзгерту_мән 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    талдау_құралы.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 мекенжай. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN мекенжай: сыртқы_мән қосылым_e05f319b')
    талдау_құралы.add_argument('--forward', action='append', default=[], help='--network қосу_енгізу Байланысу: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    талдау_құралы.add_argument('--pip', action='store_true', help='PyPI көз_дарақ жинау 중계 Орындау_2 (--network 필요, MicroPython 호환 소스만)')
    талдау_құралы.add_argument('--pip-port', type=int, default=8027, help='жинау 중계의 localhost TCP 포트')
    талдау_құралы.add_argument('--pip-cache', type=Path, default=жоба_түбір/'build/pip-cache')
    талдау_құралы.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    аргумент_массив = талдау_құралы.parse_args()
    if аргумент_массив.remote:
        аргумент_массив.network=True
        аргумент_массив.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; құпиясөз_мән: python3 Құралдар/원격설정.py show'.format(аргумент_массив.network_host,аргумент_массив.network_host),flush=True)
    if аргумент_массив.pip and not аргумент_массив.network: талдау_құралы.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= аргумент_массив.pip_port <= 65535: талдау_құралы.error('--pip-port 범위는 1~65535입니다.')
    if аргумент_массив.forward and not аргумент_массив.network: талдау_құралы.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ресурс_мән:
        if аргумент_массив.pip:
            from 꾸러미중계 import 꾸러미중계
            ресурс_мән.enter_context(꾸러미중계(аргумент_массив.pip_port, аргумент_массив.pip_cache, аргумент_массив.pip_offline))
            print('жинау 중계: 127.0.0.1:' + str(аргумент_массив.pip_port), flush=True)
        Орындау(аргумент_массив)


def Орындау(аргумент_массив):
    if аргумент_массив.desktop:
        if аргумент_массив.vnc or аргумент_массив.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from үстелдік_Көрініс import орындалу_үстелдік
        raise SystemExit(орындалу_үстелдік(аргумент_массив.port, желі=аргумент_массив.network, файл_тасымалдау_порт_нөмірі=аргумент_массив.ftp_port, 전달규칙들=аргумент_массив.forward, ажыратымдылық_мән=аргумент_массив.resolution, қонақ_мекенжай=аргумент_массив.guest_ip, орналастыру_мекенжай=аргумент_массив.network_host))
    Параметрлер = ['-display', аргумент_массив.display, '-serial', 'mon:stdio']
    if аргумент_массив.vnc:
        Параметрлер += ['-vnc', аргумент_массив.vnc]
    if аргумент_массив.network:
        from желі_көпір import желі_көпір
        with желі_көпір(аргумент_массив.ftp_port, аргумент_массив.forward, қонақ_мекенжай=аргумент_массив.guest_ip, орналастыру_мекенжай=аргумент_массив.network_host) as көпір:
            күй_мән = subprocess.call(Команда(аргумент_массив.resolution) + Параметрлер + көпір.전달인수())
            if көпір.Қате: raise SystemExit('network bridge: ' + көпір.Қате)
        raise SystemExit(күй_мән)
    raise SystemExit(subprocess.call(Команда(аргумент_массив.resolution) + Параметрлер))


if __name__ == '__main__':
    Орындау_2()
