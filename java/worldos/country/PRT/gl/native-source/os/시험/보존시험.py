#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from 사용자통신시험 import máquina_virtual

Posición = Path(__file__).resolve().parents[1]
명세 = importlib.util.spec_from_file_location('soporte_ferramenta', Posición / 'Ferramentas/crear_soporte.py')
soporte_ferramenta = importlib.util.module_from_spec(명세)
명세.loader.exec_module(soporte_ferramenta)

def editar_VALOR(máquina, Contido_VALOR):
    Executar_2 = len(máquina.LOG_fila)
    máquina.직렬.sendall(('edit note.txt\n' + Contido_VALOR + '\n.save\n').encode())
    return máquina.agarda_Estado('jkoros> ', Executar_2)

def executar_comando():
    RESULTANTE = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        soporte_VALOR_e2cae547 = Path(임시) / 'files.img'
        soporte_ferramenta.crear_introdución(soporte_VALOR_e2cae547)
        máquina = máquina_virtual(Posición / 'build/kernel.elf', 저장매체=soporte_VALOR_e2cae547)
        try:
            máquina.Orde('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            editar_VALOR(máquina, 'generation-one')
            máquina.Orde('sync', ['Sync: 0'])
            editar_VALOR(máquina, 'generation-two')
            máquina.Orde('sync', ['Sync: 0'])
            editar_VALOR(máquina, 'unsynced-three')
            RESULTANTE['save'] = máquina.LOG_fila.decode('utf-8', 'replace')
        finally:
            máquina.Pechar()
        máquina = máquina_virtual(Posición / 'build/kernel.iso', 'iso', 저장매체=soporte_VALOR_e2cae547)
        try:
            Saída = máquina.Orde('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Saída
            máquina.Orde('cat stored.txt', ['saved-from-C'])
            RESULTANTE['restore'] = máquina.LOG_fila.decode('utf-8', 'replace')
        finally:
            máquina.Pechar()
        datos = bytearray(soporte_VALOR_e2cae547.read_bytes())
        세대들 = [struct.unpack_from('<I', datos, (1 + ÍNDICE * 259) * 512 + 4)[0] for ÍNDICE in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        datos[(1 + 최신 * 259 + 3) * 512] ^= 1
        soporte_VALOR_e2cae547.write_bytes(datos)
        máquina = máquina_virtual(Posición / 'build/kernel.elf', 저장매체=soporte_VALOR_e2cae547)
        try:
            máquina.Orde('cat note.txt', ['generation-one'])
            máquina.Orde('cat stored.txt', ['saved-from-C'])
            RESULTANTE['checksum_fallback'] = máquina.LOG_fila.decode('utf-8', 'replace')
        finally:
            máquina.Pechar()
        다른매체 = Path(임시) / 'foreign.img'
        다른매체.write_bytes(bytes([0x5a]) * (2048 * 512))
        이전 = hashlib.sha256(다른매체.read_bytes()).hexdigest()
        máquina = máquina_virtual(Posición / 'build/kernel.elf', 저장매체=다른매체)
        try:
            máquina.Orde('sync', ['Sync: -19'])
        finally:
            máquina.Pechar()
        assert hashlib.sha256(다른매체.read_bytes()).hexdigest() == 이전
        RESULTANTE['foreign_disk_unchanged'] = True
    (Posición / 'build/보존시험.json').write_text(json.dumps(RESULTANTE, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALOR/ISO 재부팅/suma_de_comprobación recuperar_Estado/다른 soporte_VALOR_e2cae547 비변경', flush=True)

if __name__ == '__main__':
    executar_comando()
