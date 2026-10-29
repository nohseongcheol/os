#!/usr/bin/env python3
"""장치별 клавіша_значэнне·кантакт_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def Падрыхтаваць(기준=기준):
    ШЛЯХ = 기준 / 'build/remote'
    ШЛЯХ.mkdir(parents=True, exist_ok=True)
    Усталёўкі = ШЛЯХ / 'access.json'
    клавіша_значэнне = ШЛЯХ / 'host-key.der'
    if not клавіша_значэнне.exists():
        with клавіша_значэнне.open('xb') as Файл:
            os.chmod(str(клавіша_значэнне), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Файл)
    if not Усталёўкі.exists():
        дадзеныя = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Усталёўкі.open('x') as Файл:
            os.chmod(str(Усталёўкі), 0o600)
            json.dump(дадзеныя, Файл, ensure_ascii=False, indent=2)
            Файл.write('\n')
    дадзеныя = json.loads(Усталёўкі.read_text())
    if not isinstance(дадзеныя, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if дадзеныя.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Назва in ('ssh_password', 'vnc_password'):
        if not isinstance(дадзеныя.get(Назва), str):
            raise SystemExit('access.json: ' + Назва + '는 문자열이어야 합니다.')
    абалонка_пароль = дадзеныя['ssh_password'].encode('utf-8')
    if len(абалонка_пароль) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = дадзеныя['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. даўжыня_значэнне 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def масіў_значэнне(Назва, значэнне):
        return 'static const unsigned char '+Назва+'[] = {'+','.join(str(수) for 수 in значэнне)+'};\n'
    머리 = масіў_значэнне('прылада_клавіша', клавіша_значэнне.read_bytes())
    머리 += масіў_значэнне('셸암호요약', hashlib.sha256(абалонка_пароль).digest())
    머리 += масіў_значэнне('화면암호', 화면열쇠)
    생성 = ШЛЯХ / 'Профіль.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return дадзеныя


if __name__ == '__main__':
    аналізатар_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатар_48ee4b1b.add_argument('Дзеянне', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = аналізатар_48ee4b1b.parse_args()
    дадзеныя = Падрыхтаваць()
    if 인수.Дзеянне == 'show':
        print(json.dumps(дадзеныя, ensure_ascii=False, indent=2))
    else:
        print('장치별 аддалены_значэнне кантакт_e05f319b Усталёўкі 준비됨. пароль_значэнне праверыць: python3 Інструменты/аддалены_Налады.py show')
