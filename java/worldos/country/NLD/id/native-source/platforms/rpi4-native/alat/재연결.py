#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 Asli 커널을 coba_lagi_VALUE 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

Tugas_akar = Path(__file__).resolve().parent


def Jalankan_perintah(Kata_SMS):
    subprocess.check_call([str(entri_VALUE) for entri_VALUE in Kata_SMS], cwd=str(Tugas_akar))


def jalankan():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 periksa')
    parser_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a gunakan_VALUE')
    parser_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 coba_lagi_VALUE 컴파일하고 커널에 탑재')
    parser_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    argumen = parser_48ee4b1b.parse_args()
    spes = json.loads((Tugas_akar / 'relink.json').read_text())
    bangun = Tugas_akar / 'build'
    새묶음 = bangun / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    Konektor = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arsip_alat = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    jarak_jauh_Pengaturan = json.loads((bangun / 'remote/libassh-build.json').read_text())
    Konfigurasi = jarak_jauh_Pengaturan['flags']
    if argumen.libassh_archive:
        Keamanan_paket = argumen.libassh_archive.resolve()
    else:
        목적들 = []
        deklarasi = ['-I', Tugas_akar / 'jarak_jauh_VALUE', '-I', Tugas_akar / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Nama_2 in jarak_jauh_Pengaturan['sources']:
            tujuan_VALUE = 새묶음 / (Path(Nama_2).stem + '.o')
            Jalankan_perintah([번역기] + Konfigurasi + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + deklarasi +
                 ['-c', Tugas_akar / Nama_2, '-o', tujuan_VALUE])
            목적들.append(tujuan_VALUE)
        Keamanan_paket = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Jalankan_perintah([Arsip_alat, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Keamanan_paket)
    if argumen.tinycc:
        if not argumen.sdk:
            parser_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = argumen.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            parser_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [pilihan_VALUE for pilihan_VALUE in Konfigurasi if pilihan_VALUE != '-mgeneral-regs-only']
        tujuan_VALUE = 새묶음 / '번역기.o'
        Jalankan_perintah([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Tugas_akar / '시언어번역기', '-I', Tugas_akar / 'vendor/tinycc', '-I', Tugas_akar / 'ruang_pengguna',
             '-I', bangun / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', Tugas_akar / '시언어번역기/번역기.c', '-o', tujuan_VALUE])
        Jalankan_perintah([Konektor, '--gc-sections', '-T', Tugas_akar / 'ruang_pengguna/tata_letak_penautan.ld', '-z', 'max-page-size=4096',
             '-o', bangun / 'user/cc.elf', bangun / 'user/start.o', bangun / 'user/runtime.o', tujuan_VALUE] +
             [bangun / 'ccompiler' / (Nama_2 + '.o') for Nama_2 in ('runtime_bahasa_umum_dukung', 'jalankan', '미리번역', 'kembalikan_bridge')] +
             [bangun / 'user' / (Nama_2 + '.o') for Nama_2 in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        kepala_VALUE = bangun / 'programs.h'
        kepala_VALUE.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((bangun / 'user/cc.elf').stat().st_size), kepala_VALUE.read_text()))
        Jalankan_perintah([번역기] + Konfigurasi + ['-c', bangun / 'programs.S', '-o', Tugas_akar / 'objects/programs.o'])
        Jalankan_perintah([번역기] + Konfigurasi + ['-std=c11', '-I', Tugas_akar / 'posix-kor/arm64-native/deklarasi', '-I', bangun,
             '-c', Tugas_akar / 'mesin/ruang_pengguna.c', '-o', Tugas_akar / 'objects/user.o'])
    Jalankan_perintah([Konektor, '--gc-sections', '-T', Tugas_akar / 'awal_mesin/tata_letak_penautan.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Tugas_akar / jalur for jalur in spes['objects']] + ['--start-group'] +
         [Keamanan_paket if jalur == 'objects/libassh.a' else Tugas_akar / jalur for jalur in spes['libraries']] + ['--end-group'])
    Jalankan_perintah([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_file = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if argumen.verify and hash_file != spes['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_file)
    print('RELINK PASS', hash_file, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    jalankan()
