#!/usr/bin/env python3
"""dağıtım_değer 묶음에서 libassh/TinyCC를 교체하고 Öz 커널을 yeniden_denemek_değer 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

işlem_kök = Path(__file__).resolve().parent


def yürütmek_komut(Word_SMS):
    subprocess.check_call([str(girdi_değer) for girdi_değer in Word_SMS], cwd=str(işlem_kök))


def çalıştır():
    ayrıştırıcı_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ayrıştırıcı_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 doğrulamak')
    ayrıştırıcı_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a kullanmak_değer')
    ayrıştırıcı_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 yeniden_denemek_değer 컴파일하고 커널에 탑재')
    ayrıştırıcı_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    bağımsız_değişkenler = ayrıştırıcı_48ee4b1b.parse_args()
    명세 = json.loads((işlem_kök / 'relink.json').read_text())
    oluştur = işlem_kök / 'build'
    새묶음 = oluştur / 'relinked'
    새묶음.mkdir(exist_ok=True)
    derleyici_araç = os.environ.get('ARM64_CC', 'clang')
    Bağlayıcı = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arşiv_araç = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    uzak_Ayarlar = json.loads((oluştur / 'remote/libassh-build.json').read_text())
    Ayarlar = uzak_Ayarlar['flags']
    if bağımsız_değişkenler.libassh_archive:
        Güvenlik_paket_iş = bağımsız_değişkenler.libassh_archive.resolve()
    else:
        목적들 = []
        bildirimler = ['-I', işlem_kök / 'uzak_değer', '-I', işlem_kök / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for İsim in uzak_Ayarlar['sources']:
            hedef_değer = 새묶음 / (Path(İsim).stem + '.o')
            yürütmek_komut([derleyici_araç] + Ayarlar + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + bildirimler +
                 ['-c', işlem_kök / İsim, '-o', hedef_değer])
            목적들.append(hedef_değer)
        Güvenlik_paket_iş = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            yürütmek_komut([Arşiv_araç, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Güvenlik_paket_iş)
    if bağımsız_değişkenler.tinycc:
        if not bağımsız_değişkenler.sdk:
            ayrıştırıcı_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = bağımsız_değişkenler.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            ayrıştırıcı_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [seçim_değer for seçim_değer in Ayarlar if seçim_değer != '-mgeneral-regs-only']
        hedef_değer = 새묶음 / 'derleyici_araç.o'
        yürütmek_komut([derleyici_araç] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', işlem_kök / 'C_derleyici', '-I', işlem_kök / 'vendor/tinycc', '-I', işlem_kök / 'kullanıcı_alanı',
             '-I', oluştur / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', işlem_kök / 'C_derleyici/derleyici_araç.c', '-o', hedef_değer])
        yürütmek_komut([Bağlayıcı, '--gc-sections', '-T', işlem_kök / 'kullanıcı_alanı/bağlama_düzeni.ld', '-z', 'max-page-size=4096',
             '-o', oluştur / 'user/cc.elf', oluştur / 'user/start.o', oluştur / 'user/runtime.o', hedef_değer] +
             [oluştur / 'ccompiler' / (İsim + '.o') for İsim in ('CLR_Destek', 'çalıştır', '미리번역', 'İade_köprü')] +
             [oluştur / 'user' / (İsim + '.o') for İsim in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = oluştur / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((oluştur / 'user/cc.elf').stat().st_size), 머리.read_text()))
        yürütmek_komut([derleyici_araç] + Ayarlar + ['-c', oluştur / 'programs.S', '-o', işlem_kök / 'objects/programs.o'])
        yürütmek_komut([derleyici_araç] + Ayarlar + ['-std=c11', '-I', işlem_kök / 'posix-kor/arm64-native/bildirimler', '-I', oluştur,
             '-c', işlem_kök / 'makine/kullanıcı_alanı.c', '-o', işlem_kök / 'objects/user.o'])
    yürütmek_komut([Bağlayıcı, '--gc-sections', '-T', işlem_kök / 'makine_başlatma/bağlama_düzeni.ld', '-o', 새묶음 / 'kernel.elf'] +
         [işlem_kök / yol for yol in 명세['objects']] + ['--start-group'] +
         [Güvenlik_paket_iş if yol == 'objects/libassh.a' else işlem_kök / yol for yol in 명세['libraries']] + ['--end-group'])
    yürütmek_komut([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    özet_Dosya = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if bağımsız_değişkenler.verify and özet_Dosya != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + özet_Dosya)
    print('RELINK PASS', özet_Dosya, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    çalıştır()
