#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 اپنا 커널을 다시 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

عکس_ڈالنا_روٹ = Path(__file__).resolve().parent


def نفاذ_کریں_حکم(الفاظ_متن):
    subprocess.check_call([str(اندراج_قدر) for اندراج_قدر in الفاظ_متن], cwd=str(عکس_ڈالنا_روٹ))


def چلائیں():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 تصدیق_کریں')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    دلائل = 해석기.parse_args()
    명세 = json.loads((عکس_ڈالنا_روٹ / 'relink.json').read_text())
    بلڈ_نظام = عکس_ڈالنا_روٹ / 'build'
    새묶음 = بلڈ_نظام / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    کنکٹر = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    محفوظ_ٹول = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    بعید_سیٹنگز = json.loads((بلڈ_نظام / 'remote/libassh-build.json').read_text())
    ترتیبات = بعید_سیٹنگز['flags']
    if دلائل.libassh_archive:
        سلامتی_بنڈل = دلائل.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', عکس_ڈالنا_روٹ / 'بعید_قدر', '-I', عکس_ڈالنا_روٹ / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for نام in بعید_سیٹنگز['sources']:
            منزل_مقصود_قدر = 새묶음 / (Path(نام).stem + '.o')
            نفاذ_کریں_حکم([번역기] + ترتیبات + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', عکس_ڈالنا_روٹ / نام, '-o', منزل_مقصود_قدر])
            목적들.append(منزل_مقصود_قدر)
        سلامتی_بنڈل = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            نفاذ_کریں_حکم([محفوظ_ٹول, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(سلامتی_بنڈل)
    if دلائل.tinycc:
        if not دلائل.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = دلائل.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [انتخاب_قدر for انتخاب_قدر in ترتیبات if انتخاب_قدر != '-mgeneral-regs-only']
        منزل_مقصود_قدر = 새묶음 / '번역기.o'
        نفاذ_کریں_حکم([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', عکس_ڈالنا_روٹ / '시언어번역기', '-I', عکس_ڈالنا_روٹ / 'vendor/tinycc', '-I', عکس_ڈالنا_روٹ / 'صارف',
             '-I', بلڈ_نظام / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', عکس_ڈالنا_روٹ / '시언어번역기/번역기.c', '-o', منزل_مقصود_قدر])
        نفاذ_کریں_حکم([کنکٹر, '--gc-sections', '-T', عکس_ڈالنا_روٹ / 'صارف/ربط_ترتیب.ld', '-z', 'max-page-size=4096',
             '-o', بلڈ_نظام / 'user/cc.elf', بلڈ_نظام / 'user/start.o', بلڈ_نظام / 'user/runtime.o', منزل_مقصود_قدر] +
             [بلڈ_نظام / 'ccompiler' / (نام + '.o') for نام in ('عام_زبان_چلت_عرصہ_معاونت', 'چلائیں', '미리번역', '되돌림')] +
             [بلڈ_نظام / 'user' / (نام + '.o') for نام in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = بلڈ_نظام / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((بلڈ_نظام / 'user/cc.elf').stat().st_size), 머리.read_text()))
        نفاذ_کریں_حکم([번역기] + ترتیبات + ['-c', بلڈ_نظام / 'programs.S', '-o', عکس_ڈالنا_روٹ / 'objects/programs.o'])
        نفاذ_کریں_حکم([번역기] + ترتیبات + ['-std=c11', '-I', عکس_ڈالنا_روٹ / 'posix-kor/arm64-native/포함', '-I', بلڈ_نظام,
             '-c', عکس_ڈالنا_روٹ / 'مشین/صارف.c', '-o', عکس_ڈالنا_روٹ / 'objects/user.o'])
    نفاذ_کریں_حکم([کنکٹر, '--gc-sections', '-T', عکس_ڈالنا_روٹ / '부팅/ربط_ترتیب.ld', '-o', 새묶음 / 'kernel.elf'] +
         [عکس_ڈالنا_روٹ / راستہ_2 for راستہ_2 in 명세['objects']] + ['--start-group'] +
         [سلامتی_بنڈل if راستہ_2 == 'objects/libassh.a' else عکس_ڈالنا_روٹ / راستہ_2 for راستہ_2 in 명세['libraries']] + ['--end-group'])
    نفاذ_کریں_حکم([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    ہيش_فائل = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if دلائل.verify and ہيش_فائل != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + ہيش_فائل)
    print('RELINK PASS', ہيش_فائل, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    چلائیں()
