#!/usr/bin/env python3
"""장치별 tuş_değer·cxn_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

işlem_kök = Path(__file__).resolve().parents[1]


def Hazırlan(işlem_kök=işlem_kök):
    yol = işlem_kök / 'build/remote'
    yol.mkdir(parents=True, exist_ok=True)
    Ayarlar = yol / 'access.json'
    tuş_değer = yol / 'host-key.der'
    if not tuş_değer.exists():
        with tuş_değer.open('xb') as dosya:
            os.chmod(str(tuş_değer), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=dosya)
    if not Ayarlar.exists():
        veri = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Ayarlar.open('x') as dosya:
            os.chmod(str(Ayarlar), 0o600)
            json.dump(veri, dosya, ensure_ascii=False, indent=2)
            dosya.write('\n')
    veri = json.loads(Ayarlar.read_text())
    if not isinstance(veri, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if veri.get('user') != 'user':
        raise SystemExit('access.json: user는 geçerli_öğe "user"만 지원합니다.')
    for İsim in ('ssh_password', 'vnc_password'):
        if not isinstance(veri.get(İsim), str):
            raise SystemExit('access.json: ' + İsim + '는 문자열이어야 합니다.')
    kabuk_parola = veri['ssh_password'].encode('utf-8')
    if len(kabuk_parola) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = veri['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. süre_değer 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def DİZİ_değer(İsim, değer):
        return 'static const unsigned char '+İsim+'[] = {'+','.join(str(수) for 수 in değer)+'};\n'
    머리 = DİZİ_değer('cihaz_tuş', tuş_değer.read_bytes())
    머리 += DİZİ_değer('kabuk_parola_özet', hashlib.sha256(kabuk_parola).digest())
    머리 += DİZİ_değer('화면암호', 화면열쇠)
    oluşturmak = yol / 'Profil.h'
    oluşturmak.write_text(머리)
    os.chmod(str(oluşturmak), 0o600)
    return veri


if __name__ == '__main__':
    ayrıştırıcı_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ayrıştırıcı_48ee4b1b.add_argument('Eylem', choices=['show', 'prepare'], nargs='?', default='prepare')
    bağımsız_değişkenler = ayrıştırıcı_48ee4b1b.parse_args()
    veri = Hazırlan()
    if bağımsız_değişkenler.Eylem == 'show':
        print(json.dumps(veri, ensure_ascii=False, indent=2))
    else:
        print('장치별 uzak_değer cxn_e05f319b Ayarlar 준비됨. parola_değer doğrulamak: python3 araçlar/uzak_Ayarlar.py show')
