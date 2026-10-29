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

racineProjet = Path(__file__).resolve().parents[1]
FichiersAléatoire = []


def AléatoireNettoyage():
    for chemin in FichiersAléatoire:
        try:
            os.unlink(chemin)
        except FileNotFoundError:
            pass


atexit.register(AléatoireNettoyage)


def argumentsAléatoireDistant():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as Fichier:
        Fichier.write(b'JKRENRG1' + os.urandom(32))
        FichiersAléatoire.append(Fichier.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(Fichier.name)]


def MachineSimulacre():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    Hôte = racineProjet.parent / 'rpi4/build/host'
    chargeur = Hôte / 'lib/ld-musl-x86_64.so.1'
    binaire = Hôte / 'usr/bin/qemu-system-aarch64'
    if chargeur.is_file() and binaire.is_file():
        return [str(chargeur), '--library-path', str(Hôte / 'usr/lib') + ':' + str(Hôte / 'lib'),
                str(binaire), '-L', str(Hôte / 'usr/share/qemu')]
    binaire = shutil.which('qemu-system-aarch64')
    if not binaire:
        raise SystemExit('raspi4b valeurPriseEnCharge QEMU valeurNécessaire. QEMU_AARCH64로 경로를 지정하세요.')
    return [binaire]


def lireRésolution(texte):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', texte):
        raise argparse.ArgumentTypeError('valeurRésolution valeurFormat: 1920x1080')
    valeurLargeur, valeurHauteur = map(int, texte.split('x'))
    if not (640 <= valeurLargeur <= 1920 and 480 <= valeurHauteur <= 1080):
        raise argparse.ArgumentTypeError('valeurPriseEnCharge rogner: valeurLargeur 640~1920, valeurHauteur 480~1080')
    return valeurLargeur, valeurHauteur


def commande(valeurRésolution=(640, 480)):
    valeurArrièrePlan = MachineSimulacre()
    fonctionnalitésPrisEnCharge = subprocess.check_output(valeurArrièrePlan + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in fonctionnalitésPrisEnCharge:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. valeurDernierRécent QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    valeurLargeur, valeurHauteur = lireRésolution('{}x{}'.format(*valeurRésolution))
    return valeurArrièrePlan + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(valeurLargeur),
                   '-global', 'bcm2835-fb.yres=' + str(valeurHauteur), '-kernel',
                   str(racineProjet / 'build/kernel8.img'), '-no-reboot'] + argumentsAléatoireDistant()


def lancer():
    analyseur = argparse.ArgumentParser(description='interne Java Pi4 valeurNoyau. valeurSériel 셸은 Ctrl+A X, --desktop은 Ctrl+C로 programmeQuitter.')
    analyseur.add_argument('--display', default='none', help='none 또는 gtk/sdl (Hôte valeurPriseEnCharge valeurNécessaire)')
    analyseur.add_argument('--resolution', type=lireRésolution, default=(640, 480), help='Amorçage Écran taille. 예: 1920x1080; valeurDéfaut 640x480')
    analyseur.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC portMatériel 5902. valeurTouche 입력은 UART 터미널에서 합니다.')
    analyseur.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    analyseur.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC portMatériel')
    analyseur.add_argument('--network', action='store_true', help='valeurAuxiliaire UART SLIP와 QEMU NAT를 connecter; --desktop과 함께 valeurUtiliser 가능; 게스트에서 ftpd start')
    analyseur.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    analyseur.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP valeurContrôle portMatériel (데이터 50000..50007)')
    analyseur.add_argument('--guest-ip', default=None, help='QEMU NAT valeurAvantDirection valeurCible. 기본은 ip.conf의 IP; changerValeur 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    analyseur.add_argument('--network-host', default='127.0.0.1', help='NAT recevoirValeur adresse. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN adresse: valeurExtérieur connexion')
    analyseur.add_argument('--forward', action='append', default=[], help='--network ajouterFinEntréeÉlément connecter: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    analyseur.add_argument('--pip', action='store_true', help='PyPI arbreSource Paquet relayerValeur lancer (--network valeurNécessaire, MicroPython 호환 소스만)')
    analyseur.add_argument('--pip-port', type=int, default=8027, help='Paquet 중계의 localhost TCP portMatériel')
    analyseur.add_argument('--pip-cache', type=Path, default=racineProjet/'build/pip-cache')
    analyseur.add_argument('--pip-offline', action='store_true', help='이미 받은 valeurDistribution 파일만 제공')
    tableauArgument = analyseur.parse_args()
    if tableauArgument.remote:
        tableauArgument.network=True
        tableauArgument.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; valeurMotPasse: python3 Outils/réglagesDistant.py show'.format(tableauArgument.network_host,tableauArgument.network_host),flush=True)
    if tableauArgument.pip and not tableauArgument.network: analyseur.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= tableauArgument.pip_port <= 65535: analyseur.error('--pip-port 범위는 1~65535입니다.')
    if tableauArgument.forward and not tableauArgument.network: analyseur.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as valeurRessource:
        if tableauArgument.pip:
            from relayerLot import relayerLot
            valeurRessource.enter_context(relayerLot(tableauArgument.pip_port, tableauArgument.pip_cache, tableauArgument.pip_offline))
            print('Paquet relayerValeur: 127.0.0.1:' + str(tableauArgument.pip_port), flush=True)
        exécuterTâche(tableauArgument)


def exécuterTâche(tableauArgument):
    if tableauArgument.desktop:
        if tableauArgument.vnc or tableauArgument.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from vueBureau import lancerBureau
        raise SystemExit(lancerBureau(tableauArgument.port, réseau=tableauArgument.network, numéroPortTransfertFichier=tableauArgument.ftp_port, règlesTransfertEnCours=tableauArgument.forward, valeurRésolution=tableauArgument.resolution, adresseInvité=tableauArgument.guest_ip, adresseHôte=tableauArgument.network_host))
    options = ['-display', tableauArgument.display, '-serial', 'mon:stdio']
    if tableauArgument.vnc:
        options += ['-vnc', tableauArgument.vnc]
    if tableauArgument.network:
        from pontRéseau import pontRéseau
        with pontRéseau(tableauArgument.ftp_port, tableauArgument.forward, adresseInvité=tableauArgument.guest_ip, adresseHôte=tableauArgument.network_host) as pont:
            valeurÉtatValeur = subprocess.call(commande(tableauArgument.resolution) + options + pont.argumentTransféré())
            if pont.erreur: raise SystemExit('network bridge: ' + pont.erreur)
        raise SystemExit(valeurÉtatValeur)
    raise SystemExit(subprocess.call(commande(tableauArgument.resolution) + options))


if __name__ == '__main__':
    lancer()
