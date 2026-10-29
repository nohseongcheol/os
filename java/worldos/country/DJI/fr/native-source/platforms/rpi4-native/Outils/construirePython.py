"""고정한 공식 MicroPython 소스로 interne SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

valeurÉdition = '1.24.1'
hachageValidation = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def créerPython(cheminRacine, CompilateurC, outilÉditeurLiens):
    nom = 'micropython-' + valeurÉdition
    archive = cheminRacine / 'vendor' / (nom + '.tar.gz')
    if not archive.is_file() or hashlib.sha256(archive.read_bytes()).hexdigest() != hachageValidation:
        raise SystemExit('MicroPython arbreSource méthodeManquant/fichierHachage 불일치: ' + str(archive))
    donnéesOriginal = cheminRacine / 'build' / nom
    if not (donnéesOriginal / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(archive)) as lotTAR:
            for membre in lotTAR.getmembers():
                chemin = Path(membre.name)
                if chemin.is_absolute() or '..' in chemin.parts or chemin.parts[0] != nom:
                    raise SystemExit('안전하지 않은 arbreSource chemin')
                if membre.isfile() or membre.isdir():
                    lotTAR.extract(membre, str(cheminRacine / 'build'))
        (donnéesOriginal / '.jkoros-source-sha256').write_text(hachageValidation + '\n')
    newlib = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(newlib) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE valeurNécessaire')
    subprocess.check_call(['make', '-j2', 'CC=' + CompilateurC, 'LD=' + outilÉditeurLiens, 'NEWLIB_INCLUDE=' + newlib], cwd=str(cheminRacine / 'pontPython'))
