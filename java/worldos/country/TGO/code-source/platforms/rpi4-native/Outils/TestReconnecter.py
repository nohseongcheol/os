#!/usr/bin/env python3
"""valeurDistribution 자료만으로 LGPL 재연결과 수정한 TinyCC의 donnéesEffectif 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from exécuterCommande import racineProjet, commande


def lancer():
    Analyseur = argparse.ArgumentParser(description=__doc__)
    Analyseur.add_argument('--sdk', type=Path, default=racineProjet.parent / 'rpi4/build/rootfs')
    arguments = Analyseur.parse_args()
    Sortie = racineProjet / 'build/verification/cosl-relink'
    Sortie.mkdir(parents=True, exist_ok=True)
    valeurRapport = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((racineProjet / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as valeurTemporaire:
            chemin = Path(valeurTemporaire)
            with tarfile.open(str(racineProjet / 'dist/jkoros-native-relink.tar.gz')) as valeurGroupe:
                for valeurEntréeÉlément in valeurGroupe.getmembers():
                    if chemin not in (chemin / valeurEntréeÉlément.name).resolve().parents or valeurEntréeÉlément.issym() or valeurEntréeÉlément.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + valeurEntréeÉlément.name)
                valeurGroupe.extractall(str(chemin))
            source = chemin / 'jkoros-native-relink'
            def extrémitéReconnecter(nom, listeArguments):
                with (Sortie / nom).open('wb') as enregistrementJournal:
                    subprocess.run(['python3', 'relink.py'] + listeArguments, cwd=str(source),
                                   stdout=enregistrementJournal, stderr=subprocess.STDOUT, check=True, timeout=180)
            extrémitéReconnecter('original.log', ['--verify'])
            valeurRapport['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            outilCompilateur = source / 'vendor/tinycc/libtcc.c'
            texteCorps = outilCompilateur.read_text()
            position = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert texteCorps.count(position) == 1
            outilCompilateur.write_text(texteCorps.replace(position, position + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            extrémitéReconnecter('modified-tinycc.log', ['--tinycc', '--sdk', str(arguments.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            valeurImage = source / 'build/relinked/kernel8.img'
            valeurRapport['modified_kernel_sha256'] = hashlib.sha256(valeurImage.read_bytes()).hexdigest()
            assert valeurRapport['modified_kernel_sha256'] != valeurRapport['kernel_sha256']
            valeurRapport['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            listeArguments = commande()
            listeArguments[listeArguments.index('-kernel') + 1] = str(valeurImage)
            valeurProcessus = subprocess.Popen(listeArguments + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            enregistrementJournal = bytearray()
            valeurSélection = selectors.DefaultSelector()
            valeurSélection.register(valeurProcessus.stdout, selectors.EVENT_READ)
            def attendreÉtatValeur(afficherValeur=b'jkoros-native> ', élémentListeInitialValeur=0):
                terminaison = time.monotonic() + 40
                while afficherValeur not in enregistrementJournal[élémentListeInitialValeur:]:
                    if time.monotonic() > terminaison or valeurProcessus.poll() is not None:
                        raise AssertionError('Missing ' + repr(afficherValeur) + '\n' + enregistrementJournal[élémentListeInitialValeur:].decode('utf-8', 'replace'))
                    for valeurEntréeÉlément, _ in valeurSélection.select(.1):
                        Données = valeurEntréeÉlément.fileobj.read(65536)
                        if Données:
                            enregistrementJournal.extend(Données)
                return bytes(enregistrementJournal[élémentListeInitialValeur:])
            def envoyer(texteMot, afficherValeur=b'jkoros-native> '):
                élémentListeInitialValeur = len(enregistrementJournal)
                valeurProcessus.stdin.write(texteMot.encode() + b'\n')
                valeurProcessus.stdin.flush()
                return attendreÉtatValeur(afficherValeur, élémentListeInitialValeur)
            try:
                attendreÉtatValeur()
                Tests = '#include <ABIFichier.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return écrireDonnéesFichier(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                envoyer('load /relink.c', b'hex> ')
                for indicePosition in range(0, len(Tests), 64):
                    envoyer(Tests[indicePosition:indicePosition+64].hex(), b'hex> ')
                assert b'LOADED' in envoyer('.')
                résultat = envoyer('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in résultat, résultat
                résultat = envoyer('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in résultat and b'exit 0' in résultat, résultat
                valeurRapport['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                valeurSélection.close()
                if valeurProcessus.poll() is None:
                    valeurProcessus.terminate()
                    try:
                        valeurProcessus.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        valeurProcessus.kill()
                        valeurProcessus.wait()
                (Sortie / 'guest.log').write_bytes(enregistrementJournal)
        valeurRapport['passed'] = True
        print(json.dumps(valeurRapport, ensure_ascii=False, indent=2))
    finally:
        (Sortie / 'report.json').write_text(json.dumps(valeurRapport, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    lancer()
