#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 ίδιο 커널을 δοκιμάζω_ξανά_τιμή 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

έργο_ρίζα = Path(__file__).resolve().parent


def εκτελώ_εντολή(λέξη_μήνυμα):
    subprocess.check_call([str(καταχώρηση_τιμή) for καταχώρηση_τιμή in λέξη_μήνυμα], cwd=str(έργο_ρίζα))


def Εκτέλεση_2():
    ανάλυση_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ανάλυση_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 επαληθεύω')
    ανάλυση_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a χρήση_τιμή')
    ανάλυση_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 δοκιμάζω_ξανά_τιμή 컴파일하고 커널에 탑재')
    ανάλυση_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Παράμετροι = ανάλυση_48ee4b1b.parse_args()
    명세 = json.loads((έργο_ρίζα / 'relink.json').read_text())
    δομή_Σύστημα = έργο_ρίζα / 'build'
    새묶음 = δομή_Σύστημα / 'relinked'
    새묶음.mkdir(exist_ok=True)
    πρόγραμμα_μεταγλώττισης_εργαλείο = os.environ.get('ARM64_CC', 'clang')
    Σύνδεση_99e0bece = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Αρχειοθήκη_εργαλείο = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    απομακρυσμένος_Ρυθμίσεις = json.loads((δομή_Σύστημα / 'remote/libassh-build.json').read_text())
    Ρυθμίσεις = απομακρυσμένος_Ρυθμίσεις['flags']
    if Παράμετροι.libassh_archive:
        Ασφάλεια_πακέτο = Παράμετροι.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', έργο_ρίζα / 'απομακρυσμένος_τιμή', '-I', έργο_ρίζα / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Όνομα in απομακρυσμένος_Ρυθμίσεις['sources']:
            προορισμός_τιμή = 새묶음 / (Path(Όνομα).stem + '.o')
            εκτελώ_εντολή([πρόγραμμα_μεταγλώττισης_εργαλείο] + Ρυθμίσεις + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', έργο_ρίζα / Όνομα, '-o', προορισμός_τιμή])
            목적들.append(προορισμός_τιμή)
        Ασφάλεια_πακέτο = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            εκτελώ_εντολή([Αρχειοθήκη_εργαλείο, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Ασφάλεια_πακέτο)
    if Παράμετροι.tinycc:
        if not Παράμετροι.sdk:
            ανάλυση_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Παράμετροι.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            ανάλυση_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [επιλογή_τιμή for επιλογή_τιμή in Ρυθμίσεις if επιλογή_τιμή != '-mgeneral-regs-only']
        προορισμός_τιμή = 새묶음 / 'πρόγραμμα_μεταγλώττισης_εργαλείο.o'
        εκτελώ_εντολή([πρόγραμμα_μεταγλώττισης_εργαλείο] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', έργο_ρίζα / 'Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης', '-I', έργο_ρίζα / 'vendor/tinycc', '-I', έργο_ρίζα / 'χρήστης',
             '-I', δομή_Σύστημα / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', έργο_ρίζα / 'Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης/πρόγραμμα_μεταγλώττισης_εργαλείο.c', '-o', προορισμός_τιμή])
        εκτελώ_εντολή([Σύνδεση_99e0bece, '--gc-sections', '-T', έργο_ρίζα / 'χρήστης/συνδέω_Διάταξη.ld', '-z', 'max-page-size=4096',
             '-o', δομή_Σύστημα / 'user/cc.elf', δομή_Σύστημα / 'user/start.o', δομή_Σύστημα / 'user/runtime.o', προορισμός_τιμή] +
             [δομή_Σύστημα / 'ccompiler' / (Όνομα + '.o') for Όνομα in ('περιβάλλον_εκτέλεσης_στήριγμα', 'Εκτέλεση_2', '미리번역', 'επιστρέφω_γέφυρα')] +
             [δομή_Σύστημα / 'user' / (Όνομα + '.o') for Όνομα in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = δομή_Σύστημα / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((δομή_Σύστημα / 'user/cc.elf').stat().st_size), 머리.read_text()))
        εκτελώ_εντολή([πρόγραμμα_μεταγλώττισης_εργαλείο] + Ρυθμίσεις + ['-c', δομή_Σύστημα / 'programs.S', '-o', έργο_ρίζα / 'objects/programs.o'])
        εκτελώ_εντολή([πρόγραμμα_μεταγλώττισης_εργαλείο] + Ρυθμίσεις + ['-std=c11', '-I', έργο_ρίζα / 'posix-kor/arm64-native/포함', '-I', δομή_Σύστημα,
             '-c', έργο_ρίζα / 'υπολογιστής_5eb260fa/χρήστης.c', '-o', έργο_ρίζα / 'objects/user.o'])
    εκτελώ_εντολή([Σύνδεση_99e0bece, '--gc-sections', '-T', έργο_ρίζα / '부팅/συνδέω_Διάταξη.ld', '-o', 새묶음 / 'kernel.elf'] +
         [έργο_ρίζα / ΔΙΑΔΡΟΜΗ for ΔΙΑΔΡΟΜΗ in 명세['objects']] + ['--start-group'] +
         [Ασφάλεια_πακέτο if ΔΙΑΔΡΟΜΗ == 'objects/libassh.a' else έργο_ρίζα / ΔΙΑΔΡΟΜΗ for ΔΙΑΔΡΟΜΗ in 명세['libraries']] + ['--end-group'])
    εκτελώ_εντολή([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    κατακερματισμός_Αρχείο = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Παράμετροι.verify and κατακερματισμός_Αρχείο != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + κατακερματισμός_Αρχείο)
    print('RELINK PASS', κατακερματισμός_Αρχείο, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Εκτέλεση_2()
