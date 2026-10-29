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

projektWurzel = Path(__file__).resolve().parents[1]
ZufälligDateien = []


def BereinigungZufällig():
    for pfad in ZufälligDateien:
        try:
            os.unlink(pfad)
        except FileNotFoundError:
            pass


atexit.register(BereinigungZufällig)


def entferntZufälligArgumente():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Datei:
        Datei.write(b'JKRENRG1' + os.urandom(32))
        ZufälligDateien.append(Datei.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Datei.name)]


def AttrappeMaschine():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    Wirtssystem = projektWurzel.parent / 'rpi4/build/host'
    lader = Wirtssystem / 'lib/ld-musl-x86_64.so.1'
    binär = Wirtssystem / 'usr/bin/qemu-system-aarch64'
    if lader.is_file() and binär.is_file():
        return [str(lader), '--library-path', str(Wirtssystem / 'usr/lib') + ':' + str(Wirtssystem / 'lib'),
                str(binär), '-L', str(Wirtssystem / 'usr/share/qemu')]
    binär = shutil.which('qemu-system-aarch64')
    if not binär:
        raise SystemExit('raspi4b unterstützungWert QEMU benötigtWert. QEMU_AARCH64로 경로를 지정하세요.')
    return [binär]


def auflösungLesen(Text):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', Text):
        raise argparse.ArgumentTypeError('auflösungWert formatWert: 1920x1080')
    breiteWert, höheWert = map(int, Text.split('x'))
    if not (640 <= breiteWert <= 1920 and 480 <= höheWert <= 1080):
        raise argparse.ArgumentTypeError('unterstützungWert beschneiden: breiteWert 640~1920, höheWert 480~1080')
    return breiteWert, höheWert


def befehl(auflösungWert=(640, 480)):
    hintergrundWert = AttrappeMaschine()
    unterstütztMerkmale = subprocess.check_output(hintergrundWert + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in unterstütztMerkmale:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. neuesterWert QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    breiteWert, höheWert = auflösungLesen('{}x{}'.format(*auflösungWert))
    return hintergrundWert + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(breiteWert),
                   '-global', 'bcm2835-fb.yres=' + str(höheWert), '-kernel',
                   str(projektWurzel / 'build/kernel8.img'), '-no-reboot'] + entferntZufälligArgumente()


def ausführenVorgang():
    strukturanalysierer = argparse.ArgumentParser(description='eigen Java Pi4 betriebskernWert. seriellWert 셸은 Ctrl+A X, --desktop은 Ctrl+C로 verlassenProzessProgramm.')
    strukturanalysierer.add_argument('--display', default='none', help='none 또는 gtk/sdl (Wirtssystem unterstützungWert benötigtWert)')
    strukturanalysierer.add_argument('--resolution', type=auflösungLesen, default=(640, 480), help='Startvorgang Bildschirm größe. 예: 1920x1080; standardwertWert 640x480')
    strukturanalysierer.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC hardwarePort 5902. tasteWert 입력은 UART 터미널에서 합니다.')
    strukturanalysierer.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    strukturanalysierer.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC hardwarePort')
    strukturanalysierer.add_argument('--network', action='store_true', help='hilfsWert UART SLIP와 QEMU NAT를 verbinden; --desktop과 함께 benutzenWert 가능; 게스트에서 ftpd start')
    strukturanalysierer.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    strukturanalysierer.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP steuerungWert hardwarePort (데이터 50000..50007)')
    strukturanalysierer.add_argument('--guest-ip', default=None, help='QEMU NAT vorwärtsWert zielobjektWert. 기본은 ip.conf의 IP; wertÄndern 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    strukturanalysierer.add_argument('--network-host', default='127.0.0.1', help='NAT wertEmpfangen adresse. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN adresse: externWert verbindung')
    strukturanalysierer.add_argument('--forward', action='append', default=[], help='--network eintragAnhängen verbinden: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    strukturanalysierer.add_argument('--pip', action='store_true', help='PyPI quelltextBaum Paket wertWeitergeben ausführenVorgang (--network benötigtWert, MicroPython 호환 소스만)')
    strukturanalysierer.add_argument('--pip-port', type=int, default=8027, help='Paket 중계의 localhost TCP hardwarePort')
    strukturanalysierer.add_argument('--pip-cache', type=Path, default=projektWurzel/'build/pip-cache')
    strukturanalysierer.add_argument('--pip-offline', action='store_true', help='이미 받은 verteilungWert 파일만 제공')
    argumentDatenfeld = strukturanalysierer.parse_args()
    if argumentDatenfeld.remote:
        argumentDatenfeld.network=True
        argumentDatenfeld.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; passwortWert: python3 Werkzeuge/entferntEinstellungen.py show'.format(argumentDatenfeld.network_host,argumentDatenfeld.network_host),flush=True)
    if argumentDatenfeld.pip and not argumentDatenfeld.network: strukturanalysierer.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= argumentDatenfeld.pip_port <= 65535: strukturanalysierer.error('--pip-port 범위는 1~65535입니다.')
    if argumentDatenfeld.forward and not argumentDatenfeld.network: strukturanalysierer.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as betriebsmittelEintragWert:
        if argumentDatenfeld.pip:
            from bündelWeitergeben import bündelWeitergeben
            betriebsmittelEintragWert.enter_context(bündelWeitergeben(argumentDatenfeld.pip_port, argumentDatenfeld.pip_cache, argumentDatenfeld.pip_offline))
            print('Paket wertWeitergeben: 127.0.0.1:' + str(argumentDatenfeld.pip_port), flush=True)
        aufgabeAusführen(argumentDatenfeld)


def aufgabeAusführen(argumentDatenfeld):
    if argumentDatenfeld.desktop:
        if argumentDatenfeld.vnc or argumentDatenfeld.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from arbeitsflächeAnsicht import arbeitsflächeAusführenVorgang
        raise SystemExit(arbeitsflächeAusführenVorgang(argumentDatenfeld.port, netzwerk=argumentDatenfeld.network, dateiÜbertragungPortNummer=argumentDatenfeld.ftp_port, weiterleitendRegeln=argumentDatenfeld.forward, auflösungWert=argumentDatenfeld.resolution, gastAdresse=argumentDatenfeld.guest_ip, wirtssystemAdresse=argumentDatenfeld.network_host))
    wahlmöglichkeiten = ['-display', argumentDatenfeld.display, '-serial', 'mon:stdio']
    if argumentDatenfeld.vnc:
        wahlmöglichkeiten += ['-vnc', argumentDatenfeld.vnc]
    if argumentDatenfeld.network:
        from netzwerkBrücke import netzwerkBrücke
        with netzwerkBrücke(argumentDatenfeld.ftp_port, argumentDatenfeld.forward, gastAdresse=argumentDatenfeld.guest_ip, wirtssystemAdresse=argumentDatenfeld.network_host) as brücke:
            statuswertWert = subprocess.call(befehl(argumentDatenfeld.resolution) + wahlmöglichkeiten + brücke.weitergeleitetArgument())
            if brücke.fehler: raise SystemExit('network bridge: ' + brücke.fehler)
        raise SystemExit(statuswertWert)
    raise SystemExit(subprocess.call(befehl(argumentDatenfeld.resolution) + wahlmöglichkeiten))


if __name__ == '__main__':
    ausführenVorgang()
