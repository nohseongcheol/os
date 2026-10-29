#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 copiarPreservado 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from pruebaRedUsuario import MáquinaVirtual

posición = Path(__file__).resolve().parents[1]
especificación = importlib.util.spec_from_file_location('herramientaMedios', posición / 'Herramientas/CrearMedioAlmacenamiento.py')
herramientaMedios = importlib.util.module_from_spec(especificación)
especificación.loader.exec_module(herramientaMedios)

def valorEditar(máquina, valorContenidoValor):
    ponerEnMarcha = len(máquina.registroEntradaDiario)
    máquina.valorSerie.sendall(('edit note.txt\n' + valorContenidoValor + '\n.save\n').encode())
    return máquina.esperarEstadoValor('jkoros> ', ponerEnMarcha)

def ejecutarComando():
    resultado = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as valorTemporal:
        valorMedios = Path(valorTemporal) / 'files.img'
        herramientaMedios.crearEntradaElemento(valorMedios)
        máquina = MáquinaVirtual(posición / 'build/kernel.elf', medianoAlmacenamiento=valorMedios)
        try:
            máquina.comando('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            valorEditar(máquina, 'generation-one')
            máquina.comando('sync', ['Sync: 0'])
            valorEditar(máquina, 'generation-two')
            máquina.comando('sync', ['Sync: 0'])
            valorEditar(máquina, 'unsynced-three')
            resultado['save'] = máquina.registroEntradaDiario.decode('utf-8', 'replace')
        finally:
            máquina.cerrar()
        máquina = MáquinaVirtual(posición / 'build/kernel.iso', 'iso', medianoAlmacenamiento=valorMedios)
        try:
            Salida = máquina.comando('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Salida
            máquina.comando('cat stored.txt', ['saved-from-C'])
            resultado['restore'] = máquina.registroEntradaDiario.decode('utf-8', 'replace')
        finally:
            máquina.cerrar()
        Datos = bytearray(valorMedios.read_bytes())
        listaGeneraciones = [struct.unpack_from('<I', Datos, (1 + número * 259) * 512 + 4)[0] for número in (0, 1)]
        valorÚltimoReciente = 0 if listaGeneraciones[0] > listaGeneraciones[1] else 1
        Datos[(1 + valorÚltimoReciente * 259 + 3) * 512] ^= 1
        valorMedios.write_bytes(Datos)
        máquina = MáquinaVirtual(posición / 'build/kernel.elf', medianoAlmacenamiento=valorMedios)
        try:
            máquina.comando('cat note.txt', ['generation-one'])
            máquina.comando('cat stored.txt', ['saved-from-C'])
            resultado['checksum_fallback'] = máquina.registroEntradaDiario.decode('utf-8', 'replace')
        finally:
            máquina.cerrar()
        mediosOtro = Path(valorTemporal) / 'foreign.img'
        mediosOtro.write_bytes(bytes([0x5a]) * (2048 * 512))
        elementoListaElementoPrevio = hashlib.sha256(mediosOtro.read_bytes()).hexdigest()
        máquina = MáquinaVirtual(posición / 'build/kernel.elf', medianoAlmacenamiento=mediosOtro)
        try:
            máquina.comando('sync', ['Sync: -19'])
        finally:
            máquina.cerrar()
        assert hashlib.sha256(mediosOtro.read_bytes()).hexdigest() == elementoListaElementoPrevio
        resultado['foreign_disk_unchanged'] = True
    (posición / 'build/PruebaPersistencia.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE valorAlmacenar/ISO 재부팅/sumaComprobación recuperarEstadoValor/다른 valorMedios 비변경', flush=True)

if __name__ == '__main__':
    ejecutarComando()
