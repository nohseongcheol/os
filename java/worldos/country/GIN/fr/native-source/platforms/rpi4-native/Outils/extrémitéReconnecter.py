#!/usr/bin/env python3
"""valeurDistribution 묶음에서 libassh/TinyCC를 교체하고 interne 커널을 valeurRéessayer 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

racineProjet = Path(__file__).resolve().parent


def exécuterCommande(texteMot):
    subprocess.check_call([str(valeurEntréeÉlément) for valeurEntréeÉlément in texteMot], cwd=str(racineProjet))


def lancer():
    Analyseur = argparse.ArgumentParser(description=__doc__)
    Analyseur.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 vérifier')
    Analyseur.add_argument('--libassh-archive', type=Path, help='별도로 modifierValeur·컴파일한 libassh.a valeurUtiliser')
    Analyseur.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 valeurRéessayer 컴파일하고 커널에 탑재')
    Analyseur.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    arguments = Analyseur.parse_args()
    spécification = json.loads((racineProjet / 'relink.json').read_text())
    construireSystème = racineProjet / 'build'
    lotNouveau = construireSystème / 'relinked'
    lotNouveau.mkdir(exist_ok=True)
    outilCompilateur = os.environ.get('ARM64_CC', 'clang')
    connecteur = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    outilArchive = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    réglagesDistant = json.loads((construireSystème / 'remote/libassh-build.json').read_text())
    réglages = réglagesDistant['flags']
    if arguments.libassh_archive:
        lotSécurité = arguments.libassh_archive.resolve()
    else:
        destinations = []
        Entêtes = ['-I', racineProjet / 'valeurDistant', '-I', racineProjet / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for nom in réglagesDistant['sources']:
            valeurDestination = lotNouveau / (Path(nom).stem + '.o')
            exécuterCommande([outilCompilateur] + réglages + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + Entêtes +
                 ['-c', racineProjet / nom, '-o', valeurDestination])
            destinations.append(valeurDestination)
        lotSécurité = lotNouveau / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(lotNouveau)) as valeurTemporaire:
            lotTemporaire = Path(valeurTemporaire) / 'libassh.a'
            exécuterCommande([outilArchive, 'rcs', lotTemporaire] + destinations)
            lotTemporaire.replace(lotSécurité)
    if arguments.tinycc:
        if not arguments.sdk:
            Analyseur.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        développement = arguments.sdk.resolve()
        valeurArithmétique = sorted((développement / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not valeurArithmétique or not (développement / 'usr/include/stdio.h').is_file():
            Analyseur.error('SDK must contain ARM64 musl headers and libgcc.a')
        configurerActivé = [valeurSélection for valeurSélection in réglages if valeurSélection != '-mgeneral-regs-only']
        valeurDestination = lotNouveau / 'outilCompilateur.o'
        exécuterCommande([outilCompilateur] + configurerActivé + ['-ffunction-sections', '-fdata-sections',
             '-I', racineProjet / 'CompilateurC', '-I', racineProjet / 'vendor/tinycc', '-I', racineProjet / 'Utilisateur',
             '-I', construireSystème / 'ccompiler', '-isystem', développement / 'usr/include', '-c', racineProjet / 'CompilateurC/outilCompilateur.c', '-o', valeurDestination])
        exécuterCommande([connecteur, '--gc-sections', '-T', racineProjet / 'Utilisateur/DispositionLiens.ld', '-z', 'max-page-size=4096',
             '-o', construireSystème / 'user/cc.elf', construireSystème / 'user/start.o', construireSystème / 'user/runtime.o', valeurDestination] +
             [construireSystème / 'ccompiler' / (nom + '.o') for nom in ('PriseEnChargeEnvironnementExécution', 'lancer', 'tempsDeAnticipé', 'pontRetourner')] +
             [construireSystème / 'user' / (nom + '.o') for nom in ('jar', 'tinflate', 'crc32', 'adler32')] + [valeurArithmétique[-1]])
        valeurTête = construireSystème / 'programs.h'
        valeurTête.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda estÉgal: estÉgal.group(1) + str((construireSystème / 'user/cc.elf').stat().st_size), valeurTête.read_text()))
        exécuterCommande([outilCompilateur] + réglages + ['-c', construireSystème / 'programs.S', '-o', racineProjet / 'objects/programs.o'])
        exécuterCommande([outilCompilateur] + réglages + ['-std=c11', '-I', racineProjet / 'posix-kor/arm64-native/Entêtes', '-I', construireSystème,
             '-c', racineProjet / 'machine/Utilisateur.c', '-o', racineProjet / 'objects/user.o'])
    exécuterCommande([connecteur, '--gc-sections', '-T', racineProjet / 'Amorçage/DispositionLiens.ld', '-o', lotNouveau / 'kernel.elf'] +
         [racineProjet / chemin for chemin in spécification['objects']] + ['--start-group'] +
         [lotSécurité if chemin == 'objects/libassh.a' else racineProjet / chemin for chemin in spécification['libraries']] + ['--end-group'])
    exécuterCommande([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', lotNouveau / 'kernel.elf', lotNouveau / 'kernel8.img'])
    fichierHachage = hashlib.sha256((lotNouveau / 'kernel8.img').read_bytes()).hexdigest()
    if arguments.verify and fichierHachage != spécification['kernel_sha256']:
        raise SystemExit('extrémitéReconnecter 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + fichierHachage)
    print('RELINK PASS', fichierHachage, lotNouveau / 'kernel8.img')


if __name__ == '__main__':
    lancer()
