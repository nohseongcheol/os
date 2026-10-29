#!/usr/bin/env python3
"""장치별 khii_boleng·kgokaganya_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def Lokišetša(기준=기준):
    Tsejana = 기준 / 'build/remote'
    Tsejana.mkdir(parents=True, exist_ok=True)
    Dipeakanyo = Tsejana / 'access.json'
    khii_boleng = Tsejana / 'host-key.der'
    if not khii_boleng.exists():
        with khii_boleng.open('xb') as Faele:
            os.chmod(str(khii_boleng), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Faele)
    if not Dipeakanyo.exists():
        data = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Dipeakanyo.open('x') as Faele:
            os.chmod(str(Dipeakanyo), 0o600)
            json.dump(data, Faele, ensure_ascii=False, indent=2)
            Faele.write('\n')
    data = json.loads(Dipeakanyo.read_text())
    if not isinstance(data, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if data.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Leina in ('ssh_password', 'vnc_password'):
        if not isinstance(data.get(Leina), str):
            raise SystemExit('access.json: ' + Leina + '는 문자열이어야 합니다.')
    šele_phasewete = data['ssh_password'].encode('utf-8')
    if len(šele_phasewete) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = data['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. botelele_boleng 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def arei_boleng(Leina, boleng):
        return 'static const unsigned char '+Leina+'[] = {'+','.join(str(수) for 수 in boleng)+'};\n'
    머리 = arei_boleng('sedirišwa_khii', khii_boleng.read_bytes())
    머리 += arei_boleng('šele_phasewete_khutsofatšo', hashlib.sha256(šele_phasewete).digest())
    머리 += arei_boleng('화면암호', 화면열쇠)
    생성 = Tsejana / 'Profaele.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return data


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('Mogato', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    data = Lokišetša()
    if 인수.Mogato == 'show':
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print('장치별 ya_kgole_boleng kgokaganya_e05f319b Dipeakanyo 준비됨. phasewete_boleng kgonthiša: python3 Ditholosi/ya_kgole_Dipeakanyo.py show')
