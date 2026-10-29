#!/usr/bin/env python3
"""장치별 Ключ_стойност·връзка_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

проект_корен = Path(__file__).resolve().parents[1]


def Подготвяне(проект_корен=проект_корен):
    ПЪТ = проект_корен / 'build/remote'
    ПЪТ.mkdir(parents=True, exist_ok=True)
    Настройки = ПЪТ / 'access.json'
    Ключ_стойност = ПЪТ / 'host-key.der'
    if not Ключ_стойност.exists():
        with Ключ_стойност.open('xb') as Файл:
            os.chmod(str(Ключ_стойност), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Файл)
    if not Настройки.exists():
        данни = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Настройки.open('x') as Файл:
            os.chmod(str(Настройки), 0o600)
            json.dump(данни, Файл, ensure_ascii=False, indent=2)
            Файл.write('\n')
    данни = json.loads(Настройки.read_text())
    if not isinstance(данни, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if данни.get('user') != 'user':
        raise SystemExit('access.json: user는 в_срок_артикул "user"만 지원합니다.')
    for Име in ('ssh_password', 'vnc_password'):
        if not isinstance(данни.get(Име), str):
            raise SystemExit('access.json: ' + Име + '는 문자열이어야 합니다.')
    обвивка_парола = данни['ssh_password'].encode('utf-8')
    if len(обвивка_парола) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = данни['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. 길이 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def масив_стойност(Име, стойност):
        return 'static const unsigned char '+Име+'[] = {'+','.join(str(수) for 수 in стойност)+'};\n'
    머리 = масив_стойност('устройство_Ключ', Ключ_стойност.read_bytes())
    머리 += масив_стойност('обвивка_парола_резюме', hashlib.sha256(обвивка_парола).digest())
    머리 += масив_стойност('화면암호', 화면열쇠)
    генерирам = ПЪТ / 'Профил.h'
    генерирам.write_text(머리)
    os.chmod(str(генерирам), 0o600)
    return данни


if __name__ == '__main__':
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('Операция', choices=['show', 'prepare'], nargs='?', default='prepare')
    Параметри = анализатор_48ee4b1b.parse_args()
    данни = Подготвяне()
    if Параметри.Операция == 'show':
        print(json.dumps(данни, ensure_ascii=False, indent=2))
    else:
        print('장치별 отдалечен_стойност връзка_e05f319b Настройки 준비됨. парола_стойност проверявам: python3 Инструменти/отдалечен_Настройки.py show')
