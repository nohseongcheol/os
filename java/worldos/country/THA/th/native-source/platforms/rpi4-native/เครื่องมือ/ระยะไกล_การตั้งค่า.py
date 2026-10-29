#!/usr/bin/env python3
"""장치별 คีย์_ค่า·เพื่อน_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

แสดง_ราก = Path(__file__).resolve().parents[1]


def จัดเตรียม(แสดง_ราก=แสดง_ราก):
    เส้นทาง = แสดง_ราก / 'build/remote'
    เส้นทาง.mkdir(parents=True, exist_ok=True)
    ตั้งค่า = เส้นทาง / 'access.json'
    คีย์_ค่า = เส้นทาง / 'host-key.der'
    if not คีย์_ค่า.exists():
        with คีย์_ค่า.open('xb') as แฟ้ม:
            os.chmod(str(คีย์_ค่า), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=แฟ้ม)
    if not ตั้งค่า.exists():
        ข้อมูล = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with ตั้งค่า.open('x') as แฟ้ม:
            os.chmod(str(ตั้งค่า), 0o600)
            json.dump(ข้อมูล, แฟ้ม, ensure_ascii=False, indent=2)
            แฟ้ม.write('\n')
    ข้อมูล = json.loads(ตั้งค่า.read_text())
    if not isinstance(ข้อมูล, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if ข้อมูล.get('user') != 'user':
        raise SystemExit('access.json: user는 ปัจจุบัน_รายการ "user"만 지원합니다.')
    for ชื่อ in ('ssh_password', 'vnc_password'):
        if not isinstance(ข้อมูล.get(ชื่อ), str):
            raise SystemExit('access.json: ' + ชื่อ + '는 문자열이어야 합니다.')
    เชลล์_รหัสผ่าน = ข้อมูล['ssh_password'].encode('utf-8')
    if len(เชลล์_รหัสผ่าน) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = ข้อมูล['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. 길이 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def อาร์เรย์_ค่า(ชื่อ, ค่า):
        return 'static const unsigned char '+ชื่อ+'[] = {'+','.join(str(หมายเลข) for หมายเลข in ค่า)+'};\n'
    머리 = อาร์เรย์_ค่า('อุปกรณ์_คีย์', คีย์_ค่า.read_bytes())
    머리 += อาร์เรย์_ค่า('เชลล์_รหัสผ่าน_สรุป', hashlib.sha256(เชลล์_รหัสผ่าน).digest())
    머리 += อาร์เรย์_ค่า('화면암호', 화면열쇠)
    สร้าง_167eff27 = เส้นทาง / 'โปรไฟล์.h'
    สร้าง_167eff27.write_text(머리)
    os.chmod(str(สร้าง_167eff27), 0o600)
    return ข้อมูล


if __name__ == '__main__':
    ตัวแยกวิเคราะห์_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('การกระทํา', choices=['show', 'prepare'], nargs='?', default='prepare')
    อาร์กิวเมนต์ = ตัวแยกวิเคราะห์_48ee4b1b.parse_args()
    ข้อมูล = จัดเตรียม()
    if อาร์กิวเมนต์.การกระทํา == 'show':
        print(json.dumps(ข้อมูล, ensure_ascii=False, indent=2))
    else:
        print('장치별 ระยะไกล_ค่า เพื่อน_e05f319b ตั้งค่า 준비됨. รหัสผ่าน_ค่า ยืนยัน: python3 เครื่องมือ/ระยะไกล_การตั้งค่า.py show')
