#!/usr/bin/env python3
"""장치별 ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ·ᎫᏓᎸᎢ_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def ᎭᏛᏅᎢᏍᏓ(기준=기준):
    ᎠᏍᏓᏩᏛᏍᏗ = 기준 / 'build/remote'
    ᎠᏍᏓᏩᏛᏍᏗ.mkdir(parents=True, exist_ok=True)
    ᏕᎦᎧᎲᎢ = ᎠᏍᏓᏩᏛᏍᏗ / 'access.json'
    ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ = ᎠᏍᏓᏩᏛᏍᏗ / 'host-key.der'
    if not ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ.exists():
        with ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ.open('xb') as ᎠᏍᏆᏂᎪᏙᏗ:
            os.chmod(str(ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ᎠᏍᏆᏂᎪᏙᏗ)
    if not ᏕᎦᎧᎲᎢ.exists():
        ᎦᏟᏌᏅᎯ = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with ᏕᎦᎧᎲᎢ.open('x') as ᎠᏍᏆᏂᎪᏙᏗ:
            os.chmod(str(ᏕᎦᎧᎲᎢ), 0o600)
            json.dump(ᎦᏟᏌᏅᎯ, ᎠᏍᏆᏂᎪᏙᏗ, ensure_ascii=False, indent=2)
            ᎠᏍᏆᏂᎪᏙᏗ.write('\n')
    ᎦᏟᏌᏅᎯ = json.loads(ᏕᎦᎧᎲᎢ.read_text())
    if not isinstance(ᎦᏟᏌᏅᎯ, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if ᎦᏟᏌᏅᎯ.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for ᏚᏙᎥᎢ in ('ssh_password', 'vnc_password'):
        if not isinstance(ᎦᏟᏌᏅᎯ.get(ᏚᏙᎥᎢ), str):
            raise SystemExit('access.json: ' + ᏚᏙᎥᎢ + '는 문자열이어야 합니다.')
    ᎤᏯᏍᎦ_ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ = ᎦᏟᏌᏅᎯ['ssh_password'].encode('utf-8')
    if len(ᎤᏯᏍᎦ_ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = ᎦᏟᏌᏅᎯ['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def array_ᏧᎬᏩᎶᏗᏯ(ᏚᏙᎥᎢ, ᏧᎬᏩᎶᏗᏯ):
        return 'static const unsigned char '+ᏚᏙᎥᎢ+'[] = {'+','.join(str(수) for 수 in ᏧᎬᏩᎶᏗᏯ)+'};\n'
    머리 = array_ᏧᎬᏩᎶᏗᏯ('ᎠᏂᎩᏍᎩ_ᏍᏚᎢᏍᏗ', ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ.read_bytes())
    머리 += array_ᏧᎬᏩᎶᏗᏯ('셸암호요약', hashlib.sha256(ᎤᏯᏍᎦ_ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ).digest())
    머리 += array_ᏧᎬᏩᎶᏗᏯ('화면암호', 화면열쇠)
    생성 = ᎠᏍᏓᏩᏛᏍᏗ / 'ᎬᏗᏍᎩ_ᏄᏍᏗᏓᏅᎢ.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return ᎦᏟᏌᏅᎯ


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('ᎠᏛᏁᎵᏓ', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    ᎦᏟᏌᏅᎯ = ᎭᏛᏅᎢᏍᏓ()
    if 인수.ᎠᏛᏁᎵᏓ == 'show':
        print(json.dumps(ᎦᏟᏌᏅᎯ, ensure_ascii=False, indent=2))
    else:
        print('장치별 원격 ᎫᏓᎸᎢ_e05f319b ᏕᎦᎧᎲᎢ 준비됨. ᎠᏍᏚᎢᏍᏙᏗ_ᎥᎧᏁᎬᎢ_ᏧᎬᏩᎶᏗᏯ ᎰᎯᏳᏓ: python3 도구/원격설정.py show')
