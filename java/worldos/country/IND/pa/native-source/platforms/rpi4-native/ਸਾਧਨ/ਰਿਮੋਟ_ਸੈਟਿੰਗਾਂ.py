#!/usr/bin/env python3
"""장치별 ਕੀ_ਕੀਮਤ·ਸਬੰਧ_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Path(__file__).resolve().parents[1]


def ਤਿਆਰ_ਕਰੋ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ):
    ਮਾਰਗ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/remote'
    ਮਾਰਗ.mkdir(parents=True, exist_ok=True)
    ਸੈਟਿੰਗ = ਮਾਰਗ / 'access.json'
    ਕੀ_ਕੀਮਤ = ਮਾਰਗ / 'host-key.der'
    if not ਕੀ_ਕੀਮਤ.exists():
        with ਕੀ_ਕੀਮਤ.open('xb') as ਫਾਇਲ:
            os.chmod(str(ਕੀ_ਕੀਮਤ), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ਫਾਇਲ)
    if not ਸੈਟਿੰਗ.exists():
        ਸਮੱਗਰੀ = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with ਸੈਟਿੰਗ.open('x') as ਫਾਇਲ:
            os.chmod(str(ਸੈਟਿੰਗ), 0o600)
            json.dump(ਸਮੱਗਰੀ, ਫਾਇਲ, ensure_ascii=False, indent=2)
            ਫਾਇਲ.write('\n')
    ਸਮੱਗਰੀ = json.loads(ਸੈਟਿੰਗ.read_text())
    if not isinstance(ਸਮੱਗਰੀ, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if ਸਮੱਗਰੀ.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for ਨਾਂ in ('ssh_password', 'vnc_password'):
        if not isinstance(ਸਮੱਗਰੀ.get(ਨਾਂ), str):
            raise SystemExit('access.json: ' + ਨਾਂ + '는 문자열이어야 합니다.')
    ਸ਼ੈਲ_ਪਾਸਵਰਡ = ਸਮੱਗਰੀ['ssh_password'].encode('utf-8')
    if len(ਸ਼ੈਲ_ਪਾਸਵਰਡ) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = ਸਮੱਗਰੀ['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. ਲੰਬਾਈ_ਕੀਮਤ 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ਤਰਤੀਬ_ਦੇਣਾ_ਕੀਮਤ(ਨਾਂ, ਕੀਮਤ):
        return 'static const unsigned char '+ਨਾਂ+'[] = {'+','.join(str(수) for 수 in ਕੀਮਤ)+'};\n'
    머리 = ਤਰਤੀਬ_ਦੇਣਾ_ਕੀਮਤ('ਤਜਵੀਜ_ਕੀ', ਕੀ_ਕੀਮਤ.read_bytes())
    머리 += ਤਰਤੀਬ_ਦੇਣਾ_ਕੀਮਤ('ਸ਼ੈਲ_ਪਾਸਵਰਡ_ਸਾਰ', hashlib.sha256(ਸ਼ੈਲ_ਪਾਸਵਰਡ).digest())
    머리 += ਤਰਤੀਬ_ਦੇਣਾ_ਕੀਮਤ('화면암호', 화면열쇠)
    ਜਨਰੇਟ_ਕਰੋ = ਮਾਰਗ / 'ਪ੍ਰੋਫਾਈਲ.h'
    ਜਨਰੇਟ_ਕਰੋ.write_text(머리)
    os.chmod(str(ਜਨਰੇਟ_ਕਰੋ), 0o600)
    return ਸਮੱਗਰੀ


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('ਐਕਸ਼ਨ', choices=['show', 'prepare'], nargs='?', default='prepare')
    ਆਰਗੂਮੈਂਟ = 해석기.parse_args()
    ਸਮੱਗਰੀ = ਤਿਆਰ_ਕਰੋ()
    if ਆਰਗੂਮੈਂਟ.ਐਕਸ਼ਨ == 'show':
        print(json.dumps(ਸਮੱਗਰੀ, ensure_ascii=False, indent=2))
    else:
        print('장치별 ਰਿਮੋਟ_ਕੀਮਤ ਸਬੰਧ_e05f319b ਸੈਟਿੰਗ 준비됨. ਪਾਸਵਰਡ_ਕੀਮਤ ਤਸਦੀਕ: python3 ਸਾਧਨ/ਰਿਮੋਟ_ਸੈਟਿੰਗਾਂ.py show')
