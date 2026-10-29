#!/usr/bin/env python3
"""donnéesEffectif ring 3 ELF/Hôte UDP 왕복/protégerValeur erreur/valeurTemps valeurLimite/잘못된 ELF를 검증한다."""
import json
import hashlib
from pathlib import Path
import select
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time

position = Path(__file__).resolve().parents[1]


class MachineVirtuelle:
    def __init__(self, chemin, valeurGenre='elf', valeurRéseau=True, moyenStockage=None):
        self.valeurTemporaire = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        valeurRépertoire = Path(self.valeurTemporaire.name)
        self.enregistrementJournal = bytearray()
        self.valeurSériel = socket.socket(socket.AF_UNIX)
        self.valeurMoniteur = socket.socket(socket.AF_UNIX)
        cheminSériel, cheminMoniteur = valeurRépertoire / 'serial.sock', valeurRépertoire / 'monitor.sock'
        commande = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(cheminSériel) + ',server,nowait',
                '-monitor', 'unix:' + str(cheminMoniteur) + ',server,nowait']
        commande += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if valeurRéseau else ['-net', 'none']
        commande += ['-kernel', str(chemin)] if valeurGenre == 'elf' else ['-cdrom', str(chemin), '-boot', 'd']
        if moyenStockage is not None:
            commande += ['-drive', 'file=' + str(moyenStockage) + ',format=raw,if=ide,index=0']
        self.valeurProcessus = subprocess.Popen(commande, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            terminaison = time.monotonic() + 10
            while not (cheminSériel.exists() and cheminMoniteur.exists()):
                if self.valeurProcessus.poll() is not None:
                    raise AssertionError(self.valeurProcessus.stderr.read().decode())
                if time.monotonic() > terminaison: raise AssertionError('QEMU lancer valeurTemps 초과')
                time.sleep(0.03)
            self.valeurSériel.connect(str(cheminSériel))
            self.valeurMoniteur.connect(str(cheminMoniteur))
            self.valeurSériel.setblocking(False)
            self.valeurMoniteur.sendall(b'cont\n')
            self.attendreÉtatValeur('jkoros> ')
        except BaseException:
            self.fermer()
            raise

    def attendreÉtatValeur(self, valeurExpressionPhrase, lancer=0, valeurLimite=15):
        terminaison = time.monotonic() + valeurLimite
        while time.monotonic() < terminaison:
            if valeurExpressionPhrase.encode() in self.enregistrementJournal[lancer:]:
                return self.enregistrementJournal[lancer:].decode('utf-8', 'replace')
            lire, _, _ = select.select([self.valeurSériel], [], [], 0.1)
            if lire:
                Données = self.valeurSériel.recv(65536)
                if not Données: break
                self.enregistrementJournal.extend(Données)
            if self.valeurProcessus.poll() is not None: break
        raise AssertionError('attendreValeur valeurÉchec: ' + valeurExpressionPhrase + '\n' + self.enregistrementJournal.decode('utf-8', 'replace'))

    def commande(self, Chaîne, attente):
        lancer = len(self.enregistrementJournal)
        self.valeurSériel.sendall((Chaîne + '\n').encode())
        résultat = self.attendreÉtatValeur('jkoros> ', lancer)
        for valeurExpressionPhrase in attente:
            assert valeurExpressionPhrase in résultat, (Chaîne, valeurExpressionPhrase, résultat)
        assert 'PANIC' not in résultat, résultat
        return résultat

    def fermer(self):
        self.valeurSériel.close()
        self.valeurMoniteur.close()
        if self.valeurProcessus.poll() is None:
            self.valeurProcessus.terminate()
            try: self.valeurProcessus.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.valeurProcessus.kill()
                self.valeurProcessus.wait()
        self.valeurProcessus.communicate()
        self.valeurTemporaire.cleanup()


def noyauProtégé(valeurRépertoire):
    listeCasListe = {
        'badmem': 'movl $7, 0x00100000',
        'badport': 'movw $0x3f8, %dx\noutb %al, %dx',
        'spin': '1: jmp 1b',
        'badptr': 'movl $1,%eax\nmovl $0x00100000,%ebx\nint $0x80\ncmpl $-14,%eax\njne fail\n'
                  'movl $999,%eax\nint $0x80\ncmpl $-38,%eax\njne fail\n'
                  'xorl %ebx,%ebx\nxorl %eax,%eax\nint $0x80\nfail: movl $1,%ebx\nxorl %eax,%eax\nint $0x80',
        'fault': 'ud2',
        'badfile': '''
            movl $20,%eax
            movl $0x00100000,%ebx
            movl $empty,%ecx
            int $0x80
            cmpl $-14,%eax
            jne fail
            movl $20,%eax
            movl $name,%ebx
            movl $0x00100000,%ecx
            int $0x80
            cmpl $-14,%eax
            jne fail
            movl $21,%eax
            movl $name,%ebx
            movl $negative,%ecx
            xorl %edx,%edx
            int $0x80
            cmpl $-14,%eax
            jne fail
            movl $21,%eax
            movl $name,%ebx
            movl $empty,%ecx
            movl $1,%edx
            int $0x80
            cmpl $-22,%eax
            jne fail
            movl $20,%eax
            movl $empty,%ebx
            movl $empty,%ecx
            int $0x80
            cmpl $-22,%eax
            jne fail
            xorl %eax,%eax
            xorl %ebx,%ebx
            int $0x80
        fail:
            xorl %eax,%eax
            movl $1,%ebx
            int $0x80
        .balign 4
        name: .long 1,88
        empty: .long 0
        negative: .long -1
        ''',
    }
    listeEntréesListe = ['hello=' + str(position / 'build/apps/hello.elf')]
    for nom, valeurContenuValeur in listeCasListe.items():
        source = valeurRépertoire / (nom + '.s')
        source.write_text('.code32\n.text\n.globl _start\n_start:\n' + valeurContenuValeur +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(valeurRépertoire / (nom + '.o')), str(source)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(position.parent / 'compiler/dispositionLierUtilisateur.ld'),
                        '-o', str(valeurRépertoire / (nom + '.elf')), str(valeurRépertoire / (nom + '.o'))], check=True)
        listeEntréesListe.append(nom + '=' + str(valeurRépertoire / (nom + '.elf')))
    estNormal = bytearray((position / 'build/apps/hello.elf').read_bytes())
    listeVariantes = {}
    résultatInvalide = bytearray(estNormal); résultatInvalide[0] = 0; listeVariantes['badelf'] = résultatInvalide
    résultatInvalide = bytearray(estNormal); struct.pack_into('<I', résultatInvalide, 24, 0x00100000); listeVariantes['badentry'] = résultatInvalide
    résultatInvalide = bytearray(estNormal); struct.pack_into('<I', résultatInvalide, 28, 0x7fffffff); listeVariantes['badtable'] = résultatInvalide
    résultatInvalide = bytearray(estNormal); Table = struct.unpack_from('<I', résultatInvalide, 28)[0]
    struct.pack_into('<I', résultatInvalide, Table + 20, 0x7fffffff); listeVariantes['badsize'] = résultatInvalide
    for nom, Données in listeVariantes.items():
        Fichier = valeurRépertoire / (nom + '.elf'); Fichier.write_bytes(Données)
        listeEntréesListe.append(nom + '=' + str(Fichier))
    subprocess.run([sys.executable, str(position / 'Outils/EmballerExécutables.py'), '-o', str(valeurRépertoire / 'apps.bin')] + listeEntréesListe, check=True)
    source = valeurRépertoire / 'apps.s'
    source.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(valeurRépertoire / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(valeurRépertoire / 'apps.o'), str(source)], check=True)
    valeurNoyau = valeurRépertoire / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(position / 'Amorçage/DispositionLiens.ld'), '-o', str(valeurNoyau),
                    str(position / 'build/boot.o'), str(position / 'build/java.o'), str(position / 'build/user.o'), str(valeurRépertoire / 'apps.o')], check=True)
    return valeurNoyau


