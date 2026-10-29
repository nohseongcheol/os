#!/usr/bin/env python3
"""장치별 ачкыч_VALUE·тоташу_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

экранга_җибәрү_тамыр = Path(__file__).resolve().parents[1]


def Әзерләү(экранга_җибәрү_тамыр=экранга_җибәрү_тамыр):
    Yul = экранга_җибәрү_тамыр / 'build/remote'
    Yul.mkdir(parents=True, exist_ok=True)
    Caylaw = Yul / 'access.json'
    ачкыч_VALUE = Yul / 'host-key.der'
    if not ачкыч_VALUE.exists():
        with ачкыч_VALUE.open('xb') as Birem:
            os.chmod(str(ачкыч_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Birem)
    if not Caylaw.exists():
        мәгълүмат = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Caylaw.open('x') as Birem:
            os.chmod(str(Caylaw), 0o600)
            json.dump(мәгълүмат, Birem, ensure_ascii=False, indent=2)
            Birem.write('\n')
    мәгълүмат = json.loads(Caylaw.read_text())
    if not isinstance(мәгълүмат, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if мәгълүмат.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for исем in ('ssh_password', 'vnc_password'):
        if not isinstance(мәгълүмат.get(исем), str):
            raise SystemExit('access.json: ' + исем + '는 문자열이어야 합니다.')
    тышча_серсүз = мәгълүмат['ssh_password'].encode('utf-8')
    if len(тышча_серсүз) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = мәгълүмат['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. озынлык_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def МАССИВ_VALUE(исем, VALUE):
        return 'static const unsigned char '+исем+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = МАССИВ_VALUE('мобиль_ачкыч', ачкыч_VALUE.read_bytes())
    머리 += МАССИВ_VALUE('тышча_серсүз_Җыелма_нәтиҗә', hashlib.sha256(тышча_серсүз).digest())
    머리 += МАССИВ_VALUE('화면암호', 화면열쇠)
    булдыру = Yul / 'Профиль.h'
    булдыру.write_text(머리)
    os.chmod(str(булдыру), 0o600)
    return мәгълүмат


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('Гамәл', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    мәгълүмат = Әзерләү()
    if 인수.Гамәл == 'show':
        print(json.dumps(мәгълүмат, ensure_ascii=False, indent=2))
    else:
        print('장치별 читтәге_VALUE тоташу_e05f319b Caylaw 준비됨. серсүз_VALUE раслау: python3 Кораллар/читтәге_Параметрлар.py show')
