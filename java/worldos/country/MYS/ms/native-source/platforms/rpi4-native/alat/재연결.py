#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 Asli 커널을 다시 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

projek_akar = Path(__file__).resolve().parent


def laksanakan_perintah(Word_SMS):
    subprocess.check_call([str(pemasukan_VALUE) for pemasukan_VALUE in Word_SMS], cwd=str(projek_akar))


def Jalan():
    penghurai_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    penghurai_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 tentu_sahkan')
    penghurai_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    penghurai_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    penghurai_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = penghurai_48ee4b1b.parse_args()
    명세 = json.loads((projek_akar / 'relink.json').read_text())
    bina_sistem = projek_akar / 'build'
    새묶음 = bina_sistem / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    Penyambung = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arkib_alat = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    jauh_Seting = json.loads((bina_sistem / 'remote/libassh-build.json').read_text())
    Tetapan = jauh_Seting['flags']
    if 인수.libassh_archive:
        Keselamatan_pakej = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        pengisytiharan = ['-I', projek_akar / 'jauh_VALUE', '-I', projek_akar / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Nama in jauh_Seting['sources']:
            destinasi_VALUE = 새묶음 / (Path(Nama).stem + '.o')
            laksanakan_perintah([번역기] + Tetapan + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + pengisytiharan +
                 ['-c', projek_akar / Nama, '-o', destinasi_VALUE])
            목적들.append(destinasi_VALUE)
        Keselamatan_pakej = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            laksanakan_perintah([Arkib_alat, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Keselamatan_pakej)
    if 인수.tinycc:
        if not 인수.sdk:
            penghurai_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            penghurai_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [pilihan_VALUE for pilihan_VALUE in Tetapan if pilihan_VALUE != '-mgeneral-regs-only']
        destinasi_VALUE = 새묶음 / '번역기.o'
        laksanakan_perintah([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', projek_akar / '시언어번역기', '-I', projek_akar / 'vendor/tinycc', '-I', projek_akar / 'ruang_pengguna',
             '-I', bina_sistem / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', projek_akar / '시언어번역기/번역기.c', '-o', destinasi_VALUE])
        laksanakan_perintah([Penyambung, '--gc-sections', '-T', projek_akar / 'ruang_pengguna/susun_atur_pautan.ld', '-z', 'max-page-size=4096',
             '-o', bina_sistem / 'user/cc.elf', bina_sistem / 'user/start.o', bina_sistem / 'user/runtime.o', destinasi_VALUE] +
             [bina_sistem / 'ccompiler' / (Nama + '.o') for Nama in ('masa_jalan_bahasa_biasa_Sokongan', 'Jalan', '미리번역', 'kembalikan_penghubung')] +
             [bina_sistem / 'user' / (Nama + '.o') for Nama in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = bina_sistem / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((bina_sistem / 'user/cc.elf').stat().st_size), 머리.read_text()))
        laksanakan_perintah([번역기] + Tetapan + ['-c', bina_sistem / 'programs.S', '-o', projek_akar / 'objects/programs.o'])
        laksanakan_perintah([번역기] + Tetapan + ['-std=c11', '-I', projek_akar / 'posix-kor/arm64-native/pengisytiharan', '-I', bina_sistem,
             '-c', projek_akar / 'mesin/ruang_pengguna.c', '-o', projek_akar / 'objects/user.o'])
    laksanakan_perintah([Penyambung, '--gc-sections', '-T', projek_akar / 'permulaan_mesin/susun_atur_pautan.ld', '-o', 새묶음 / 'kernel.elf'] +
         [projek_akar / LALUAN for LALUAN in 명세['objects']] + ['--start-group'] +
         [Keselamatan_pakej if LALUAN == 'objects/libassh.a' else projek_akar / LALUAN for LALUAN in 명세['libraries']] + ['--end-group'])
    laksanakan_perintah([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    cincangan_fail = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and cincangan_fail != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + cincangan_fail)
    print('RELINK PASS', cincangan_fail, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Jalan()
