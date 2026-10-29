#!/usr/bin/env python3
"""장치별 යතුර_අගය·සබැඳුම_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def පිළියෙල_කරන්න(기준=기준):
    මාර්_ගය = 기준 / 'build/remote'
    මාර්_ගය.mkdir(parents=True, exist_ok=True)
    සැකසුම් = මාර්_ගය / 'access.json'
    යතුර_අගය = මාර්_ගය / 'host-key.der'
    if not යතුර_අගය.exists():
        with යතුර_අගය.open('xb') as ගොනු:
            os.chmod(str(යතුර_අගය), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ගොනු)
    if not සැකසුම්.exists():
        දත්ත = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with සැකසුම්.open('x') as ගොනු:
            os.chmod(str(සැකසුම්), 0o600)
            json.dump(දත්ත, ගොනු, ensure_ascii=False, indent=2)
            ගොනු.write('\n')
    දත්ත = json.loads(සැකසුම්.read_text())
    if not isinstance(දත්ත, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if දත්ත.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for නම in ('ssh_password', 'vnc_password'):
        if not isinstance(දත්ත.get(නම), str):
            raise SystemExit('access.json: ' + නම + '는 문자열이어야 합니다.')
    කවචය_මුර_පදය = දත්ත['ssh_password'].encode('utf-8')
    if len(කවචය_මුර_පදය) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = දත්ත['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. දිග_අගය 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ආරා_ව_අගය(නම, අගය):
        return 'static const unsigned char '+නම+'[] = {'+','.join(str(수) for 수 in අගය)+'};\n'
    머리 = ආරා_ව_අගය('ජංගම_යතුර', යතුර_අගය.read_bytes())
    머리 += ආරා_ව_අගය('කවචය_මුර_පදය_සාරාංශය', hashlib.sha256(කවචය_මුර_පදය).digest())
    머리 += ආරා_ව_අගය('화면암호', 화면열쇠)
    생성 = මාර්_ගය / 'පැතිකඩ.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return දත්ත


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('ක්_රීයාව', choices=['show', 'prepare'], nargs='?', default='prepare')
    විස්තාරක = 해석기.parse_args()
    දත්ත = පිළියෙල_කරන්න()
    if විස්තාරක.ක්_රීයාව == 'show':
        print(json.dumps(දත්ත, ensure_ascii=False, indent=2))
    else:
        print('장치별 දුරස්ථ_අගය සබැඳුම_e05f319b සැකසුම් 준비됨. මුර_පදය_අගය තහවුරු_කරන්න: python3 මෙවලම්/දුරස්ථ_පසුතල.py show')
