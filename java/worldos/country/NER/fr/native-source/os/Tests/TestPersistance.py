#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 copierPréservé 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from testRéseauUtilisateur import MachineVirtuelle

position = Path(__file__).resolve().parents[1]
spécification = importlib.util.spec_from_file_location('outilSupports', position / 'Outils/CréerSupportStockage.py')
outilSupports = importlib.util.module_from_spec(spécification)
spécification.loader.exec_module(outilSupports)

def valeurÉditer(machine, valeurContenuValeur):
    lancer = len(machine.enregistrementJournal)
    machine.valeurSériel.sendall(('edit note.txt\n' + valeurContenuValeur + '\n.save\n').encode())
    return machine.attendreÉtatValeur('jkoros> ', lancer)

def exécuterCommande():
    résultat = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as valeurTemporaire:
        valeurSupports = Path(valeurTemporaire) / 'files.img'
        outilSupports.créerEntréeÉlément(valeurSupports)
        machine = MachineVirtuelle(position / 'build/kernel.elf', moyenStockage=valeurSupports)
        try:
            machine.commande('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            valeurÉditer(machine, 'generation-one')
            machine.commande('sync', ['Sync: 0'])
            valeurÉditer(machine, 'generation-two')
            machine.commande('sync', ['Sync: 0'])
            valeurÉditer(machine, 'unsynced-three')
            résultat['save'] = machine.enregistrementJournal.decode('utf-8', 'replace')
        finally:
            machine.fermer()
        machine = MachineVirtuelle(position / 'build/kernel.iso', 'iso', moyenStockage=valeurSupports)
        try:
            Sortie = machine.commande('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Sortie
            machine.commande('cat stored.txt', ['saved-from-C'])
            résultat['restore'] = machine.enregistrementJournal.decode('utf-8', 'replace')
        finally:
            machine.fermer()
        Données = bytearray(valeurSupports.read_bytes())
        listeGénérations = [struct.unpack_from('<I', Données, (1 + numéro * 259) * 512 + 4)[0] for numéro in (0, 1)]
        valeurDernierRécent = 0 if listeGénérations[0] > listeGénérations[1] else 1
        Données[(1 + valeurDernierRécent * 259 + 3) * 512] ^= 1
        valeurSupports.write_bytes(Données)
        machine = MachineVirtuelle(position / 'build/kernel.elf', moyenStockage=valeurSupports)
        try:
            machine.commande('cat note.txt', ['generation-one'])
            machine.commande('cat stored.txt', ['saved-from-C'])
            résultat['checksum_fallback'] = machine.enregistrementJournal.decode('utf-8', 'replace')
        finally:
            machine.fermer()
        supportsAutre = Path(valeurTemporaire) / 'foreign.img'
        supportsAutre.write_bytes(bytes([0x5a]) * (2048 * 512))
        élémentListePrécédentÉlément = hashlib.sha256(supportsAutre.read_bytes()).hexdigest()
        machine = MachineVirtuelle(position / 'build/kernel.elf', moyenStockage=supportsAutre)
        try:
            machine.commande('sync', ['Sync: -19'])
        finally:
            machine.fermer()
        assert hashlib.sha256(supportsAutre.read_bytes()).hexdigest() == élémentListePrécédentÉlément
        résultat['foreign_disk_unchanged'] = True
    (position / 'build/TestPersistance.json').write_text(json.dumps(résultat, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE valeurStocker/ISO 재부팅/sommeContrôle récupérerÉtatValeur/다른 valeurSupports 비변경', flush=True)

if __name__ == '__main__':
    exécuterCommande()
