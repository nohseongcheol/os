#!/usr/bin/env python3
"""giáTrịBảnPhânPhối 묶음에서 libassh/TinyCC를 교체하고 tựThân 커널을 giáTrịThửLại 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

gốcCâyDựÁn = Path(__file__).resolve().parent


def thựcThiLệnh(vănBảnTừ):
    subprocess.check_call([str(giáTrịMục) for giáTrịMục in vănBảnTừ], cwd=str(gốcCâyDựÁn))


def chạy():
    BộPhânTích = argparse.ArgumentParser(description=__doc__)
    BộPhânTích.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 xácMinh')
    BộPhânTích.add_argument('--libassh-archive', type=Path, help='별도로 chỉnhSửaGiáTrị·컴파일한 libassh.a giáTrịDùng')
    BộPhânTích.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 giáTrịThửLại 컴파일하고 커널에 탑재')
    BộPhânTích.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    cácĐốiSố = BộPhânTích.parse_args()
    đặcTả = json.loads((gốcCâyDựÁn / 'relink.json').read_text())
    xâyDựngHệThống = gốcCâyDựÁn / 'build'
    góiGộpMới = xâyDựngHệThống / 'relinked'
    góiGộpMới.mkdir(exist_ok=True)
    côngCụTrìnhBiênDịch = os.environ.get('ARM64_CC', 'clang')
    đầuNối = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    côngCụKhoLưuTrữ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    cácThiếtLậpTừXa = json.loads((xâyDựngHệThống / 'remote/libassh-build.json').read_text())
    cácThiếtLập = cácThiếtLậpTừXa['flags']
    if cácĐốiSố.libassh_archive:
        góiGộpBảoMật = cácĐốiSố.libassh_archive.resolve()
    else:
        cácĐích = []
        TệpĐầuMục = ['-I', gốcCâyDựÁn / 'giáTrịTừXa', '-I', gốcCâyDựÁn / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for tên in cácThiếtLậpTừXa['sources']:
            giáTrịĐích = góiGộpMới / (Path(tên).stem + '.o')
            thựcThiLệnh([côngCụTrìnhBiênDịch] + cácThiếtLập + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + TệpĐầuMục +
                 ['-c', gốcCâyDựÁn / tên, '-o', giáTrịĐích])
            cácĐích.append(giáTrịĐích)
        góiGộpBảoMật = góiGộpMới / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(góiGộpMới)) as giáTrịTạm:
            góiGộpTạm = Path(giáTrịTạm) / 'libassh.a'
            thựcThiLệnh([côngCụKhoLưuTrữ, 'rcs', góiGộpTạm] + cácĐích)
            góiGộpTạm.replace(góiGộpBảoMật)
    if cácĐốiSố.tinycc:
        if not cácĐốiSố.sdk:
            BộPhânTích.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        phátTriển = cácĐốiSố.sdk.resolve()
        giáTrịSốHọc = sorted((phátTriển / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not giáTrịSốHọc or not (phátTriển / 'usr/include/stdio.h').is_file():
            BộPhânTích.error('SDK must contain ARM64 musl headers and libgcc.a')
        đặtCấuHìnhBậtTrạngThái = [giáTrịViệcChọn for giáTrịViệcChọn in cácThiếtLập if giáTrịViệcChọn != '-mgeneral-regs-only']
        giáTrịĐích = góiGộpMới / 'côngCụTrìnhBiênDịch.o'
        thựcThiLệnh([côngCụTrìnhBiênDịch] + đặtCấuHìnhBậtTrạngThái + ['-ffunction-sections', '-fdata-sections',
             '-I', gốcCâyDựÁn / 'TrìnhBiênDịchC', '-I', gốcCâyDựÁn / 'vendor/tinycc', '-I', gốcCâyDựÁn / 'NgườiDùng',
             '-I', xâyDựngHệThống / 'ccompiler', '-isystem', phátTriển / 'usr/include', '-c', gốcCâyDựÁn / 'TrìnhBiênDịchC/côngCụTrìnhBiênDịch.c', '-o', giáTrịĐích])
        thựcThiLệnh([đầuNối, '--gc-sections', '-T', gốcCâyDựÁn / 'NgườiDùng/BốTríLiênKết.ld', '-z', 'max-page-size=4096',
             '-o', xâyDựngHệThống / 'user/cc.elf', xâyDựngHệThống / 'user/start.o', xâyDựngHệThống / 'user/runtime.o', giáTrịĐích] +
             [xâyDựngHệThống / 'ccompiler' / (tên + '.o') for tên in ('HỗTrợMôiTrườngChạy', 'chạy', 'thờiGianCủaTrước', 'cầuNốiTrảVề')] +
             [xâyDựngHệThống / 'user' / (tên + '.o') for tên in ('jar', 'tinflate', 'crc32', 'adler32')] + [giáTrịSốHọc[-1]])
        giáTrịĐầu = xâyDựngHệThống / 'programs.h'
        giáTrịĐầu.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda làBằng: làBằng.group(1) + str((xâyDựngHệThống / 'user/cc.elf').stat().st_size), giáTrịĐầu.read_text()))
        thựcThiLệnh([côngCụTrìnhBiênDịch] + cácThiếtLập + ['-c', xâyDựngHệThống / 'programs.S', '-o', gốcCâyDựÁn / 'objects/programs.o'])
        thựcThiLệnh([côngCụTrìnhBiênDịch] + cácThiếtLập + ['-std=c11', '-I', gốcCâyDựÁn / 'posix-kor/arm64-native/TệpĐầuMục', '-I', xâyDựngHệThống,
             '-c', gốcCâyDựÁn / 'máy/NgườiDùng.c', '-o', gốcCâyDựÁn / 'objects/user.o'])
    thựcThiLệnh([đầuNối, '--gc-sections', '-T', gốcCâyDựÁn / 'KhởiĐộng/BốTríLiênKết.ld', '-o', góiGộpMới / 'kernel.elf'] +
         [gốcCâyDựÁn / đườngDẫn for đườngDẫn in đặcTả['objects']] + ['--start-group'] +
         [góiGộpBảoMật if đườngDẫn == 'objects/libassh.a' else gốcCâyDựÁn / đườngDẫn for đườngDẫn in đặcTả['libraries']] + ['--end-group'])
    thựcThiLệnh([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', góiGộpMới / 'kernel.elf', góiGộpMới / 'kernel8.img'])
    tệpMãBăm = hashlib.sha256((góiGộpMới / 'kernel8.img').read_bytes()).hexdigest()
    if cácĐốiSố.verify and tệpMãBăm != đặcTả['kernel_sha256']:
        raise SystemExit('điểmCuốiKếtNốiLại 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + tệpMãBăm)
    print('RELINK PASS', tệpMãBăm, góiGộpMới / 'kernel8.img')


if __name__ == '__main__':
    chạy()
