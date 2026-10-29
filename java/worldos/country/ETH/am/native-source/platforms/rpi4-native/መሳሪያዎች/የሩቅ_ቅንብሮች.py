#!/usr/bin/env python3
"""장치별 ቁልፍ_እሴት·ግንኙነት_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

አሳይ_ስር = Path(__file__).resolve().parents[1]


def አዘጋጅ_9ce364fc(አሳይ_ስር=አሳይ_ስር):
    መተላለፊያ = አሳይ_ስር / 'build/remote'
    መተላለፊያ.mkdir(parents=True, exist_ok=True)
    ማሰናጃዎች = መተላለፊያ / 'access.json'
    ቁልፍ_እሴት = መተላለፊያ / 'host-key.der'
    if not ቁልፍ_እሴት.exists():
        with ቁልፍ_እሴት.open('xb') as ፋይል:
            os.chmod(str(ቁልፍ_እሴት), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ፋይል)
    if not ማሰናጃዎች.exists():
        ውሂብ = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with ማሰናጃዎች.open('x') as ፋይል:
            os.chmod(str(ማሰናጃዎች), 0o600)
            json.dump(ውሂብ, ፋይል, ensure_ascii=False, indent=2)
            ፋይል.write('\n')
    ውሂብ = json.loads(ማሰናጃዎች.read_text())
    if not isinstance(ውሂብ, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if ውሂብ.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for ስም in ('ssh_password', 'vnc_password'):
        if not isinstance(ውሂብ.get(ስም), str):
            raise SystemExit('access.json: ' + ስም + '는 문자열이어야 합니다.')
    ሼል_የይለፍ_ቃል = ውሂብ['ssh_password'].encode('utf-8')
    if len(ሼል_የይለፍ_ቃል) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = ውሂብ['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. ርዝመት_እሴት 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ድርድር_እሴት(ስም, እሴት):
        return 'static const unsigned char '+ስም+'[] = {'+','.join(str(수) for 수 in እሴት)+'};\n'
    머리 = ድርድር_እሴት('መሳሪያ_ቁልፍ', ቁልፍ_እሴት.read_bytes())
    머리 += ድርድር_እሴት('ሼል_የይለፍ_ቃል_ማጠቃለያ', hashlib.sha256(ሼል_የይለፍ_ቃል).digest())
    머리 += ድርድር_እሴት('화면암호', 화면열쇠)
    አዘጋጅ = መተላለፊያ / 'መገለጫ.h'
    አዘጋጅ.write_text(머리)
    os.chmod(str(አዘጋጅ), 0o600)
    return ውሂብ


if __name__ == '__main__':
    አግልሎ_ማስቀመጥ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('ተግባር', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = አግልሎ_ማስቀመጥ_48ee4b1b.parse_args()
    ውሂብ = አዘጋጅ_9ce364fc()
    if 인수.ተግባር == 'show':
        print(json.dumps(ውሂብ, ensure_ascii=False, indent=2))
    else:
        print('장치별 የሩቅ_እሴት ግንኙነት_e05f319b ማሰናጃዎች 준비됨. የይለፍ_ቃል_እሴት አረጋግጥ: python3 መሳሪያዎች/የሩቅ_ቅንብሮች.py show')
