"""고정한 공식 MicroPython 소스로 eigen SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

ausgabeversionWert = '1.24.1'
validierungPrüfsumme = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def pythonErstellen(wurzelPfad, CÜbersetzer, binderWerkzeug):
    Name = 'micropython-' + ausgabeversionWert
    archiv = wurzelPfad / 'vendor' / (Name + '.tar.gz')
    if not archiv.is_file() or hashlib.sha256(archiv.read_bytes()).hexdigest() != validierungPrüfsumme:
        raise SystemExit('MicroPython quelltextBaum fehlendMethode/prüfsummeDatei 불일치: ' + str(archiv))
    ursprünglichDaten = wurzelPfad / 'build' / Name
    if not (ursprünglichDaten / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(archiv)) as tARBündel:
            for mitglied in tARBündel.getmembers():
                pfad = Path(mitglied.name)
                if pfad.is_absolute() or '..' in pfad.parts or pfad.parts[0] != Name:
                    raise SystemExit('안전하지 않은 quelltextBaum pfad')
                if mitglied.isfile() or mitglied.isdir():
                    tARBündel.extract(mitglied, str(wurzelPfad / 'build'))
        (ursprünglichDaten / '.jkoros-source-sha256').write_text(validierungPrüfsumme + '\n')
    newlib = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(newlib) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE benötigtWert')
    subprocess.check_call(['make', '-j2', 'CC=' + CÜbersetzer, 'LD=' + binderWerkzeug, 'NEWLIB_INCLUDE=' + newlib], cwd=str(wurzelPfad / 'pythonBrücke'))
