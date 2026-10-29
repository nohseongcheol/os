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

기준 = Path(__file__).resolve().parent


def def_ndigel(Word_SMS):
    subprocess.check_call([str(dugal_xabaar_xëyma) for dugal_xabaar_xëyma in Word_SMS], cwd=str(기준))


def daw():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 luñutu')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    tabax_kureel = 기준 / 'build'
    새묶음 = tabax_kureel / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    Jokkalóo = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    denc_jumtukaay = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    lu_soree_Jekkal_yi = json.loads((tabax_kureel / 'remote/libassh-build.json').read_text())
    Jekkal_yi = lu_soree_Jekkal_yi['flags']
    if 인수.libassh_archive:
        kaarànge_takku_xéewël = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'lu_soree_xëyma', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for tur_253d1510 in lu_soree_Jekkal_yi['sources']:
            jëmmukaay_xëyma = 새묶음 / (Path(tur_253d1510).stem + '.o')
            def_ndigel([번역기] + Jekkal_yi + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / tur_253d1510, '-o', jëmmukaay_xëyma])
            목적들.append(jëmmukaay_xëyma)
        kaarànge_takku_xéewël = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            def_ndigel([denc_jumtukaay, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(kaarànge_takku_xéewël)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [tanneef_xëyma for tanneef_xëyma in Jekkal_yi if tanneef_xëyma != '-mgeneral-regs-only']
        jëmmukaay_xëyma = 새묶음 / '번역기.o'
        def_ndigel([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'kiy_jariñoo_internet',
             '-I', tabax_kureel / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', jëmmukaay_xëyma])
        def_ndigel([Jokkalóo, '--gc-sections', '-T', 기준 / 'kiy_jariñoo_internet/lëkkale_Tëralin.ld', '-z', 'max-page-size=4096',
             '-o', tabax_kureel / 'user/cc.elf', tabax_kureel / 'user/start.o', tabax_kureel / 'user/runtime.o', jëmmukaay_xëyma] +
             [tabax_kureel / 'ccompiler' / (tur_253d1510 + '.o') for tur_253d1510 in ('common_language_runtime_Ndimbal', 'daw', '미리번역', '되돌림')] +
             [tabax_kureel / 'user' / (tur_253d1510 + '.o') for tur_253d1510 in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = tabax_kureel / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((tabax_kureel / 'user/cc.elf').stat().st_size), 머리.read_text()))
        def_ndigel([번역기] + Jekkal_yi + ['-c', tabax_kureel / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        def_ndigel([번역기] + Jekkal_yi + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', tabax_kureel,
             '-c', 기준 / 'masin/kiy_jariñoo_internet.c', '-o', 기준 / 'objects/user.o'])
    def_ndigel([Jokkalóo, '--gc-sections', '-T', 기준 / '부팅/lëkkale_Tëralin.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / Yoonu_jëmale for Yoonu_jëmale in 명세['objects']] + ['--start-group'] +
         [kaarànge_takku_xéewël if Yoonu_jëmale == 'objects/libassh.a' else 기준 / Yoonu_jëmale for Yoonu_jëmale in 명세['libraries']] + ['--end-group'])
    def_ndigel([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    caabiy_teqale_bi_bara_denc = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and caabiy_teqale_bi_bara_denc != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + caabiy_teqale_bi_bara_denc)
    print('RELINK PASS', caabiy_teqale_bi_bara_denc, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    daw()