def exécuterCommande():
    résultat = {}
    valeurServeur = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    valeurServeur.bind(('127.0.0.1', 0))
    valeurServeur.settimeout(0.1)
    valeurPort = valeurServeur.getsockname()[1]
    élémentListeReçu = []
    programmeQuitter = threading.Event()
    def réponseRépercuter():
        while not programmeQuitter.is_set():
            try: Données, valeurPairRéseau = valeurServeur.recvfrom(4096)
            except socket.timeout: continue
            élémentListeReçu.append(Données)
            if Données != b'drop-me': valeurServeur.sendto(Données, valeurPairRéseau)
    valeurTâcheFond = threading.Thread(target=réponseRépercuter, daemon=True)
    valeurTâcheFond.start()
    try:
        for valeurGenre in ('elf', 'iso'):
            machine = MachineVirtuelle(position / ('build/kernel.elf' if valeurGenre == 'elf' else 'build/kernel.iso'), valeurGenre)
            try:
                machine.commande('apps', ['hello', 'udp', 'netcheck', 'stress'])
                machine.commande('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                machine.commande('run missing', ['Exit: -2'])
                machine.commande('net', ['NET RTL8139'])
                machine.commande('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for valeurContenuValeur in ('hello-network', 'odd', 'even', 'repeat-123'):
                    machine.commande('run udp 10.0.2.2 {} {}'.format(valeurPort, valeurContenuValeur), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert valeurContenuValeur.encode() in élémentListeReçu, 'Hôte 서버에서 자료를 받지 못함'
                machine.commande('run stress {}'.format(valeurPort), ['UDP STRESS PASS', 'Exit: 0'])
                machine.commande('run udp 10.0.2.2 {} drop-me'.format(valeurPort), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                machine.commande('run hello recovered', ['arg: recovered', 'Exit: 0'])
                résultat[valeurGenre] = machine.enregistrementJournal.decode('utf-8', 'replace')
                print('PASS: {} Utilisateur ELF/ring 3/arguments/UDP Hôte 왕복/valeurTemps 초과/interpréteurCommandes 복귀'.format(valeurGenre), flush=True)
            finally:
                try: machine.commande('net', [])
                except Exception: pass
                (position / 'build/사용자통신-last.log').write_bytes(machine.enregistrementJournal)
                machine.fermer()
        machine = MachineVirtuelle(position / 'build/kernel.elf', valeurRéseau=False)
        try:
            machine.commande('net', ['NET unavailable'])
            machine.commande('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            machine.commande('run hello', ['USER MODE ring 3', 'Exit: 0'])
            résultat['no_nic'] = machine.enregistrementJournal.decode()
        finally: machine.fermer()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as valeurTemporaire:
            machine = MachineVirtuelle(noyauProtégé(Path(valeurTemporaire)), valeurRéseau=False)
            try:
                for nom, valeurÉtatValeur in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    machine.commande('run ' + nom, ['Exit: ' + str(valeurÉtatValeur)])
                    machine.commande('run hello', ['USER MODE ring 3', 'Exit: 0'])
                résultat['protection'] = machine.enregistrementJournal.decode()
                print('PASS: Utilisateur donnéesMémoire/portMatériel 격리, 잘못된 pointeur/ELF, CPU exception, 무한 valeurItération valeurLimite', flush=True)
            finally:
                (position / 'build/TestProtection-last.log').write_bytes(machine.enregistrementJournal)
                machine.fermer()
    finally:
        programmeQuitter.set()
        valeurTâcheFond.join(timeout=2)
        valeurServeur.close()
    résultat['host_udp_received'] = [{'length': len(Données), 'sha256': hashlib.sha256(Données).hexdigest()} for Données in élémentListeReçu]
    (position / 'build/testRéseauUtilisateur.json').write_text(json.dumps(résultat, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    exécuterCommande()
