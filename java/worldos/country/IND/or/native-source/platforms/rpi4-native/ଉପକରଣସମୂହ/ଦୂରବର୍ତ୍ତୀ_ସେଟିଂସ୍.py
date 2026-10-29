#!/usr/bin/env python3
"""장치별 କୀ_ମୂଲ୍ୟ·ସଂଯୋଗ_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Path(__file__).resolve().parents[1]


def ପ୍ରସ୍ତୁତ(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍):
    ପଥ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/remote'
    ପଥ.mkdir(parents=True, exist_ok=True)
    ବିନ୍ଯାସ = ପଥ / 'access.json'
    କୀ_ମୂଲ୍ୟ = ପଥ / 'host-key.der'
    if not କୀ_ମୂଲ୍ୟ.exists():
        with କୀ_ମୂଲ୍ୟ.open('xb') as ଫାଇଲ:
            os.chmod(str(କୀ_ମୂଲ୍ୟ), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ଫାଇଲ)
    if not ବିନ୍ଯାସ.exists():
        ଡାଟା = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with ବିନ୍ଯାସ.open('x') as ଫାଇଲ:
            os.chmod(str(ବିନ୍ଯାସ), 0o600)
            json.dump(ଡାଟା, ଫାଇଲ, ensure_ascii=False, indent=2)
            ଫାଇଲ.write('\n')
    ଡାଟା = json.loads(ବିନ୍ଯାସ.read_text())
    if not isinstance(ଡାଟା, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if ଡାଟା.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for ନାମ in ('ssh_password', 'vnc_password'):
        if not isinstance(ଡାଟା.get(ନାମ), str):
            raise SystemExit('access.json: ' + ନାମ + '는 문자열이어야 합니다.')
    ଖୋଳ_ପାସ୍_ୱାର୍ଡ୍ = ଡାଟା['ssh_password'].encode('utf-8')
    if len(ଖୋଳ_ପାସ୍_ୱାର୍ଡ୍) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = ଡାଟା['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ଆରେ_ମୂଲ୍ୟ(ନାମ, ମୂଲ୍ୟ):
        return 'static const unsigned char '+ନାମ+'[] = {'+','.join(str(수) for 수 in ମୂଲ୍ୟ)+'};\n'
    머리 = ଆରେ_ମୂଲ୍ୟ('ଡିଭାଇସ_କୀ', କୀ_ମୂଲ୍ୟ.read_bytes())
    머리 += ଆରେ_ମୂଲ୍ୟ('ଖୋଳ_ପାସ୍_ୱାର୍ଡ୍_ସାରାଂଶ', hashlib.sha256(ଖୋଳ_ପାସ୍_ୱାର୍ଡ୍).digest())
    머리 += ଆରେ_ମୂଲ୍ୟ('화면암호', 화면열쇠)
    ସୃଷ୍ଟି_କରିବା = ପଥ / 'ପ୍ରୋଫାଇଲ୍.h'
    ସୃଷ୍ଟି_କରିବା.write_text(머리)
    os.chmod(str(ସୃଷ୍ଟି_କରିବା), 0o600)
    return ଡାଟା


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('କାମ', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    ଡାଟା = ପ୍ରସ୍ତୁତ()
    if 인수.କାମ == 'show':
        print(json.dumps(ଡାଟା, ensure_ascii=False, indent=2))
    else:
        print('장치별 ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ ସଂଯୋଗ_e05f319b ବିନ୍ଯାସ 준비됨. ପାସ୍_ୱାର୍ଡ୍_ମୂଲ୍ୟ ଯାଞ୍ଚ୍_କରିବା: python3 ଉପକରଣସମୂହ/ଦୂରବର୍ତ୍ତୀ_ସେଟିଂସ୍.py show')
