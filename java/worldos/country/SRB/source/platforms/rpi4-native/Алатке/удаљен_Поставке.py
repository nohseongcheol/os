#!/usr/bin/env python3
"""장치별 Кључ_вриједност·веза_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

пројектовати_корен = Path(__file__).resolve().parents[1]


def Припремити(пројектовати_корен=пројектовати_корен):
    ПУТАЊА = пројектовати_корен / 'build/remote'
    ПУТАЊА.mkdir(parents=True, exist_ok=True)
    Поставке = ПУТАЊА / 'access.json'
    Кључ_вриједност = ПУТАЊА / 'host-key.der'
    if not Кључ_вриједност.exists():
        with Кључ_вриједност.open('xb') as Датотека:
            os.chmod(str(Кључ_вриједност), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Датотека)
    if not Поставке.exists():
        подаци = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Поставке.open('x') as Датотека:
            os.chmod(str(Поставке), 0o600)
            json.dump(подаци, Датотека, ensure_ascii=False, indent=2)
            Датотека.write('\n')
    подаци = json.loads(Поставке.read_text())
    if not isinstance(подаци, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if подаци.get('user') != 'user':
        raise SystemExit('access.json: user는 актуелно_ставка "user"만 지원합니다.')
    for Назив in ('ssh_password', 'vnc_password'):
        if not isinstance(подаци.get(Назив), str):
            raise SystemExit('access.json: ' + Назив + '는 문자열이어야 합니다.')
    љуска_лозинка = подаци['ssh_password'].encode('utf-8')
    if len(љуска_лозинка) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = подаци['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. дужина_вриједност 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def низ_вриједност(Назив, вриједност):
        return 'static const unsigned char '+Назив+'[] = {'+','.join(str(수) for 수 in вриједност)+'};\n'
    머리 = низ_вриједност('уређај_Кључ', Кључ_вриједност.read_bytes())
    머리 += низ_вриједност('љуска_лозинка_резиме', hashlib.sha256(љуска_лозинка).digest())
    머리 += низ_вриједност('화면암호', 화면열쇠)
    генерисати = ПУТАЊА / 'Профил.h'
    генерисати.write_text(머리)
    os.chmod(str(генерисати), 0o600)
    return подаци


if __name__ == '__main__':
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('радња', choices=['show', 'prepare'], nargs='?', default='prepare')
    Аргументи = анализатор_48ee4b1b.parse_args()
    подаци = Припремити()
    if Аргументи.радња == 'show':
        print(json.dumps(подаци, ensure_ascii=False, indent=2))
    else:
        print('장치별 удаљен_вриједност веза_e05f319b Поставке 준비됨. лозинка_вриједност потврдити: python3 Алатке/удаљен_Поставке.py show')
