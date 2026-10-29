#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 보존본 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from teste_Usenet import VM

posição = Path(__file__).resolve().parents[1]
especificação = importlib.util.spec_from_file_location('Mídia_ferramenta', posição / 'ferramentas/Criar_Armazenamento_Mídia.py')
Mídia_ferramenta = importlib.util.module_from_spec(especificação)
especificação.loader.exec_module(Mídia_ferramenta)

def Editar_VALOR(computador, Conteúdo_VALOR):
    iniciar = len(computador.LOG_linha)
    computador.직렬.sendall(('edit note.txt\n' + Conteúdo_VALOR + '\n.save\n').encode())
    return computador.estado_de_espera('jkoros> ', iniciar)

def Executar_comando():
    resultado = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as 임시:
        Mídia_VALOR = Path(임시) / 'files.img'
        Mídia_ferramenta.Criar_entrada(Mídia_VALOR)
        computador = VM(posição / 'build/kernel.elf', Armazenamento_meio=Mídia_VALOR)
        try:
            computador.comando('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            Editar_VALOR(computador, 'generation-one')
            computador.comando('sync', ['Sync: 0'])
            Editar_VALOR(computador, 'generation-two')
            computador.comando('sync', ['Sync: 0'])
            Editar_VALOR(computador, 'unsynced-three')
            resultado['save'] = computador.LOG_linha.decode('utf-8', 'replace')
        finally:
            computador.Fechar()
        computador = VM(posição / 'build/kernel.iso', 'iso', Armazenamento_meio=Mídia_VALOR)
        try:
            saídaTexto = computador.comando('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in saídaTexto
            computador.comando('cat stored.txt', ['saved-from-C'])
            resultado['restore'] = computador.LOG_linha.decode('utf-8', 'replace')
        finally:
            computador.Fechar()
        dados = bytearray(Mídia_VALOR.read_bytes())
        세대들 = [struct.unpack_from('<I', dados, (1 + ÍNDICE * 259) * 512 + 4)[0] for ÍNDICE in (0, 1)]
        최신 = 0 if 세대들[0] > 세대들[1] else 1
        dados[(1 + 최신 * 259 + 3) * 512] ^= 1
        Mídia_VALOR.write_bytes(dados)
        computador = VM(posição / 'build/kernel.elf', Armazenamento_meio=Mídia_VALOR)
        try:
            computador.comando('cat note.txt', ['generation-one'])
            computador.comando('cat stored.txt', ['saved-from-C'])
            resultado['checksum_fallback'] = computador.LOG_linha.decode('utf-8', 'replace')
        finally:
            computador.Fechar()
        Outros_Mídia = Path(임시) / 'foreign.img'
        Outros_Mídia.write_bytes(bytes([0x5a]) * (2048 * 512))
        Anterior_item = hashlib.sha256(Outros_Mídia.read_bytes()).hexdigest()
        computador = VM(posição / 'build/kernel.elf', Armazenamento_meio=Outros_Mídia)
        try:
            computador.comando('sync', ['Sync: -19'])
        finally:
            computador.Fechar()
        assert hashlib.sha256(Outros_Mídia.read_bytes()).hexdigest() == Anterior_item
        resultado['foreign_disk_unchanged'] = True
    (posição / 'build/보존시험.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE Store_VALOR/ISO 재부팅/soma_de_verificação recuperar_Estado/다른 Mídia_VALOR 비변경', flush=True)

if __name__ == '__main__':
    Executar_comando()
