#!/usr/bin/env python3
"""jkoros 전용 VirtualBox LanceurProgramme. 기존 VM/디스크/valeurStocker 상태는 삭제하지 않는다."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import uuid


class erreurExécution(RuntimeError):
    pass


def exécuterCommandeInterpréteurCommandes(arguments):
    environnement = dict(os.environ, LC_ALL='C')
    résultat = subprocess.run([str(valeur) for valeur in arguments], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=environnement, timeout=180)
    valeurContenuValeur = résultat.stdout.decode('utf-8', 'replace')
    if résultat.returncode:
        raise erreurExécution('commande valeurÉchec: ' + ' '.join(str(valeur) for valeur in arguments) + '\n' + valeurContenuValeur[-10000:])
    return valeurContenuValeur


def valeurAttribut(valeurContenuValeur):
    résultat = {}
    for ligne in valeurContenuValeur.splitlines():
        if '=' not in ligne:
            continue
        nom, valeur = ligne.split('=', 1)
        if nom.startswith('"'):
            nom = json.loads(nom)
        if valeur.startswith('"'):
            try:
                lireValeur, terminaison = json.JSONDecoder().raw_decode(valeur)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if terminaison == len(valeur): valeur = lireValeur
            except ValueError:
                raise erreurExécution('VirtualBox valeurAttribut valeurFormat erreur: ' + ligne)
        résultat[nom] = valeur
    return résultat


def entréesListeInscrit(valeurContenuValeur):
    résultat = {}
    for ligne in valeurContenuValeur.splitlines():
        estÉgal = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', ligne)
        if estÉgal: résultat[estÉgal.group(2).lower()] = estÉgal.group(1)
    return résultat


def sommeContrôle(chemin):
    valeur = hashlib.sha256()
    with chemin.open('rb') as Fichier:
        for Données in iter(lambda: Fichier.read(1024 * 1024), b''): valeur.update(Données)
    return valeur.hexdigest()


class LanceurProgramme:
    def __init__(self, valeurRacine, nom, modeMéthode='gui', commande=exécuterCommandeInterpréteurCommandes):
        self.valeurRacine = Path(valeurRacine).resolve()
        self.nom, self.modeMéthode, self.commande = nom, modeMéthode, commande
        self.préserverValeur = self.valeurRacine / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', nom) or nom in ('.', '..'):
            raise erreurExécution('VM 이름은 Caractères·valeurChiffre·공백·밑줄·괄호·마침표·하이픈만 사용할 nombre 있습니다.')
        if modeMéthode not in ('gui', 'headless'): raise erreurExécution('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def chemin(self, valeurPairRéseau):
        if Path(valeurPairRéseau).is_absolute() or '..' in Path(valeurPairRéseau).parts:
            raise erreurExécution('잘못된 관리 chemin: ' + str(valeurPairRéseau))
        résultat = self.préserverValeur
        for valeurSousPartie in ['.vbox'] + list(Path(valeurPairRéseau).parts):
            if valeurSousPartie == '.vbox': résultat = self.préserverValeur
            else: résultat = résultat / valeurSousPartie
            if résultat.is_symlink(): raise erreurExécution('connecter 경로는 사용하지 않습니다: ' + str(résultat))
        return résultat

    def lire(self):
        chemin = self.chemin('state.json')
        if not chemin.exists(): return None
        valeurÉtatValeur = json.loads(chemin.read_text(encoding='utf-8'))
        if valeurÉtatValeur.get('version') != 1 or valeurÉtatValeur.get('name') != self.nom:
            raise erreurExécution('관리 상태의 VM nom/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for nom in ('uuid', 'owner'):
            if str(uuid.UUID(valeurÉtatValeur[nom])) != valeurÉtatValeur[nom]: raise erreurExécution('잘못된 VM valeurIdentificateur')
        return valeurÉtatValeur

    def valeurStocker(self, valeurÉtatValeur):
        valeurDestination = self.chemin('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.préserverValeur), delete=False) as Fichier:
            json.dump(valeurÉtatValeur, Fichier, ensure_ascii=False, indent=2)
            Fichier.write('\n')
            valeurTemporaire = Fichier.name
        os.replace(valeurTemporaire, str(valeurDestination))

    def informationSystème(self, valeurÉtatValeur, valeurInscrit, récupérerÉtatValeur=False):
        if valeurÉtatValeur['uuid'] not in valeurInscrit:
            raise erreurExécution('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        informationSystème = valeurAttribut(self.commande(['VBoxManage', 'showvminfo', valeurÉtatValeur['uuid'], '--machinereadable']))
        position = Path(informationSystème.get('CfgFile', '')).resolve()
        if self.chemin('machines').resolve() not in position.parents or informationSystème.get('UUID') != valeurÉtatValeur['uuid']:
            raise erreurExécution('이 프로젝트의 VM réglages chemin/UUID와 일치하지 않아 변경하지 않습니다.')
        valeurMarqueur = self.commande(['VBoxManage', 'getextradata', valeurÉtatValeur['uuid'], 'JKOROS/Owner']).strip()
        if valeurMarqueur != 'Value: ' + valeurÉtatValeur['owner']:
            if récupérerÉtatValeur and valeurÉtatValeur.get('pending') and valeurMarqueur == 'No value set!':
                self.commande(['VBoxManage', 'setextradata', valeurÉtatValeur['uuid'], 'JKOROS/Owner', valeurÉtatValeur['owner']])
            else:
                raise erreurExécution('VM valeurPropriétaire 표식이 일치하지 않아 변경하지 않습니다.')
        return informationSystème

    def contrôlerSupports(self, valeurÉtatValeur, informationSystème):
        listeContrôleurs = [valeur for nom, valeur in informationSystème.items() if re.fullmatch(r'storagecontrollername\d+', nom)]
        autoriserValeur = [str(self.chemin(valeur)) for valeur in valeurÉtatValeur.get('media', [])]
        for nom, valeur in informationSystème.items():
            if any(re.fullmatch(re.escape(Contrôleur) + r'-\d+-\d+', nom) for Contrôleur in listeContrôleurs):
                if valeur not in ('none', 'emptydrive') and valeur not in autoriserValeur:
                    raise erreurExécution('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + valeur)

    def afficherÉtatValeur(self):
        valeurÉtatValeur = self.lire()
        if valeurÉtatValeur is None: return {'name': self.nom, 'state': 'not-created'}
        informationSystème = self.informationSystème(valeurÉtatValeur, entréesListeInscrit(self.commande(['VBoxManage', 'list', 'vms'])))
        return {'name': informationSystème.get('name', valeurÉtatValeur['name']), 'uuid': valeurÉtatValeur['uuid'], 'state': informationSystème.get('VMState'),
                'iso': str(self.chemin(valeurÉtatValeur['iso'])) if valeurÉtatValeur.get('iso') else None,
                'serial_log': str(self.chemin(valeurÉtatValeur['serial_log'])) if valeurÉtatValeur.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def exécuterCommande(self):
        valeurÉtatValeur = self.lire()
        valeurInscrit = entréesListeInscrit(self.commande(['VBoxManage', 'list', 'vms']))
        informationSystème = None
        if valeurÉtatValeur is not None and valeurÉtatValeur['uuid'] in valeurInscrit:
            informationSystème = self.informationSystème(valeurÉtatValeur, valeurInscrit, récupérerÉtatValeur=True)
            élémentListeActuel = informationSystème.get('VMState')
            if élémentListeActuel == 'running':
                print('이미 exécuterCommande 중입니다. 재빌드·재시작하지 않습니다.')
                return self.afficherÉtatValeur()
            self.contrôlerSupports(valeurÉtatValeur, informationSystème)
            if élémentListeActuel in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 valeurStocker 상태를 버리지 않습니다.'.format(élémentListeActuel))
                if élémentListeActuel == 'paused':
                    self.commande(['VBoxManage', 'controlvm', valeurÉtatValeur['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 valeurRéessayer ouvrir 전에 기존 기록도 보관한다.
                    if valeurÉtatValeur.get('serial_log'):
                        original = self.chemin(valeurÉtatValeur['serial_log'])
                        if original.is_file():
                            shutil.copyfile(str(original), str(self.chemin('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.commande(['VBoxManage', 'startvm', valeurÉtatValeur['uuid'], '--type', self.modeMéthode])
                return self.afficherÉtatValeur()
            if élémentListeActuel not in ('poweroff', 'aborted'):
                raise erreurExécution('VM이 modeCommuter 중입니다 ({}). 작업이 끝난 valeurRetourArrièreCôté valeurRéessayer 실행하세요.'.format(élémentListeActuel))
        elif valeurÉtatValeur is not None and not valeurÉtatValeur.get('pending'):
            raise erreurExécution('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 valeurRéessayer 등록하세요.')
        elif self.nom in valeurInscrit.values():
            raise erreurExécution('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # valeurStocker/exécuterCommande 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.commande(['make', '-C', str(self.valeurRacine / 'os'), 'iso']), end='')
        original = self.valeurRacine / 'os/build/kernel.iso'
        if not original.is_file() or original.stat().st_size == 0: raise erreurExécution('Amorçage ISO가 생성되지 않았습니다.')
        valeurSupports = 'media/kernel-' + sommeContrôle(original) + '.iso'
        valeurDestination = self.chemin(valeurSupports)
        valeurDestination.parent.mkdir(exist_ok=True)
        if valeurDestination.exists():
            if sommeContrôle(valeurDestination) != sommeContrôle(original): raise erreurExécution('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(valeurDestination))
        else:
            with tempfile.NamedTemporaryFile(dir=str(valeurDestination.parent)) as Fichier:
                shutil.copyfile(str(original), Fichier.name)
                os.link(Fichier.name, str(valeurDestination))

        if valeurÉtatValeur is None:
            valeurÉtatValeur = {'version': 1, 'name': self.nom, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.valeurStocker(valeurÉtatValeur)
        if informationSystème is None:
            self.commande(['VBoxManage', 'createvm', '--name', valeurÉtatValeur['name'], '--uuid', valeurÉtatValeur['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.chemin('machines')), '--register'])
            self.commande(['VBoxManage', 'setextradata', valeurÉtatValeur['uuid'], 'JKOROS/Owner', valeurÉtatValeur['owner']])
        # construireSystème 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        informationSystème = self.informationSystème(valeurÉtatValeur, entréesListeInscrit(self.commande(['VBoxManage', 'list', 'vms'])))
        if informationSystème.get('VMState') not in ('poweroff', 'aborted'):
            raise erreurExécution('construireSystème 중 VM 상태가 바뀌었습니다. valeurRéessayer make vbox를 실행하세요.')
        self.contrôlerSupports(valeurÉtatValeur, informationSystème)
        valeurÉtatValeur['iso'] = valeurSupports
        if valeurSupports not in valeurÉtatValeur['media']: valeurÉtatValeur['media'].append(valeurSupports)
        valeurÉtatValeur['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        valeurJournal = self.chemin(valeurÉtatValeur['serial_log'])
        valeurJournal.parent.mkdir(exist_ok=True)
        self.valeurStocker(valeurÉtatValeur)
        self.commande(['VBoxManage', 'modifyvm', valeurÉtatValeur['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(valeurJournal)])
        listeContrôleurs = [valeur for nom, valeur in informationSystème.items() if re.fullmatch(r'storagecontrollername\d+', nom)]
        if 'JKOROS IDE' not in listeContrôleurs:
            self.commande(['VBoxManage', 'storagectl', valeurÉtatValeur['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.commande(['VBoxManage', 'storageattach', valeurÉtatValeur['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(valeurDestination)])
        valeurÉtatValeur['pending'] = False
        self.valeurStocker(valeurÉtatValeur)
        self.commande(['VBoxManage', 'startvm', valeurÉtatValeur['uuid'], '--type', self.modeMéthode])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.afficherÉtatValeur()


def lancer():
    analyserValeur = argparse.ArgumentParser(description='jkoros 전용 VirtualBox exécuterCommande 및 valeurÉtatValeur valeurInterroger')
    analyserValeur.add_argument('action', choices=['run', 'status'])
    argumentParamètre = analyserValeur.parse_args()
    exécuterCommande = LanceurProgramme(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if argumentParamètre.action == 'status':
        print(json.dumps(exécuterCommande.afficherÉtatValeur(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise erreurExécution('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise erreurExécution('/dev/vboxdrv에 접근할 nombre 없습니다. Hôte 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/valeurPermission 변경은 하지 않습니다.')
    os.umask(0o077)
    exécuterCommande.chemin('lock').parent.mkdir(parents=True, exist_ok=True)
    with exécuterCommande.chemin('lock').open('a') as valeurVerrou:
        try: fcntl.flock(valeurVerrou, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise erreurExécution('다른 jkoros VirtualBox exécuterCommande 작업이 진행 중입니다.')
        print(json.dumps(exécuterCommande.exécuterCommande(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: lancer()
    except (erreurExécution, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as erreur:
        print('VBOX erreur: ' + str(erreur), file=sys.stderr)
        sys.exit(1)
