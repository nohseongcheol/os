#!/usr/bin/env python3
"""장치별 Ключ_ЗНАЧЕН·контакт_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

задача_корень = Path(__file__).resolve().parents[1]


def Подготовить(задача_корень=задача_корень):
    путь = задача_корень / 'build/remote'
    путь.mkdir(parents=True, exist_ok=True)
    Настройки = путь / 'access.json'
    Ключ_ЗНАЧЕН = путь / 'host-key.der'
    if not Ключ_ЗНАЧЕН.exists():
        with Ключ_ЗНАЧЕН.open('xb') as файл:
            os.chmod(str(Ключ_ЗНАЧЕН), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=файл)
    if not Настройки.exists():
        данные = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Настройки.open('x') as файл:
            os.chmod(str(Настройки), 0o600)
            json.dump(данные, файл, ensure_ascii=False, indent=2)
            файл.write('\n')
    данные = json.loads(Настройки.read_text())
    if not isinstance(данные, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if данные.get('user') != 'user':
        raise SystemExit('access.json: user는 текущий_товар "user"만 지원합니다.')
    for Название in ('ssh_password', 'vnc_password'):
        if not isinstance(данные.get(Название), str):
            raise SystemExit('access.json: ' + Название + '는 문자열이어야 합니다.')
    оболочка_пароль = данные['ssh_password'].encode('utf-8')
    if len(оболочка_пароль) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        экран_пароль = данные['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. длина_ЗНАЧЕН 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    экран_Ключ = экран_пароль[:8].ljust(8, b'\0')
    def МАССИВ_ЗНАЧЕН(Название, ЗНАЧЕН):
        return 'static const unsigned char '+Название+'[] = {'+','.join(str(수) for 수 in ЗНАЧЕН)+'};\n'
    HEAD_ЗНАЧЕН = МАССИВ_ЗНАЧЕН('устройство_Ключ', Ключ_ЗНАЧЕН.read_bytes())
    HEAD_ЗНАЧЕН += МАССИВ_ЗНАЧЕН('оболочка_пароль_сводка', hashlib.sha256(оболочка_пароль).digest())
    HEAD_ЗНАЧЕН += МАССИВ_ЗНАЧЕН('экран_пароль', экран_Ключ)
    генерировать = путь / 'Profile.h'
    генерировать.write_text(HEAD_ЗНАЧЕН)
    os.chmod(str(генерировать), 0o600)
    return данные


if __name__ == '__main__':
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('Действие', choices=['show', 'prepare'], nargs='?', default='prepare')
    аргументы = анализатор_48ee4b1b.parse_args()
    данные = Подготовить()
    if аргументы.Действие == 'show':
        print(json.dumps(данные, ensure_ascii=False, indent=2))
    else:
        print('장치별 удаленный_ЗНАЧЕН контакт_e05f319b Настройки 준비됨. пароль_ЗНАЧЕН проверять: python3 инструменты/удаленный_Настройки.py show')
