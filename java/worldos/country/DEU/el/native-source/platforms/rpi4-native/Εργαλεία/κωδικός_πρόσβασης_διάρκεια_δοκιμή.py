#!/usr/bin/env python3
"""개인 σύνδεση_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from απομακρυσμένος_Ρυθμίσεις import Προετοίμασε
from COSL배포 import προορισμός_όνομα, βιβλιοθήκη

έργο_ρίζα = Path(__file__).resolve().parents[1]


def Εκτέλεση_2():
    Έξοδος = έργο_ρίζα / 'build/verification/password-length'
    Έξοδος.mkdir(parents=True, exist_ok=True)
    προσωπικές_ρυθμίσεις = έργο_ρίζα / 'build/remote/access.json'
    원래설정 = προσωπικές_ρυθμίσεις.read_bytes()
    έκθεση_τιμή = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            δοκιμή_χώρος_εργασίας = Path(임시)
            Ρυθμίσεις_διαδρομή = δοκιμή_χώρος_εργασίας / 'build/remote'
            Ρυθμίσεις_διαδρομή.mkdir(parents=True)
            Ρυθμίσεις_Αρχείο = Ρυθμίσεις_διαδρομή / 'access.json'
            def εγγράφω_Ρυθμίσεις(δεδομένα):
                Ρυθμίσεις_Αρχείο.write_text(json.dumps(δεδομένα, ensure_ascii=False) + '\n')
                Ρυθμίσεις_Αρχείο.chmod(0o600)
            def επαληθεύω_Ρυθμίσεις(κέλυφος, 화면):
                εγγράφω_Ρυθμίσεις({'user': 'user', 'ssh_password': κέλυφος, 'vnc_password': 화면})
                원본 = Ρυθμίσεις_Αρχείο.read_bytes()
                Προετοίμασε(δοκιμή_χώρος_εργασίας)
                assert Ρυθμίσεις_Αρχείο.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Ρυθμίσεις_διαδρομή / 'Προφίλ.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Ρυθμίσεις_διαδρομή / 'Προφίλ.h').stat().st_mode & 0o777 == 0o600
            for κέλυφος, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                επαληθεύω_Ρυθμίσεις(κέλυφος, 화면)
            έκθεση_τιμή['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for αλλάζω_τιμή, καταχώρηση_τιμή in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                δεδομένα = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                δεδομένα.update(αλλάζω_τιμή)
                εγγράφω_Ρυθμίσεις(δεδομένα)
                try:
                    Προετοίμασε(δοκιμή_χώρος_εργασίας)
                except SystemExit as ΣΦΑΛΜΑ:
                    assert καταχώρηση_τιμή in str(ΣΦΑΛΜΑ), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + καταχώρηση_τιμή)
            έκθεση_τιμή['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Ρυθμίσεις = json.loads((έργο_ρίζα / 'build/remote/libassh-build.json').read_text())['flags']
            πρόγραμμα_μεταγλώττισης_εργαλείο = os.environ.get('ARM64_CC', 'clang')
            Σύνδεση_99e0bece = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Αρχειοθήκη_εργαλείο = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def εκτελώ_εντολή(Παράμετροι, καταγράφω_ρεκόρ):
                subprocess.run(list(map(str, Παράμετροι)), cwd=str(έργο_ρίζα), stdout=καταγράφω_ρεκόρ,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Όνομα, κέλυφος, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Όνομα, flush=True)
                επαληθεύω_Ρυθμίσεις(κέλυφος, 화면)
                μέτρηση = Έξοδος / Όνομα
                μέτρηση.mkdir(exist_ok=True)
                with (μέτρηση / 'build.log').open('wb') as καταγράφω_ρεκόρ:
                    목적들 = []
                    for 원본 in sorted((έργο_ρίζα / 'απομακρυσμένος_τιμή').glob('*.c')):
                        προορισμός_τιμή = δοκιμή_χώρος_εργασίας / (원본.stem + '.o')
                        εκτελώ_εντολή([πρόγραμμα_μεταγλώττισης_εργαλείο] + Ρυθμίσεις + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Ρυθμίσεις_διαδρομή, '-I', έργο_ρίζα / 'απομακρυσμένος_τιμή', '-I', έργο_ρίζα / 'vendor/libassh/src',
                             '-I', έργο_ρίζα / 'vendor/bearssl/inc', '-I', έργο_ρίζα / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', προορισμός_τιμή], καταγράφω_ρεκόρ)
                        목적들.append(προορισμός_τιμή)
                    απομακρυσμένος_πακέτο = δοκιμή_χώρος_εργασίας / 'libremote.a'
                    εκτελώ_εντολή([Αρχειοθήκη_εργαλείο, 'rcs', απομακρυσμένος_πακέτο] + 목적들, καταγράφω_ρεκόρ)
                    εκτελώ_εντολή([Σύνδεση_99e0bece, '--gc-sections', '-T', έργο_ρίζα / '부팅/συνδέω_Διάταξη.ld', '-o', δοκιμή_χώρος_εργασίας / 'kernel.elf'] +
                         [έργο_ρίζα / 'build' / (Όνομα + '.o') for Όνομα in προορισμός_όνομα] + ['--start-group'] +
                         [απομακρυσμένος_πακέτο if ΔΙΑΔΡΟΜΗ == 'remote/libremote.a' else έργο_ρίζα / 'build' / ΔΙΑΔΡΟΜΗ for ΔΙΑΔΡΟΜΗ in βιβλιοθήκη] + ['--end-group'], καταγράφω_ρεκόρ)
                    εκτελώ_εντολή([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         δοκιμή_χώρος_εργασίας / 'kernel.elf', δοκιμή_χώρος_εργασίας / 'kernel8.img'], καταγράφω_ρεκόρ)
                with (μέτρηση / 'remote-test.log').open('wb') as καταγράφω_ρεκόρ:
                    εκτελώ_εντολή(['python3', έργο_ρίζα / 'Εργαλεία/απομακρυσμένη_σύνδεση_δοκιμή.py', '--kernel', δοκιμή_χώρος_εργασίας / 'kernel8.img',
                         '--access', Ρυθμίσεις_Αρχείο, '--output', μέτρηση], καταγράφω_ρεκόρ)
                επικυρώνω = json.loads((μέτρηση / 'report.json').read_text())
                assert επικυρώνω['passed']
                έκθεση_τιμή['checks'].append(Όνομα + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        έκθεση_τιμή['passed'] = True
    finally:
        έκθεση_τιμή['personal_settings_unchanged'] = προσωπικές_ρυθμίσεις.read_bytes() == 원래설정
        if not έκθεση_τιμή['personal_settings_unchanged']:
            έκθεση_τιμή['passed'] = False
        έκθεση_τιμή['kernel_sha256'] = hashlib.sha256((έργο_ρίζα / 'build/kernel8.img').read_bytes()).hexdigest()
        (Έξοδος / 'report.json').write_text(json.dumps(έκθεση_τιμή, ensure_ascii=False, indent=2) + '\n')
    assert έκθεση_τιμή['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(έκθεση_τιμή, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Εκτέλεση_2()
