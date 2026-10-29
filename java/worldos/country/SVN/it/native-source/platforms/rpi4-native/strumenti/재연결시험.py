#!/usr/bin/env python3
"""distribuzione_VALORE 자료만으로 LGPL 재연결과 수정한 TinyCC의 effettivo_dati 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Esegui_comando import azione_radice, comando


def avvia():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--sdk', type=Path, default=azione_radice.parent / 'rpi4/build/rootfs')
    argomenti = parser_48ee4b1b.parse_args()
    uscitaTesto = azione_radice / 'build/verification/cosl-relink'
    uscitaTesto.mkdir(parents=True, exist_ok=True)
    Report_VALORE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((azione_radice / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            percorso = Path(임시)
            with tarfile.open(str(azione_radice / 'dist/jkoros-native-relink.tar.gz')) as gruppo_VALORE:
                for voce_VALORE in gruppo_VALORE.getmembers():
                    if percorso not in (percorso / voce_VALORE.name).resolve().parents or voce_VALORE.issym() or voce_VALORE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + voce_VALORE.name)
                gruppo_VALORE.extractall(str(percorso))
            codiceSorgente = percorso / 'jkoros-native-relink'
            def 재연결(Nome, 인수들):
                with (uscitaTesto / Nome).open('wb') as LOG_riga:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(codiceSorgente),
                                   stdout=LOG_riga, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            Report_VALORE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            compilatore_strumento = codiceSorgente / 'vendor/tinycc/libtcc.c'
            corpo_del_testo = compilatore_strumento.read_text()
            posizione = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert corpo_del_testo.count(posizione) == 1
            compilatore_strumento.write_text(corpo_del_testo.replace(posizione, posizione + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(argomenti.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            foto_VALORE = codiceSorgente / 'build/relinked/kernel8.img'
            Report_VALORE['modified_kernel_sha256'] = hashlib.sha256(foto_VALORE.read_bytes()).hexdigest()
            assert Report_VALORE['modified_kernel_sha256'] != Report_VALORE['kernel_sha256']
            Report_VALORE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = comando()
            인수들[인수들.index('-kernel') + 1] = str(foto_VALORE)
            Processi_VALORE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_riga = bytearray()
            selezione_VALORE = selectors.DefaultSelector()
            selezione_VALORE.register(Processi_VALORE.stdout, selectors.EVENT_READ)
            def stato_di_attesa(mostrare_VALORE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while mostrare_VALORE not in LOG_riga[처음:]:
                    if time.monotonic() > 끝 or Processi_VALORE.poll() is not None:
                        raise AssertionError('Missing ' + repr(mostrare_VALORE) + '\n' + LOG_riga[처음:].decode('utf-8', 'replace'))
                    for voce_VALORE, _ in selezione_VALORE.select(.1):
                        dati = voce_VALORE.fileobj.read(65536)
                        if dati:
                            LOG_riga.extend(dati)
                return bytes(LOG_riga[처음:])
            def inviare(Word_SMS, mostrare_VALORE=b'jkoros-native> '):
                처음 = len(LOG_riga)
                Processi_VALORE.stdin.write(Word_SMS.encode() + b'\n')
                Processi_VALORE.stdin.flush()
                return stato_di_attesa(mostrare_VALORE, 처음)
            try:
                stato_di_attesa()
                prove = '#include <File_ABI.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return scrivere_File_dati(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                inviare('load /relink.c', b'hex> ')
                for funzione_INDICE in range(0, len(prove), 64):
                    inviare(prove[funzione_INDICE:funzione_INDICE+64].hex(), b'hex> ')
                assert b'LOADED' in inviare('.')
                risultato = inviare('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in risultato, risultato
                risultato = inviare('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in risultato and b'exit 0' in risultato, risultato
                Report_VALORE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                selezione_VALORE.close()
                if Processi_VALORE.poll() is None:
                    Processi_VALORE.terminate()
                    try:
                        Processi_VALORE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Processi_VALORE.kill()
                        Processi_VALORE.wait()
                (uscitaTesto / 'guest.log').write_bytes(LOG_riga)
        Report_VALORE['passed'] = True
        print(json.dumps(Report_VALORE, ensure_ascii=False, indent=2))
    finally:
        (uscitaTesto / 'report.json').write_text(json.dumps(Report_VALORE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    avvia()
