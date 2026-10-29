#!/usr/bin/env python3
"""distributie_WAARDE 자료만으로 LGPL 재연결과 수정한 TinyCC의 werkelijk_gegevens 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Uitvoeren_opdracht import Taken_wortel, opdracht


def starten():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--sdk', type=Path, default=Taken_wortel.parent / 'rpi4/build/rootfs')
    argumenten = parser_48ee4b1b.parse_args()
    tekstuitvoer = Taken_wortel / 'build/verification/cosl-relink'
    tekstuitvoer.mkdir(parents=True, exist_ok=True)
    Rapport_WAARDE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Taken_wortel / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            pad = Path(임시)
            with tarfile.open(str(Taken_wortel / 'dist/jkoros-native-relink.tar.gz')) as Groep_WAARDE:
                for invoer_WAARDE_962f286b in Groep_WAARDE.getmembers():
                    if pad not in (pad / invoer_WAARDE_962f286b.name).resolve().parents or invoer_WAARDE_962f286b.issym() or invoer_WAARDE_962f286b.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + invoer_WAARDE_962f286b.name)
                Groep_WAARDE.extractall(str(pad))
            broncode = pad / 'jkoros-native-relink'
            def 재연결(Naam, 인수들):
                with (tekstuitvoer / Naam).open('wb') as LOG_RECORD:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(broncode),
                                   stdout=LOG_RECORD, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            Rapport_WAARDE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            compiler_hulpmiddel = broncode / 'vendor/tinycc/libtcc.c'
            hoofdtekst = compiler_hulpmiddel.read_text()
            positie = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert hoofdtekst.count(positie) == 1
            compiler_hulpmiddel.write_text(hoofdtekst.replace(positie, positie + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(argumenten.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            kopie_WAARDE = broncode / 'build/relinked/kernel8.img'
            Rapport_WAARDE['modified_kernel_sha256'] = hashlib.sha256(kopie_WAARDE.read_bytes()).hexdigest()
            assert Rapport_WAARDE['modified_kernel_sha256'] != Rapport_WAARDE['kernel_sha256']
            Rapport_WAARDE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = opdracht()
            인수들[인수들.index('-kernel') + 1] = str(kopie_WAARDE)
            Proces_WAARDE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_RECORD = bytearray()
            selectie_WAARDE = selectors.DefaultSelector()
            selectie_WAARDE.register(Proces_WAARDE.stdout, selectors.EVENT_READ)
            def wachtstatus(weergeven_WAARDE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while weergeven_WAARDE not in LOG_RECORD[처음:]:
                    if time.monotonic() > 끝 or Proces_WAARDE.poll() is not None:
                        raise AssertionError('Missing ' + repr(weergeven_WAARDE) + '\n' + LOG_RECORD[처음:].decode('utf-8', 'replace'))
                    for invoer_WAARDE_962f286b, _ in selectie_WAARDE.select(.1):
                        gegevens = invoer_WAARDE_962f286b.fileobj.read(65536)
                        if gegevens:
                            LOG_RECORD.extend(gegevens)
                return bytes(LOG_RECORD[처음:])
            def e_mailen(Word_sms, weergeven_WAARDE=b'jkoros-native> '):
                처음 = len(LOG_RECORD)
                Proces_WAARDE.stdin.write(Word_sms.encode() + b'\n')
                Proces_WAARDE.stdin.flush()
                return wachtstatus(weergeven_WAARDE, 처음)
            try:
                wachtstatus()
                tests = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return schrijven_Bestand_gegevens(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                e_mailen('load /relink.c', b'hex> ')
                for plaatsingsindex in range(0, len(tests), 64):
                    e_mailen(tests[plaatsingsindex:plaatsingsindex+64].hex(), b'hex> ')
                assert b'LOADED' in e_mailen('.')
                resultaat = e_mailen('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in resultaat, resultaat
                resultaat = e_mailen('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in resultaat and b'exit 0' in resultaat, resultaat
                Rapport_WAARDE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                selectie_WAARDE.close()
                if Proces_WAARDE.poll() is None:
                    Proces_WAARDE.terminate()
                    try:
                        Proces_WAARDE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proces_WAARDE.kill()
                        Proces_WAARDE.wait()
                (tekstuitvoer / 'guest.log').write_bytes(LOG_RECORD)
        Rapport_WAARDE['passed'] = True
        print(json.dumps(Rapport_WAARDE, ensure_ascii=False, indent=2))
    finally:
        (tekstuitvoer / 'report.json').write_text(json.dumps(Rapport_WAARDE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    starten()
