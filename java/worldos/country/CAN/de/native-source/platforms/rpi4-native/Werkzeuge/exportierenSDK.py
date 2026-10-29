#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from befehlAusführen import projektWurzel


def ausführenVorgang():
    verteilungPfad = projektWurzel / 'dist'
    verteilungPfad.mkdir(exist_ok=True)
    pOSIX = projektWurzel.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(projektWurzel / 'build')) as arbeitendPfad:
        entwicklungWerkzeugsatz = Path(arbeitendPfad) / 'jkoros-native-sdk'
        dateiListe = {
            projektWurzel.parents[1] / 'LICENSE': 'LICENSE',
            projektWurzel.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            projektWurzel / 'Werkzeuge/sDKÜbersetzen.py': 'compile.py',
            projektWurzel / 'Benutzer/aufrufen.h': 'include/aufrufen.h',
            projektWurzel / 'benennung/maschineBindenNamen.h': 'benennung/maschineBindenNamen.h',
            projektWurzel / 'Benutzer/Bindungsanordnung.ld': 'user.ld',
            pOSIX / 'Kopfdateien/DateiABI.h': 'include/DateiABI.h',
            pOSIX / 'Kopfdateien/NetzwerkABI.h': 'include/NetzwerkABI.h',
            projektWurzel / 'build/user/start.o': 'lib/start.o',
            projektWurzel / 'build/user/runtime.o': 'lib/runtime.o',
            projektWurzel / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            projektWurzel / 'Benutzer/Dateibeispiel.cpp': 'examples/Dateibeispiel.cpp',
            projektWurzel / 'Beispiele/HangulKodierweise/Gruß.c': 'examples/Gruß.c',
            projektWurzel / 'Beispiele/HangulKodierweise/datenstromWert.c': 'examples/datenstromWert.c',
            projektWurzel / 'Beispiele/HangulKodierweise/Gruß.cpp': 'examples/Gruß.cpp',
            projektWurzel / 'Benutzer/KommunikationBeispiel.cpp': 'examples/KommunikationBeispiel.cpp',
            projektWurzel / 'build/user/demo.elf': 'examples/demo.elf',
            projektWurzel / 'build/user/network.elf': 'examples/network.elf',
        }
        bündelInhaltsverzeichnis = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for ursprünglichDaten, zielobjektWert in dateiListe.items():
            zielDatenAdresse = entwicklungWerkzeugsatz / zielobjektWert
            zielDatenAdresse.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(ursprünglichDaten), str(zielDatenAdresse))
            bündelInhaltsverzeichnis['sha256'][zielobjektWert] = hashlib.sha256(zielDatenAdresse.read_bytes()).hexdigest()
        (entwicklungWerkzeugsatz / 'manifest.json').write_text(json.dumps(bündelInhaltsverzeichnis, indent=2) + '\n')
        (entwicklungWerkzeugsatz / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/Dateibeispiel.cpp -o demo.elf\n'
            'python3 compile.py examples/Gruß.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int benutzerProgrammStarten(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Werkzeuge/befehlAusführen.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Werkzeuge/dateiAusführen.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: benutzerArgumentAnzahl()/benutzerArgument() in aufrufen.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        archiv = Path(arbeitendPfad) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(archiv), 'w:gz') as ergebnisDaten:
            ergebnisDaten.add(str(entwicklungWerkzeugsatz), arcname=entwicklungWerkzeugsatz.name)
        archiv.replace(verteilungPfad / archiv.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        übersetzerArchiv = Path(arbeitendPfad) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(übersetzerArchiv), 'w:gz') as ergebnisDaten:
            for Name in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                ergebnisDaten.add(str(projektWurzel.parents[1] / Name), arcname='jkoros-native/' + Name)
            for relativPfad in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'CÜbersetzer', 'Benutzer', 'benennung',
                             'Werkzeuge/cÜbersetzerErzeugenAbbild.py', 'Werkzeuge/benutzerRaumErzeugenAbbild.py', 'DateiÜbertragungUndÜbersetzungsvorgang.md'):
                ergebnisDaten.add(str(projektWurzel / relativPfad), arcname='jkoros-native/' + relativPfad)
            for Name in ('crt.o', 'aot-runtime.o', 'LaufzeitUnterstützung.o', 'ausführenVorgang.o', 'vorabVonElementZeit.o', 'zurückkehrenBrücke.o'):
                zielDatei = projektWurzel / 'build/ccompiler' / Name
                ergebnisDaten.add(str(zielDatei), arcname='jkoros-native/relink/' + Name)
            for Name in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                ergebnisDaten.add(str(projektWurzel / 'build/user' / Name), arcname='jkoros-native/relink/user/' + Name)
            ergebnisDaten.add(str(projektWurzel / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            ergebnisDaten.add(str(pOSIX), arcname='posix-kor/arm64-native')
        übersetzerArchiv.replace(verteilungPfad / übersetzerArchiv.name)
    print('SDK:', verteilungPfad / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    ausführenVorgang()
