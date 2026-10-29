#!/usr/bin/env python3
"""장치별 键值·接通状态 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

项目根 = Path(__file__).resolve().parents[1]


def 准备(项目根=项目根):
    路径 = 项目根 / 'build/remote'
    路径.mkdir(parents=True, exist_ok=True)
    设置 = 路径 / 'access.json'
    键值 = 路径 / 'host-key.der'
    if not 键值.exists():
        with 键值.open('xb') as 文件:
            os.chmod(str(键值), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=文件)
    if not 设置.exists():
        数据 = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with 设置.open('x') as 文件:
            os.chmod(str(设置), 0o600)
            json.dump(数据, 文件, ensure_ascii=False, indent=2)
            文件.write('\n')
    数据 = json.loads(设置.read_text())
    if not isinstance(数据, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if 数据.get('user') != 'user':
        raise SystemExit('access.json: user는 当前项目 "user"만 지원합니다.')
    for 名称 in ('ssh_password', 'vnc_password'):
        if not isinstance(数据.get(名称), str):
            raise SystemExit('access.json: ' + 名称 + '는 문자열이어야 합니다.')
    命令壳密码 = 数据['ssh_password'].encode('utf-8')
    if len(命令壳密码) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        屏幕密码 = 数据['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. 长度 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    屏幕键 = 屏幕密码[:8].ljust(8, b'\0')
    def 数组值(名称, 值):
        return 'static const unsigned char '+名称+'[] = {'+','.join(str(数) for 数 in 值)+'};\n'
    头值 = 数组值('设备键', 键值.read_bytes())
    头值 += 数组值('命令壳密码摘要', hashlib.sha256(命令壳密码).digest())
    头值 += 数组值('屏幕密码', 屏幕键)
    生成 = 路径 / '配置档.h'
    生成.write_text(头值)
    os.chmod(str(生成), 0o600)
    return 数据


if __name__ == '__main__':
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('动作', choices=['show', 'prepare'], nargs='?', default='prepare')
    实参 = 解析器.parse_args()
    数据 = 准备()
    if 实参.动作 == 'show':
        print(json.dumps(数据, ensure_ascii=False, indent=2))
    else:
        print('장치별 远程值 接通状态 设置 是否已准备. 密码值 验证: python3 工具集/远程设置.py show')
