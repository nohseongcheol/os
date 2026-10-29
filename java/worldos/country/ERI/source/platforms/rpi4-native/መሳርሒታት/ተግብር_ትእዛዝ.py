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
    for መገዲ in _난수파일들:
        try:
            os.unlink(መገዲ)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as ፋይል:
        ፋይል.write(b'JKRENRG1' + os.urandom(32))
        _난수파일들.append(ፋይል.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(ፋይል.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    አዐንግድ = 기준.parent / 'rpi4/build/host'
    적재기 = አዐንግድ / 'lib/ld-musl-x86_64.so.1'
    ጽምዳዊ = አዐንግድ / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and ጽምዳዊ.is_file():
        return [str(적재기), '--library-path', str(አዐንግድ / 'usr/lib') + ':' + str(አዐንግድ / 'lib'),
                str(ጽምዳዊ), '-L', str(አዐንግድ / 'usr/share/qemu')]
    ጽምዳዊ = shutil.which('qemu-system-aarch64')
    if not ጽምዳዊ:
        raise SystemExit('raspi4b ሓገዝ_ዋጋ QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ጽምዳዊ]


def 해상도읽기(ጽሑፍ):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', ጽሑፍ):
        raise argparse.ArgumentTypeError('ንጹርነት_ዋጋ ቅረጽ_ዋጋ: 1920x1080')
    너비, 높이 = map(int, ጽሑፍ.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('ሓገዝ_ዋጋ ቅንጣብ: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def ትእዛዝ(ንጹርነት_ዋጋ=(640, 480)):
    ድሕረባይታ_ዋጋ = 모의기계()
    지원목록 = subprocess.check_output(ድሕረባይታ_ዋጋ + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*ንጹርነት_ዋጋ))
    return ድሕረባይታ_ዋጋ + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(기준 / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def ኣኺድ():
    인수해석기 = argparse.ArgumentParser(description='자체 Java Pi4 ፍረ_ዋጋ. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 ውጻእ_መተግበሪ.')
    인수해석기.add_argument('--display', default='none', help='none 또는 gtk/sdl (አዐንግድ ሓገዝ_ዋጋ 필요)')
    인수해석기.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 መጠን. 예: 1920x1080; ንቡር_ዋጋ 640x480')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC ሃርድዌር_ወደብ 5902. መፍትሕ_ዋጋ 입력은 UART 터미널에서 합니다.')
    인수해석기.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    인수해석기.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC ሃርድዌር_ወደብ')
    인수해석기.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 ኣላግብ; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    인수해석기.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    인수해석기.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP ቁጽጽር_ዋጋ ሃርድዌር_ወደብ (데이터 50000..50007)')
    인수해석기.add_argument('--guest-ip', default=None, help='QEMU NAT ኣሕልፍ_ዋጋ ዕላማ. 기본은 ip.conf의 IP; ለውጥ_ዋጋ 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    인수해석기.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 ኣድራሻ. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ኣድራሻ: 외부 ርክብ_e05f319b')
    인수해석기.add_argument('--forward', action='append', default=[], help='--network 추가 ኣላግብ: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    인수해석기.add_argument('--pip', action='store_true', help='PyPI ምንጪ_ገረብ ጥማር 중계 ኣኺድ (--network 필요, MicroPython 호환 소스만)')
    인수해석기.add_argument('--pip-port', type=int, default=8027, help='ጥማር 중계의 localhost TCP ሃርድዌር_ወደብ')
    인수해석기.add_argument('--pip-cache', type=Path, default=기준/'build/pip-cache')
    인수해석기.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    ሓባሪ_ቁጽሪ_ተርታ = 인수해석기.parse_args()
    if ሓባሪ_ቁጽሪ_ተርታ.remote:
        ሓባሪ_ቁጽሪ_ተርታ.network=True
        ሓባሪ_ቁጽሪ_ተርታ.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; መሕለፊ_ቃል_ዋጋ: python3 መሳርሒታት/ርሑቕ_ኣቀማምጣታት.py show'.format(ሓባሪ_ቁጽሪ_ተርታ.network_host,ሓባሪ_ቁጽሪ_ተርታ.network_host),flush=True)
    if ሓባሪ_ቁጽሪ_ተርታ.pip and not ሓባሪ_ቁጽሪ_ተርታ.network: 인수해석기.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= ሓባሪ_ቁጽሪ_ተርታ.pip_port <= 65535: 인수해석기.error('--pip-port 범위는 1~65535입니다.')
    if ሓባሪ_ቁጽሪ_ተርታ.forward and not ሓባሪ_ቁጽሪ_ተርታ.network: 인수해석기.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ሃብቲ_ዋጋ:
        if ሓባሪ_ቁጽሪ_ተርታ.pip:
            from 꾸러미중계 import 꾸러미중계
            ሃብቲ_ዋጋ.enter_context(꾸러미중계(ሓባሪ_ቁጽሪ_ተርታ.pip_port, ሓባሪ_ቁጽሪ_ተርታ.pip_cache, ሓባሪ_ቁጽሪ_ተርታ.pip_offline))
            print('ጥማር 중계: 127.0.0.1:' + str(ሓባሪ_ቁጽሪ_ተርታ.pip_port), flush=True)
        ተግብር_ዕማም(ሓባሪ_ቁጽሪ_ተርታ)


def ተግብር_ዕማም(ሓባሪ_ቁጽሪ_ተርታ):
    if ሓባሪ_ቁጽሪ_ተርታ.desktop:
        if ሓባሪ_ቁጽሪ_ተርታ.vnc or ሓባሪ_ቁጽሪ_ተርታ.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ዴስክቶፕ_ትርኢት import ኣኺድ_ዴስክቶፕ
        raise SystemExit(ኣኺድ_ዴስክቶፕ(ሓባሪ_ቁጽሪ_ተርታ.port, ማሕበራዊ_ኔትወርክ=ሓባሪ_ቁጽሪ_ተርታ.network, 파일전송접속번호=ሓባሪ_ቁጽሪ_ተርታ.ftp_port, 전달규칙들=ሓባሪ_ቁጽሪ_ተርታ.forward, ንጹርነት_ዋጋ=ሓባሪ_ቁጽሪ_ተርታ.resolution, 게스트주소=ሓባሪ_ቁጽሪ_ተርታ.guest_ip, አዐንግድ_ኣድራሻ=ሓባሪ_ቁጽሪ_ተርታ.network_host))
    ኣማራጽታት = ['-display', ሓባሪ_ቁጽሪ_ተርታ.display, '-serial', 'mon:stdio']
    if ሓባሪ_ቁጽሪ_ተርታ.vnc:
        ኣማራጽታት += ['-vnc', ሓባሪ_ቁጽሪ_ተርታ.vnc]
    if ሓባሪ_ቁጽሪ_ተርታ.network:
        from 통신다리 import 통신다리
        with 통신다리(ሓባሪ_ቁጽሪ_ተርታ.ftp_port, ሓባሪ_ቁጽሪ_ተርታ.forward, 게스트주소=ሓባሪ_ቁጽሪ_ተርታ.guest_ip, አዐንግድ_ኣድራሻ=ሓባሪ_ቁጽሪ_ተርታ.network_host) as 연결다리:
            ደረጃ_ዋጋ = subprocess.call(ትእዛዝ(ሓባሪ_ቁጽሪ_ተርታ.resolution) + ኣማራጽታት + 연결다리.전달인수())
            if 연결다리.ጌጋ: raise SystemExit('network bridge: ' + 연결다리.ጌጋ)
        raise SystemExit(ደረጃ_ዋጋ)
    raise SystemExit(subprocess.call(ትእዛዝ(ሓባሪ_ቁጽሪ_ተርታ.resolution) + ኣማራጽታት))


if __name__ == '__main__':
    ኣኺድ()
