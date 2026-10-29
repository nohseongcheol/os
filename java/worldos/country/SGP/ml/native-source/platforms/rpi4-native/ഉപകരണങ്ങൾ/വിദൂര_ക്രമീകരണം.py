#!/usr/bin/env python3
"""장치별 കീ_മൂല്യം·കണക്ഷൻ_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = Path(__file__).resolve().parents[1]


def തയ്യാറാക്കുക(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം):
    വഴി = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/remote'
    വഴി.mkdir(parents=True, exist_ok=True)
    സജ്ജീകരണം = വഴി / 'access.json'
    കീ_മൂല്യം = വഴി / 'host-key.der'
    if not കീ_മൂല്യം.exists():
        with കീ_മൂല്യം.open('xb') as ഫയല്:
            os.chmod(str(കീ_മൂല്യം), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ഫയല്)
    if not സജ്ജീകരണം.exists():
        ഡാറ്റാ = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with സജ്ജീകരണം.open('x') as ഫയല്:
            os.chmod(str(സജ്ജീകരണം), 0o600)
            json.dump(ഡാറ്റാ, ഫയല്, ensure_ascii=False, indent=2)
            ഫയല്.write('\n')
    ഡാറ്റാ = json.loads(സജ്ജീകരണം.read_text())
    if not isinstance(ഡാറ്റാ, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if ഡാറ്റാ.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for പേരു് in ('ssh_password', 'vnc_password'):
        if not isinstance(ഡാറ്റാ.get(പേരു്), str):
            raise SystemExit('access.json: ' + പേരു് + '는 문자열이어야 합니다.')
    ഷെല്_പാസ്_വേഡ് = ഡാറ്റാ['ssh_password'].encode('utf-8')
    if len(ഷെല്_പാസ്_വേഡ്) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = ഡാറ്റാ['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. ദൈര്_ഘ്യം_മൂല്യം 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def അരേ_മൂല്യം(പേരു്, മൂല്യം):
        return 'static const unsigned char '+പേരു്+'[] = {'+','.join(str(수) for 수 in മൂല്യം)+'};\n'
    머리 = അരേ_മൂല്യം('മൊബൈൽ_കീ', കീ_മൂല്യം.read_bytes())
    머리 += അരേ_മൂല്യം('셸암호요약', hashlib.sha256(ഷെല്_പാസ്_വേഡ്).digest())
    머리 += അരേ_മൂല്യം('화면암호', 화면열쇠)
    സൃഷ്_ടിക്കുക = വഴി / 'പ്രൊഫൈൽ.h'
    സൃഷ്_ടിക്കുക.write_text(머리)
    os.chmod(str(സൃഷ്_ടിക്കുക), 0o600)
    return ഡാറ്റാ


if __name__ == '__main__':
    പാഴ്_സർ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    പാഴ്_സർ_48ee4b1b.add_argument('നടപടി', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = പാഴ്_സർ_48ee4b1b.parse_args()
    ഡാറ്റാ = തയ്യാറാക്കുക()
    if 인수.നടപടി == 'show':
        print(json.dumps(ഡാറ്റാ, ensure_ascii=False, indent=2))
    else:
        print('장치별 വിദൂര_മൂല്യം കണക്ഷൻ_e05f319b സജ്ജീകരണം 준비됨. പാസ്_വേഡ്_മൂല്യം പരിശോധിക്കുക: python3 ഉപകരണങ്ങൾ/വിദൂര_ക്രമീകരണം.py show')
