#!/usr/bin/env python3
"""PyPI matérielPhysique 배포와 부정 valeurEntrée·RAM 되돌림을 interne 커널에서 검사한다."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import selectors
import shutil
import socket
import subprocess
import time
import zipfile
from relayerLot import dépôtLot, décomprimer
from exécuterCommande import racineProjet


def testMolette(nom, entréesListeFichier, valeurContrat='Root-Is-Purelib: true\n', dépendances=''):
    Données = io.BytesIO()
    with zipfile.ZipFile(Données, 'w', zipfile.ZIP_DEFLATED) as Paquet:
        Paquet.writestr(nom + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + valeurContrat)
        Paquet.writestr(nom + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + nom + '\nVersion: 1.0\n' + dépendances)
        for chemin, valeurContenuValeur in entréesListeFichier.items():
            Paquet.writestr(chemin, valeurContenuValeur)
    return Données.getvalue()


def contrôlerHôte():
    estNormal = testMolette('jkoros-fixture', {'mod.py': 'valeur=42\n'})
    assert décomprimer('jkoros_fixture-1.0-py3-none-any.whl', estNormal, 'jkoros-fixture', '1.0') == {'mod.py': 'valeur=42\n'.encode()}
    for Données in (
            testMolette('jkoros-fixture', {'../escape.py': ''}),
            testMolette('jkoros-fixture', {'/abs.py': ''}),
            testMolette('jkoros-fixture', {'big.py': 'x' * 16385}),
            testMolette('jkoros-fixture', {'mod.so': ''}),
            testMolette('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            testMolette('jkoros-fixture', {'mod.py': ''}, dépendances='Requires-Dist: requests\n')):
        try:
            décomprimer('jkoros_fixture-1.0-py3-none-any.whl', Données, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel chemin·taille·C valeurExtension·dépendances rejeterValeur')


def numéroPortVide():
    with socket.socket() as valeurPriseRéseau:
        valeurPriseRéseau.bind(('127.0.0.1', 0))
        return valeurPriseRéseau.getsockname()[1]


def lancer():
    Analyseur = argparse.ArgumentParser(description=__doc__)
    Analyseur.add_argument('--host-only', action='store_true')
    arguments = Analyseur.parse_args()
    contrôlerHôte()
    if arguments.host_only:
        return
    cheminRésultat = racineProjet/'build/verification/pip'
    cheminRésultat.mkdir(parents=True, exist_ok=True)
    cheminStockage = cheminRésultat/'cache'
    cheminStockage.mkdir(exist_ok=True)
    # donnéesEffectif PyPI valeurDistribution Fichier. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    dépôtLot(racineProjet/'build/pip-cache').préparer('micropython-bisect==3.3.3')
    for valeurQueueExtrémité in ('.archive', '.json'):
        shutil.copyfile(str(racineProjet/'build/pip-cache'/('micropython-bisect==3.3.3'+valeurQueueExtrémité)), str(cheminStockage/('micropython-bisect==3.3.3'+valeurQueueExtrémité)))
    journalMatériel = json.loads((cheminStockage/'micropython-bisect==3.3.3.json').read_text())
    assert journalMatériel['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for nom, entréesListeFichier in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .calculRésultat import ajouterValeurs\n', '검증꾸러미/calculRésultat.py': 'def ajouterValeurs(opérandePremier,opérandeDeuxième):\n return opérandePremier+opérandeDeuxième\n'}),
            ('jkoros-space', {'space%d.py' % nombre: 'valeur=1\n' for nombre in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        Données = testMolette(nom, entréesListeFichier)
        (cheminStockage/(nom+'==1.0.archive')).write_bytes(Données)
        (cheminStockage/(nom+'==1.0.json')).write_text(json.dumps({'name': nom, 'version': '1.0',
            'filename': nom.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(Données).hexdigest()}))
    valider = {'passed': False, 'kernel_sha256': hashlib.sha256((racineProjet/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': journalMatériel, 'checks': []}
    numéroPort = numéroPortVide()
    processus = subprocess.Popen(['python3', str(racineProjet/'Outils/exécuterCommande.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(numéroPort), '--pip-cache', str(cheminStockage), '--ftp-port', str(numéroPortVide())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    Sélecteur = selectors.DefaultSelector()
    Sélecteur.register(processus.stdout, selectors.EVENT_READ)
    transcription = bytearray()
    def attendreFin(afficherValeur=b'jkoros-native> '):
        valeurContenuValeur = bytearray()
        terminaison = time.monotonic()+120
        while afficherValeur not in valeurContenuValeur:
            if time.monotonic() > terminaison or processus.poll() is not None:
                raise AssertionError('게스트 réponse méthodeManquant: '+valeurContenuValeur.decode('utf-8','replace'))
            for valeurEntréeÉlément, _ in Sélecteur.select(.1):
                valeurFragment = valeurEntréeÉlément.fileobj.read(4096)
                valeurContenuValeur.extend(valeurFragment)
                transcription.extend(valeurFragment)
        return valeurContenuValeur.decode('utf-8', 'replace').replace('\r\n','\n')
    def interpréteurCommandes(commande, afficherValeur=b'jkoros-native> '):
        processus.stdin.write(commande.encode()+b'\n')
        processus.stdin.flush()
        return attendreFin(afficherValeur)
    def exécuterCommande(commande, valeursAttendu, valeurÉtatValeur=0):
        valeurContenuValeur = interpréteurCommandes(commande)
        assert valeursAttendu in valeurContenuValeur and '\nexit '+str(valeurÉtatValeur)+'\n' in valeurContenuValeur, valeurContenuValeur
        valider['checks'].append(commande)
        return valeurContenuValeur
    def fichiersTéléverser(nom, Données):
        interpréteurCommandes('load '+nom, b'hex> ')
        for indicePosition in range(0, len(Données), 64):
            interpréteurCommandes(Données[indicePosition:indicePosition+64].hex(), b'hex> ')
        assert 'LOADED' in interpréteurCommandes('.')
    try:
        attendreFin()
        exécuterCommande('pip --help', 'MicroPython arbreSource 설치기')
        fichiersTéléverser('오류시험.py', (racineProjet/'Tests/Python/TestErreurCoréen.py').read_bytes())
        exécuterCommande('python 오류시험.py', 'français Fichier exception vérifier')
        exécuterCommande('pip install micropython-bisect==3.3.3 --port '+str(numéroPort), 'installerValeur estTerminé: micropython-bisect 3.3.3')
        exécuterCommande('python -c \'from bisect import insort as 순서대로넣기; valeur=[1,5]; 순서대로넣기(valeur,3); print(valeur)\'', '[1, 3, 5]')
        exécuterCommande('python -m pip list', 'micropython-bisect 3.3.3')
        exécuterCommande('pip install micropython-bisect==3.3.3 --port '+str(numéroPort), '이미 설치됨:')
        exécuterCommande('pip install jkoros-fixture==1.0 --port '+str(numéroPort), 'installerValeur estTerminé: jkoros-fixture')
        exécuterCommande('python -c \'from 검증꾸러미 import ajouterValeurs; print(ajouterValeurs(20,22))\'', '\n42\n')
        exécuterCommande('pip install jkoros-syntax==1.0 --port '+str(numéroPort), 'Paquet erreur:', 1)
        exécuterCommande('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 erreur 보존")\'', '구문 erreur 보존')
        fichiersTéléverser('공간시험.py', (racineProjet/'Tests/Python/TestEspaceNomsLot.py').read_bytes())
        exécuterCommande('python 공간시험.py '+str(numéroPort), 'Paquet régionAdresse 부족 pontRetourner vérifier')
        exécuterCommande('pip uninstall jkoros-fixture', 'supprimerEntréeÉlément estTerminé: jkoros-fixture')
        exécuterCommande('pip uninstall micropython-bisect', 'supprimerEntréeÉlément estTerminé: micropython-bisect')
        exécuterCommande('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("supprimerEntréeÉlément vérifier")\'', 'supprimerEntréeÉlément vérifier')
        valider['passed'] = True
        print('PASS: PyPI matérielPhysique installerValeur·import·exécuterCommande, français exception, 패키지 valeurRépertoire, valeurÉchec pontRetourner, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 programmeQuitter 키로 QEMU를 끝내면 실행기의 relayerValeur 문맥도 정리된다.
            processus.stdin.write(b'\x01x')
            processus.stdin.flush()
            processus.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            processus.terminate()
            try:
                processus.wait(timeout=8)
            except subprocess.TimeoutExpired:
                processus.kill()
                processus.wait()
        if processus.poll() is None:
            processus.kill()
            processus.wait()
        Sélecteur.close()
        processus.stdin.close()
        processus.stdout.close()
        (cheminRésultat/'serial.log').write_bytes(transcription)
        (cheminRésultat/'report.json').write_text(json.dumps(valider, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    lancer()
