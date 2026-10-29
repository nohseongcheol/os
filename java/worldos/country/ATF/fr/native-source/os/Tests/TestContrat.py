#!/usr/bin/env python3
"""Hôte libc 없이 연결한 français C 프로그램을 donnéesEffectif ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from testRéseauUtilisateur import MachineVirtuelle

position = Path(__file__).resolve().parents[1]

def exécuterCommande():
    résultat = {}
    valeurServeur = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    valeurServeur.bind(('127.0.0.1', 0))
    valeurServeur.settimeout(0.1)
    numéroPort = valeurServeur.getsockname()[1]
    donnéesReçu = []
    étatValeurTerminaisonÉtat = threading.Event()
    def réponseRépercuter():
        while not étatValeurTerminaisonÉtat.is_set():
            try:
                Données, adresse = valeurServeur.recvfrom(4096)
            except socket.timeout:
                continue
            donnéesReçu.append(Données)
            valeurServeur.sendto(Données, adresse)
    valeurTâcheFond = threading.Thread(target=réponseRépercuter, daemon=True)
    valeurTâcheFond.start()
    try:
        for valeurGenre in ('elf', 'iso'):
            machine = MachineVirtuelle(position / ('build/kernel.' + valeurGenre), valeurGenre)
            try:
                for valeurItération in range(2):
                    machine.commande('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    machine.commande('run posixudp ' + str(numéroPort), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                lancer = len(machine.enregistrementJournal)
                machine.valeurSériel.sendall(b'run posixinput\n')
                machine.attendreÉtatValeur('POSIX INPUT READY', lancer)
                machine.valeurSériel.sendall(b'abcdef')
                Sortie = machine.attendreÉtatValeur('jkoros> ', lancer)
                assert 'POSIX INPUT PASS' in Sortie and 'Exit: 0' in Sortie, Sortie
                machine.commande('javac Hello.java', ['Exit: 0'])
                machine.commande('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                machine.commande('run hello recovered', ['arg: recovered', 'Exit: 0'])
                résultat[valeurGenre] = machine.enregistrementJournal.decode('utf-8', 'replace')
                print('PASS:', valeurGenre, 'POSIX Fichier/공유 position/삭제 수명/adresse protégerValeur/UDP/표준 valeurEntrée/기존 Java', flush=True)
            finally:
                machine.fermer()
        assert b'posix-udp' in donnéesReçu and b'truncate' in donnéesReçu and b'' in donnéesReçu
    finally:
        étatValeurTerminaisonÉtat.set(); valeurTâcheFond.join(timeout=2); valeurServeur.close()
    résultat['host_datagrams'] = [Données.decode() for Données in donnéesReçu]
    (position / 'build/TestContrat.json').write_text(json.dumps(résultat, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    exécuterCommande()
