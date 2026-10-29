#!/usr/bin/env python3
"""장치별 キー値·接続状態 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

計画根 = Path(__file__).resolve().parents[1]


def 用意(計画根=計画根):
    経路 = 計画根 / 'build/remote'
    経路.mkdir(parents=True, exist_ok=True)
    設定値 = 経路 / 'access.json'
    キー値 = 経路 / 'host-key.der'
    if not キー値.exists():
        with キー値.open('xb') as ファイル:
            os.chmod(str(キー値), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ファイル)
    if not 設定値.exists():
        データ = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with 設定値.open('x') as ファイル:
            os.chmod(str(設定値), 0o600)
            json.dump(データ, ファイル, ensure_ascii=False, indent=2)
            ファイル.write('\n')
    データ = json.loads(設定値.read_text())
    if not isinstance(データ, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if データ.get('user') != 'user':
        raise SystemExit('access.json: user는 現在項目 "user"만 지원합니다.')
    for 名前 in ('ssh_password', 'vnc_password'):
        if not isinstance(データ.get(名前), str):
            raise SystemExit('access.json: ' + 名前 + '는 문자열이어야 합니다.')
    シェル合言葉 = データ['ssh_password'].encode('utf-8')
    if len(シェル合言葉) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        画面合言葉 = データ['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. 長さ 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    画面キー = 画面合言葉[:8].ljust(8, b'\0')
    def 配列値(名前, 値):
        return 'static const unsigned char '+名前+'[] = {'+','.join(str(数) for 数 in 値)+'};\n'
    先頭部値 = 配列値('装置キー', キー値.read_bytes())
    先頭部値 += 配列値('シェル合言葉要約', hashlib.sha256(シェル合言葉).digest())
    先頭部値 += 配列値('画面合言葉', 画面キー)
    生成 = 経路 / '動作設定.h'
    生成.write_text(先頭部値)
    os.chmod(str(生成), 0o600)
    return データ


if __name__ == '__main__':
    構文解析器 = argparse.ArgumentParser(description=__doc__)
    構文解析器.add_argument('動作', choices=['show', 'prepare'], nargs='?', default='prepare')
    引数 = 構文解析器.parse_args()
    データ = 用意()
    if 引数.動作 == 'show':
        print(json.dumps(データ, ensure_ascii=False, indent=2))
    else:
        print('장치별 遠隔値 接続状態 設定値 判定用意済み. 合言葉値 検証: python3 道具/遠隔設定値.py show')
