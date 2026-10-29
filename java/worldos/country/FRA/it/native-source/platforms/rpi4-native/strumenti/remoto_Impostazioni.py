#!/usr/bin/env python3
"""장치별 tasto_VALORE·connessione_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

azione_radice = Path(__file__).resolve().parents[1]


def Prepara(azione_radice=azione_radice):
    percorso = azione_radice / 'build/remote'
    percorso.mkdir(parents=True, exist_ok=True)
    Impostazioni = percorso / 'access.json'
    tasto_VALORE = percorso / 'host-key.der'
    if not tasto_VALORE.exists():
        with tasto_VALORE.open('xb') as file:
            os.chmod(str(tasto_VALORE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=file)
    if not Impostazioni.exists():
        dati = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Impostazioni.open('x') as file:
            os.chmod(str(Impostazioni), 0o600)
            json.dump(dati, file, ensure_ascii=False, indent=2)
            file.write('\n')
    dati = json.loads(Impostazioni.read_text())
    if not isinstance(dati, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if dati.get('user') != 'user':
        raise SystemExit('access.json: user는 Regolari_articolo "user"만 지원합니다.')
    for Nome in ('ssh_password', 'vnc_password'):
        if not isinstance(dati.get(Nome), str):
            raise SystemExit('access.json: ' + Nome + '는 문자열이어야 합니다.')
    Shell_password = dati['ssh_password'].encode('utf-8')
    if len(Shell_password) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        schermata_password = dati['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. durata_VALORE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    schermata_tasto = schermata_password[:8].ljust(8, b'\0')
    def array_VALORE(Nome, VALORE):
        return 'static const unsigned char '+Nome+'[] = {'+','.join(str(numero) for numero in VALORE)+'};\n'
    intestazione_VALORE = array_VALORE('cellulare_tasto', tasto_VALORE.read_bytes())
    intestazione_VALORE += array_VALORE('Shell_password_riepilogo', hashlib.sha256(Shell_password).digest())
    intestazione_VALORE += array_VALORE('schermata_password', schermata_tasto)
    generare = percorso / 'Profilo.h'
    generare.write_text(intestazione_VALORE)
    os.chmod(str(generare), 0o600)
    return dati


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('Azione', choices=['show', 'prepare'], nargs='?', default='prepare')
    argomenti = parser_48ee4b1b.parse_args()
    dati = Prepara()
    if argomenti.Azione == 'show':
        print(json.dumps(dati, ensure_ascii=False, indent=2))
    else:
        print('장치별 remoto_VALORE connessione_e05f319b Impostazioni 준비됨. password_VALORE verificare: python3 strumenti/remoto_Impostazioni.py show')
