#!/usr/bin/env python3
"""개인 kwihuza_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from kure_Amagenamiterere import Gutegura
from COSL배포 import aho_ijya_izina, isomero

기준 = Path(__file__).resolve().parents[1]


def ihuriro():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    imiterere_yihitiwemo = 기준 / 'build/remote/access.json'
    원래설정 = imiterere_yihitiwemo.read_bytes()
    raporo_agaciro = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Amagenamiterere_inzira = 시험터 / 'build/remote'
            Amagenamiterere_inzira.mkdir(parents=True)
            Amagenamiterere_dosiye = Amagenamiterere_inzira / 'access.json'
            def kwandika_Amagenamiterere(amakurushingiro):
                Amagenamiterere_dosiye.write_text(json.dumps(amakurushingiro, ensure_ascii=False) + '\n')
                Amagenamiterere_dosiye.chmod(0o600)
            def gusuzuma_Amagenamiterere(insomamabwiriza, 화면):
                kwandika_Amagenamiterere({'user': 'user', 'ssh_password': insomamabwiriza, 'vnc_password': 화면})
                원본 = Amagenamiterere_dosiye.read_bytes()
                Gutegura(시험터)
                assert Amagenamiterere_dosiye.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Amagenamiterere_inzira / 'Umwirondoro.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Amagenamiterere_inzira / 'Umwirondoro.h').stat().st_mode & 0o777 == 0o600
            for insomamabwiriza, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                gusuzuma_Amagenamiterere(insomamabwiriza, 화면)
            raporo_agaciro['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for guhindura_agaciro_16f64fe4, icyinjizwa_agaciro in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                amakurushingiro = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                amakurushingiro.update(guhindura_agaciro_16f64fe4)
                kwandika_Amagenamiterere(amakurushingiro)
                try:
                    Gutegura(시험터)
                except SystemExit as IKOSA:
                    assert icyinjizwa_agaciro in str(IKOSA), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + icyinjizwa_agaciro)
            raporo_agaciro['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Amagenamiterere = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            agahuza = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            gushyingura_igikoresho = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def gukora_ibwiriza(인수, kubika_umurongo):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=kubika_umurongo,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Izina, insomamabwiriza, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Izina, flush=True)
                gusuzuma_Amagenamiterere(insomamabwiriza, 화면)
                결과 = 출력 / Izina
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as kubika_umurongo:
                    목적들 = []
                    for 원본 in sorted((기준 / 'kure_agaciro').glob('*.c')):
                        aho_ijya_agaciro = 시험터 / (원본.stem + '.o')
                        gukora_ibwiriza([번역기] + Amagenamiterere + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Amagenamiterere_inzira, '-I', 기준 / 'kure_agaciro', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', aho_ijya_agaciro], kubika_umurongo)
                        목적들.append(aho_ijya_agaciro)
                    kure_ipaki = 시험터 / 'libremote.a'
                    gukora_ibwiriza([gushyingura_igikoresho, 'rcs', kure_ipaki] + 목적들, kubika_umurongo)
                    gukora_ibwiriza([agahuza, '--gc-sections', '-T', 기준 / '부팅/Ihuza_Imimerere.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (Izina + '.o') for Izina in aho_ijya_izina] + ['--start-group'] +
                         [kure_ipaki if Inzira == 'remote/libremote.a' else 기준 / 'build' / Inzira for Inzira in isomero] + ['--end-group'], kubika_umurongo)
                    gukora_ibwiriza([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], kubika_umurongo)
                with (결과 / 'remote-test.log').open('wb') as kubika_umurongo:
                    gukora_ibwiriza(['python3', 기준 / 'Ibikoresho/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Amagenamiterere_dosiye, '--output', 결과], kubika_umurongo)
                kwemeza = json.loads((결과 / 'report.json').read_text())
                assert kwemeza['passed']
                raporo_agaciro['checks'].append(Izina + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        raporo_agaciro['passed'] = True
    finally:
        raporo_agaciro['personal_settings_unchanged'] = imiterere_yihitiwemo.read_bytes() == 원래설정
        if not raporo_agaciro['personal_settings_unchanged']:
            raporo_agaciro['passed'] = False
        raporo_agaciro['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(raporo_agaciro, ensure_ascii=False, indent=2) + '\n')
    assert raporo_agaciro['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(raporo_agaciro, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ihuriro()
