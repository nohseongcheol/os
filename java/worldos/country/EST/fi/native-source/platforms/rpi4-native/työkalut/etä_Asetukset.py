#!/usr/bin/env python3
"""장치별 Avain_ARVO·yhteys_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

aloite_juuri = Path(__file__).resolve().parents[1]


def Valmistele(aloite_juuri=aloite_juuri):
    polku_2 = aloite_juuri / 'build/remote'
    polku_2.mkdir(parents=True, exist_ok=True)
    Asetukset = polku_2 / 'access.json'
    Avain_ARVO = polku_2 / 'host-key.der'
    if not Avain_ARVO.exists():
        with Avain_ARVO.open('xb') as tiedoston_nimi:
            os.chmod(str(Avain_ARVO), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=tiedoston_nimi)
    if not Asetukset.exists():
        data = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Asetukset.open('x') as tiedoston_nimi:
            os.chmod(str(Asetukset), 0o600)
            json.dump(data, tiedoston_nimi, ensure_ascii=False, indent=2)
            tiedoston_nimi.write('\n')
    data = json.loads(Asetukset.read_text())
    if not isinstance(data, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if data.get('user') != 'user':
        raise SystemExit('access.json: user는 nykyinen_kohde "user"만 지원합니다.')
    for Nimi in ('ssh_password', 'vnc_password'):
        if not isinstance(data.get(Nimi), str):
            raise SystemExit('access.json: ' + Nimi + '는 문자열이어야 합니다.')
    liittymä_salasana = data['ssh_password'].encode('utf-8')
    if len(liittymä_salasana) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = data['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. kesto_ARVO 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def MATRIISI_ARVO(Nimi, ARVO):
        return 'static const unsigned char '+Nimi+'[] = {'+','.join(str(numero) for numero in ARVO)+'};\n'
    머리 = MATRIISI_ARVO('laite_Avain', Avain_ARVO.read_bytes())
    머리 += MATRIISI_ARVO('liittymä_salasana_yhteenveto', hashlib.sha256(liittymä_salasana).digest())
    머리 += MATRIISI_ARVO('화면암호', 화면열쇠)
    generoida = polku_2 / 'Profiili.h'
    generoida.write_text(머리)
    os.chmod(str(generoida), 0o600)
    return data


if __name__ == '__main__':
    jäsennin_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    jäsennin_48ee4b1b.add_argument('Toiminto', choices=['show', 'prepare'], nargs='?', default='prepare')
    argumentit = jäsennin_48ee4b1b.parse_args()
    data = Valmistele()
    if argumentit.Toiminto == 'show':
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print('장치별 etä_ARVO yhteys_e05f319b Asetukset 준비됨. salasana_ARVO tarkistaa: python3 työkalut/etä_Asetukset.py show')
