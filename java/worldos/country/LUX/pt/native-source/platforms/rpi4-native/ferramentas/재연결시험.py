#!/usr/bin/env python3
"""distribuição_VALOR 자료만으로 LGPL 재연결과 수정한 TinyCC의 real_dados 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Executar_comando import ação_raiz, comando


def iniciar():
    analisador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analisador_48ee4b1b.add_argument('--sdk', type=Path, default=ação_raiz.parent / 'rpi4/build/rootfs')
    argumentos = analisador_48ee4b1b.parse_args()
    saídaTexto = ação_raiz / 'build/verification/cosl-relink'
    saídaTexto.mkdir(parents=True, exist_ok=True)
    relatar_VALOR = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((ação_raiz / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            caminho = Path(임시)
            with tarfile.open(str(ação_raiz / 'dist/jkoros-native-relink.tar.gz')) as Grupo_VALOR:
                for entrada_VALOR_962f286b in Grupo_VALOR.getmembers():
                    if caminho not in (caminho / entrada_VALOR_962f286b.name).resolve().parents or entrada_VALOR_962f286b.issym() or entrada_VALOR_962f286b.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + entrada_VALOR_962f286b.name)
                Grupo_VALOR.extractall(str(caminho))
            códigoFonte = caminho / 'jkoros-native-relink'
            def 재연결(Nome, 인수들):
                with (saídaTexto / Nome).open('wb') as LOG_linha:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(códigoFonte),
                                   stdout=LOG_linha, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            relatar_VALOR['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            compilador_ferramenta = códigoFonte / 'vendor/tinycc/libtcc.c'
            corpo_de_texto = compilador_ferramenta.read_text()
            posição = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert corpo_de_texto.count(posição) == 1
            compilador_ferramenta.write_text(corpo_de_texto.replace(posição, posição + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(argumentos.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            foto_VALOR = códigoFonte / 'build/relinked/kernel8.img'
            relatar_VALOR['modified_kernel_sha256'] = hashlib.sha256(foto_VALOR.read_bytes()).hexdigest()
            assert relatar_VALOR['modified_kernel_sha256'] != relatar_VALOR['kernel_sha256']
            relatar_VALOR['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = comando()
            인수들[인수들.index('-kernel') + 1] = str(foto_VALOR)
            Processo_VALOR = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_linha = bytearray()
            seleção_VALOR = selectors.DefaultSelector()
            seleção_VALOR.register(Processo_VALOR.stdout, selectors.EVENT_READ)
            def estado_de_espera(mostrar_VALOR=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while mostrar_VALOR not in LOG_linha[처음:]:
                    if time.monotonic() > 끝 or Processo_VALOR.poll() is not None:
                        raise AssertionError('Missing ' + repr(mostrar_VALOR) + '\n' + LOG_linha[처음:].decode('utf-8', 'replace'))
                    for entrada_VALOR_962f286b, _ in seleção_VALOR.select(.1):
                        dados = entrada_VALOR_962f286b.fileobj.read(65536)
                        if dados:
                            LOG_linha.extend(dados)
                return bytes(LOG_linha[처음:])
            def enviar(Word_SMS, mostrar_VALOR=b'jkoros-native> '):
                처음 = len(LOG_linha)
                Processo_VALOR.stdin.write(Word_SMS.encode() + b'\n')
                Processo_VALOR.stdin.flush()
                return estado_de_espera(mostrar_VALOR, 처음)
            try:
                estado_de_espera()
                testes = '#include <Arquivo_ABI.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return gravar_Arquivo_dados(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                enviar('load /relink.c', b'hex> ')
                for cargo_ÍNDICE in range(0, len(testes), 64):
                    enviar(testes[cargo_ÍNDICE:cargo_ÍNDICE+64].hex(), b'hex> ')
                assert b'LOADED' in enviar('.')
                resultado = enviar('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in resultado, resultado
                resultado = enviar('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in resultado and b'exit 0' in resultado, resultado
                relatar_VALOR['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                seleção_VALOR.close()
                if Processo_VALOR.poll() is None:
                    Processo_VALOR.terminate()
                    try:
                        Processo_VALOR.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Processo_VALOR.kill()
                        Processo_VALOR.wait()
                (saídaTexto / 'guest.log').write_bytes(LOG_linha)
        relatar_VALOR['passed'] = True
        print(json.dumps(relatar_VALOR, ensure_ascii=False, indent=2))
    finally:
        (saídaTexto / 'report.json').write_text(json.dumps(relatar_VALOR, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    iniciar()
