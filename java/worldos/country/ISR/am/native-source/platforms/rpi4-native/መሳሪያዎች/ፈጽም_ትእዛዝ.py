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

አሳይ_ስር = Path(__file__).resolve().parents[1]
_난수파일들 = []


def _난수정리():
    for መተላለፊያ in _난수파일들:
        try:
            os.unlink(መተላለፊያ)
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
    አዘጋጅ_b78e430d = አሳይ_ስር.parent / 'rpi4/build/host'
    적재기 = አዘጋጅ_b78e430d / 'lib/ld-musl-x86_64.so.1'
    ባይነሪ = አዘጋጅ_b78e430d / 'usr/bin/qemu-system-aarch64'
    if 적재기.is_file() and ባይነሪ.is_file():
        return [str(적재기), '--library-path', str(አዘጋጅ_b78e430d / 'usr/lib') + ':' + str(አዘጋጅ_b78e430d / 'lib'),
                str(ባይነሪ), '-L', str(አዘጋጅ_b78e430d / 'usr/share/qemu')]
    ባይነሪ = shutil.which('qemu-system-aarch64')
    if not ባይነሪ:
        raise SystemExit('raspi4b ድገፍ_እሴት QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ባይነሪ]


def 해상도읽기(ጽሁፍ):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', ጽሁፍ):
        raise argparse.ArgumentTypeError('ጥራት_እሴት ቅርጸት_እሴት: 1920x1080')
    너비, 높이 = map(int, ጽሁፍ.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('ድገፍ_እሴት ቅንጥብ: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def ትእዛዝ(ጥራት_እሴት=(640, 480)):
    ልጣፍ_እሴት = 모의기계()
    지원목록 = subprocess.check_output(ልጣፍ_እሴት + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*ጥራት_እሴት))
    return ልጣፍ_እሴት + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(አሳይ_ስር / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def ማስኬጃ():
    አግልሎ_ማስቀመጥ = argparse.ArgumentParser(description='자체 Java Pi4 ዓንኳር_እሴት. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 ውጣ_ፕሮግራም.')
    አግልሎ_ማስቀመጥ.add_argument('--display', default='none', help='none 또는 gtk/sdl (አዘጋጅ_b78e430d ድገፍ_እሴት 필요)')
    አግልሎ_ማስቀመጥ.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='부팅 화면 መጠን. 예: 1920x1080; ነባሪ_እሴት 640x480')
    አግልሎ_ማስቀመጥ.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC 포트 5902. ቁልፍ_እሴት 입력은 UART 터미널에서 합니다.')
    አግልሎ_ማስቀመጥ.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    አግልሎ_ማስቀመጥ.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC 포트')
    አግልሎ_ማስቀመጥ.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 መገናኛ; --desktop과 함께 사용 가능; 게스트에서 ftpd start')
    አግልሎ_ማስቀመጥ.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    አግልሎ_ማስቀመጥ.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP ቁጥጥር_እሴት 포트 (데이터 50000..50007)')
    አግልሎ_ማስቀመጥ.add_argument('--guest-ip', default=None, help='QEMU NAT አሳልፍ_እሴት ዓላማ. 기본은 ip.conf의 IP; ለውጥ_እሴት 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    አግልሎ_ማስቀመጥ.add_argument('--network-host', default='127.0.0.1', help='NAT 수신 አድራሻ. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN አድራሻ: 외부 ግንኙነት_e05f319b')
    አግልሎ_ማስቀመጥ.add_argument('--forward', action='append', default=[], help='--network 추가 መገናኛ: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    አግልሎ_ማስቀመጥ.add_argument('--pip', action='store_true', help='PyPI ምንጭ_ዛፍ ቀርቅብ 중계 ማስኬጃ (--network 필요, MicroPython 호환 소스만)')
    አግልሎ_ማስቀመጥ.add_argument('--pip-port', type=int, default=8027, help='ቀርቅብ 중계의 localhost TCP 포트')
    አግልሎ_ማስቀመጥ.add_argument('--pip-cache', type=Path, default=አሳይ_ስር/'build/pip-cache')
    አግልሎ_ማስቀመጥ.add_argument('--pip-offline', action='store_true', help='이미 받은 배포 파일만 제공')
    ነጋሪ_እሴት_ድርድር = አግልሎ_ማስቀመጥ.parse_args()
    if ነጋሪ_እሴት_ድርድር.remote:
        ነጋሪ_እሴት_ድርድር.network=True
        ነጋሪ_እሴት_ድርድር.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; የይለፍ_ቃል_እሴት: python3 መሳሪያዎች/የሩቅ_ቅንብሮች.py show'.format(ነጋሪ_እሴት_ድርድር.network_host,ነጋሪ_እሴት_ድርድር.network_host),flush=True)
    if ነጋሪ_እሴት_ድርድር.pip and not ነጋሪ_እሴት_ድርድር.network: አግልሎ_ማስቀመጥ.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= ነጋሪ_እሴት_ድርድር.pip_port <= 65535: አግልሎ_ማስቀመጥ.error('--pip-port 범위는 1~65535입니다.')
    if ነጋሪ_እሴት_ድርድር.forward and not ነጋሪ_እሴት_ድርድር.network: አግልሎ_ማስቀመጥ.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as ሃብት_እሴት:
        if ነጋሪ_እሴት_ድርድር.pip:
            from 꾸러미중계 import 꾸러미중계
            ሃብት_እሴት.enter_context(꾸러미중계(ነጋሪ_እሴት_ድርድር.pip_port, ነጋሪ_እሴት_ድርድር.pip_cache, ነጋሪ_እሴት_ድርድር.pip_offline))
            print('ቀርቅብ 중계: 127.0.0.1:' + str(ነጋሪ_እሴት_ድርድር.pip_port), flush=True)
        መፈጸሚያ(ነጋሪ_እሴት_ድርድር)


def መፈጸሚያ(ነጋሪ_እሴት_ድርድር):
    if ነጋሪ_እሴት_ድርድር.desktop:
        if ነጋሪ_እሴት_ድርድር.vnc or ነጋሪ_እሴት_ድርድር.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from ዴስክቶፕ_እየው import አሂድ_ዴስክቶፕ
        raise SystemExit(አሂድ_ዴስክቶፕ(ነጋሪ_እሴት_ድርድር.port, መረብ=ነጋሪ_እሴት_ድርድር.network, ፋይል_ትልልፍ_የወደብ_ቁጥር=ነጋሪ_እሴት_ድርድር.ftp_port, 전달규칙들=ነጋሪ_እሴት_ድርድር.forward, ጥራት_እሴት=ነጋሪ_እሴት_ድርድር.resolution, እንግዳ_አድራሻ=ነጋሪ_እሴት_ድርድር.guest_ip, አዘጋጅ_አድራሻ=ነጋሪ_እሴት_ድርድር.network_host))
    አማራጮች = ['-display', ነጋሪ_እሴት_ድርድር.display, '-serial', 'mon:stdio']
    if ነጋሪ_እሴት_ድርድር.vnc:
        አማራጮች += ['-vnc', ነጋሪ_እሴት_ድርድር.vnc]
    if ነጋሪ_እሴት_ድርድር.network:
        from መረብ_ድልድይ import መረብ_ድልድይ
        with መረብ_ድልድይ(ነጋሪ_እሴት_ድርድር.ftp_port, ነጋሪ_እሴት_ድርድር.forward, እንግዳ_አድራሻ=ነጋሪ_እሴት_ድርድር.guest_ip, አዘጋጅ_አድራሻ=ነጋሪ_እሴት_ድርድር.network_host) as ድልድይ:
            ዞን_እሴት = subprocess.call(ትእዛዝ(ነጋሪ_እሴት_ድርድር.resolution) + አማራጮች + ድልድይ.전달인수())
            if ድልድይ.ስህተት: raise SystemExit('network bridge: ' + ድልድይ.ስህተት)
        raise SystemExit(ዞን_እሴት)
    raise SystemExit(subprocess.call(ትእዛዝ(ነጋሪ_እሴት_ድርድር.resolution) + አማራጮች))


if __name__ == '__main__':
    ማስኬጃ()
