#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from exécuterCommande import racineProjet


def lancer():
    cheminDistribution = racineProjet / 'dist'
    cheminDistribution.mkdir(exist_ok=True)
    pOSIX = racineProjet.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(racineProjet / 'build')) as cheminTravailEnCours:
        trousseDéveloppement = Path(cheminTravailEnCours) / 'jkoros-native-sdk'
        listeFichier = {
            racineProjet.parents[1] / 'LICENSE': 'LICENSE',
            racineProjet.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            racineProjet / 'Outils/compilerSDK.py': 'compile.py',
            racineProjet / 'Utilisateur/invoquer.h': 'include/invoquer.h',
            racineProjet / 'nommage/nomsLierMachine.h': 'nommage/nomsLierMachine.h',
            racineProjet / 'Utilisateur/DispositionLiens.ld': 'user.ld',
            pOSIX / 'Entêtes/ABIFichier.h': 'include/ABIFichier.h',
            pOSIX / 'Entêtes/ABIRéseau.h': 'include/ABIRéseau.h',
            racineProjet / 'build/user/start.o': 'lib/start.o',
            racineProjet / 'build/user/runtime.o': 'lib/runtime.o',
            racineProjet / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            racineProjet / 'Utilisateur/ExempleFichier.cpp': 'examples/ExempleFichier.cpp',
            racineProjet / 'Exemples/CodageHangul/Salutation.c': 'examples/Salutation.c',
            racineProjet / 'Exemples/CodageHangul/valeurFlux.c': 'examples/valeurFlux.c',
            racineProjet / 'Exemples/CodageHangul/Salutation.cpp': 'examples/Salutation.cpp',
            racineProjet / 'Utilisateur/ExempleCommunication.cpp': 'examples/ExempleCommunication.cpp',
            racineProjet / 'build/user/demo.elf': 'examples/demo.elf',
            racineProjet / 'build/user/network.elf': 'examples/network.elf',
        }
        manifesteLot = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for donnéesOriginal, valeurCible in listeFichier.items():
            adresseDonnéesDestination = trousseDéveloppement / valeurCible
            adresseDonnéesDestination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(donnéesOriginal), str(adresseDonnéesDestination))
            manifesteLot['sha256'][valeurCible] = hashlib.sha256(adresseDonnéesDestination.read_bytes()).hexdigest()
        (trousseDéveloppement / 'manifest.json').write_text(json.dumps(manifesteLot, indent=2) + '\n')
        (trousseDéveloppement / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/ExempleFichier.cpp -o demo.elf\n'
            'python3 compile.py examples/Salutation.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int démarrerProgrammeUtilisateur(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Outils/exécuterCommande.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Outils/exécuterFichier.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: nombreÉlémentsArgumentUtilisateur()/argumentUtilisateur() in invoquer.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        archive = Path(cheminTravailEnCours) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(archive), 'w:gz') as donnéesRésultat:
            donnéesRésultat.add(str(trousseDéveloppement), arcname=trousseDéveloppement.name)
        archive.replace(cheminDistribution / archive.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        archiveCompilateur = Path(cheminTravailEnCours) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(archiveCompilateur), 'w:gz') as donnéesRésultat:
            for nom in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                donnéesRésultat.add(str(racineProjet.parents[1] / nom), arcname='jkoros-native/' + nom)
            for cheminRelatif in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'CompilateurC', 'Utilisateur', 'nommage',
                             'Outils/construireCompilateurC.py', 'Outils/construireEspaceUtilisateur.py', 'CompilationEtTransfertFichier.md'):
                donnéesRésultat.add(str(racineProjet / cheminRelatif), arcname='jkoros-native/' + cheminRelatif)
            for nom in ('crt.o', 'aot-runtime.o', 'PriseEnChargeEnvironnementExécution.o', 'lancer.o', 'tempsDeAnticipé.o', 'pontRetourner.o'):
                fichierDestination = racineProjet / 'build/ccompiler' / nom
                donnéesRésultat.add(str(fichierDestination), arcname='jkoros-native/relink/' + nom)
            for nom in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                donnéesRésultat.add(str(racineProjet / 'build/user' / nom), arcname='jkoros-native/relink/user/' + nom)
            donnéesRésultat.add(str(racineProjet / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            donnéesRésultat.add(str(pOSIX), arcname='posix-kor/arm64-native')
        archiveCompilateur.replace(cheminDistribution / archiveCompilateur.name)
    print('SDK:', cheminDistribution / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    lancer()
