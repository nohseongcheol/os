#!/usr/bin/env python3
"""장치별 taetsi_Boleng·Kgolagano_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def Baakanya(기준=기준):
    tsela = 기준 / 'build/remote'
    tsela.mkdir(parents=True, exist_ok=True)
    Diseting = tsela / 'access.json'
    taetsi_Boleng = tsela / 'host-key.der'
    if not taetsi_Boleng.exists():
        with taetsi_Boleng.open('xb') as faele:
            os.chmod(str(taetsi_Boleng), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=faele)
    if not Diseting.exists():
        tshedimosetso = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Diseting.open('x') as faele:
            os.chmod(str(Diseting), 0o600)
            json.dump(tshedimosetso, faele, ensure_ascii=False, indent=2)
            faele.write('\n')
    tshedimosetso = json.loads(Diseting.read_text())
    if not isinstance(tshedimosetso, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if tshedimosetso.get('user') != 'user':
        raise SystemExit('access.json: user는 ga_jaana_selwana "user"만 지원합니다.')
    for leina in ('ssh_password', 'vnc_password'):
        if not isinstance(tshedimosetso.get(leina), str):
            raise SystemExit('access.json: ' + leina + '는 문자열이어야 합니다.')
    setlhalosataelo_khoututseno = tshedimosetso['ssh_password'].encode('utf-8')
    if len(setlhalosataelo_khoututseno) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = tshedimosetso['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. boleele_Boleng 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def setlhopha_Boleng_ed437109(leina, Boleng):
        return 'static const unsigned char '+leina+'[] = {'+','.join(str(수) for 수 in Boleng)+'};\n'
    머리 = setlhopha_Boleng_ed437109('mobaele_taetsi', taetsi_Boleng.read_bytes())
    머리 += setlhopha_Boleng_ed437109('setlhalosataelo_khoututseno_tshobokanyo', hashlib.sha256(setlhalosataelo_khoututseno).digest())
    머리 += setlhopha_Boleng_ed437109('화면암호', 화면열쇠)
    생성 = tsela / 'Porofaele.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return tshedimosetso


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('tiro', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    tshedimosetso = Baakanya()
    if 인수.tiro == 'show':
        print(json.dumps(tshedimosetso, ensure_ascii=False, indent=2))
    else:
        print('장치별 kgakala_Boleng Kgolagano_e05f319b Diseting 준비됨. khoututseno_Boleng netefatsa: python3 Thuluse/kgakala_Diseting.py show')
