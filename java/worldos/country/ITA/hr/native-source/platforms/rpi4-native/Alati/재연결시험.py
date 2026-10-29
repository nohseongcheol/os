#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 stvaran_podaci 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Izvrši_naredba import akcija_korijen, Naredba


def Pokreni():
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('--sdk', type=Path, default=akcija_korijen.parent / 'rpi4/build/rootfs')
    Argumenti = analizator_48ee4b1b.parse_args()
    Izlaz = akcija_korijen / 'build/verification/cosl-relink'
    Izlaz.mkdir(parents=True, exist_ok=True)
    izvješće_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((akcija_korijen / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            PUTANJA = Path(임시)
            with tarfile.open(str(akcija_korijen / 'dist/jkoros-native-relink.tar.gz')) as Grupa_VALUE:
                for unos_VALUE in Grupa_VALUE.getmembers():
                    if PUTANJA not in (PUTANJA / unos_VALUE.name).resolve().parents or unos_VALUE.issym() or unos_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + unos_VALUE.name)
                Grupa_VALUE.extractall(str(PUTANJA))
            IZVOR = PUTANJA / 'jkoros-native-relink'
            def 재연결(Ime, 인수들):
                with (Izlaz / Ime).open('wb') as LOG_zapis:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(IZVOR),
                                   stdout=LOG_zapis, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            izvješće_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            kompilator_alat = IZVOR / 'vendor/tinycc/libtcc.c'
            tijelo_teksta = kompilator_alat.read_text()
            Položaj = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert tijelo_teksta.count(Položaj) == 1
            kompilator_alat.write_text(tijelo_teksta.replace(Položaj, Položaj + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Argumenti.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = IZVOR / 'build/relinked/kernel8.img'
            izvješće_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert izvješće_VALUE['modified_kernel_sha256'] != izvješće_VALUE['kernel_sha256']
            izvješće_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Naredba()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            Proces_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_zapis = bytearray()
            odabir_VALUE = selectors.DefaultSelector()
            odabir_VALUE.register(Proces_VALUE.stdout, selectors.EVENT_READ)
            def stanje_čekanja(emisija_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while emisija_VALUE not in LOG_zapis[처음:]:
                    if time.monotonic() > 끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(emisija_VALUE) + '\n' + LOG_zapis[처음:].decode('utf-8', 'replace'))
                    for unos_VALUE, _ in odabir_VALUE.select(.1):
                        podaci = unos_VALUE.fileobj.read(65536)
                        if podaci:
                            LOG_zapis.extend(podaci)
                return bytes(LOG_zapis[처음:])
            def slati(Word_SMS, emisija_VALUE=b'jkoros-native> '):
                처음 = len(LOG_zapis)
                Proces_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Proces_VALUE.stdin.flush()
                return stanje_čekanja(emisija_VALUE, 처음)
            try:
                stanje_čekanja()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return zapisivanje_Datoteka_podaci(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                slati('load /relink.c', b'hex> ')
                for indeks_položaja in range(0, len(시험), 64):
                    slati(시험[indeks_položaja:indeks_položaja+64].hex(), b'hex> ')
                assert b'LOADED' in slati('.')
                REZULTAT = slati('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in REZULTAT, REZULTAT
                REZULTAT = slati('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in REZULTAT and b'exit 0' in REZULTAT, REZULTAT
                izvješće_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                odabir_VALUE.close()
                if Proces_VALUE.poll() is None:
                    Proces_VALUE.terminate()
                    try:
                        Proces_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proces_VALUE.kill()
                        Proces_VALUE.wait()
                (Izlaz / 'guest.log').write_bytes(LOG_zapis)
        izvješće_VALUE['passed'] = True
        print(json.dumps(izvješće_VALUE, ensure_ascii=False, indent=2))
    finally:
        (Izlaz / 'report.json').write_text(json.dumps(izvješće_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Pokreni()
