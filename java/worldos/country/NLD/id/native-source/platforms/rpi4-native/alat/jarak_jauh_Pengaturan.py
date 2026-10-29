#!/usr/bin/env python3
"""장치별 Kunci_VALUE·koneksi_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Tugas_akar = Path(__file__).resolve().parents[1]


def Siapkan(Tugas_akar=Tugas_akar):
    jalur = Tugas_akar / 'build/remote'
    jalur.mkdir(parents=True, exist_ok=True)
    Konfigurasi = jalur / 'access.json'
    Kunci_VALUE = jalur / 'host-key.der'
    if not Kunci_VALUE.exists():
        with Kunci_VALUE.open('xb') as berkas:
            os.chmod(str(Kunci_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=berkas)
    if not Konfigurasi.exists():
        data = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Konfigurasi.open('x') as berkas:
            os.chmod(str(Konfigurasi), 0o600)
            json.dump(data, berkas, ensure_ascii=False, indent=2)
            berkas.write('\n')
    data = json.loads(Konfigurasi.read_text())
    if not isinstance(data, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if data.get('user') != 'user':
        raise SystemExit('access.json: user는 saat_ini_item "user"만 지원합니다.')
    for Nama_2 in ('ssh_password', 'vnc_password'):
        if not isinstance(data.get(Nama_2), str):
            raise SystemExit('access.json: ' + Nama_2 + '는 문자열이어야 합니다.')
    shell_sandi = data['ssh_password'].encode('utf-8')
    if len(shell_sandi) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = data['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. panjang_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(Nama_2, VALUE):
        return 'static const unsigned char '+Nama_2+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    kepala_VALUE = ARRAY_VALUE('Ponsel_Kunci', Kunci_VALUE.read_bytes())
    kepala_VALUE += ARRAY_VALUE('shell_sandi_ringkasan', hashlib.sha256(shell_sandi).digest())
    kepala_VALUE += ARRAY_VALUE('화면암호', 화면열쇠)
    buat = jalur / 'Profil.h'
    buat.write_text(kepala_VALUE)
    os.chmod(str(buat), 0o600)
    return data


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('Aksi', choices=['show', 'prepare'], nargs='?', default='prepare')
    argumen = parser_48ee4b1b.parse_args()
    data = Siapkan()
    if argumen.Aksi == 'show':
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print('장치별 jarak_jauh_VALUE koneksi_e05f319b Konfigurasi 준비됨. sandi_VALUE periksa: python3 alat/jarak_jauh_Pengaturan.py show')
