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

បញ្ចាំង_ឬស = Path(__file__).resolve().parent


def អនុវត្ត_ពាក្យបញ្ជា(ពាក្យ_អត្ថបទ):
    subprocess.check_call([str(ការបញ្ចូល_តំលៃ) for ការបញ្ចូល_តំលៃ in ពាក្យ_អត្ថបទ], cwd=str(បញ្ចាំង_ឬស))


def រត់():
    មុខងារ_ញែក_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    មុខងារ_ញែក_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 ផ្ទៀងផ្ទាត់')
    មុខងារ_ញែក_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    មុខងារ_ញែក_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    មុខងារ_ញែក_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    អាគុយម៉ង់ = មុខងារ_ញែក_48ee4b1b.parse_args()
    명세 = json.loads((បញ្ចាំង_ឬស / 'relink.json').read_text())
    ចងក្រង_ប្រព័ន្ធ = បញ្ចាំង_ឬស / 'build'
    새묶음 = ចងក្រង_ប្រព័ន្ធ / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    អង្គភ្ជាប់ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ប័ណ្ណសារ_ឧបករណ៏ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    ពីចម្ងាយ_ការកំណត់ = json.loads((ចងក្រង_ប្រព័ន្ធ / 'remote/libassh-build.json').read_text())
    ការកំណត់ = ពីចម្ងាយ_ការកំណត់['flags']
    if អាគុយម៉ង់.libassh_archive:
        សុវត្ថិភាព_បាច់ = អាគុយម៉ង់.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', បញ្ចាំង_ឬស / 'ពីចម្ងាយ_តំលៃ', '-I', បញ្ចាំង_ឬស / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for ឈ្មោះ in ពីចម្ងាយ_ការកំណត់['sources']:
            ទិសដៅ_តំលៃ = 새묶음 / (Path(ឈ្មោះ).stem + '.o')
            អនុវត្ត_ពាក្យបញ្ជា([번역기] + ការកំណត់ + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', បញ្ចាំង_ឬស / ឈ្មោះ, '-o', ទិសដៅ_តំលៃ])
            목적들.append(ទិសដៅ_តំលៃ)
        សុវត្ថិភាព_បាច់ = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            អនុវត្ត_ពាក្យបញ្ជា([ប័ណ្ណសារ_ឧបករណ៏, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(សុវត្ថិភាព_បាច់)
    if អាគុយម៉ង់.tinycc:
        if not អាគុយម៉ង់.sdk:
            មុខងារ_ញែក_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = អាគុយម៉ង់.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            មុខងារ_ញែក_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [ការជ្រើស_តំលៃ for ការជ្រើស_តំលៃ in ការកំណត់ if ការជ្រើស_តំលៃ != '-mgeneral-regs-only']
        ទិសដៅ_តំលៃ = 새묶음 / '번역기.o'
        អនុវត្ត_ពាក្យបញ្ជា([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', បញ្ចាំង_ឬស / '시언어번역기', '-I', បញ្ចាំង_ឬស / 'vendor/tinycc', '-I', បញ្ចាំង_ឬស / 'អ្នកប្រើ',
             '-I', ចងក្រង_ប្រព័ន្ធ / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', បញ្ចាំង_ឬស / '시언어번역기/번역기.c', '-o', ទិសដៅ_តំលៃ])
        អនុវត្ត_ពាក្យបញ្ជា([អង្គភ្ជាប់, '--gc-sections', '-T', បញ្ចាំង_ឬស / 'អ្នកប្រើ/តំណ_ប្លង់.ld', '-z', 'max-page-size=4096',
             '-o', ចងក្រង_ប្រព័ន្ធ / 'user/cc.elf', ចងក្រង_ប្រព័ន្ធ / 'user/start.o', ចងក្រង_ប្រព័ន្ធ / 'user/runtime.o', ទិសដៅ_តំលៃ] +
             [ចងក្រង_ប្រព័ន្ធ / 'ccompiler' / (ឈ្មោះ + '.o') for ឈ្មោះ in ('ដំណើរការភាសាទូទៅ_ទម្រ', 'រត់', '미리번역', '되돌림')] +
             [ចងក្រង_ប្រព័ន្ធ / 'user' / (ឈ្មោះ + '.o') for ឈ្មោះ in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = ចងក្រង_ប្រព័ន្ធ / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((ចងក្រង_ប្រព័ន្ធ / 'user/cc.elf').stat().st_size), 머리.read_text()))
        អនុវត្ត_ពាក្យបញ្ជា([번역기] + ការកំណត់ + ['-c', ចងក្រង_ប្រព័ន្ធ / 'programs.S', '-o', បញ្ចាំង_ឬស / 'objects/programs.o'])
        អនុវត្ត_ពាក្យបញ្ជា([번역기] + ការកំណត់ + ['-std=c11', '-I', បញ្ចាំង_ឬស / 'posix-kor/arm64-native/포함', '-I', ចងក្រង_ប្រព័ន្ធ,
             '-c', បញ្ចាំង_ឬស / 'ម៉ាស៊ីន/អ្នកប្រើ.c', '-o', បញ្ចាំង_ឬស / 'objects/user.o'])
    អនុវត្ត_ពាក្យបញ្ជា([អង្គភ្ជាប់, '--gc-sections', '-T', បញ្ចាំង_ឬស / '부팅/តំណ_ប្លង់.ld', '-o', 새묶음 / 'kernel.elf'] +
         [បញ្ចាំង_ឬស / ផ្លូវ for ផ្លូវ in 명세['objects']] + ['--start-group'] +
         [សុវត្ថិភាព_បាច់ if ផ្លូវ == 'objects/libassh.a' else បញ្ចាំង_ឬស / ផ្លូវ for ផ្លូវ in 명세['libraries']] + ['--end-group'])
    អនុវត្ត_ពាក្យបញ្ជា([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    ហាស_ឯកសារ = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if អាគុយម៉ង់.verify and ហាស_ឯកសារ != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + ហាស_ឯកសារ)
    print('RELINK PASS', ហាស_ឯកសារ, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    រត់()
