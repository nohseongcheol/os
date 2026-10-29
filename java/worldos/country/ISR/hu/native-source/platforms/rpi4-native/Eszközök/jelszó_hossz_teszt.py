#!/usr/bin/env python3
"""개인 ismerős_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from távoli_Gépház import Előkészítés
from COSL배포 import cél_név, kódtár

teendő_gyök = Path(__file__).resolve().parents[1]


def Futtatás():
    Kimenet = teendő_gyök / 'build/verification/password-length'
    Kimenet.mkdir(parents=True, exist_ok=True)
    személyes_beállítások = teendő_gyök / 'build/remote/access.json'
    원래설정 = személyes_beállítások.read_bytes()
    jelent_ÉRTÉK = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            teszt_munkaterület = Path(임시)
            Gépház_útvonal = teszt_munkaterület / 'build/remote'
            Gépház_útvonal.mkdir(parents=True)
            Gépház_Fájl = Gépház_útvonal / 'access.json'
            def ír_Gépház(adat):
                Gépház_Fájl.write_text(json.dumps(adat, ensure_ascii=False) + '\n')
                Gépház_Fájl.chmod(0o600)
            def igazol_Gépház(felület, 화면):
                ír_Gépház({'user': 'user', 'ssh_password': felület, 'vnc_password': 화면})
                원본 = Gépház_Fájl.read_bytes()
                Előkészítés(teszt_munkaterület)
                assert Gépház_Fájl.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Gépház_útvonal / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Gépház_útvonal / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for felület, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                igazol_Gépház(felület, 화면)
            jelent_ÉRTÉK['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for módosítás_ÉRTÉK, bejegyzés_ÉRTÉK in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                adat = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                adat.update(módosítás_ÉRTÉK)
                ír_Gépház(adat)
                try:
                    Előkészítés(teszt_munkaterület)
                except SystemExit as HIBA:
                    assert bejegyzés_ÉRTÉK in str(HIBA), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + bejegyzés_ÉRTÉK)
            jelent_ÉRTÉK['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Beállítások = json.loads((teendő_gyök / 'build/remote/libassh-build.json').read_text())['flags']
            fordítóprogram_eszköz = os.environ.get('ARM64_CC', 'clang')
            Összekötő = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            archív_eszköz = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def végrehajt_parancs(Argumentumok, LOG_REKORD):
                subprocess.run(list(map(str, Argumentumok)), cwd=str(teendő_gyök), stdout=LOG_REKORD,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Név, felület, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Név, flush=True)
                igazol_Gépház(felület, 화면)
                KR = Kimenet / Név
                KR.mkdir(exist_ok=True)
                with (KR / 'build.log').open('wb') as LOG_REKORD:
                    목적들 = []
                    for 원본 in sorted((teendő_gyök / 'távoli_ÉRTÉK').glob('*.c')):
                        cél_ÉRTÉK = teszt_munkaterület / (원본.stem + '.o')
                        végrehajt_parancs([fordítóprogram_eszköz] + Beállítások + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Gépház_útvonal, '-I', teendő_gyök / 'távoli_ÉRTÉK', '-I', teendő_gyök / 'vendor/libassh/src',
                             '-I', teendő_gyök / 'vendor/bearssl/inc', '-I', teendő_gyök / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', cél_ÉRTÉK], LOG_REKORD)
                        목적들.append(cél_ÉRTÉK)
                    távoli_köteg = teszt_munkaterület / 'libremote.a'
                    végrehajt_parancs([archív_eszköz, 'rcs', távoli_köteg] + 목적들, LOG_REKORD)
                    végrehajt_parancs([Összekötő, '--gc-sections', '-T', teendő_gyök / '부팅/csatol_Navigáció.ld', '-o', teszt_munkaterület / 'kernel.elf'] +
                         [teendő_gyök / 'build' / (Név + '.o') for Név in cél_név] + ['--start-group'] +
                         [távoli_köteg if ÚTVONAL == 'remote/libremote.a' else teendő_gyök / 'build' / ÚTVONAL for ÚTVONAL in kódtár] + ['--end-group'], LOG_REKORD)
                    végrehajt_parancs([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         teszt_munkaterület / 'kernel.elf', teszt_munkaterület / 'kernel8.img'], LOG_REKORD)
                with (KR / 'remote-test.log').open('wb') as LOG_REKORD:
                    végrehajt_parancs(['python3', teendő_gyök / 'Eszközök/távoli_kapcsolat_teszt.py', '--kernel', teszt_munkaterület / 'kernel8.img',
                         '--access', Gépház_Fájl, '--output', KR], LOG_REKORD)
                ellenőriz = json.loads((KR / 'report.json').read_text())
                assert ellenőriz['passed']
                jelent_ÉRTÉK['checks'].append(Név + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        jelent_ÉRTÉK['passed'] = True
    finally:
        jelent_ÉRTÉK['personal_settings_unchanged'] = személyes_beállítások.read_bytes() == 원래설정
        if not jelent_ÉRTÉK['personal_settings_unchanged']:
            jelent_ÉRTÉK['passed'] = False
        jelent_ÉRTÉK['kernel_sha256'] = hashlib.sha256((teendő_gyök / 'build/kernel8.img').read_bytes()).hexdigest()
        (Kimenet / 'report.json').write_text(json.dumps(jelent_ÉRTÉK, ensure_ascii=False, indent=2) + '\n')
    assert jelent_ÉRTÉK['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(jelent_ÉRTÉK, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Futtatás()
