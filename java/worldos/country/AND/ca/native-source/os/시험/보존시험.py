#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import màquina_virtual

Posició = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('suport_físic_eina', Posició / 'Eines/Crear_Emmagatzematge_suport_físic.py')
suport_físic_eina = importlib.util.module_from_spec(명세)
명세.loader.exec_module(suport_físic_eina)

def Editar_VALOR(màquina, contingut_VALOR):
    Executa_2 = len(màquina.LOG_fila)
    màquina.직렬.sendall(('edit note.txt\n' + contingut_VALOR + '\n.save\n').encode())
    return màquina.Espera_Estat('jkoros> ', Executa_2)

def Executa_ordre():
    RESULTAT = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        suport_físic_VALOR = Path(임시) / 'files.img'
        suport_físic_eina.Crear_introducció(suport_físic_VALOR)
        màquina = màquina_virtual(Posició / 'build/kernel.elf', 저장매체=suport_físic_VALOR)
        try:
            màquina.Ordre('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Editar_VALOR(màquina, 'generation-one')
            màquina.Ordre('sync', ['Sync: 0'])
            Editar_VALOR(màquina, 'generation-two')
            màquina.Ordre('sync', ['Sync: 0'])
            Editar_VALOR(màquina, 'unsynced-three')
            RESULTAT['save'] = màquina.LOG_fila.decode('utf-8', 'replace')
        finally:
            màquina.Tanca()
        màquina = màquina_virtual(Posició / 'build/kernel.iso', 'iso', 저장매체=suport_físic_VALOR)
        try:
            Sortida = màquina.Ordre('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Sortida
            màquina.Ordre('cat stored.txt', ['saved-from-C'])
            RESULTAT['restore'] = màquina.LOG_fila.decode('utf-8', 'replace')
        finally:
            màquina.Tanca()
        dades = bytearray(suport_físic_VALOR.read_bytes())
        세대들 = [struct.unpack_from('<I', dades, (1 + INDEX * 259) * 512 + 4)[0] for INDEX in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        dades[(1 + 최신 * 259 + 3) * 512] ^= 1
        suport_físic_VALOR.write_bytes(dades)
        màquina = màquina_virtual(Posició / 'build/kernel.elf', 저장매체=suport_físic_VALOR)
        try:
            màquina.Ordre('cat note.txt', ['generation-one'])
            màquina.Ordre('cat stored.txt', ['saved-from-C'])
            RESULTAT['checksum_fallback'] = màquina.LOG_fila.decode('utf-8', 'replace')
        finally:
            màquina.Tanca()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        màquina = màquina_virtual(Posició / 'build/kernel.elf', 저장매체=다른매체)
        try:
            màquina.Ordre('sync', ['Sync: -19'])
        finally:
            màquina.Tanca()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        RESULTAT['foreign_disk_unchanged'] = True
    (Posició / 'build/보존시험.json').write_text(json.dumps(RESULTAT, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALOR/ISO 재부팅/suma_de_comprovació recuperar_Estat/다른 suport_físic_VALOR 비변경', flush=True)

if __name__ == '__main__':
    Executa_ordre()
