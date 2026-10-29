#!/usr/bin/env python3
"""장치별 valeurTouche·connexion 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

racineProjet = Path(__file__).resolve().parents[1]


def préparer(racineProjet=racineProjet):
    chemin = racineProjet / 'build/remote'
    chemin.mkdir(parents=True, exist_ok=True)
    réglages = chemin / 'access.json'
    valeurTouche = chemin / 'host-key.der'
    if not valeurTouche.exists():
        with valeurTouche.open('xb') as Fichier:
            os.chmod(str(valeurTouche), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Fichier)
    if not réglages.exists():
        Données = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with réglages.open('x') as Fichier:
            os.chmod(str(réglages), 0o600)
            json.dump(Données, Fichier, ensure_ascii=False, indent=2)
            Fichier.write('\n')
    Données = json.loads(réglages.read_text())
    if not isinstance(Données, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if Données.get('user') != 'user':
        raise SystemExit('access.json: user는 élémentListeActuel "user"만 지원합니다.')
    for nom in ('ssh_password', 'vnc_password'):
        if not isinstance(Données.get(nom), str):
            raise SystemExit('access.json: ' + nom + '는 문자열이어야 합니다.')
    motPasseInterpréteurCommandes = Données['ssh_password'].encode('utf-8')
    if len(motPasseInterpréteurCommandes) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        motPasseÉcran = Données['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. longueur 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    toucheÉcran = motPasseÉcran[:8].ljust(8, b'\0')
    def valeurTableau(nom, valeur):
        return 'static const unsigned char '+nom+'[] = {'+','.join(str(nombre) for nombre in valeur)+'};\n'
    valeurTête = valeurTableau('touchePériphérique', valeurTouche.read_bytes())
    valeurTête += valeurTableau('résuméMotPasseInterpréteurCommandes', hashlib.sha256(motPasseInterpréteurCommandes).digest())
    valeurTête += valeurTableau('motPasseÉcran', toucheÉcran)
    générer = chemin / 'profil.h'
    générer.write_text(valeurTête)
    os.chmod(str(générer), 0o600)
    return Données


if __name__ == '__main__':
    Analyseur = argparse.ArgumentParser(description=__doc__)
    Analyseur.add_argument('action', choices=['show', 'prepare'], nargs='?', default='prepare')
    arguments = Analyseur.parse_args()
    Données = préparer()
    if arguments.action == 'show':
        print(json.dumps(Données, ensure_ascii=False, indent=2))
    else:
        print('장치별 valeurDistant connexion réglages estPréparé. valeurMotPasse vérifier: python3 Outils/réglagesDistant.py show')
