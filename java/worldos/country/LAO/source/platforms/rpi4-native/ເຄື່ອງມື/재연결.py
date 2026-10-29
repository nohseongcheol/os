#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 자체 커널을 다시 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ໂຄງ_ການ_ເລກຮາກ = Path(__file__).resolve().parent


def ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ):
    subprocess.check_call([str(ເຂົ້າໃນ_ຄ່າ) for ເຂົ້າໃນ_ຄ່າ in ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ], cwd=str(ໂຄງ_ການ_ເລກຮາກ))


def ແລ່ນ():
    ຕົວແຍກວິເຄາະ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 확인')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = ຕົວແຍກວິເຄາະ_48ee4b1b.parse_args()
    명세 = json.loads((ໂຄງ_ການ_ເລກຮາກ / 'relink.json').read_text())
    ສ້າງ_ລະບົບ = ໂຄງ_ການ_ເລກຮາກ / 'build'
    새묶음 = ສ້າງ_ລະບົບ / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    ຕົວ_ເຊື່ອມ_ຕໍ່ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ການສໍາເນົາ_ເຄື່ອງມື = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    ທາງ_ໄກ_ການຕັ້ງຄ່າ = json.loads((ສ້າງ_ລະບົບ / 'remote/libassh-build.json').read_text())
    ການຕັ້ງຄ່າ = ທາງ_ໄກ_ການຕັ້ງຄ່າ['flags']
    if 인수.libassh_archive:
        ຄວາມປອດໄພ_ຂາຍສ່ວນຕ່າງຮວມເຂົ້າດ້ວຍກັນ = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', ໂຄງ_ການ_ເລກຮາກ / 'ທາງ_ໄກ_ຄ່າ', '-I', ໂຄງ_ການ_ເລກຮາກ / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for ຊື່ in ທາງ_ໄກ_ການຕັ້ງຄ່າ['sources']:
            ປາຍທາງ_ຄ່າ = 새묶음 / (Path(ຊື່).stem + '.o')
            ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([번역기] + ການຕັ້ງຄ່າ + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', ໂຄງ_ການ_ເລກຮາກ / ຊື່, '-o', ປາຍທາງ_ຄ່າ])
            목적들.append(ປາຍທາງ_ຄ່າ)
        ຄວາມປອດໄພ_ຂາຍສ່ວນຕ່າງຮວມເຂົ້າດ້ວຍກັນ = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([ການສໍາເນົາ_ເຄື່ອງມື, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(ຄວາມປອດໄພ_ຂາຍສ່ວນຕ່າງຮວມເຂົ້າດ້ວຍກັນ)
    if 인수.tinycc:
        if not 인수.sdk:
            ຕົວແຍກວິເຄາະ_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            ຕົວແຍກວິເຄາະ_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [ການ_ເລືອກ_ຄ່າ for ການ_ເລືອກ_ຄ່າ in ການຕັ້ງຄ່າ if ການ_ເລືອກ_ຄ່າ != '-mgeneral-regs-only']
        ປາຍທາງ_ຄ່າ = 새묶음 / '번역기.o'
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', ໂຄງ_ການ_ເລກຮາກ / '시언어번역기', '-I', ໂຄງ_ການ_ເລກຮາກ / 'vendor/tinycc', '-I', ໂຄງ_ການ_ເລກຮາກ / 'ຜູ້ໃຊ້',
             '-I', ສ້າງ_ລະບົບ / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', ໂຄງ_ການ_ເລກຮາກ / '시언어번역기/번역기.c', '-o', ປາຍທາງ_ຄ່າ])
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([ຕົວ_ເຊື່ອມ_ຕໍ່, '--gc-sections', '-T', ໂຄງ_ການ_ເລກຮາກ / 'ຜູ້ໃຊ້/ລິ້ງ_ຮູບແບບ.ld', '-z', 'max-page-size=4096',
             '-o', ສ້າງ_ລະບົບ / 'user/cc.elf', ສ້າງ_ລະບົບ / 'user/start.o', ສ້າງ_ລະບົບ / 'user/runtime.o', ປາຍທາງ_ຄ່າ] +
             [ສ້າງ_ລະບົບ / 'ccompiler' / (ຊື່ + '.o') for ຊື່ in ('실행지원', 'ແລ່ນ', '미리번역', '되돌림')] +
             [ສ້າງ_ລະບົບ / 'user' / (ຊື່ + '.o') for ຊື່ in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = ສ້າງ_ລະບົບ / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((ສ້າງ_ລະບົບ / 'user/cc.elf').stat().st_size), 머리.read_text()))
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([번역기] + ການຕັ້ງຄ່າ + ['-c', ສ້າງ_ລະບົບ / 'programs.S', '-o', ໂຄງ_ການ_ເລກຮາກ / 'objects/programs.o'])
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([번역기] + ການຕັ້ງຄ່າ + ['-std=c11', '-I', ໂຄງ_ການ_ເລກຮາກ / 'posix-kor/arm64-native/포함', '-I', ສ້າງ_ລະບົບ,
             '-c', ໂຄງ_ການ_ເລກຮາກ / 'ເຄື່ອງຈັກ/ຜູ້ໃຊ້.c', '-o', ໂຄງ_ການ_ເລກຮາກ / 'objects/user.o'])
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([ຕົວ_ເຊື່ອມ_ຕໍ່, '--gc-sections', '-T', ໂຄງ_ການ_ເລກຮາກ / '부팅/ລິ້ງ_ຮູບແບບ.ld', '-o', 새묶음 / 'kernel.elf'] +
         [ໂຄງ_ການ_ເລກຮາກ / ທາງໂຄຈອນ for ທາງໂຄຈອນ in 명세['objects']] + ['--start-group'] +
         [ຄວາມປອດໄພ_ຂາຍສ່ວນຕ່າງຮວມເຂົ້າດ້ວຍກັນ if ທາງໂຄຈອນ == 'objects/libassh.a' else ໂຄງ_ການ_ເລກຮາກ / ທາງໂຄຈອນ for ທາງໂຄຈອນ in 명세['libraries']] + ['--end-group'])
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    ແຮຊ_ຟາຍ = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and ແຮຊ_ຟາຍ != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + ແຮຊ_ຟາຍ)
    print('RELINK PASS', ແຮຊ_ຟາຍ, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    ແລ່ນ()
