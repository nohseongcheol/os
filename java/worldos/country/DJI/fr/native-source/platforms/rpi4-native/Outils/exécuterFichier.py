#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. Hôte 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from exécuterCommande import commande


def lancer():
    analyseur = argparse.ArgumentParser(description=__doc__)
    analyseur.add_argument('file', type=Path)
    analyseur.add_argument('arguments', nargs='*')
    analyseur.add_argument('--class-name', help='패키지가 있는 .class의 전체 nom(예: valider.testLot)')
    analyseur.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 invoquer ABI valeurUtiliser')
    analyseur.add_argument('--vnc', help='예: 127.0.0.1:2')
    analyseur.add_argument('--include', action='append', type=Path, default=[], help='ajouterFinEntréeÉlément class Fichier 또는 class 디렉터리(패키지 nom retenirValeur)')
    tableauArgument = analyseur.parse_args()
    Données = tableauArgument.file.read_bytes()
    if tableauArgument.class_name and tableauArgument.file.suffix != '.class': analyseur.error('--class-name은 .class 입력에서 사용합니다.')
    nom = tableauArgument.class_name + '.class' if tableauArgument.class_name else tableauArgument.file.name
    if len(Données) > 16384 or not 1 <= len(nom.encode('utf-8')) <= 63 or '\n' in nom or '\r' in nom:
        analyseur.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    valeurCatégorie = '.elf' if Données[:4] == b'\x7fELF' else tableauArgument.file.suffix
    if tableauArgument.linux and valeurCatégorie != '.elf': analyseur.error('--linux는 ELF 바이너리에만 사용합니다.')
    if valeurCatégorie not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        analyseur.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(tableauArgument.arguments) > 7 or any(len(donnéesChaîne.encode('utf-8')) > 255 or '\n' in donnéesChaîne or '\r' in donnéesChaîne for donnéesChaîne in tableauArgument.arguments):
        analyseur.error('인수는 valeurMaximal 7개, 각각 UTF-8 255바이트 이하입니다.')
    options = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if tableauArgument.vnc: options += ['-vnc', tableauArgument.vnc]
    processus = subprocess.Popen(commande() + options, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    sélecteur = selectors.DefaultSelector(); sélecteur.register(processus.stdout, selectors.EVENT_READ)
    def recevoirMessage(marqueur, délaiExpirationExécution=45):
        sortie = bytearray(); décalageFin = time.monotonic() + délaiExpirationExécution
        while marqueur not in sortie:
            if time.monotonic() > décalageFin: raise RuntimeError('UART timeout: ' + sortie.decode('utf-8', 'replace'))
            for valeurEnfoncé, _ in sélecteur.select(0.1):
                valeurFragment = valeurEnfoncé.fileobj.read(4096)
                if valeurFragment: sortie.extend(valeurFragment)
            if b'PANIC:' in sortie or b'FAIL ' in sortie: raise RuntimeError(sortie.decode('utf-8', 'replace'))
            if processus.poll() is not None: raise RuntimeError('QEMU exited: ' + sortie.decode('utf-8', 'replace'))
        return bytes(sortie)
    def envoyer(ligne, marqueur=b'jkoros-native> '):
        processus.stdin.write(ligne.encode('utf-8') + b'\n'); processus.stdin.flush()
        return recevoirMessage(marqueur)
    def exécuterCommande(ligne):
        sortie = envoyer(ligne); sys.stdout.buffer.write(sortie); sys.stdout.buffer.flush()
        estÉgal = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', sortie)
        if not estÉgal: raise RuntimeError('guest did not report exit status')
        return int(estÉgal.group(1))
    try:
        recevoirMessage(b'jkoros-native> ')
        listeFichier = []
        for inclure in tableauArgument.include:
            if inclure.is_dir():
                listeFichier += [(str(positionDonnées.relative_to(inclure).with_suffix('')).replace('/', '.') + '.class', positionDonnées.read_bytes()) for positionDonnées in sorted(inclure.rglob('*.class'))]
            else:
                listeFichier.append((inclure.name, inclure.read_bytes()))
        listeFichier = [(nombreÉlémentsÉlémentListe, donnéesDestination) for nombreÉlémentsÉlémentListe, donnéesDestination in listeFichier if nombreÉlémentsÉlémentListe != nom] + [(nom, Données)]
        for nomTéléverser, donnéesTéléverser in listeFichier:
            if len(donnéesTéléverser) > 16384 or len(nomTéléverser.encode('utf-8')) > 63 or '\n' in nomTéléverser or '\r' in nomTéléverser:
                raise ValueError('ajouterFinEntréeÉlément 파일의 nom/taille valeurLimite 초과: ' + nomTéléverser)
            envoyer('load ' + shlex.quote(nomTéléverser), b'hex> ')
            for indiceOrdinal in range(0, len(donnéesTéléverser), 64): envoyer(donnéesTéléverser[indiceOrdinal:indiceOrdinal+64].hex(), b'hex> ')
            if b'LOADED' not in envoyer('.'): raise RuntimeError('upload failed: ' + nomTéléverser)
            extraitBrut = envoyer('hex ' + shlex.quote(nomTéléverser))
            estÉgal = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', extraitBrut, re.S)
            if not estÉgal or bytes.fromhex(''.join(estÉgal.group(2).decode().split())) != donnéesTéléverser: raise RuntimeError('upload verification failed')
        if valeurCatégorie == '.java' and exécuterCommande('javac ' + shlex.quote(nom)) != 0: return 1
        imageCodeExécutable = tableauArgument.file.stem + '.elf'
        if valeurCatégorie == '.c' and exécuterCommande('cc ' + shlex.quote(nom) + ' -o ' + shlex.quote(imageCodeExécutable)) != 0: return 1
        programme = 'java ' + shlex.quote(tableauArgument.class_name or tableauArgument.file.stem) if valeurCatégorie in ('.java', '.class') else ('python ' if valeurCatégorie == '.py' else 'run ') + shlex.quote(nom)
        if valeurCatégorie == '.jar': programme = 'java -jar ' + shlex.quote(nom)
        if valeurCatégorie == '.c': programme = 'run ' + shlex.quote(imageCodeExécutable)
        if tableauArgument.linux: programme = 'run --linux ' + shlex.quote(nom)
        if tableauArgument.arguments: programme += ' ' + ' '.join(shlex.quote(donnéesChaîne) for donnéesChaîne in tableauArgument.arguments)
        return 0 if exécuterCommande(programme) == 0 else 1
    finally:
        if processus.poll() is None:
            processus.terminate()
            try: processus.wait(timeout=5)
            except subprocess.TimeoutExpired: processus.kill(); processus.wait(timeout=5)
        sélecteur.close(); processus.stdin.close(); processus.stdout.close()


if __name__ == '__main__':
    raise SystemExit(lancer())
