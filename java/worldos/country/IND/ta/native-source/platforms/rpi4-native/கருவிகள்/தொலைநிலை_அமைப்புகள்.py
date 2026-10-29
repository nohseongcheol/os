#!/usr/bin/env python3
"""장치별 சாவி_மதிப்பு·இணைப்பு_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

திட்டப்பணி_மூலம் = Path(__file__).resolve().parents[1]


def தயார்படுத்த(திட்டப்பணி_மூலம்=திட்டப்பணி_மூலம்):
    பாதை_2 = திட்டப்பணி_மூலம் / 'build/remote'
    பாதை_2.mkdir(parents=True, exist_ok=True)
    அமைப்புகள் = பாதை_2 / 'access.json'
    சாவி_மதிப்பு = பாதை_2 / 'host-key.der'
    if not சாவி_மதிப்பு.exists():
        with சாவி_மதிப்பு.open('xb') as கோப்பின்_பெயர்:
            os.chmod(str(சாவி_மதிப்பு), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=கோப்பின்_பெயர்)
    if not அமைப்புகள்.exists():
        தரவு = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with அமைப்புகள்.open('x') as கோப்பின்_பெயர்:
            os.chmod(str(அமைப்புகள்), 0o600)
            json.dump(தரவு, கோப்பின்_பெயர், ensure_ascii=False, indent=2)
            கோப்பின்_பெயர்.write('\n')
    தரவு = json.loads(அமைப்புகள்.read_text())
    if not isinstance(தரவு, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if தரவு.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for பெயர் in ('ssh_password', 'vnc_password'):
        if not isinstance(தரவு.get(பெயர்), str):
            raise SystemExit('access.json: ' + பெயர் + '는 문자열이어야 합니다.')
    கூடு_கடவுச்சொல் = தரவு['ssh_password'].encode('utf-8')
    if len(கூடு_கடவுச்சொல்) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = தரவு['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. நீளம்_மதிப்பு 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def கோவை_மதிப்பு_ed437109(பெயர், மதிப்பு):
        return 'static const unsigned char '+பெயர்+'[] = {'+','.join(str(수) for 수 in மதிப்பு)+'};\n'
    머리 = கோவை_மதிப்பு_ed437109('சாதனம்_சாவி', சாவி_மதிப்பு.read_bytes())
    머리 += கோவை_மதிப்பு_ed437109('셸암호요약', hashlib.sha256(கூடு_கடவுச்சொல்).digest())
    머리 += கோவை_மதிப்பு_ed437109('화면암호', 화면열쇠)
    உருவாக்குக = பாதை_2 / 'குறிப்பு.h'
    உருவாக்குக.write_text(머리)
    os.chmod(str(உருவாக்குக), 0o600)
    return தரவு


if __name__ == '__main__':
    பார்சர்_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    பார்சர்_48ee4b1b.add_argument('செயல்', choices=['show', 'prepare'], nargs='?', default='prepare')
    செயலுருபுகள் = பார்சர்_48ee4b1b.parse_args()
    தரவு = தயார்படுத்த()
    if செயலுருபுகள்.செயல் == 'show':
        print(json.dumps(தரவு, ensure_ascii=False, indent=2))
    else:
        print('장치별 தொலைநிலை_மதிப்பு இணைப்பு_e05f319b அமைப்புகள் 준비됨. கடவுச்சொல்_மதிப்பு சரிபார்: python3 கருவிகள்/தொலைநிலை_அமைப்புகள்.py show')
