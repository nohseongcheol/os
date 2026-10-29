#!/usr/bin/env python3
"""장치별 కీ_మూల్యం·కనెక్షన్_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

ప్రొజెక్ట్_మూలం = Path(__file__).resolve().parents[1]


def సిద్ధం_చేయు(ప్రొజెక్ట్_మూలం=ప్రొజెక్ట్_మూలం):
    పాత్ = ప్రొజెక్ట్_మూలం / 'build/remote'
    పాత్.mkdir(parents=True, exist_ok=True)
    అమరికలు = పాత్ / 'access.json'
    కీ_మూల్యం = పాత్ / 'host-key.der'
    if not కీ_మూల్యం.exists():
        with కీ_మూల్యం.open('xb') as దస్త్రం:
            os.chmod(str(కీ_మూల్యం), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=దస్త్రం)
    if not అమరికలు.exists():
        డేటా = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with అమరికలు.open('x') as దస్త్రం:
            os.chmod(str(అమరికలు), 0o600)
            json.dump(డేటా, దస్త్రం, ensure_ascii=False, indent=2)
            దస్త్రం.write('\n')
    డేటా = json.loads(అమరికలు.read_text())
    if not isinstance(డేటా, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if డేటా.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for పేరు in ('ssh_password', 'vnc_password'):
        if not isinstance(డేటా.get(పేరు), str):
            raise SystemExit('access.json: ' + పేరు + '는 문자열이어야 합니다.')
    షెల్_అనుమతిపదం = డేటా['ssh_password'].encode('utf-8')
    if len(షెల్_అనుమతిపదం) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = డేటా['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. పొడవు_మూల్యం 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def శ్రేణి_మూల్యం(పేరు, మూల్యం):
        return 'static const unsigned char '+పేరు+'[] = {'+','.join(str(수) for 수 in మూల్యం)+'};\n'
    머리 = శ్రేణి_మూల్యం('పరికరం_కీ', కీ_మూల్యం.read_bytes())
    머리 += శ్రేణి_మూల్యం('셸암호요약', hashlib.sha256(షెల్_అనుమతిపదం).digest())
    머리 += శ్రేణి_మూల్యం('화면암호', 화면열쇠)
    రూపొందించు = పాత్ / 'ప్రొఫైల్.h'
    రూపొందించు.write_text(머리)
    os.chmod(str(రూపొందించు), 0o600)
    return డేటా


if __name__ == '__main__':
    పార్సర్_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    పార్సర్_48ee4b1b.add_argument('చర్య', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = పార్సర్_48ee4b1b.parse_args()
    డేటా = సిద్ధం_చేయు()
    if 인수.చర్య == 'show':
        print(json.dumps(డేటా, ensure_ascii=False, indent=2))
    else:
        print('장치별 రిమోట్_మూల్యం కనెక్షన్_e05f319b అమరికలు 준비됨. అనుమతిపదం_మూల్యం సరిచూడు: python3 ఉపకరణాలు/రిమోట్_సెట్టింగ్_లు.py show')
