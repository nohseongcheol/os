#!/usr/bin/env python3
"""장치별 Klucz_WARTOŚĆ·połączenie_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Project_korzeń = Path(__file__).resolve().parents[1]


def Przygotuj(Project_korzeń=Project_korzeń):
    ścieżka_2 = Project_korzeń / 'build/remote'
    ścieżka_2.mkdir(parents=True, exist_ok=True)
    Ustawienia = ścieżka_2 / 'access.json'
    Klucz_WARTOŚĆ = ścieżka_2 / 'host-key.der'
    if not Klucz_WARTOŚĆ.exists():
        with Klucz_WARTOŚĆ.open('xb') as nazwa_pliku:
            os.chmod(str(Klucz_WARTOŚĆ), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=nazwa_pliku)
    if not Ustawienia.exists():
        dane = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Ustawienia.open('x') as nazwa_pliku:
            os.chmod(str(Ustawienia), 0o600)
            json.dump(dane, nazwa_pliku, ensure_ascii=False, indent=2)
            nazwa_pliku.write('\n')
    dane = json.loads(Ustawienia.read_text())
    if not isinstance(dane, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if dane.get('user') != 'user':
        raise SystemExit('access.json: user는 bieżący_towar "user"만 지원합니다.')
    for Nazwa in ('ssh_password', 'vnc_password'):
        if not isinstance(dane.get(Nazwa), str):
            raise SystemExit('access.json: ' + Nazwa + '는 문자열이어야 합니다.')
    powłoka_hasło = dane['ssh_password'].encode('utf-8')
    if len(powłoka_hasło) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = dane['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. długość_WARTOŚĆ 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def TABLICA_WARTOŚĆ(Nazwa, WARTOŚĆ):
        return 'static const unsigned char '+Nazwa+'[] = {'+','.join(str(identyfikator) for identyfikator in WARTOŚĆ)+'};\n'
    머리 = TABLICA_WARTOŚĆ('urządzenie_Klucz', Klucz_WARTOŚĆ.read_bytes())
    머리 += TABLICA_WARTOŚĆ('powłoka_hasło_podsumowanie', hashlib.sha256(powłoka_hasło).digest())
    머리 += TABLICA_WARTOŚĆ('화면암호', 화면열쇠)
    generować = ścieżka_2 / 'Profil.h'
    generować.write_text(머리)
    os.chmod(str(generować), 0o600)
    return dane


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('Akcja', choices=['show', 'prepare'], nargs='?', default='prepare')
    argumenty = parser_48ee4b1b.parse_args()
    dane = Przygotuj()
    if argumenty.Akcja == 'show':
        print(json.dumps(dane, ensure_ascii=False, indent=2))
    else:
        print('장치별 zdalny_WARTOŚĆ połączenie_e05f319b Ustawienia 준비됨. hasło_WARTOŚĆ 확인: python3 narzędzia/zdalny_Ustawienia.py show')
