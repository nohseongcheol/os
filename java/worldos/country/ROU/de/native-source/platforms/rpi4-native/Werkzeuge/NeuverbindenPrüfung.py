#!/usr/bin/env python3
"""verteilungWert 자료만으로 LGPL 재연결과 수정한 TinyCC의 tatsächlichDaten 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from befehlAusführen import projektWurzel, befehl


def ausführenVorgang():
    Strukturanalysierer = argparse.ArgumentParser(description=__doc__)
    Strukturanalysierer.add_argument('--sdk', type=Path, default=projektWurzel.parent / 'rpi4/build/rootfs')
    argumente = Strukturanalysierer.parse_args()
    Ausgabe = projektWurzel / 'build/verification/cosl-relink'
    Ausgabe.mkdir(parents=True, exist_ok=True)
    berichtWert = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((projektWurzel / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as vorläufigWert:
            pfad = Path(vorläufigWert)
            with tarfile.open(str(projektWurzel / 'dist/jkoros-native-relink.tar.gz')) as gruppeWert:
                for eintragWert in gruppeWert.getmembers():
                    if pfad not in (pfad / eintragWert.name).resolve().parents or eintragWert.issym() or eintragWert.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + eintragWert.name)
                gruppeWert.extractall(str(pfad))
            Quelltext = pfad / 'jkoros-native-relink'
            def neuverbindenEndpunkt(Name, argumenteListe):
                with (Ausgabe / Name).open('wb') as protokolldateiAufzeichnung:
                    subprocess.run(['python3', 'relink.py'] + argumenteListe, cwd=str(Quelltext),
                                   stdout=protokolldateiAufzeichnung, stderr=subprocess.STDOUT, check=True, timeout=180)
            neuverbindenEndpunkt('original.log', ['--verify'])
            berichtWert['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            übersetzerWerkzeug = Quelltext / 'vendor/tinycc/libtcc.c'
            rumpfText = übersetzerWerkzeug.read_text()
            position = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert rumpfText.count(position) == 1
            übersetzerWerkzeug.write_text(rumpfText.replace(position, position + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            neuverbindenEndpunkt('modified-tinycc.log', ['--tinycc', '--sdk', str(argumente.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            abbildWert = Quelltext / 'build/relinked/kernel8.img'
            berichtWert['modified_kernel_sha256'] = hashlib.sha256(abbildWert.read_bytes()).hexdigest()
            assert berichtWert['modified_kernel_sha256'] != berichtWert['kernel_sha256']
            berichtWert['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            argumenteListe = befehl()
            argumenteListe[argumenteListe.index('-kernel') + 1] = str(abbildWert)
            prozessWert = subprocess.Popen(argumenteListe + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            protokolldateiAufzeichnung = bytearray()
            auswahlWert = selectors.DefaultSelector()
            auswahlWert.register(prozessWert.stdout, selectors.EVENT_READ)
            def statuswertWarten(wertAnzeigen=b'jkoros-native> ', anfänglichElementeintrag=0):
                endung = time.monotonic() + 40
                while wertAnzeigen not in protokolldateiAufzeichnung[anfänglichElementeintrag:]:
                    if time.monotonic() > endung or prozessWert.poll() is not None:
                        raise AssertionError('Missing ' + repr(wertAnzeigen) + '\n' + protokolldateiAufzeichnung[anfänglichElementeintrag:].decode('utf-8', 'replace'))
                    for eintragWert, _ in auswahlWert.select(.1):
                        Daten = eintragWert.fileobj.read(65536)
                        if Daten:
                            protokolldateiAufzeichnung.extend(Daten)
                return bytes(protokolldateiAufzeichnung[anfänglichElementeintrag:])
            def senden(maschinenwortText, wertAnzeigen=b'jkoros-native> '):
                anfänglichElementeintrag = len(protokolldateiAufzeichnung)
                prozessWert.stdin.write(maschinenwortText.encode() + b'\n')
                prozessWert.stdin.flush()
                return statuswertWarten(wertAnzeigen, anfänglichElementeintrag)
            try:
                statuswertWarten()
                Prüfungen = '#include <DateiABI.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return dateiDatenSchreiben(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                senden('load /relink.c', b'hex> ')
                for positionIndex in range(0, len(Prüfungen), 64):
                    senden(Prüfungen[positionIndex:positionIndex+64].hex(), b'hex> ')
                assert b'LOADED' in senden('.')
                ergebnis = senden('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in ergebnis, ergebnis
                ergebnis = senden('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in ergebnis and b'exit 0' in ergebnis, ergebnis
                berichtWert['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                auswahlWert.close()
                if prozessWert.poll() is None:
                    prozessWert.terminate()
                    try:
                        prozessWert.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        prozessWert.kill()
                        prozessWert.wait()
                (Ausgabe / 'guest.log').write_bytes(protokolldateiAufzeichnung)
        berichtWert['passed'] = True
        print(json.dumps(berichtWert, ensure_ascii=False, indent=2))
    finally:
        (Ausgabe / 'report.json').write_text(json.dumps(berichtWert, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    ausführenVorgang()
