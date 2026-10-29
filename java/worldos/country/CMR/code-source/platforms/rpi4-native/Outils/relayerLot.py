#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost relayerValeur. 게스트는 TCP로 받은 소스를 직접 installerValeur·실행한다."""
import argparse
import email.parser
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import socketserver
import struct
import tarfile
import threading
import urllib.request
import zipfile

racineProjet = Path(__file__).resolve().parents[1]


def analyserRequête(requête):
    estCorrespondant = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', requête)
    if not estCorrespondant:
        raise ValueError('Paquet nom 또는 nom==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', estCorrespondant[1]).lower(), estCorrespondant[2]


def validerChemin(nom, cheminInstallation=True):
    chemin = PurePosixPath(nom)
    if chemin.is_absolute() or any(valeurSousPartie in ('', '.', '..') or valeurSousPartie.startswith('.') for valeurSousPartie in nom.split('/')):
        raise ValueError('허용하지 않는 Paquet chemin: ' + nom)
    if '\\' in nom or any(ord(valeurCaractère) < 32 or ord(valeurCaractère) == 127 for valeurCaractère in nom):
        raise ValueError('잘못된 Paquet chemin Caractères')
    if cheminInstallation and (len(('/lib/' + nom).encode()) > 63 or nom in ('français.py', 'Paquet.py')):
        raise ValueError('Paquet chemin valeurLimite 또는 valeurDéfaut bibliothèque 충돌: ' + nom)
    return nom


def décomprimer(nomEntréeÉlémentFichier, Données, nom, valeurVersion):
    entréesListeFichier = {}
    spécifications = []
    def ajouterFinEntréeÉlément(chemin, valeurContenuValeur):
        validerChemin(chemin)
        if chemin in entréesListeFichier:
            raise ValueError('중복 Paquet chemin: ' + chemin)
        if len(valeurContenuValeur) > 16384:
            raise ValueError('파일당 16 KiB valeurLimite 초과: ' + chemin)
        valeurContenuValeur.decode('utf-8')
        entréesListeFichier[chemin] = valeurContenuValeur
        if len(entréesListeFichier) > 16 or sum(map(len, entréesListeFichier.values())) > 65536:
            raise ValueError('꾸러미는 arbreSource 16개·valeurTotal 64 KiB 이하여야 합니다.')
    if nomEntréeÉlémentFichier.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(Données)) as Paquet:
            listeEntréesListe = Paquet.infolist()
            if len(listeEntréesListe) > 256 or sum(valeurEntréeÉlément.file_size for valeurEntréeÉlément in listeEntréesListe) > 1048576:
                raise ValueError('valeurArchive libérerStockage taille valeurLimite 초과')
            listeContrat = [valeurEntréeÉlément for valeurEntréeÉlément in listeEntréesListe if valeurEntréeÉlément.filename.endswith('.dist-info/WHEEL')]
            if len(listeContrat) != 1:
                raise ValueError('wheel valeurContrat 명세가 필요합니다.')
            valeurContrat = email.parser.Parser().parsestr(Paquet.read(listeContrat[0]).decode())
            if valeurContrat.get('Root-Is-Purelib', '').lower() != 'true' or not nomEntréeÉlémentFichier.endswith('-none-any.whl'):
                raise ValueError('C valeurExtension·플랫폼 전용 wheel은 지원하지 않습니다.')
            for valeurEntréeÉlément in listeEntréesListe:
                chemin = valeurEntréeÉlément.filename.rstrip('/')
                validerChemin(chemin, False)
                if (valeurEntréeÉlément.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 nombre 없습니다.')
                if valeurEntréeÉlément.filename.endswith('/'):
                    continue
                if '.dist-info/' in chemin:
                    if chemin.endswith('/METADATA'):
                        spécifications.append(Paquet.read(valeurEntréeÉlément).decode())
                    continue
                if not chemin.endswith('.py') or '.data/' in chemin:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + chemin)
                ajouterFinEntréeÉlément(chemin, Paquet.read(valeurEntréeÉlément))
    elif nomEntréeÉlémentFichier.endswith('.tar.gz') and nom.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py exécuterCommande 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(Données), mode='r|gz') as Paquet:
            listeRacines = set()
            nombreÉlémentsEntréeÉlément = 0
            tailleTotal = 0
            for valeurEntréeÉlément in Paquet:
                nombreÉlémentsEntréeÉlément += 1
                tailleTotal += valeurEntréeÉlément.size
                if nombreÉlémentsEntréeÉlément > 256 or tailleTotal > 1048576:
                    raise ValueError('valeurArchive libérerStockage taille valeurLimite 초과')
                validerChemin(valeurEntréeÉlément.name, False)
                parties = valeurEntréeÉlément.name.split('/')
                listeRacines.add(parties[0])
                if valeurEntréeÉlément.isdir():
                    continue
                if not valeurEntréeÉlément.isfile() or len(parties) < 2:
                    raise ValueError('잘못된 MicroPython arbreSource 배포형')
                chemin = '/'.join(parties[1:])
                valeurContenuValeur = Paquet.extractfile(valeurEntréeÉlément).read()
                if chemin.endswith('PKG-INFO'):
                    spécifications.append(valeurContenuValeur.decode())
                elif chemin.endswith('.py') and chemin not in ('setup.py',):
                    ajouterFinEntréeÉlément(chemin, valeurContenuValeur)
                elif '.egg-info/' not in chemin and not chemin.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + chemin)
            if len(listeRacines) != 1:
                raise ValueError('MicroPython 소스의 valeurRacine 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* arbreSource 배포형이 필요합니다.')
    if not entréesListeFichier or len(spécifications) != 1:
        raise ValueError('소스와 valeurDistribution 메타데이터가 필요합니다.')
    spécification = email.parser.Parser().parsestr(spécifications[0])
    if analyserRequête(spécification.get('Name', ''))[0] != nom or spécification.get('Version') != valeurVersion:
        raise ValueError('valeurDistribution 메타데이터의 nom·버전 불일치')
    if spécification.get_all('Requires-Dist') or spécification.get_all('Requires'):
        raise ValueError('자동 dépendances 해결은 아직 지원하지 않습니다. dépendances 없는 호환 꾸러미를 사용하십시오.')
    return entréesListeFichier


