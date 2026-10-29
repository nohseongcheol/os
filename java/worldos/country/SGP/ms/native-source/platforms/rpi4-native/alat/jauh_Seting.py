#!/usr/bin/env python3
"""장치별 Kunci_VALUE·hubungan_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

projek_akar = Path(__file__).resolve().parents[1]


def Sediakan(projek_akar=projek_akar):
    LALUAN = projek_akar / 'build/remote'
    LALUAN.mkdir(parents=True, exist_ok=True)
    Tetapan = LALUAN / 'access.json'
    Kunci_VALUE = LALUAN / 'host-key.der'
    if not Kunci_VALUE.exists():
        with Kunci_VALUE.open('xb') as Fail:
            os.chmod(str(Kunci_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Fail)
    if not Tetapan.exists():
        data = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Tetapan.open('x') as Fail:
            os.chmod(str(Tetapan), 0o600)
            json.dump(data, Fail, ensure_ascii=False, indent=2)
            Fail.write('\n')
    data = json.loads(Tetapan.read_text())
    if not isinstance(data, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if data.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Nama in ('ssh_password', 'vnc_password'):
        if not isinstance(data.get(Nama), str):
            raise SystemExit('access.json: ' + Nama + '는 문자열이어야 합니다.')
    cangkerang_kata_laluan = data['ssh_password'].encode('utf-8')
    if len(cangkerang_kata_laluan) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = data['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. kepanjangan_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(Nama, VALUE):
        return 'static const unsigned char '+Nama+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = ARRAY_VALUE('peranti_Kunci', Kunci_VALUE.read_bytes())
    머리 += ARRAY_VALUE('cangkerang_kata_laluan_ringkasan', hashlib.sha256(cangkerang_kata_laluan).digest())
    머리 += ARRAY_VALUE('화면암호', 화면열쇠)
    jana = LALUAN / 'Profil.h'
    jana.write_text(머리)
    os.chmod(str(jana), 0o600)
    return data


if __name__ == '__main__':
    penghurai_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    penghurai_48ee4b1b.add_argument('Aksi', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = penghurai_48ee4b1b.parse_args()
    data = Sediakan()
    if 인수.Aksi == 'show':
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print('장치별 jauh_VALUE hubungan_e05f319b Tetapan 준비됨. kata_laluan_VALUE tentu_sahkan: python3 alat/jauh_Seting.py show')
