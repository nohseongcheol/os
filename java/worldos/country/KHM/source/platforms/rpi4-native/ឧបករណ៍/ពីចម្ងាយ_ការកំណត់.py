#!/usr/bin/env python3
"""장치별 ឃី_តំលៃ·ការភ្ជាប់_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

បញ្ចាំង_ឬស = Path(__file__).resolve().parents[1]


def រៀបចំ(បញ្ចាំង_ឬស=បញ្ចាំង_ឬស):
    ផ្លូវ = បញ្ចាំង_ឬស / 'build/remote'
    ផ្លូវ.mkdir(parents=True, exist_ok=True)
    ការកំណត់ = ផ្លូវ / 'access.json'
    ឃី_តំលៃ = ផ្លូវ / 'host-key.der'
    if not ឃី_តំលៃ.exists():
        with ឃី_តំលៃ.open('xb') as ឯកសារ:
            os.chmod(str(ឃី_តំលៃ), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ឯកសារ)
    if not ការកំណត់.exists():
        ទិន្នន័យ = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with ការកំណត់.open('x') as ឯកសារ:
            os.chmod(str(ការកំណត់), 0o600)
            json.dump(ទិន្នន័យ, ឯកសារ, ensure_ascii=False, indent=2)
            ឯកសារ.write('\n')
    ទិន្នន័យ = json.loads(ការកំណត់.read_text())
    if not isinstance(ទិន្នន័យ, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if ទិន្នន័យ.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for ឈ្មោះ in ('ssh_password', 'vnc_password'):
        if not isinstance(ទិន្នន័យ.get(ឈ្មោះ), str):
            raise SystemExit('access.json: ' + ឈ្មោះ + '는 문자열이어야 합니다.')
    셸암호 = ទិន្នន័យ['ssh_password'].encode('utf-8')
    if len(셸암호) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = ទិន្នន័យ['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. ប្រវែង_តំលៃ 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def អារេ_តំលៃ(ឈ្មោះ, តំលៃ):
        return 'static const unsigned char '+ឈ្មោះ+'[] = {'+','.join(str(수) for 수 in តំលៃ)+'};\n'
    머리 = អារេ_តំលៃ('ឧបករណ៍_ឃី', ឃី_តំលៃ.read_bytes())
    머리 += អារេ_តំលៃ('셸암호요약', hashlib.sha256(셸암호).digest())
    머리 += អារេ_តំលៃ('화면암호', 화면열쇠)
    បង្កើត = ផ្លូវ / 'ទម្រង់.h'
    បង្កើត.write_text(머리)
    os.chmod(str(បង្កើត), 0o600)
    return ទិន្នន័យ


if __name__ == '__main__':
    មុខងារ_ញែក_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    មុខងារ_ញែក_48ee4b1b.add_argument('អំពើ', choices=['show', 'prepare'], nargs='?', default='prepare')
    អាគុយម៉ង់ = មុខងារ_ញែក_48ee4b1b.parse_args()
    ទិន្នន័យ = រៀបចំ()
    if អាគុយម៉ង់.អំពើ == 'show':
        print(json.dumps(ទិន្នន័យ, ensure_ascii=False, indent=2))
    else:
        print('장치별 ពីចម្ងាយ_តំលៃ ការភ្ជាប់_e05f319b ការកំណត់ 준비됨. លេខសម្ងាត់_តំលៃ ផ្ទៀងផ្ទាត់: python3 ឧបករណ៍/ពីចម្ងាយ_ការកំណត់.py show')
