#!/usr/bin/env python3
"""장치별 Makulli_Daraja·haɗi_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def Shirya(기준=기준):
    Hanyar_shiga = 기준 / 'build/remote'
    Hanyar_shiga.mkdir(parents=True, exist_ok=True)
    Saituna = Hanyar_shiga / 'access.json'
    Makulli_Daraja = Hanyar_shiga / 'host-key.der'
    if not Makulli_Daraja.exists():
        with Makulli_Daraja.open('xb') as Fayil:
            os.chmod(str(Makulli_Daraja), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Fayil)
    if not Saituna.exists():
        Tarin_bayani = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Saituna.open('x') as Fayil:
            os.chmod(str(Saituna), 0o600)
            json.dump(Tarin_bayani, Fayil, ensure_ascii=False, indent=2)
            Fayil.write('\n')
    Tarin_bayani = json.loads(Saituna.read_text())
    if not isinstance(Tarin_bayani, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if Tarin_bayani.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Suna in ('ssh_password', 'vnc_password'):
        if not isinstance(Tarin_bayani.get(Suna), str):
            raise SystemExit('access.json: ' + Suna + '는 문자열이어야 합니다.')
    Mai_fayyace_umani_kalmar_sirri = Tarin_bayani['ssh_password'].encode('utf-8')
    if len(Mai_fayyace_umani_kalmar_sirri) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = Tarin_bayani['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. Tsawo_Daraja 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def TSARI_Daraja(Suna, Daraja):
        return 'static const unsigned char '+Suna+'[] = {'+','.join(str(수) for 수 in Daraja)+'};\n'
    머리 = TSARI_Daraja('na_ura_Makulli', Makulli_Daraja.read_bytes())
    머리 += TSARI_Daraja('Mai_fayyace_umani_kalmar_sirri_taƙaitawa', hashlib.sha256(Mai_fayyace_umani_kalmar_sirri).digest())
    머리 += TSARI_Daraja('화면암호', 화면열쇠)
    생성 = Hanyar_shiga / 'furofayil.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return Tarin_bayani


if __name__ == '__main__':
    tatsar_manhaja_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    tatsar_manhaja_48ee4b1b.add_argument('Aiki', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = tatsar_manhaja_48ee4b1b.parse_args()
    Tarin_bayani = Shirya()
    if 인수.Aiki == 'show':
        print(json.dumps(Tarin_bayani, ensure_ascii=False, indent=2))
    else:
        print('장치별 na_nesa_Daraja haɗi_e05f319b Saituna 준비됨. kalmar_sirri_Daraja Tabbatar_da: python3 Kaya/na_nesa_Saituna.py show')
