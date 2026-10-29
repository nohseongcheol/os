#!/usr/bin/env python3
"""장치별 ກະແຈ_ຄ່າ·ການເຊື່ອມຕໍ່_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

ໂຄງ_ການ_ເລກຮາກ = Path(__file__).resolve().parents[1]


def ກະ_ກຽມ(ໂຄງ_ການ_ເລກຮາກ=ໂຄງ_ການ_ເລກຮາກ):
    ທາງໂຄຈອນ = ໂຄງ_ການ_ເລກຮາກ / 'build/remote'
    ທາງໂຄຈອນ.mkdir(parents=True, exist_ok=True)
    ການຕັ້ງຄ່າ = ທາງໂຄຈອນ / 'access.json'
    ກະແຈ_ຄ່າ = ທາງໂຄຈອນ / 'host-key.der'
    if not ກະແຈ_ຄ່າ.exists():
        with ກະແຈ_ຄ່າ.open('xb') as ຟາຍ:
            os.chmod(str(ກະແຈ_ຄ່າ), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ຟາຍ)
    if not ການຕັ້ງຄ່າ.exists():
        ຂໍ້ມູນ = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with ການຕັ້ງຄ່າ.open('x') as ຟາຍ:
            os.chmod(str(ການຕັ້ງຄ່າ), 0o600)
            json.dump(ຂໍ້ມູນ, ຟາຍ, ensure_ascii=False, indent=2)
            ຟາຍ.write('\n')
    ຂໍ້ມູນ = json.loads(ການຕັ້ງຄ່າ.read_text())
    if not isinstance(ຂໍ້ມູນ, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if ຂໍ້ມູນ.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for ຊື່ in ('ssh_password', 'vnc_password'):
        if not isinstance(ຂໍ້ມູນ.get(ຊື່), str):
            raise SystemExit('access.json: ' + ຊື່ + '는 문자열이어야 합니다.')
    ເຊລ_ລະຫັດຜ່ານ = ຂໍ້ມູນ['ssh_password'].encode('utf-8')
    if len(ເຊລ_ລະຫັດຜ່ານ) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = ຂໍ້ມູນ['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. ຄວາມຍາວ_ຄ່າ 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ການຈັດຄ່າຮອບວຽນ_ຄ່າ(ຊື່, ຄ່າ):
        return 'static const unsigned char '+ຊື່+'[] = {'+','.join(str(수) for 수 in ຄ່າ)+'};\n'
    머리 = ການຈັດຄ່າຮອບວຽນ_ຄ່າ('ມືຖື_ກະແຈ', ກະແຈ_ຄ່າ.read_bytes())
    머리 += ການຈັດຄ່າຮອບວຽນ_ຄ່າ('셸암호요약', hashlib.sha256(ເຊລ_ລະຫັດຜ່ານ).digest())
    머리 += ການຈັດຄ່າຮອບວຽນ_ຄ່າ('화면암호', 화면열쇠)
    ສ້າງ_167eff27 = ທາງໂຄຈອນ / 'ໂປຣໄຟລ໌.h'
    ສ້າງ_167eff27.write_text(머리)
    os.chmod(str(ສ້າງ_167eff27), 0o600)
    return ຂໍ້ມູນ


if __name__ == '__main__':
    ຕົວແຍກວິເຄາະ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('ຄໍາສັ່ງ', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = ຕົວແຍກວິເຄາະ_48ee4b1b.parse_args()
    ຂໍ້ມູນ = ກະ_ກຽມ()
    if 인수.ຄໍາສັ່ງ == 'show':
        print(json.dumps(ຂໍ້ມູນ, ensure_ascii=False, indent=2))
    else:
        print('장치별 ທາງ_ໄກ_ຄ່າ ການເຊື່ອມຕໍ່_e05f319b ການຕັ້ງຄ່າ 준비됨. ລະຫັດຜ່ານ_ຄ່າ 확인: python3 ເຄື່ອງມື/ທາງ_ໄກ_ການຕັ້ງຄ່າ.py show')