def lireWeb(adresse, limiteCapacité):
    if not adresse.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS valeurDistribution 주소만 허용합니다.')
    with urllib.request.urlopen(adresse, timeout=30) as réponse:
        if not réponse.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 valeurDistribution adresse valeurDéplacer')
        Données = réponse.read(limiteCapacité + 1)
    if len(Données) > limiteCapacité:
        raise ValueError('valeurDistribution Fichier taille valeurLimite 초과')
    return Données


def lotTransfert(nom, valeurVersion, entréesListeFichier, valeurOrigine):
    spécification = {'name': nom, 'version': valeurVersion, 'source': valeurOrigine, 'files': [
        {'path': chemin, 'size': len(Données), 'sha256': hashlib.sha256(Données).hexdigest()}
        for chemin, Données in sorted(entréesListeFichier.items())]}
    valeurTête = json.dumps(spécification, ensure_ascii=False).encode()
    if len(valeurTête) > 8192:
        raise ValueError('Paquet spécification taille 초과')
    return b'JKP1' + struct.pack('>I', len(valeurTête)) + valeurTête + b''.join(entréesListeFichier[valeurEntréeÉlément['path']] for valeurEntréeÉlément in spécification['files'])


class dépôtLot:
    def __init__(valeurSoi, chemin, estHorsLigne=False):
        valeurSoi.chemin = Path(chemin)
        valeurSoi.chemin.mkdir(parents=True, exist_ok=True)
        valeurSoi.estHorsLigne = estHorsLigne

    def préparer(valeurSoi, requête):
        nom, valeurVersion = analyserRequête(requête)
        matériauTouche = nom + ('==' + valeurVersion if valeurVersion else '')
        cheminJournal = valeurSoi.chemin / (matériauTouche + '.json')
        cheminDistribution = valeurSoi.chemin / (matériauTouche + '.archive')
        if cheminJournal.is_file() and cheminDistribution.is_file():
            enregistrementJournal = json.loads(cheminJournal.read_text())
            Données = cheminDistribution.read_bytes()
            if hashlib.sha256(Données).hexdigest() != enregistrementJournal['sha256']:
                raise ValueError('저장된 valeurDistribution 파일의 SHA-256 불일치')
        else:
            if valeurSoi.estHorsLigne:
                raise ValueError('estHorsLigne 저장소에 없는 Paquet: ' + requête)
            adresse = 'https://pypi.org/pypi/' + nom + ('/' + valeurVersion if valeurVersion else '') + '/json'
            informationSystème = json.loads(lireWeb(adresse, 4194304).decode())
            if informationSystème['info'].get('requires_dist'):
                raise ValueError('자동 dépendances 해결은 아직 지원하지 않습니다.')
            candidat = [valeurEntréeÉlément for valeurEntréeÉlément in informationSystème['urls'] if not valeurEntréeÉlément.get('yanked') and valeurEntréeÉlément['filename'].endswith('-none-any.whl')]
            if not candidat and nom.startswith('micropython-'):
                candidat = [valeurEntréeÉlément for valeurEntréeÉlément in informationSystème['urls'] if not valeurEntréeÉlément.get('yanked') and valeurEntréeÉlément['filename'].endswith('.tar.gz')]
            if not candidat:
                raise ValueError('지원되는 순수 Python valeurDistribution 파일이 없습니다.')
            valeurSélection = candidat[0]
            Données = lireWeb(valeurSélection['url'], 4194304)
            if hashlib.sha256(Données).hexdigest() != valeurSélection['digests']['sha256']:
                raise ValueError('PyPI valeurDistribution Fichier SHA-256 불일치')
            enregistrementJournal = {'name': nom, 'version': informationSystème['info']['version'], 'filename': valeurSélection['filename'],
                    'url': valeurSélection['url'], 'sha256': valeurSélection['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            décomprimer(enregistrementJournal['filename'], Données, nom, enregistrementJournal['version'])
            cheminDistribution.write_bytes(Données)
            cheminJournal.write_text(json.dumps(enregistrementJournal, ensure_ascii=False, indent=2) + '\n')
        if enregistrementJournal['name'] != nom or valeurVersion and enregistrementJournal['version'] != valeurVersion:
            raise ValueError('racineDépôt nom·버전 불일치')
        entréesListeFichier = décomprimer(enregistrementJournal['filename'], Données, nom, enregistrementJournal['version'])
        return lotTransfert(nom, enregistrementJournal['version'], entréesListeFichier, enregistrementJournal['url'])


class requêteLot(socketserver.BaseRequestHandler):
    def handle(valeurSoi):
        valeurSoi.request.settimeout(10)
        try:
            requête = bytearray()
            while b'\n' not in requête and len(requête) < 100:
                valeurFragment = valeurSoi.request.recv(100 - len(requête))
                if not valeurFragment:
                    return
                requête.extend(valeurFragment)
            if not requête.endswith(b'\n') or requête.count(b'\n') != 1:
                raise ValueError('잘못된 Paquet requête')
            réponse = valeurSoi.server.racineDépôt.préparer(requête[:-1].decode('ascii'))
        except Exception as erreur:
            valeurTête = json.dumps({'error': str(erreur)[:500]}, ensure_ascii=False).encode()
            réponse = b'JKP1' + struct.pack('>I', len(valeurTête)) + valeurTête
        try:
            valeurSoi.request.sendall(réponse)
        except OSError:
            pass


class relayerLot:
    def __init__(valeurSoi, numéroPort=8027, chemin=None, estHorsLigne=False):
        valeurSoi.valeurServeur = socketserver.TCPServer(('127.0.0.1', numéroPort), requêteLot, bind_and_activate=False)
        valeurSoi.valeurServeur.allow_reuse_address = True
        valeurSoi.valeurServeur.server_bind()
        valeurSoi.valeurServeur.server_activate()
        valeurSoi.valeurServeur.racineDépôt = dépôtLot(chemin or racineProjet/'build/pip-cache', estHorsLigne)
        valeurSoi.numéroPort = valeurSoi.valeurServeur.server_address[1]
        valeurSoi.valeurFilExécution = threading.Thread(target=valeurSoi.valeurServeur.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(valeurSoi):
        valeurSoi.valeurFilExécution.start()
        return valeurSoi

    def __exit__(valeurSoi, *arguments):
        valeurSoi.valeurServeur.shutdown()
        valeurSoi.valeurServeur.server_close()
        valeurSoi.valeurFilExécution.join(timeout=2)


def lancer():
    Analyseur = argparse.ArgumentParser(description=__doc__)
    Analyseur.add_argument('--port', type=int, default=8027)
    Analyseur.add_argument('--cache', type=Path, default=racineProjet/'build/pip-cache')
    Analyseur.add_argument('--offline', action='store_true')
    Analyseur.add_argument('--fetch', help='exécuterCommande 없이 호환 valeurDistribution 파일을 내려받아 Contrôles·valeurStocker')
    arguments = Analyseur.parse_args()
    if arguments.fetch:
        Données = dépôtLot(arguments.cache, arguments.offline).préparer(arguments.fetch)
        print('Paquet préparer estTerminé:', arguments.fetch, len(Données), 'valeurOctet')
        return
    with relayerLot(arguments.port, arguments.cache, arguments.offline) as relayerValeur:
        print('Paquet relayerValeur: 127.0.0.1:' + str(relayerValeur.numéroPort), flush=True)
        try:
            relayerValeur.valeurFilExécution.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    lancer()
