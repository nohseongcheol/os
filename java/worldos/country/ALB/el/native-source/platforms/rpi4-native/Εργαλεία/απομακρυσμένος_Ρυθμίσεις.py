#!/usr/bin/env python3
"""장치별 Κλειδί_τιμή·σύνδεση_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

έργο_ρίζα = Path(__file__).resolve().parents[1]


def Προετοίμασε(έργο_ρίζα=έργο_ρίζα):
    ΔΙΑΔΡΟΜΗ = έργο_ρίζα / 'build/remote'
    ΔΙΑΔΡΟΜΗ.mkdir(parents=True, exist_ok=True)
    Ρυθμίσεις = ΔΙΑΔΡΟΜΗ / 'access.json'
    Κλειδί_τιμή = ΔΙΑΔΡΟΜΗ / 'host-key.der'
    if not Κλειδί_τιμή.exists():
        with Κλειδί_τιμή.open('xb') as Αρχείο:
            os.chmod(str(Κλειδί_τιμή), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Αρχείο)
    if not Ρυθμίσεις.exists():
        δεδομένα = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Ρυθμίσεις.open('x') as Αρχείο:
            os.chmod(str(Ρυθμίσεις), 0o600)
            json.dump(δεδομένα, Αρχείο, ensure_ascii=False, indent=2)
            Αρχείο.write('\n')
    δεδομένα = json.loads(Ρυθμίσεις.read_text())
    if not isinstance(δεδομένα, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if δεδομένα.get('user') != 'user':
        raise SystemExit('access.json: user는 τρέχων_στοιχείο "user"만 지원합니다.')
    for Όνομα in ('ssh_password', 'vnc_password'):
        if not isinstance(δεδομένα.get(Όνομα), str):
            raise SystemExit('access.json: ' + Όνομα + '는 문자열이어야 합니다.')
    κέλυφος_κωδικός_πρόσβασης = δεδομένα['ssh_password'].encode('utf-8')
    if len(κέλυφος_κωδικός_πρόσβασης) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = δεδομένα['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. διάρκεια_τιμή 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def πίνακας_τιμή(Όνομα, τιμή):
        return 'static const unsigned char '+Όνομα+'[] = {'+','.join(str(수) for 수 in τιμή)+'};\n'
    머리 = πίνακας_τιμή('συσκευή_Κλειδί', Κλειδί_τιμή.read_bytes())
    머리 += πίνακας_τιμή('κέλυφος_κωδικός_πρόσβασης_σύνοψη', hashlib.sha256(κέλυφος_κωδικός_πρόσβασης).digest())
    머리 += πίνακας_τιμή('화면암호', 화면열쇠)
    δημιουργώ = ΔΙΑΔΡΟΜΗ / 'Προφίλ.h'
    δημιουργώ.write_text(머리)
    os.chmod(str(δημιουργώ), 0o600)
    return δεδομένα


if __name__ == '__main__':
    ανάλυση_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ανάλυση_48ee4b1b.add_argument('Ενέργεια', choices=['show', 'prepare'], nargs='?', default='prepare')
    Παράμετροι = ανάλυση_48ee4b1b.parse_args()
    δεδομένα = Προετοίμασε()
    if Παράμετροι.Ενέργεια == 'show':
        print(json.dumps(δεδομένα, ensure_ascii=False, indent=2))
    else:
        print('장치별 απομακρυσμένος_τιμή σύνδεση_e05f319b Ρυθμίσεις 준비됨. κωδικός_πρόσβασης_τιμή επαληθεύω: python3 Εργαλεία/απομακρυσμένος_Ρυθμίσεις.py show')
