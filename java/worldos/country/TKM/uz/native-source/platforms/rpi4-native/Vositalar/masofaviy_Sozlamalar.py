#!/usr/bin/env python3
"""장치별 Kalit_VALUE·aloqa_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Project_ildiz = Path(__file__).resolve().parents[1]


def Tayyorlamoq(Project_ildiz=Project_ildiz):
    yo_l = Project_ildiz / 'build/remote'
    yo_l.mkdir(parents=True, exist_ok=True)
    Moslamalar = yo_l / 'access.json'
    Kalit_VALUE = yo_l / 'host-key.der'
    if not Kalit_VALUE.exists():
        with Kalit_VALUE.open('xb') as Fayl:
            os.chmod(str(Kalit_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Fayl)
    if not Moslamalar.exists():
        ma_lumotlar = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Moslamalar.open('x') as Fayl:
            os.chmod(str(Moslamalar), 0o600)
            json.dump(ma_lumotlar, Fayl, ensure_ascii=False, indent=2)
            Fayl.write('\n')
    ma_lumotlar = json.loads(Moslamalar.read_text())
    if not isinstance(ma_lumotlar, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if ma_lumotlar.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Nomi in ('ssh_password', 'vnc_password'):
        if not isinstance(ma_lumotlar.get(Nomi), str):
            raise SystemExit('access.json: ' + Nomi + '는 문자열이어야 합니다.')
    qobiq_parol = ma_lumotlar['ssh_password'].encode('utf-8')
    if len(qobiq_parol) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = ma_lumotlar['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. uzunlik_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(Nomi, VALUE):
        return 'static const unsigned char '+Nomi+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = ARRAY_VALUE('qurilma_Kalit', Kalit_VALUE.read_bytes())
    머리 += ARRAY_VALUE('qobiq_parol_xulosa', hashlib.sha256(qobiq_parol).digest())
    머리 += ARRAY_VALUE('화면암호', 화면열쇠)
    generatsiiyalash = yo_l / 'Profil.h'
    generatsiiyalash.write_text(머리)
    os.chmod(str(generatsiiyalash), 0o600)
    return ma_lumotlar


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('Amal', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = parser_48ee4b1b.parse_args()
    ma_lumotlar = Tayyorlamoq()
    if 인수.Amal == 'show':
        print(json.dumps(ma_lumotlar, ensure_ascii=False, indent=2))
    else:
        print('장치별 masofaviy_VALUE aloqa_e05f319b Moslamalar 준비됨. parol_VALUE tasdiqlamoq: python3 Vositalar/masofaviy_Sozlamalar.py show')
