#!/usr/bin/env python3
"""장치별 કી_મૂલ્ય·કનેક્શન_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

પ્રોજેક્ટ_રૂટ = Path(__file__).resolve().parents[1]


def તૈયાર_કરો(પ્રોજેક્ટ_રૂટ=પ્રોજેક્ટ_રૂટ):
    પથ = પ્રોજેક્ટ_રૂટ / 'build/remote'
    પથ.mkdir(parents=True, exist_ok=True)
    સુયોજના = પથ / 'access.json'
    કી_મૂલ્ય = પથ / 'host-key.der'
    if not કી_મૂલ્ય.exists():
        with કી_મૂલ્ય.open('xb') as ફાઈલ:
            os.chmod(str(કી_મૂલ્ય), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ફાઈલ)
    if not સુયોજના.exists():
        ડેટા = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with સુયોજના.open('x') as ફાઈલ:
            os.chmod(str(સુયોજના), 0o600)
            json.dump(ડેટા, ફાઈલ, ensure_ascii=False, indent=2)
            ફાઈલ.write('\n')
    ડેટા = json.loads(સુયોજના.read_text())
    if not isinstance(ડેટા, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if ડેટા.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for નામ in ('ssh_password', 'vnc_password'):
        if not isinstance(ડેટા.get(નામ), str):
            raise SystemExit('access.json: ' + નામ + '는 문자열이어야 합니다.')
    શેલ_પાસવર્ડ = ડેટા['ssh_password'].encode('utf-8')
    if len(શેલ_પાસવર્ડ) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = ડેટા['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. લંબાઈ_મૂલ્ય 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def અરે_મૂલ્ય(નામ, મૂલ્ય):
        return 'static const unsigned char '+નામ+'[] = {'+','.join(str(수) for 수 in મૂલ્ય)+'};\n'
    머리 = અરે_મૂલ્ય('ડિવાઇસ_કી', કી_મૂલ્ય.read_bytes())
    머리 += અરે_મૂલ્ય('셸암호요약', hashlib.sha256(શેલ_પાસવર્ડ).digest())
    머리 += અરે_મૂલ્ય('화면암호', 화면열쇠)
    જનરેટ_કરો = પથ / 'પ્રોફાઇલ.h'
    જનરેટ_કરો.write_text(머리)
    os.chmod(str(જનરેટ_કરો), 0o600)
    return ડેટા


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('ક્રિયા', choices=['show', 'prepare'], nargs='?', default='prepare')
    દલીલો = 해석기.parse_args()
    ડેટા = તૈયાર_કરો()
    if દલીલો.ક્રિયા == 'show':
        print(json.dumps(ડેટા, ensure_ascii=False, indent=2))
    else:
        print('장치별 રિમોટ_મૂલ્ય કનેક્શન_e05f319b સુયોજના 준비됨. પાસવર્ડ_મૂલ્ય ચકાસવું: python3 ઉપકરણો/રિમોટ_સેટિંગ્સ.py show')
