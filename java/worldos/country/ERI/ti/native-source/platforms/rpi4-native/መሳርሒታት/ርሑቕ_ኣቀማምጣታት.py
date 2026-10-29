#!/usr/bin/env python3
"""장치별 መፍትሕ_ዋጋ·ርክብ_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def ኣዳልው(기준=기준):
    መገዲ = 기준 / 'build/remote'
    መገዲ.mkdir(parents=True, exist_ok=True)
    ኣቀማምጣታት = መገዲ / 'access.json'
    መፍትሕ_ዋጋ = መገዲ / 'host-key.der'
    if not መፍትሕ_ዋጋ.exists():
        with መፍትሕ_ዋጋ.open('xb') as ፋይል:
            os.chmod(str(መፍትሕ_ዋጋ), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ፋይል)
    if not ኣቀማምጣታት.exists():
        ሓበሬታ = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with ኣቀማምጣታት.open('x') as ፋይል:
            os.chmod(str(ኣቀማምጣታት), 0o600)
            json.dump(ሓበሬታ, ፋይል, ensure_ascii=False, indent=2)
            ፋይል.write('\n')
    ሓበሬታ = json.loads(ኣቀማምጣታት.read_text())
    if not isinstance(ሓበሬታ, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if ሓበሬታ.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for ሽም in ('ssh_password', 'vnc_password'):
        if not isinstance(ሓበሬታ.get(ሽም), str):
            raise SystemExit('access.json: ' + ሽም + '는 문자열이어야 합니다.')
    ሽፋን_መሕለፊ_ቃል = ሓበሬታ['ssh_password'].encode('utf-8')
    if len(ሽፋን_መሕለፊ_ቃል) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = ሓበሬታ['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. ንውሓት_ዋጋ 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ተርታ_ዋጋ_ed437109(ሽም, ዋጋ):
        return 'static const unsigned char '+ሽም+'[] = {'+','.join(str(수) for 수 in ዋጋ)+'};\n'
    머리 = ተርታ_ዋጋ_ed437109('መሳርሒ_መፍትሕ', መፍትሕ_ዋጋ.read_bytes())
    머리 += ተርታ_ዋጋ_ed437109('셸암호요약', hashlib.sha256(ሽፋን_መሕለፊ_ቃል).digest())
    머리 += ተርታ_ዋጋ_ed437109('화면암호', 화면열쇠)
    생성 = መገዲ / 'መግለጺ_መንነት.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return ሓበሬታ


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('ስጉምቲ', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    ሓበሬታ = ኣዳልው()
    if 인수.ስጉምቲ == 'show':
        print(json.dumps(ሓበሬታ, ensure_ascii=False, indent=2))
    else:
        print('장치별 ርሑቕ_ዋጋ ርክብ_e05f319b ኣቀማምጣታት 준비됨. መሕለፊ_ቃል_ዋጋ ኣረጋግጽ: python3 መሳርሒታት/ርሑቕ_ኣቀማምጣታት.py show')
