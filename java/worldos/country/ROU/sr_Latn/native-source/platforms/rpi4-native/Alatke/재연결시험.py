#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 stvarni_podaci 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Izvrši_komanda import radnja_koren, komanda


def koristiti():
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('--sdk', type=Path, default=radnja_koren.parent / 'rpi4/build/rootfs')
    인수 = analizator_48ee4b1b.parse_args()
    출력 = radnja_koren / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    izveštaj_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((radnja_koren / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            putanja = Path(임시)
            with tarfile.open(str(radnja_koren / 'dist/jkoros-native-relink.tar.gz')) as Grupa_VALUE:
                for stavka_VALUE in Grupa_VALUE.getmembers():
                    if putanja not in (putanja / stavka_VALUE.name).resolve().parents or stavka_VALUE.issym() or stavka_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + stavka_VALUE.name)
                Grupa_VALUE.extractall(str(putanja))
            izvor = putanja / 'jkoros-native-relink'
            def 재연결(ime, 인수들):
                with (출력 / ime).open('wb') as LOG_snimi:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(izvor),
                                   stdout=LOG_snimi, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            izveštaj_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            kompajler_alatka = izvor / 'vendor/tinycc/libtcc.c'
            telo_teksta = kompajler_alatka.read_text()
            pozicija = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert telo_teksta.count(pozicija) == 1
            kompajler_alatka.write_text(telo_teksta.replace(pozicija, pozicija + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = izvor / 'build/relinked/kernel8.img'
            izveštaj_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert izveštaj_VALUE['modified_kernel_sha256'] != izveštaj_VALUE['kernel_sha256']
            izveštaj_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = komanda()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            Proces_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_snimi = bytearray()
            izbor_VALUE = selectors.DefaultSelector()
            izbor_VALUE.register(Proces_VALUE.stdout, selectors.EVENT_READ)
            def stanje_čekanja(emisija_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while emisija_VALUE not in LOG_snimi[처음:]:
                    if time.monotonic() > 끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(emisija_VALUE) + '\n' + LOG_snimi[처음:].decode('utf-8', 'replace'))
                    for stavka_VALUE, _ in izbor_VALUE.select(.1):
                        podaci = stavka_VALUE.fileobj.read(65536)
                        if podaci:
                            LOG_snimi.extend(podaci)
                return bytes(LOG_snimi[처음:])
            def poslati(Word_SMS, emisija_VALUE=b'jkoros-native> '):
                처음 = len(LOG_snimi)
                Proces_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Proces_VALUE.stdin.flush()
                return stanje_čekanja(emisija_VALUE, 처음)
            try:
                stanje_čekanja()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return 파일자료쓰기(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                poslati('load /relink.c', b'hex> ')
                for indeks_pozicije in range(0, len(시험), 64):
                    poslati(시험[indeks_pozicije:indeks_pozicije+64].hex(), b'hex> ')
                assert b'LOADED' in poslati('.')
                KR = poslati('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in KR, KR
                KR = poslati('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in KR and b'exit 0' in KR, KR
                izveštaj_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                izbor_VALUE.close()
                if Proces_VALUE.poll() is None:
                    Proces_VALUE.terminate()
                    try:
                        Proces_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proces_VALUE.kill()
                        Proces_VALUE.wait()
                (출력 / 'guest.log').write_bytes(LOG_snimi)
        izveštaj_VALUE['passed'] = True
        print(json.dumps(izveštaj_VALUE, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(izveštaj_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    koristiti()
