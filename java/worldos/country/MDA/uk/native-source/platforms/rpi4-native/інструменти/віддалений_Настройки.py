#!/usr/bin/env python3
"""장치별 Ключ_значення·зв_язок_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Дії_корінь = Path(__file__).resolve().parents[1]


def Готувати(Дії_корінь=Дії_корінь):
    шлях = Дії_корінь / 'build/remote'
    шлях.mkdir(parents=True, exist_ok=True)
    Налаштування = шлях / 'access.json'
    Ключ_значення = шлях / 'host-key.der'
    if not Ключ_значення.exists():
        with Ключ_значення.open('xb') as файл:
            os.chmod(str(Ключ_значення), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=файл)
    if not Налаштування.exists():
        дані = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Налаштування.open('x') as файл:
            os.chmod(str(Налаштування), 0o600)
            json.dump(дані, файл, ensure_ascii=False, indent=2)
            файл.write('\n')
    дані = json.loads(Налаштування.read_text())
    if not isinstance(дані, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if дані.get('user') != 'user':
        raise SystemExit('access.json: user는 чинний_елемент "user"만 지원합니다.')
    for Назва in ('ssh_password', 'vnc_password'):
        if not isinstance(дані.get(Назва), str):
            raise SystemExit('access.json: ' + Назва + '는 문자열이어야 합니다.')
    оболонка_пароль = дані['ssh_password'].encode('utf-8')
    if len(оболонка_пароль) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = дані['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. 길이 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def масив_значення(Назва, значення):
        return 'static const unsigned char '+Назва+'[] = {'+','.join(str(수) for 수 in значення)+'};\n'
    머리 = масив_значення('пристрій_Ключ', Ключ_значення.read_bytes())
    머리 += масив_значення('оболонка_пароль_зведення', hashlib.sha256(оболонка_пароль).digest())
    머리 += масив_значення('화면암호', 화면열쇠)
    генерувати = шлях / 'Профіль.h'
    генерувати.write_text(머리)
    os.chmod(str(генерувати), 0o600)
    return дані


if __name__ == '__main__':
    аналізатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатор_48ee4b1b.add_argument('Дія', choices=['show', 'prepare'], nargs='?', default='prepare')
    аргументи = аналізатор_48ee4b1b.parse_args()
    дані = Готувати()
    if аргументи.Дія == 'show':
        print(json.dumps(дані, ensure_ascii=False, indent=2))
    else:
        print('장치별 віддалений_значення зв_язок_e05f319b Налаштування 준비됨. пароль_значення перевіряти: python3 інструменти/віддалений_Настройки.py show')
