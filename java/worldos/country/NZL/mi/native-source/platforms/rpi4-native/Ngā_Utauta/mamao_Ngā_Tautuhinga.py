#!/usr/bin/env python3
"""장치별 kī_uara·hononga_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

whakaatu_pūtake = Path(__file__).resolve().parents[1]


def Whakarite(whakaatu_pūtake=whakaatu_pūtake):
    ara = whakaatu_pūtake / 'build/remote'
    ara.mkdir(parents=True, exist_ok=True)
    Ngā_Tautuhinga = ara / 'access.json'
    kī_uara = ara / 'host-key.der'
    if not kī_uara.exists():
        with kī_uara.open('xb') as Kōnae:
            os.chmod(str(kī_uara), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Kōnae)
    if not Ngā_Tautuhinga.exists():
        raraunga = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Ngā_Tautuhinga.open('x') as Kōnae:
            os.chmod(str(Ngā_Tautuhinga), 0o600)
            json.dump(raraunga, Kōnae, ensure_ascii=False, indent=2)
            Kōnae.write('\n')
    raraunga = json.loads(Ngā_Tautuhinga.read_text())
    if not isinstance(raraunga, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if raraunga.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Ingoa in ('ssh_password', 'vnc_password'):
        if not isinstance(raraunga.get(Ingoa), str):
            raise SystemExit('access.json: ' + Ingoa + '는 문자열이어야 합니다.')
    anga_kupuhipa = raraunga['ssh_password'].encode('utf-8')
    if len(anga_kupuhipa) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = raraunga['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. roa_uara 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def HUĀNGA_uara(Ingoa, uara):
        return 'static const unsigned char '+Ingoa+'[] = {'+','.join(str(수) for 수 in uara)+'};\n'
    머리 = HUĀNGA_uara('pūkoro_kī', kī_uara.read_bytes())
    머리 += HUĀNGA_uara('anga_kupuhipa_whakarāpoto', hashlib.sha256(anga_kupuhipa).digest())
    머리 += HUĀNGA_uara('화면암호', 화면열쇠)
    waihanga = ara / 'Kōtaha.h'
    waihanga.write_text(머리)
    os.chmod(str(waihanga), 0o600)
    return raraunga


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('hohenga', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    raraunga = Whakarite()
    if 인수.hohenga == 'show':
        print(json.dumps(raraunga, ensure_ascii=False, indent=2))
    else:
        print('장치별 mamao_uara hononga_e05f319b Ngā_Tautuhinga 준비됨. kupuhipa_uara manatoko: python3 Ngā_Utauta/mamao_Ngā_Tautuhinga.py show')
