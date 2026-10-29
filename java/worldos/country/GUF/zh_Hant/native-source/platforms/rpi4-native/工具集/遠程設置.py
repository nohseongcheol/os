#!/usr/bin/env python3
"""장치별 鍵值·接通狀態 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

項目根 = Path(__file__).resolve().parents[1]


def 準備(項目根=項目根):
    路徑 = 項目根 / 'build/remote'
    路徑.mkdir(parents=True, exist_ok=True)
    設置 = 路徑 / 'access.json'
    鍵值 = 路徑 / 'host-key.der'
    if not 鍵值.exists():
        with 鍵值.open('xb') as 檔案:
            os.chmod(str(鍵值), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=檔案)
    if not 設置.exists():
        資料 = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with 設置.open('x') as 檔案:
            os.chmod(str(設置), 0o600)
            json.dump(資料, 檔案, ensure_ascii=False, indent=2)
            檔案.write('\n')
    資料 = json.loads(設置.read_text())
    if not isinstance(資料, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if 資料.get('user') != 'user':
        raise SystemExit('access.json: user는 當前項目 "user"만 지원합니다.')
    for 名稱 in ('ssh_password', 'vnc_password'):
        if not isinstance(資料.get(名稱), str):
            raise SystemExit('access.json: ' + 名稱 + '는 문자열이어야 합니다.')
    命令殼密碼 = 資料['ssh_password'].encode('utf-8')
    if len(命令殼密碼) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        屏幕密碼 = 資料['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. 長度 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    屏幕鍵 = 屏幕密碼[:8].ljust(8, b'\0')
    def 陣列值(名稱, 值):
        return 'static const unsigned char '+名稱+'[] = {'+','.join(str(數) for 數 in 值)+'};\n'
    頭值 = 陣列值('設備鍵', 鍵值.read_bytes())
    頭值 += 陣列值('命令殼密碼摘要', hashlib.sha256(命令殼密碼).digest())
    頭值 += 陣列值('屏幕密碼', 屏幕鍵)
    生成 = 路徑 / '配置檔.h'
    生成.write_text(頭值)
    os.chmod(str(生成), 0o600)
    return 資料


if __name__ == '__main__':
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('動作', choices=['show', 'prepare'], nargs='?', default='prepare')
    實參 = 解析器.parse_args()
    資料 = 準備()
    if 實參.動作 == 'show':
        print(json.dumps(資料, ensure_ascii=False, indent=2))
    else:
        print('장치별 遠程值 接通狀態 設置 是否已準備. 密碼值 驗證: python3 工具集/遠程設置.py show')
