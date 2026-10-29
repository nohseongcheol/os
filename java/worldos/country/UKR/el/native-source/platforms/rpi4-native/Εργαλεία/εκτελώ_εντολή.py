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

έργο_ρίζα = Path(__file__).resolve().parents[1]
τυχαίος_Αρχεία = []


def _난수정리():
    for ΔΙΑΔΡΟΜΗ in τυχαίος_Αρχεία:
        try:
            os.unlink(ΔΙΑΔΡΟΜΗ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Αρχείο:
        Αρχείο.write(b'JKRENRG1' + os.urandom(32))
        τυχαίος_Αρχεία.append(Αρχείο.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Αρχείο.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    φιλοξενώ = έργο_ρίζα.parent / 'rpi4/build/host'
    πρόγραμμα_φόρτωσης = φιλοξενώ / 'lib/ld-musl-x86_64.so.1'
    δυαδικός = φιλοξενώ / 'usr/bin/qemu-system-aarch64'
    if πρόγραμμα_φόρτωσης.is_file() and δυαδικός.is_file():
        return [str(πρόγραμμα_φόρτωσης), '--library-path', str(φιλοξενώ / 'usr/lib') + ':' + str(φιλοξενώ / 'lib'),
                str(δυαδικός), '-L', str(φιλοξενώ / 'usr/share/qemu')]
    δυαδικός = shutil.which('qemu-system-aarch64')
    if not δυαδικός:
        raise SystemExit('raspi4b στήριγμα_τιμή QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [δυαδικός]


def 해상도읽기(Κείμενο):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Κείμενο):
        raise argparse.ArgumentTypeError('ανάλυση_τιμή μορφή_τιμή: 1920x1080')
    너비, ύψος_τιμή = map(int, Κείμενο.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= ύψος_τιμή <= 1080):
        raise argparse.ArgumentTypeError('στήριγμα_τιμή απόσπασμα: 너비 640~1920, ύψος_τιμή 480~1080')
    return 너비, ύψος_τιμή


def Εντολή(ανάλυση_τιμή=(640, 480)):
    φόντο_τιμή = 모의기계()
    지원목록 = subprocess.check_output(φόντο_τιμή + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, ύψος_τιμή = 해상도읽기('{}x{}'.format(*ανάλυση_τιμή))
    return φόντο_τιμή + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(ύψος_τιμή), '-kernel',
                   str(έργο_ρίζα / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def Εκτέλεση_2():
    ανάλυση = argparse.ArgumentParser(description='ίδιο Java Pi4 πυρήνας_τιμή. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Έξοδος_εφαρμογή.')
    ανάλυση.add_argument('--display', default='none', help='none 또는 gtk/sdl (φιλοξενώ στήριγμα_τιμή 필요)')
    ανάλυση.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 Μέγεθος. 예: 1920x1080; προεπιλεγμένη_τιμή 640x480')
    ανάλυση.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC υλικό_θύρα 5902. Κλειδί_τιμή 입력은 UART 터미널에서 합니다.')
    ανάλυση.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    ανάλυση.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC υλικό_θύρα')
    ανάλυση.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Σύνδεση; --desktop과 함께 χρήση_τιμή 가능; 게스트에서 ftpd start')
    ανάλυση.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    ανάλυση.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP έλεγχος_τιμή υλικό_θύρα (데이터 50000..50007)')
    ανάλυση.add_argument('--guest-ip', default=None, help='QEMU NAT προωθώ_τιμή τιμή_στόχος. 기본은 ip.conf의 IP; αλλάζω_τιμή 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    ανάλυση.add_argument('--network-host', default='127.0.0.1', help='NAT λαμβάνω_τιμή_cef4d8ab διεύθυνση. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN διεύθυνση: εξωτερικός_τιμή σύνδεση_e05f319b')
    ανάλυση.add_argument('--forward', action='append', default=[], help='--network προσαρτώ_καταχώρηση Σύνδεση: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    ανάλυση.add_argument('--pip', action='store_true', help='PyPI προέλευση_δέντρο πακέτο 중계 Εκτέλεση_2 (--network 필요, MicroPython 호환 소스만)')
    ανάλυση.add_argument('--pip-port', type=int, default=8027, help='πακέτο 중계의 localhost TCP υλικό_θύρα')
    ανάλυση.add_argument('--pip-cache', type=Path, default=έργο_ρίζα/'build/pip-cache')
    ανάλυση.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    όρισμα_πίνακας = ανάλυση.parse_args()
    if όρισμα_πίνακας.remote:
        όρισμα_πίνακας.network=True
        όρισμα_πίνακας.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; κωδικός_πρόσβασης_τιμή: python3 Εργαλεία/απομακρυσμένος_Ρυθμίσεις.py show'.format(όρισμα_πίνακας.network_host,όρισμα_πίνακας.network_host),flush=True)
    if όρισμα_πίνακας.pip and not όρισμα_πίνακας.network: ανάλυση.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= όρισμα_πίνακας.pip_port <= 65535: ανάλυση.error('--pip-port 범위는 1~65535입니다.')
    if όρισμα_πίνακας.forward and not όρισμα_πίνακας.network: ανάλυση.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as πόρος_τιμή:
        if όρισμα_πίνακας.pip:
            from 꾸러미중계 import 꾸러미중계
            πόρος_τιμή.enter_context(꾸러미중계(όρισμα_πίνακας.pip_port, όρισμα_πίνακας.pip_cache, όρισμα_πίνακας.pip_offline))
            print('πακέτο 중계: 127.0.0.1:' + str(όρισμα_πίνακας.pip_port), flush=True)
        Εκτέλεση(όρισμα_πίνακας)


def Εκτέλεση(όρισμα_πίνακας):
    if όρισμα_πίνακας.desktop:
        if όρισμα_πίνακας.vnc or όρισμα_πίνακας.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from υπολογιστής_Προβολή import εκτελώ_υπολογιστής
        raise SystemExit(εκτελώ_υπολογιστής(όρισμα_πίνακας.port, δίκτυο=όρισμα_πίνακας.network, μεταφορά_αρχείων_αριθμός_θύρας=όρισμα_πίνακας.ftp_port, 전달규칙들=όρισμα_πίνακας.forward, ανάλυση_τιμή=όρισμα_πίνακας.resolution, Επισκέπτης_διεύθυνση=όρισμα_πίνακας.guest_ip, φιλοξενώ_διεύθυνση=όρισμα_πίνακας.network_host))
    Επιλογές = ['-display', όρισμα_πίνακας.display, '-serial', 'mon:stdio']
    if όρισμα_πίνακας.vnc:
        Επιλογές += ['-vnc', όρισμα_πίνακας.vnc]
    if όρισμα_πίνακας.network:
        from γέφυρα_3de4fe3a import γέφυρα_3de4fe3a
        with γέφυρα_3de4fe3a(όρισμα_πίνακας.ftp_port, όρισμα_πίνακας.forward, Επισκέπτης_διεύθυνση=όρισμα_πίνακας.guest_ip, φιλοξενώ_διεύθυνση=όρισμα_πίνακας.network_host) as γέφυρα:
            Κατάσταση_τιμή = subprocess.call(Εντολή(όρισμα_πίνακας.resolution) + Επιλογές + γέφυρα.전달인수())
            if γέφυρα.ΣΦΑΛΜΑ: raise SystemExit('network bridge: ' + γέφυρα.ΣΦΑΛΜΑ)
        raise SystemExit(Κατάσταση_τιμή)
    raise SystemExit(subprocess.call(Εντολή(όρισμα_πίνακας.resolution) + Επιλογές))


if __name__ == '__main__':
    Εκτέλεση_2()
