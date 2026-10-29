#!/usr/bin/env python3
"""장치별 ಕೀ_ಮೌಲ್ಯ·ಸಂಪರ್ಕ_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

ಬಿಂಬಿಸು_ಮೂಲ = Path(__file__).resolve().parents[1]


def ಸಿದ್ಧಪಡಿಸು(ಬಿಂಬಿಸು_ಮೂಲ=ಬಿಂಬಿಸು_ಮೂಲ):
    ಮಾರ್ಗ = ಬಿಂಬಿಸು_ಮೂಲ / 'build/remote'
    ಮಾರ್ಗ.mkdir(parents=True, exist_ok=True)
    ಸಿದ್ಧತೆಗಳು = ಮಾರ್ಗ / 'access.json'
    ಕೀ_ಮೌಲ್ಯ = ಮಾರ್ಗ / 'host-key.der'
    if not ಕೀ_ಮೌಲ್ಯ.exists():
        with ಕೀ_ಮೌಲ್ಯ.open('xb') as ಕಡತ:
            os.chmod(str(ಕೀ_ಮೌಲ್ಯ), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ಕಡತ)
    if not ಸಿದ್ಧತೆಗಳು.exists():
        ಡೇಟಾ = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with ಸಿದ್ಧತೆಗಳು.open('x') as ಕಡತ:
            os.chmod(str(ಸಿದ್ಧತೆಗಳು), 0o600)
            json.dump(ಡೇಟಾ, ಕಡತ, ensure_ascii=False, indent=2)
            ಕಡತ.write('\n')
    ಡೇಟಾ = json.loads(ಸಿದ್ಧತೆಗಳು.read_text())
    if not isinstance(ಡೇಟಾ, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if ಡೇಟಾ.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for ಹೆಸರು in ('ssh_password', 'vnc_password'):
        if not isinstance(ಡೇಟಾ.get(ಹೆಸರು), str):
            raise SystemExit('access.json: ' + ಹೆಸರು + '는 문자열이어야 합니다.')
    ಶೆಲ್_ಪಾಸ್_ವರ್ಡ್ = ಡೇಟಾ['ssh_password'].encode('utf-8')
    if len(ಶೆಲ್_ಪಾಸ್_ವರ್ಡ್) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = ಡೇಟಾ['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. ಉದ್ದ_ಮೌಲ್ಯ 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ಅರೇ_ಮೌಲ್ಯ(ಹೆಸರು, ಮೌಲ್ಯ):
        return 'static const unsigned char '+ಹೆಸರು+'[] = {'+','.join(str(수) for 수 in ಮೌಲ್ಯ)+'};\n'
    머리 = ಅರೇ_ಮೌಲ್ಯ('ಸಾಧನ_ಕೀ', ಕೀ_ಮೌಲ್ಯ.read_bytes())
    머리 += ಅರೇ_ಮೌಲ್ಯ('셸암호요약', hashlib.sha256(ಶೆಲ್_ಪಾಸ್_ವರ್ಡ್).digest())
    머리 += ಅರೇ_ಮೌಲ್ಯ('화면암호', 화면열쇠)
    ರಚಿಸಿ = ಮಾರ್ಗ / 'ಪ್ರೊಫೈಲ್.h'
    ರಚಿಸಿ.write_text(머리)
    os.chmod(str(ರಚಿಸಿ), 0o600)
    return ಡೇಟಾ


if __name__ == '__main__':
    ಪಾರ್ಸರ್_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('ಹಕ್ರಿಯೆ', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = ಪಾರ್ಸರ್_48ee4b1b.parse_args()
    ಡೇಟಾ = ಸಿದ್ಧಪಡಿಸು()
    if 인수.ಹಕ್ರಿಯೆ == 'show':
        print(json.dumps(ಡೇಟಾ, ensure_ascii=False, indent=2))
    else:
        print('장치별 ರಿಮೋಟ್_ಮೌಲ್ಯ ಸಂಪರ್ಕ_e05f319b ಸಿದ್ಧತೆಗಳು 준비됨. ಪಾಸ್_ವರ್ಡ್_ಮೌಲ್ಯ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು: python3 ಪರಿಕರಗಳು/ರಿಮೋಟ್_ಸೆಟ್ಟಿಂಗ್ಸ್.py show')
