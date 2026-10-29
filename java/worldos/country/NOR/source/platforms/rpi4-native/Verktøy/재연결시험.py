#!/usr/bin/env python3
"""distribusjon_VERDI 자료만으로 LGPL 재연결과 수정한 TinyCC의 faktisk_data 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Utfør_kommando import speile_rot, Kommando


def Kjør_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--sdk', type=Path, default=speile_rot.parent / 'rpi4/build/rootfs')
    Argumenter = parser_48ee4b1b.parse_args()
    Utgang = speile_rot / 'build/verification/cosl-relink'
    Utgang.mkdir(parents=True, exist_ok=True)
    rapport_VERDI = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((speile_rot / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Sti = Path(임시)
            with tarfile.open(str(speile_rot / 'dist/jkoros-native-relink.tar.gz')) as gruppe_VERDI:
                for oppføring_VERDI in gruppe_VERDI.getmembers():
                    if Sti not in (Sti / oppføring_VERDI.name).resolve().parents or oppføring_VERDI.issym() or oppføring_VERDI.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + oppføring_VERDI.name)
                gruppe_VERDI.extractall(str(Sti))
            KILDE = Sti / 'jkoros-native-relink'
            def 재연결(Navn, 인수들):
                with (Utgang / Navn).open('wb') as LOG_POST:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(KILDE),
                                   stdout=LOG_POST, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            rapport_VERDI['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            kompilator_verktøy = KILDE / 'vendor/tinycc/libtcc.c'
            brødtekst = kompilator_verktøy.read_text()
            Posisjon = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert brødtekst.count(Posisjon) == 1
            kompilator_verktøy.write_text(brødtekst.replace(Posisjon, Posisjon + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Argumenter.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            BILDE_VERDI = KILDE / 'build/relinked/kernel8.img'
            rapport_VERDI['modified_kernel_sha256'] = hashlib.sha256(BILDE_VERDI.read_bytes()).hexdigest()
            assert rapport_VERDI['modified_kernel_sha256'] != rapport_VERDI['kernel_sha256']
            rapport_VERDI['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Kommando()
            인수들[인수들.index('-kernel') + 1] = str(BILDE_VERDI)
            Prosess_VERDI = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_POST = bytearray()
            merket_område_VERDI = selectors.DefaultSelector()
            merket_område_VERDI.register(Prosess_VERDI.stdout, selectors.EVENT_READ)
            def ventende_tilstand(vise_VERDI_487749b8=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while vise_VERDI_487749b8 not in LOG_POST[처음:]:
                    if time.monotonic() > 끝 or Prosess_VERDI.poll() is not None:
                        raise AssertionError('Missing ' + repr(vise_VERDI_487749b8) + '\n' + LOG_POST[처음:].decode('utf-8', 'replace'))
                    for oppføring_VERDI, _ in merket_område_VERDI.select(.1):
                        data = oppføring_VERDI.fileobj.read(65536)
                        if data:
                            LOG_POST.extend(data)
                return bytes(LOG_POST[처음:])
            def sende(ord_SMS, vise_VERDI_487749b8=b'jkoros-native> '):
                처음 = len(LOG_POST)
                Prosess_VERDI.stdin.write(ord_SMS.encode() + b'\n')
                Prosess_VERDI.stdin.flush()
                return ventende_tilstand(vise_VERDI_487749b8, 처음)
            try:
                ventende_tilstand()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return skrive_Fil_data(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                sende('load /relink.c', b'hex> ')
                for posisjonsindeks in range(0, len(시험), 64):
                    sende(시험[posisjonsindeks:posisjonsindeks+64].hex(), b'hex> ')
                assert b'LOADED' in sende('.')
                KR = sende('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in KR, KR
                KR = sende('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in KR and b'exit 0' in KR, KR
                rapport_VERDI['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                merket_område_VERDI.close()
                if Prosess_VERDI.poll() is None:
                    Prosess_VERDI.terminate()
                    try:
                        Prosess_VERDI.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Prosess_VERDI.kill()
                        Prosess_VERDI.wait()
                (Utgang / 'guest.log').write_bytes(LOG_POST)
        rapport_VERDI['passed'] = True
        print(json.dumps(rapport_VERDI, ensure_ascii=False, indent=2))
    finally:
        (Utgang / 'report.json').write_text(json.dumps(rapport_VERDI, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Kjør_2()
