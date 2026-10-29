#!/usr/bin/env python3
"""개인 ການເຊື່ອມຕໍ່_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from ທາງ_ໄກ_ການຕັ້ງຄ່າ import ກະ_ກຽມ
from COSL배포 import ປາຍທາງ_ຊື່, ຫໍສະຫມຸດ

ໂຄງ_ການ_ເລກຮາກ = Path(__file__).resolve().parents[1]


def ແລ່ນ():
    출력 = ໂຄງ_ການ_ເລກຮາກ / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    ຕັ້ງຄ່າສ່ວນຕົວ = ໂຄງ_ການ_ເລກຮາກ / 'build/remote/access.json'
    원래설정 = ຕັ້ງຄ່າສ່ວນຕົວ.read_bytes()
    ລາຍງານ_ຄ່າ = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            ການຕັ້ງຄ່າ_ທາງໂຄຈອນ = 시험터 / 'build/remote'
            ການຕັ້ງຄ່າ_ທາງໂຄຈອນ.mkdir(parents=True)
            ການຕັ້ງຄ່າ_ຟາຍ = ການຕັ້ງຄ່າ_ທາງໂຄຈອນ / 'access.json'
            def ຂຽນ_ການຕັ້ງຄ່າ(ຂໍ້ມູນ):
                ການຕັ້ງຄ່າ_ຟາຍ.write_text(json.dumps(ຂໍ້ມູນ, ensure_ascii=False) + '\n')
                ການຕັ້ງຄ່າ_ຟາຍ.chmod(0o600)
            def 설정확인(ເຊລ, 화면):
                ຂຽນ_ການຕັ້ງຄ່າ({'user': 'user', 'ssh_password': ເຊລ, 'vnc_password': 화면})
                원본 = ການຕັ້ງຄ່າ_ຟາຍ.read_bytes()
                ກະ_ກຽມ(시험터)
                assert ການຕັ້ງຄ່າ_ຟາຍ.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (ການຕັ້ງຄ່າ_ທາງໂຄຈອນ / 'ໂປຣໄຟລ໌.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (ການຕັ້ງຄ່າ_ທາງໂຄຈອນ / 'ໂປຣໄຟລ໌.h').stat().st_mode & 0o777 == 0o600
            for ເຊລ, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                설정확인(ເຊລ, 화면)
            ລາຍງານ_ຄ່າ['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for ປ່ຽນ_ແປງ_ຄ່າ, ເຂົ້າໃນ_ຄ່າ in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                ຂໍ້ມູນ = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                ຂໍ້ມູນ.update(ປ່ຽນ_ແປງ_ຄ່າ)
                ຂຽນ_ການຕັ້ງຄ່າ(ຂໍ້ມູນ)
                try:
                    ກະ_ກຽມ(시험터)
                except SystemExit as ຂໍ້ຜິດພາດ:
                    assert ເຂົ້າໃນ_ຄ່າ in str(ຂໍ້ຜິດພາດ), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ເຂົ້າໃນ_ຄ່າ)
            ລາຍງານ_ຄ່າ['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            ການຕັ້ງຄ່າ = json.loads((ໂຄງ_ການ_ເລກຮາກ / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            ຕົວ_ເຊື່ອມ_ຕໍ່ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            ການສໍາເນົາ_ເຄື່ອງມື = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(인수, ບັນທຶກ_ແຖວ):
                subprocess.run(list(map(str, 인수)), cwd=str(ໂຄງ_ການ_ເລກຮາກ), stdout=ບັນທຶກ_ແຖວ,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for ຊື່, ເຊລ, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + ຊື່, flush=True)
                설정확인(ເຊລ, 화면)
                ມາດຕະການ = 출력 / ຊື່
                ມາດຕະການ.mkdir(exist_ok=True)
                with (ມາດຕະການ / 'build.log').open('wb') as ບັນທຶກ_ແຖວ:
                    목적들 = []
                    for 원본 in sorted((ໂຄງ_ການ_ເລກຮາກ / 'ທາງ_ໄກ_ຄ່າ').glob('*.c')):
                        ປາຍທາງ_ຄ່າ = 시험터 / (원본.stem + '.o')
                        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([번역기] + ການຕັ້ງຄ່າ + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', ການຕັ້ງຄ່າ_ທາງໂຄຈອນ, '-I', ໂຄງ_ການ_ເລກຮາກ / 'ທາງ_ໄກ_ຄ່າ', '-I', ໂຄງ_ການ_ເລກຮາກ / 'vendor/libassh/src',
                             '-I', ໂຄງ_ການ_ເລກຮາກ / 'vendor/bearssl/inc', '-I', ໂຄງ_ການ_ເລກຮາກ / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', ປາຍທາງ_ຄ່າ], ບັນທຶກ_ແຖວ)
                        목적들.append(ປາຍທາງ_ຄ່າ)
                    ທາງ_ໄກ_ຂາຍສ່ວນຕ່າງຮວມເຂົ້າດ້ວຍກັນ = 시험터 / 'libremote.a'
                    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([ການສໍາເນົາ_ເຄື່ອງມື, 'rcs', ທາງ_ໄກ_ຂາຍສ່ວນຕ່າງຮວມເຂົ້າດ້ວຍກັນ] + 목적들, ບັນທຶກ_ແຖວ)
                    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([ຕົວ_ເຊື່ອມ_ຕໍ່, '--gc-sections', '-T', ໂຄງ_ການ_ເລກຮາກ / '부팅/ລິ້ງ_ຮູບແບບ.ld', '-o', 시험터 / 'kernel.elf'] +
                         [ໂຄງ_ການ_ເລກຮາກ / 'build' / (ຊື່ + '.o') for ຊື່ in ປາຍທາງ_ຊື່] + ['--start-group'] +
                         [ທາງ_ໄກ_ຂາຍສ່ວນຕ່າງຮວມເຂົ້າດ້ວຍກັນ if ທາງໂຄຈອນ == 'remote/libremote.a' else ໂຄງ_ການ_ເລກຮາກ / 'build' / ທາງໂຄຈອນ for ທາງໂຄຈອນ in ຫໍສະຫມຸດ] + ['--end-group'], ບັນທຶກ_ແຖວ)
                    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], ບັນທຶກ_ແຖວ)
                with (ມາດຕະການ / 'remote-test.log').open('wb') as ບັນທຶກ_ແຖວ:
                    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(['python3', ໂຄງ_ການ_ເລກຮາກ / 'ເຄື່ອງມື/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', ການຕັ້ງຄ່າ_ຟາຍ, '--output', ມາດຕະການ], ບັນທຶກ_ແຖວ)
                ຮັບ_ຮອງ = json.loads((ມາດຕະການ / 'report.json').read_text())
                assert ຮັບ_ຮອງ['passed']
                ລາຍງານ_ຄ່າ['checks'].append(ຊື່ + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        ລາຍງານ_ຄ່າ['passed'] = True
    finally:
        ລາຍງານ_ຄ່າ['personal_settings_unchanged'] = ຕັ້ງຄ່າສ່ວນຕົວ.read_bytes() == 원래설정
        if not ລາຍງານ_ຄ່າ['personal_settings_unchanged']:
            ລາຍງານ_ຄ່າ['passed'] = False
        ລາຍງານ_ຄ່າ['kernel_sha256'] = hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(ລາຍງານ_ຄ່າ, ensure_ascii=False, indent=2) + '\n')
    assert ລາຍງານ_ຄ່າ['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(ລາຍງານ_ຄ່າ, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ແລ່ນ()
