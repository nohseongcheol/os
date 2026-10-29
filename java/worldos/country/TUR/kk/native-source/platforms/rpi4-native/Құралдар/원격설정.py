#!/usr/bin/env python3
"""장치별 Кілт_мән·қосылым_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

жоба_түбір = Path(__file__).resolve().parents[1]


def Дайындау(жоба_түбір=жоба_түбір):
    Жол_2 = жоба_түбір / 'build/remote'
    Жол_2.mkdir(parents=True, exist_ok=True)
    Баптаулар = Жол_2 / 'access.json'
    Кілт_мән = Жол_2 / 'host-key.der'
    if not Кілт_мән.exists():
        with Кілт_мән.open('xb') as Файл:
            os.chmod(str(Кілт_мән), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Файл)
    if not Баптаулар.exists():
        деректер = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Баптаулар.open('x') as Файл:
            os.chmod(str(Баптаулар), 0o600)
            json.dump(деректер, Файл, ensure_ascii=False, indent=2)
            Файл.write('\n')
    деректер = json.loads(Баптаулар.read_text())
    if not isinstance(деректер, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if деректер.get('user') != 'user':
        raise SystemExit('access.json: user는 ток_элемент "user"만 지원합니다.')
    for Аты in ('ssh_password', 'vnc_password'):
        if not isinstance(деректер.get(Аты), str):
            raise SystemExit('access.json: ' + Аты + '는 문자열이어야 합니다.')
    қоршам_құпиясөз = деректер['ssh_password'].encode('utf-8')
    if len(қоршам_құпиясөз) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = деректер['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. ұзындық_мән 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def массив_мән(Аты, мән):
        return 'static const unsigned char '+Аты+'[] = {'+','.join(str(수) for 수 in мән)+'};\n'
    머리 = массив_мән('құрылғы_Кілт', Кілт_мән.read_bytes())
    머리 += массив_мән('қоршам_құпиясөз_жиынтық', hashlib.sha256(қоршам_құпиясөз).digest())
    머리 += массив_мән('화면암호', 화면열쇠)
    жасау = Жол_2 / 'Профиль.h'
    жасау.write_text(머리)
    os.chmod(str(жасау), 0o600)
    return деректер


if __name__ == '__main__':
    талдау_құралы_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    талдау_құралы_48ee4b1b.add_argument('Әрекет', choices=['show', 'prepare'], nargs='?', default='prepare')
    Аргументтер = талдау_құралы_48ee4b1b.parse_args()
    деректер = Дайындау()
    if Аргументтер.Әрекет == 'show':
        print(json.dumps(деректер, ensure_ascii=False, indent=2))
    else:
        print('장치별 원격 қосылым_e05f319b Баптаулар 준비됨. құпиясөз_мән тексеру: python3 Құралдар/원격설정.py show')
