#!/usr/bin/env python3
"""ဖြန့်ချိမှုတန်ဖိုး 묶음에서 libassh/TinyCC를 교체하고 ကိုယ်ပိုင် 커널을 ပြန်ကြိုးစား 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

စီမံကိန်းအမြစ် = Path(__file__).resolve().parent


def စက်မောင်း(စကားလုံးစာသား):
    subprocess.check_call([str(အချက်တန်ဖိုး) for အချက်တန်ဖိုး in စကားလုံးစာသား], cwd=str(စီမံကိန်းအမြစ်))


def လုပ်ဆောင်():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 အတည်ပြု')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a သုံးစွဲမှု')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 ပြန်ကြိုးစား 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    အချက်များ = 해석기.parse_args()
    သတ်မှတ်စံ = json.loads((စီမံကိန်းအမြစ် / 'relink.json').read_text())
    တည်ဆောက် = စီမံကိန်းအမြစ် / 'build'
    အသစ်အထုပ် = တည်ဆောက် / 'relinked'
    အသစ်အထုပ်.mkdir(exist_ok=True)
    ဘာသာပြန်စက်ကိရိယာတစ်ခု = os.environ.get('ARM64_CC', 'clang')
    연결기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    မော်ကွန်းကိရိယာတစ်ခု = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    အဝေးသတ်မှတ်ချက် = json.loads((တည်ဆောက် / 'remote/libassh-build.json').read_text())
    သတ်မှတ်ချက် = အဝေးသတ်မှတ်ချက်['flags']
    if အချက်များ.libassh_archive:
        လုံခြုံရေးအထုပ် = အချက်များ.libassh_archive.resolve()
    else:
        목적들 = []
        ခေါင်းစီးဖိုင် = ['-I', စီမံကိန်းအမြစ် / 'အဝေးတန်ဖိုး', '-I', စီမံကိန်းအမြစ် / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for အမည် in အဝေးသတ်မှတ်ချက်['sources']:
            ဦးတည်ရာတန်ဖိုး = အသစ်အထုပ် / (Path(အမည်).stem + '.o')
            စက်မောင်း([ဘာသာပြန်စက်ကိရိယာတစ်ခု] + သတ်မှတ်ချက် + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + ခေါင်းစီးဖိုင် +
                 ['-c', စီမံကိန်းအမြစ် / အမည်, '-o', ဦးတည်ရာတန်ဖိုး])
            목적들.append(ဦးတည်ရာတန်ဖိုး)
        လုံခြုံရေးအထုပ် = အသစ်အထုပ် / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(အသစ်အထုပ်)) as ယာယီတန်ဖိုး:
            ယာယီအထုပ် = Path(ယာယီတန်ဖိုး) / 'libassh.a'
            စက်မောင်း([မော်ကွန်းကိရိယာတစ်ခု, 'rcs', ယာယီအထုပ်] + 목적들)
            ယာယီအထုပ်.replace(လုံခြုံရေးအထုပ်)
    if အချက်များ.tinycc:
        if not အချက်များ.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        ဖွံ့ဖြိုးရေး = အချက်များ.sdk.resolve()
        ဂဏန်းသင်္ချာတန်ဖိုး = sorted((ဖွံ့ဖြိုးရေး / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not ဂဏန်းသင်္ချာတန်ဖိုး or not (ဖွံ့ဖြိုးရေး / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [ရွေးချယ်မှုတန်ဖိုး for ရွေးချယ်မှုတန်ဖိုး in သတ်မှတ်ချက် if ရွေးချယ်မှုတန်ဖိုး != '-mgeneral-regs-only']
        ဦးတည်ရာတန်ဖိုး = အသစ်အထုပ် / 'ဘာသာပြန်စက်ကိရိယာတစ်ခု.o'
        စက်မောင်း([ဘာသာပြန်စက်ကိရိယာတစ်ခု] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', စီမံကိန်းအမြစ် / 'Cဘာသာပြန်စက်', '-I', စီမံကိန်းအမြစ် / 'vendor/tinycc', '-I', စီမံကိန်းအမြစ် / 'သုံးစွဲသူ',
             '-I', တည်ဆောက် / 'ccompiler', '-isystem', ဖွံ့ဖြိုးရေး / 'usr/include', '-c', စီမံကိန်းအမြစ် / 'Cဘာသာပြန်စက်/ဘာသာပြန်စက်ကိရိယာတစ်ခု.c', '-o', ဦးတည်ရာတန်ဖိုး])
        စက်မောင်း([연결기, '--gc-sections', '-T', စီမံကိန်းအမြစ် / 'သုံးစွဲသူ/နေရာချထားပုံ.ld', '-z', 'max-page-size=4096',
             '-o', တည်ဆောက် / 'user/cc.elf', တည်ဆောက် / 'user/start.o', တည်ဆောက် / 'user/runtime.o', ဦးတည်ရာတန်ဖိုး] +
             [တည်ဆောက် / 'ccompiler' / (အမည် + '.o') for အမည် in ('လည်ပတ်ဝန်းကျင်ထောက်ပံ့မှု', 'လုပ်ဆောင်', '미리번역', 'ပြန်ပေးတံတား')] +
             [တည်ဆောက် / 'user' / (အမည် + '.o') for အမည် in ('jar', 'tinflate', 'crc32', 'adler32')] + [ဂဏန်းသင်္ချာတန်ဖိုး[-1]])
        ဦးခေါင်းတန်ဖိုး = တည်ဆောက် / 'programs.h'
        ဦးခေါင်းတန်ဖိုး.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda ဖြစ်သောညီ: ဖြစ်သောညီ.group(1) + str((တည်ဆောက် / 'user/cc.elf').stat().st_size), ဦးခေါင်းတန်ဖိုး.read_text()))
        စက်မောင်း([ဘာသာပြန်စက်ကိရိယာတစ်ခု] + သတ်မှတ်ချက် + ['-c', တည်ဆောက် / 'programs.S', '-o', စီမံကိန်းအမြစ် / 'objects/programs.o'])
        စက်မောင်း([ဘာသာပြန်စက်ကိရိယာတစ်ခု] + သတ်မှတ်ချက် + ['-std=c11', '-I', စီမံကိန်းအမြစ် / 'posix-kor/arm64-native/ခေါင်းစီးဖိုင်', '-I', တည်ဆောက်,
             '-c', စီမံကိန်းအမြစ် / 'စက်/သုံးစွဲသူ.c', '-o', စီမံကိန်းအမြစ် / 'objects/user.o'])
    စက်မောင်း([연결기, '--gc-sections', '-T', စီမံကိန်းအမြစ် / 'စက်တင်/နေရာချထားပုံ.ld', '-o', အသစ်အထုပ် / 'kernel.elf'] +
         [စီမံကိန်းအမြစ် / လမ်း for လမ်း in သတ်မှတ်စံ['objects']] + ['--start-group'] +
         [လုံခြုံရေးအထုပ် if လမ်း == 'objects/libassh.a' else စီမံကိန်းအမြစ် / လမ်း for လမ်း in သတ်မှတ်စံ['libraries']] + ['--end-group'])
    စက်မောင်း([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', အသစ်အထုပ် / 'kernel.elf', အသစ်အထုပ် / 'kernel8.img'])
    ဖိုင်ဟက်ရှ်တွက် = hashlib.sha256((အသစ်အထုပ် / 'kernel8.img').read_bytes()).hexdigest()
    if အချက်များ.verify and ဖိုင်ဟက်ရှ်တွက် != သတ်မှတ်စံ['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + ဖိုင်ဟက်ရှ်တွက်)
    print('RELINK PASS', ဖိုင်ဟက်ရှ်တွက်, အသစ်အထုပ် / 'kernel8.img')


if __name__ == '__main__':
    လုပ်ဆောင်()
