#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from test_Usenet import VM

posizione = Path(__file__).resolve().parents[1]
specifica = importlib.util.spec_from_file_location('supporti_strumento', posizione / 'strumenti/Crea_Memoria_supporti.py')
supporti_strumento = importlib.util.module_from_spec(specifica)
specifica.loader.exec_module(supporti_strumento)

def Modifica_VALORE(computer, Contenuto_VALORE):
    avvia = len(computer.LOG_riga)
    computer.seriale_VALORE.sendall(('edit note.txt\n' + Contenuto_VALORE + '\n.save\n').encode())
    return computer.stato_di_attesa('jkoros> ', avvia)

def Esegui_comando():
    risultato = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        supporti_VALORE = Path(임시) / 'files.img'
        supporti_strumento.Crea_voce(supporti_VALORE)
        computer = VM(posizione / 'build/kernel.elf', Memoria_Medio=supporti_VALORE)
        try:
            computer.comando('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Modifica_VALORE(computer, 'generation-one')
            computer.comando('sync', ['Sync: 0'])
            Modifica_VALORE(computer, 'generation-two')
            computer.comando('sync', ['Sync: 0'])
            Modifica_VALORE(computer, 'unsynced-three')
            risultato['save'] = computer.LOG_riga.decode('utf-8', 'replace')
        finally:
            computer.Chiudi()
        computer = VM(posizione / 'build/kernel.iso', 'iso', Memoria_Medio=supporti_VALORE)
        try:
            uscitaTesto = computer.comando('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in uscitaTesto
            computer.comando('cat stored.txt', ['saved-from-C'])
            risultato['restore'] = computer.LOG_riga.decode('utf-8', 'replace')
        finally:
            computer.Chiudi()
        dati = bytearray(supporti_VALORE.read_bytes())
        세대들 = [struct.unpack_from('<I', dati, (1 + INDICE * 259) * 512 + 4)[0] for INDICE in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        dati[(1 + 최신 * 259 + 3) * 512] ^= 1
        supporti_VALORE.write_bytes(dati)
        computer = VM(posizione / 'build/kernel.elf', Memoria_Medio=supporti_VALORE)
        try:
            computer.comando('cat note.txt', ['generation-one'])
            computer.comando('cat stored.txt', ['saved-from-C'])
            risultato['checksum_fallback'] = computer.LOG_riga.decode('utf-8', 'replace')
        finally:
            computer.Chiudi()
        Altro_supporti = Path(임시) / 'foreign.img'
        Altro_supporti.write_bytes(bytes([0x5a]) * (2048 * 512))
        Indietro_articolo = hashlib.sha256(Altro_supporti.read_bytes()).hexdigest()
        computer = VM(posizione / 'build/kernel.elf', Memoria_Medio=Altro_supporti)
        try:
            computer.comando('sync', ['Sync: -19'])
        finally:
            computer.Chiudi()
        assert hashlib.sha256(Altro_supporti.read_bytes()).hexdigest() == Indietro_articolo
        risultato['foreign_disk_unchanged'] = True
    (posizione / 'build/보존시험.json').write_text(json.dumps(risultato, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALORE/ISO 재부팅/checksum recuperare_Stato/다른 supporti_VALORE 비변경', flush=True)

if __name__ == '__main__':
    Esegui_comando()
