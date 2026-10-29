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

projectRoot = Path(__file__).resolve().parents[1]
_randomFiles = []


def _cleanupRandom():
    for path in _randomFiles:
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass


atexit.register(_cleanupRandom)


def remoteRandomArguments():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as file:
        file.write(b'JKRENRG1' + os.urandom(32))
        _randomFiles.append(file.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(file.name)]


def MockMachine():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    Host = projectRoot.parent / 'rpi4/build/host'
    loader = Host / 'lib/ld-musl-x86_64.so.1'
    binary = Host / 'usr/bin/qemu-system-aarch64'
    if loader.is_file() and binary.is_file():
        return [str(loader), '--library-path', str(Host / 'usr/lib') + ':' + str(Host / 'lib'),
                str(binary), '-L', str(Host / 'usr/share/qemu')]
    binary = shutil.which('qemu-system-aarch64')
    if not binary:
        raise SystemExit('raspi4b supportValue QEMU neededValue. QEMU_AARCH64로 경로를 지정하세요.')
    return [binary]


def readResolution(text):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', text):
        raise argparse.ArgumentTypeError('resolutionValue formatValue: 1920x1080')
    widthValue, heightValue = map(int, text.split('x'))
    if not (640 <= widthValue <= 1920 and 480 <= heightValue <= 1080):
        raise argparse.ArgumentTypeError('supportValue clip: widthValue 640~1920, heightValue 480~1080')
    return widthValue, heightValue


def command(resolutionValue=(640, 480)):
    backgroundValue = MockMachine()
    supportedFeatures = subprocess.check_output(backgroundValue + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in supportedFeatures:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. latestValue QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    widthValue, heightValue = readResolution('{}x{}'.format(*resolutionValue))
    return backgroundValue + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(widthValue),
                   '-global', 'bcm2835-fb.yres=' + str(heightValue), '-kernel',
                   str(projectRoot / 'build/kernel8.img'), '-no-reboot'] + remoteRandomArguments()


def run():
    parser = argparse.ArgumentParser(description='Native Java Pi4 kernelValue. serialValue 셸은 Ctrl+A X, --desktop은 Ctrl+C로 exitProgram.')
    parser.add_argument('--display', default='none', help='none 또는 gtk/sdl (Host supportValue neededValue)')
    parser.add_argument('--resolution', type=readResolution, default=(640, 480), help='machine_boot Screen size. 예: 1920x1080; defaultValue 640x480')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC hardwarePort 5902. keyValue 입력은 UART 터미널에서 합니다.')
    parser.add_argument('--desktop', action='store_true', help='VNC 키보드/hangulText 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    parser.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC hardwarePort')
    parser.add_argument('--network', action='store_true', help='auxiliaryValue UART SLIP와 QEMU NAT를 connect; --desktop과 함께 useValue 가능; 게스트에서 ftpd start')
    parser.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    parser.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP controlValue hardwarePort (데이터 50000..50007)')
    parser.add_argument('--guest-ip', default=None, help='QEMU NAT forwardValue targetValue. 기본은 ip.conf의 IP; changeValue 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    parser.add_argument('--network-host', default='127.0.0.1', help='NAT receiveValue address. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN address: externalValue connection')
    parser.add_argument('--forward', action='append', default=[], help='--network appendEntry connect: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    parser.add_argument('--pip', action='store_true', help='PyPI sourceTree Bundle relayValue run (--network neededValue, MicroPython 호환 소스만)')
    parser.add_argument('--pip-port', type=int, default=8027, help='Bundle 중계의 localhost TCP hardwarePort')
    parser.add_argument('--pip-cache', type=Path, default=projectRoot/'build/pip-cache')
    parser.add_argument('--pip-offline', action='store_true', help='이미 받은 distributionValue 파일만 제공')
    argumentArray = parser.parse_args()
    if argumentArray.remote:
        argumentArray.network=True
        argumentArray.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; passwordValue: python3 tools/remoteSettings.py show'.format(argumentArray.network_host,argumentArray.network_host),flush=True)
    if argumentArray.pip and not argumentArray.network: parser.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argumentArray.pip_port <= 65535: parser.error('--pip-port 범위는 1~65535입니다.')
    if argumentArray.forward and not argumentArray.network: parser.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as resourceValue:
        if argumentArray.pip:
            from bundleRelay import bundleRelay
            resourceValue.enter_context(bundleRelay(argumentArray.pip_port, argumentArray.pip_cache, argumentArray.pip_offline))
            print('Bundle relayValue: 127.0.0.1:' + str(argumentArray.pip_port), flush=True)
        executeTask(argumentArray)


def executeTask(argumentArray):
    if argumentArray.desktop:
        if argumentArray.vnc or argumentArray.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from desktopView import runDesktop
        raise SystemExit(runDesktop(argumentArray.port, network=argumentArray.network, fileTransferPortNumber=argumentArray.ftp_port, forwardingRules=argumentArray.forward, resolutionValue=argumentArray.resolution, guestAddress=argumentArray.guest_ip, hostAddress=argumentArray.network_host))
    options = ['-display', argumentArray.display, '-serial', 'mon:stdio']
    if argumentArray.vnc:
        options += ['-vnc', argumentArray.vnc]
    if argumentArray.network:
        from networkBridge import networkBridge
        with networkBridge(argumentArray.ftp_port, argumentArray.forward, guestAddress=argumentArray.guest_ip, hostAddress=argumentArray.network_host) as bridge:
            stateValue = subprocess.call(command(argumentArray.resolution) + options + bridge.forwardedArgument())
            if bridge.error: raise SystemExit('network bridge: ' + bridge.error)
        raise SystemExit(stateValue)
    raise SystemExit(subprocess.call(command(argumentArray.resolution) + options))


if __name__ == '__main__':
    run()
