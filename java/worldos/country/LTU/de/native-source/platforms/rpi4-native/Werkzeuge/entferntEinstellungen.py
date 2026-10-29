#!/usr/bin/env python3
"""장치별 tasteWert·verbindung 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

projektWurzel = Path(__file__).resolve().parents[1]


def vorbereiten(projektWurzel=projektWurzel):
    pfad = projektWurzel / 'build/remote'
    pfad.mkdir(parents=True, exist_ok=True)
    einstellungen = pfad / 'access.json'
    tasteWert = pfad / 'host-key.der'
    if not tasteWert.exists():
        with tasteWert.open('xb') as Datei:
            os.chmod(str(tasteWert), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Datei)
    if not einstellungen.exists():
        Daten = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with einstellungen.open('x') as Datei:
            os.chmod(str(einstellungen), 0o600)
            json.dump(Daten, Datei, ensure_ascii=False, indent=2)
            Datei.write('\n')
    Daten = json.loads(einstellungen.read_text())
    if not isinstance(Daten, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if Daten.get('user') != 'user':
        raise SystemExit('access.json: user는 aktuellElementeintrag "user"만 지원합니다.')
    for Name in ('ssh_password', 'vnc_password'):
        if not isinstance(Daten.get(Name), str):
            raise SystemExit('access.json: ' + Name + '는 문자열이어야 합니다.')
    befehlshüllePasswort = Daten['ssh_password'].encode('utf-8')
    if len(befehlshüllePasswort) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        bildschirmPasswort = Daten['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. Länge 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    bildschirmTaste = bildschirmPasswort[:8].ljust(8, b'\0')
    def datenfeldWert(Name, Wert):
        return 'static const unsigned char '+Name+'[] = {'+','.join(str(Zahl) for Zahl in Wert)+'};\n'
    kopfWert = datenfeldWert('gerätTaste', tasteWert.read_bytes())
    kopfWert += datenfeldWert('befehlshüllePasswortZusammenfassung', hashlib.sha256(befehlshüllePasswort).digest())
    kopfWert += datenfeldWert('bildschirmPasswort', bildschirmTaste)
    generieren = pfad / 'profil.h'
    generieren.write_text(kopfWert)
    os.chmod(str(generieren), 0o600)
    return Daten


if __name__ == '__main__':
    Strukturanalysierer = argparse.ArgumentParser(description=__doc__)
    Strukturanalysierer.add_argument('aktion', choices=['show', 'prepare'], nargs='?', default='prepare')
    argumente = Strukturanalysierer.parse_args()
    Daten = vorbereiten()
    if argumente.aktion == 'show':
        print(json.dumps(Daten, ensure_ascii=False, indent=2))
    else:
        print('장치별 entferntWert verbindung einstellungen istVorbereitet. passwortWert überprüfen: python3 Werkzeuge/entferntEinstellungen.py show')
