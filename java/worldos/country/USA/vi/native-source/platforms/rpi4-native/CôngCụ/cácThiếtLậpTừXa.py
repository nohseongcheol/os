#!/usr/bin/env python3
"""장치별 giáTrịPhím·kếtNối 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

gốcCâyDựÁn = Path(__file__).resolve().parents[1]


def chuẩnBị(gốcCâyDựÁn=gốcCâyDựÁn):
    đườngDẫn = gốcCâyDựÁn / 'build/remote'
    đườngDẫn.mkdir(parents=True, exist_ok=True)
    cácThiếtLập = đườngDẫn / 'access.json'
    giáTrịPhím = đườngDẫn / 'host-key.der'
    if not giáTrịPhím.exists():
        with giáTrịPhím.open('xb') as Tệp:
            os.chmod(str(giáTrịPhím), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Tệp)
    if not cácThiếtLập.exists():
        DữLiệu = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with cácThiếtLập.open('x') as Tệp:
            os.chmod(str(cácThiếtLập), 0o600)
            json.dump(DữLiệu, Tệp, ensure_ascii=False, indent=2)
            Tệp.write('\n')
    DữLiệu = json.loads(cácThiếtLập.read_text())
    if not isinstance(DữLiệu, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if DữLiệu.get('user') != 'user':
        raise SystemExit('access.json: user는 phầnMụcHiệnTại "user"만 지원합니다.')
    for tên in ('ssh_password', 'vnc_password'):
        if not isinstance(DữLiệu.get(tên), str):
            raise SystemExit('access.json: ' + tên + '는 문자열이어야 합니다.')
    mậtKhẩuVỏLệnh = DữLiệu['ssh_password'].encode('utf-8')
    if len(mậtKhẩuVỏLệnh) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        mậtKhẩuMànHình = DữLiệu['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. độDài 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    phímMànHình = mậtKhẩuMànHình[:8].ljust(8, b'\0')
    def giáTrịMảng(tên, giáTrị):
        return 'static const unsigned char '+tên+'[] = {'+','.join(str(trịSố) for trịSố in giáTrị)+'};\n'
    giáTrịĐầu = giáTrịMảng('phímThiếtBị', giáTrịPhím.read_bytes())
    giáTrịĐầu += giáTrịMảng('tómLượcMậtKhẩuVỏLệnh', hashlib.sha256(mậtKhẩuVỏLệnh).digest())
    giáTrịĐầu += giáTrịMảng('mậtKhẩuMànHình', phímMànHình)
    sinh = đườngDẫn / 'hồSơ.h'
    sinh.write_text(giáTrịĐầu)
    os.chmod(str(sinh), 0o600)
    return DữLiệu


if __name__ == '__main__':
    BộPhânTích = argparse.ArgumentParser(description=__doc__)
    BộPhânTích.add_argument('hànhĐộng', choices=['show', 'prepare'], nargs='?', default='prepare')
    cácĐốiSố = BộPhânTích.parse_args()
    DữLiệu = chuẩnBị()
    if cácĐốiSố.hànhĐộng == 'show':
        print(json.dumps(DữLiệu, ensure_ascii=False, indent=2))
    else:
        print('장치별 giáTrịTừXa kếtNối cácThiếtLập làĐãChuẩnBị. giáTrịMậtKhẩu xácMinh: python3 CôngCụ/cácThiếtLậpTừXa.py show')
