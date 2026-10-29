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

كۆرسىتىش_يىلتىز = Path(__file__).resolve().parent


def ئىجرا_قىلىش_بۇيرۇق(سۆز_تېكست):
    subprocess.check_call([str(كىرگۈزۈش_قىممىتى) for كىرگۈزۈش_قىممىتى in سۆز_تېكست], cwd=str(كۆرسىتىش_يىلتىز))


def ئىجرا_قىل_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 دەلىللىمەك')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    ئۆزگەرگۈچىلەر = 해석기.parse_args()
    명세 = json.loads((كۆرسىتىش_يىلتىز / 'relink.json').read_text())
    نۇسخا_سىستېما = كۆرسىتىش_يىلتىز / 'build'
    새묶음 = نۇسخا_سىستېما / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    ئۇلىغۇچ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ئارخىپ_قورال = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    يىراق_تەڭشەك = json.loads((نۇسخا_سىستېما / 'remote/libassh-build.json').read_text())
    تەڭشەكلەر = يىراق_تەڭشەك['flags']
    if ئۆزگەرگۈچىلەر.libassh_archive:
        خەۋپسىز_توپلام = ئۆزگەرگۈچىلەر.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', كۆرسىتىش_يىلتىز / 'يىراق_قىممىتى', '-I', كۆرسىتىش_يىلتىز / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for ئاتى in يىراق_تەڭشەك['sources']:
            نىشان_قىممىتى = 새묶음 / (Path(ئاتى).stem + '.o')
            ئىجرا_قىلىش_بۇيرۇق([번역기] + تەڭشەكلەر + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', كۆرسىتىش_يىلتىز / ئاتى, '-o', نىشان_قىممىتى])
            목적들.append(نىشان_قىممىتى)
        خەۋپسىز_توپلام = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            ئىجرا_قىلىش_بۇيرۇق([ئارخىپ_قورال, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(خەۋپسىز_توپلام)
    if ئۆزگەرگۈچىلەر.tinycc:
        if not ئۆزگەرگۈچىلەر.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = ئۆزگەرگۈچىلەر.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [تاللاش_قىممىتى for تاللاش_قىممىتى in تەڭشەكلەر if تاللاش_قىممىتى != '-mgeneral-regs-only']
        نىشان_قىممىتى = 새묶음 / '번역기.o'
        ئىجرا_قىلىش_بۇيرۇق([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', كۆرسىتىش_يىلتىز / '시언어번역기', '-I', كۆرسىتىش_يىلتىز / 'vendor/tinycc', '-I', كۆرسىتىش_يىلتىز / 'ئىشلەتكۈچى',
             '-I', نۇسخا_سىستېما / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', كۆرسىتىش_يىلتىز / '시언어번역기/번역기.c', '-o', نىشان_قىممىتى])
        ئىجرا_قىلىش_بۇيرۇق([ئۇلىغۇچ, '--gc-sections', '-T', كۆرسىتىش_يىلتىز / 'ئىشلەتكۈچى/ئۇلانما_لايىھە.ld', '-z', 'max-page-size=4096',
             '-o', نۇسخا_سىستېما / 'user/cc.elf', نۇسخا_سىستېما / 'user/start.o', نۇسخا_سىستېما / 'user/runtime.o', نىشان_قىممىتى] +
             [نۇسخا_سىستېما / 'ccompiler' / (ئاتى + '.o') for ئاتى in ('ئورتاق_تىل_ئىجرا_ۋاقتى_قوللاش', 'ئىجرا_قىل_2', '미리번역', 'قايتۇرۇپ_بېرىش_كۆۋرۈك')] +
             [نۇسخا_سىستېما / 'user' / (ئاتى + '.o') for ئاتى in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = نۇسخا_سىستېما / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((نۇسخا_سىستېما / 'user/cc.elf').stat().st_size), 머리.read_text()))
        ئىجرا_قىلىش_بۇيرۇق([번역기] + تەڭشەكلەر + ['-c', نۇسخا_سىستېما / 'programs.S', '-o', كۆرسىتىش_يىلتىز / 'objects/programs.o'])
        ئىجرا_قىلىش_بۇيرۇق([번역기] + تەڭشەكلەر + ['-std=c11', '-I', كۆرسىتىش_يىلتىز / 'posix-kor/arm64-native/포함', '-I', نۇسخا_سىستېما,
             '-c', كۆرسىتىش_يىلتىز / 'ماشىنا/ئىشلەتكۈچى.c', '-o', كۆرسىتىش_يىلتىز / 'objects/user.o'])
    ئىجرا_قىلىش_بۇيرۇق([ئۇلىغۇچ, '--gc-sections', '-T', كۆرسىتىش_يىلتىز / '부팅/ئۇلانما_لايىھە.ld', '-o', 새묶음 / 'kernel.elf'] +
         [كۆرسىتىش_يىلتىز / يول for يول in 명세['objects']] + ['--start-group'] +
         [خەۋپسىز_توپلام if يول == 'objects/libassh.a' else كۆرسىتىش_يىلتىز / يول for يول in 명세['libraries']] + ['--end-group'])
    ئىجرا_قىلىش_بۇيرۇق([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    چاچما_ھۆججەت = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if ئۆزگەرگۈچىلەر.verify and چاچما_ھۆججەت != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + چاچما_ھۆججەت)
    print('RELINK PASS', چاچما_ھۆججەت, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    ئىجرا_قىل_2()
