#!/usr/bin/env python3
"""élémentListeActuel interne ARM64 산출물을 검사하고 LGPL arbreSource·extrémitéReconnecter 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

racineProjet = Path(__file__).resolve().parents[1]
racineDépôt = racineProjet.parents[1]
nomDestination = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
bibliothèque = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def fichierHachage(chemin):
    return hashlib.sha256(Path(chemin).read_bytes()).hexdigest()


def inspecterÉtatValeur():
    for nom in ('vendor/wolfssh', 'vendor/wolfssl', 'valeurDistant/user_settings.h'):
        if (racineProjet / nom).exists():
            raise SystemExit('COSL valeurDistribution arrêter: élémentListePrécédentÉlément GPL valeurDistant 구현이 arbreSource 트리에 남아 있습니다: ' + nom)
    valeurCâblé = (racineProjet / 'PileRéseau/réseauCâblé.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in valeurCâblé or 'SPDX-License-Identifier: GPL' in valeurCâblé:
        raise SystemExit('COSL valeurDistribution arrêter: BSD GENET réalisation·고지 vérifier valeurNécessaire')
    for nom in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (racineDépôt / nom).is_file():
            raise SystemExit('COSL valeurDistribution 고지 méthodeManquant: ' + nom)
    valeurSymbole = subprocess.check_output(['aarch64-linux-gnu-nm', str(racineProjet / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', valeurSymbole):
        raise SystemExit('COSL valeurDistribution arrêter: 커널에 élémentListePrécédentÉlément GPL valeurMotPasse/SSH 심볼이 남아 있습니다. valeurRéessayer 빌드하세요.')
    for nom in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + nom + r'$', valeurSymbole, re.M):
            raise SystemExit('COSL 대체 réalisation 누락: ' + nom)
    with tempfile.TemporaryDirectory(dir=str(racineProjet / 'build')) as valeurTemporaire:
        valeurImage = Path(valeurTemporaire) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(racineProjet / 'build/kernel.elf'), str(valeurImage)])
        if fichierHachage(valeurImage) != fichierHachage(racineProjet / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    valeurRapport = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': fichierHachage(racineProjet / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {nom: fichierHachage(racineProjet / 'build' / nom) for nom in bibliothèque}}
    (racineProjet / 'build/cosl-distribution-check.json').write_text(json.dumps(valeurRapport, ensure_ascii=False, indent=2) + '\n')
    return valeurRapport


def EmballerExécutables():
    valeurRapport = inspecterÉtatValeur()
    valeurDistribution = racineProjet / 'dist'
    valeurDistribution.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(racineProjet / 'build')) as valeurTemporaire:
        valeurGroupe = Path(valeurTemporaire) / 'jkoros-native-relink'
        valeurGroupe.mkdir()
        def copierValeur(original, valeurPairRéseau):
            valeurDestination = valeurGroupe / valeurPairRéseau
            valeurDestination.parent.mkdir(parents=True, exist_ok=True)
            if original.is_dir():
                shutil.copytree(str(original), str(valeurDestination), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(original), str(valeurDestination))
        for nom in nomDestination:
            copierValeur(racineProjet / 'build' / (nom + '.o'), 'objects/' + nom + '.o')
        for nom in bibliothèque:
            copierValeur(racineProjet / 'build' / nom, 'objects/' + Path(nom).name)
        for nom in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'CompilateurC', 'Utilisateur', 'nommage', 'machine', 'PileRéseau/PileRéseau.h', 'Amorçage/DispositionLiens.ld',
                     'valeurDistant/assh_config.h', 'valeurDistant/config.h', 'valeurDistant/ctype.h', 'valeurDistant/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'GuideDistributionCOSL.md'):
            copierValeur(racineProjet / nom, nom)
        for nom in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            copierValeur(racineDépôt / nom, nom)
        for chemin in sorted((racineProjet / 'vendor').glob('LICENSE*')):
            copierValeur(chemin, 'vendor/' + chemin.name)
        copierValeur(racineProjet / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        copierValeur(racineProjet / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        copierValeur(racineDépôt / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        copierValeur(racineProjet / 'Outils/extrémitéReconnecter.py', 'relink.py')
        for chemin in sorted((racineProjet / 'build/user').glob('*.elf')):
            copierValeur(chemin, 'build/user/' + chemin.name)
        for nom in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            copierValeur(racineProjet / 'build/user' / (nom + '.o'), 'build/user/' + nom + '.o')
        for nom in ('crt', 'aot-runtime', 'PriseEnChargeEnvironnementExécution', 'lancer', 'tempsDeAnticipé', 'pontRetourner'):
            copierValeur(racineProjet / 'build/ccompiler' / (nom + '.o'), 'build/ccompiler/' + nom + '.o')
        spécification = dict(valeurRapport, objects=['objects/' + nom + '.o' for nom in nomDestination],
                    libraries=['objects/' + Path(chemin).name for chemin in bibliothèque])
        (valeurGroupe / 'relink.json').write_text(json.dumps(spécification, ensure_ascii=False, indent=2) + '\n')
        (valeurGroupe / 'README.md').write_text('''# jkoros native LGPL source and relink kit

This kit accompanies the matching kernel image. Retain it with binary distributions.
Application terms: LICENSE. Library terms: vendor/libassh/COPYING and vendor/tinycc/COPYING.
Other notices: THIRD_PARTY_NOTICES.md. COSL does not override the LGPL permissions.
This product includes software developed by Bill Paul.

Host dependencies: Python 3, Clang supporting aarch64-none-elf, libnewlib-dev headers,
and aarch64-linux-gnu binutils. No Linux kernel is linked into the guest.

From this extracted directory:

    python3 relink.py --verify

This recompiles libassh from the included source/configuration and relinks the kernel.
The original unmodified library must produce the recorded kernel SHA256.
To change libassh, edit vendor/libassh/src, then run without --verify.
Alternatively: python3 relink.py --libassh-archive /path/to/modified/libassh.a

TinyCC source is included in vendor/tinycc; the native port is in CompilateurC.
To rebuild a modified TinyCC and replace its embedded executable:

    python3 relink.py --tinycc --sdk /path/to/alpine-arm64-rootfs

Use the same Alpine 3.24.2 ARM64 SDK headers and GCC 15.2.0 libgcc runtime as the
original build (jkoros/platforms/rpi4: make prepare-runtime; see that platform's docs).
The SDK is a host build prerequisite and is not included here. Its libgcc exception
and GPL text are in vendor/LICENSE.libgcc-runtime and vendor/LICENSE.gcc-gpl3.
GCC sources: https://gcc.gnu.org/pub/gcc/releases/gcc-15.2.0/
Both the cc ELF size table and user/program objects are regenerated when --tinycc is used.
Output: build/relinked/kernel8.img. Boot it using the same Pi4 firmware/config or QEMU
runner as the original image. There is no signature lock against modified libraries.

This is a relink kit for one device image. Objects contain the same embedded device
key as that image. Keep personal development images and build/remote credentials
out of public source uploads; provision appropriate images for recipients.
''')
        valeurCible = valeurDistribution / 'jkoros-native-relink.tar.gz'
        archiveTemporaire = Path(valeurTemporaire) / valeurCible.name
        with tarfile.open(str(archiveTemporaire), 'w:gz') as valeurArchive:
            valeurArchive.add(str(valeurGroupe), arcname=valeurGroupe.name)
        archiveTemporaire.replace(valeurCible)
    valeurRapport['relink_archive_sha256'] = fichierHachage(valeurCible)
    (valeurDistribution / 'cosl-distribution.json').write_text(json.dumps(valeurRapport, ensure_ascii=False, indent=2) + '\n')
    return valeurCible


if __name__ == '__main__':
    Analyseur = argparse.ArgumentParser(description=__doc__)
    Analyseur.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    valeur = Analyseur.parse_args()
    if valeur.command == 'bundle':
        print('COSL source/relink kit:', EmballerExécutables())
    else:
        print(json.dumps(inspecterÉtatValeur(), ensure_ascii=False, indent=2))
