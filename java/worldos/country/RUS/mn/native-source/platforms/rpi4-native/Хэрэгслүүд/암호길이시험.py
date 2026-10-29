#!/usr/bin/env python3
"""개인 холболт_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from алсын_Тохиргоо import Бэлтгэх
from COSL배포 import товлосон_газар_нэр, сан

기준 = Path(__file__).resolve().parents[1]


def Ажиллуулах():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    хувийн_тохиргоо = 기준 / 'build/remote/access.json'
    원래설정 = хувийн_тохиргоо.read_bytes()
    тайлан_утга_ddf2aaf3 = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Тохиргоо_зам = 시험터 / 'build/remote'
            Тохиргоо_зам.mkdir(parents=True)
            Тохиргоо_файл = Тохиргоо_зам / 'access.json'
            def бичих_Тохиргоо(өгөгдөл):
                Тохиргоо_файл.write_text(json.dumps(өгөгдөл, ensure_ascii=False) + '\n')
                Тохиргоо_файл.chmod(0o600)
            def шалгах_Тохиргоо(бүрхүүл, 화면):
                бичих_Тохиргоо({'user': 'user', 'ssh_password': бүрхүүл, 'vnc_password': 화면})
                원본 = Тохиргоо_файл.read_bytes()
                Бэлтгэх(시험터)
                assert Тохиргоо_файл.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Тохиргоо_зам / 'Хувийн_тохиргоо.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Тохиргоо_зам / 'Хувийн_тохиргоо.h').stat().st_mode & 0o777 == 0o600
            for бүрхүүл, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                шалгах_Тохиргоо(бүрхүүл, 화면)
            тайлан_утга_ddf2aaf3['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for өөрчлөх_утга, оролт_утга in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                өгөгдөл = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                өгөгдөл.update(өөрчлөх_утга)
                бичих_Тохиргоо(өгөгдөл)
                try:
                    Бэлтгэх(시험터)
                except SystemExit as Алдаа:
                    assert оролт_утга in str(Алдаа), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + оролт_утга)
            тайлан_утга_ddf2aaf3['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Тохиргоо = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            холбогч = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Архив_хэрэгсэл = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Гүйцэтгэх_команд(인수, бичих_мөр_6e8b375a):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=бичих_мөр_6e8b375a,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Нэр, бүрхүүл, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Нэр, flush=True)
                шалгах_Тохиргоо(бүрхүүл, 화면)
                결과 = 출력 / Нэр
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as бичих_мөр_6e8b375a:
                    목적들 = []
                    for 원본 in sorted((기준 / 'алсын_утга').glob('*.c')):
                        товлосон_газар_утга = 시험터 / (원본.stem + '.o')
                        Гүйцэтгэх_команд([번역기] + Тохиргоо + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Тохиргоо_зам, '-I', 기준 / 'алсын_утга', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', товлосон_газар_утга], бичих_мөр_6e8b375a)
                        목적들.append(товлосон_газар_утга)
                    алсын_багц = 시험터 / 'libremote.a'
                    Гүйцэтгэх_команд([Архив_хэрэгсэл, 'rcs', алсын_багц] + 목적들, бичих_мөр_6e8b375a)
                    Гүйцэтгэх_команд([холбогч, '--gc-sections', '-T', 기준 / '부팅/Холбох_Бүдүүвч.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (Нэр + '.o') for Нэр in товлосон_газар_нэр] + ['--start-group'] +
                         [алсын_багц if ЗАМ == 'remote/libremote.a' else 기준 / 'build' / ЗАМ for ЗАМ in сан] + ['--end-group'], бичих_мөр_6e8b375a)
                    Гүйцэтгэх_команд([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], бичих_мөр_6e8b375a)
                with (결과 / 'remote-test.log').open('wb') as бичих_мөр_6e8b375a:
                    Гүйцэтгэх_команд(['python3', 기준 / 'Хэрэгслүүд/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Тохиргоо_файл, '--output', 결과], бичих_мөр_6e8b375a)
                баталгаажуулах = json.loads((결과 / 'report.json').read_text())
                assert баталгаажуулах['passed']
                тайлан_утга_ddf2aaf3['checks'].append(Нэр + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        тайлан_утга_ddf2aaf3['passed'] = True
    finally:
        тайлан_утга_ddf2aaf3['personal_settings_unchanged'] = хувийн_тохиргоо.read_bytes() == 원래설정
        if not тайлан_утга_ddf2aaf3['personal_settings_unchanged']:
            тайлан_утга_ddf2aaf3['passed'] = False
        тайлан_утга_ddf2aaf3['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(тайлан_утга_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    assert тайлан_утга_ddf2aaf3['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(тайлан_утга_ddf2aaf3, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Ажиллуулах()
