#!/usr/bin/env python3
"""dystrybucja_WARTOŚĆ 자료만으로 LGPL 재연결과 수정한 TinyCC의 rzeczywisty_dane 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Wykonaj_polecenie import Project_korzeń, polecenie


def Uruchom_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--sdk', type=Path, default=Project_korzeń.parent / 'rpi4/build/rootfs')
    argumenty = parser_48ee4b1b.parse_args()
    pozycja_wyjścia = Project_korzeń / 'build/verification/cosl-relink'
    pozycja_wyjścia.mkdir(parents=True, exist_ok=True)
    Raport_WARTOŚĆ = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_korzeń / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ścieżka_2 = Path(임시)
            with tarfile.open(str(Project_korzeń / 'dist/jkoros-native-relink.tar.gz')) as grupa_WARTOŚĆ:
                for wpis_WARTOŚĆ in grupa_WARTOŚĆ.getmembers():
                    if ścieżka_2 not in (ścieżka_2 / wpis_WARTOŚĆ.name).resolve().parents or wpis_WARTOŚĆ.issym() or wpis_WARTOŚĆ.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + wpis_WARTOŚĆ.name)
                grupa_WARTOŚĆ.extractall(str(ścieżka_2))
            plik_źródłowy = ścieżka_2 / 'jkoros-native-relink'
            def 재연결(Nazwa, 인수들):
                with (pozycja_wyjścia / Nazwa).open('wb') as LOG_zapis:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(plik_źródłowy),
                                   stdout=LOG_zapis, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            Raport_WARTOŚĆ['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            kompilator_narzędzie = plik_źródłowy / 'vendor/tinycc/libtcc.c'
            tekst_podstawowy = kompilator_narzędzie.read_text()
            pozycja = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert tekst_podstawowy.count(pozycja) == 1
            kompilator_narzędzie.write_text(tekst_podstawowy.replace(pozycja, pozycja + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(argumenty.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            OBRAZ_WARTOŚĆ = plik_źródłowy / 'build/relinked/kernel8.img'
            Raport_WARTOŚĆ['modified_kernel_sha256'] = hashlib.sha256(OBRAZ_WARTOŚĆ.read_bytes()).hexdigest()
            assert Raport_WARTOŚĆ['modified_kernel_sha256'] != Raport_WARTOŚĆ['kernel_sha256']
            Raport_WARTOŚĆ['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = polecenie()
            인수들[인수들.index('-kernel') + 1] = str(OBRAZ_WARTOŚĆ)
            Proces_WARTOŚĆ = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_zapis = bytearray()
            zaznaczenie_WARTOŚĆ = selectors.DefaultSelector()
            zaznaczenie_WARTOŚĆ.register(Proces_WARTOŚĆ.stdout, selectors.EVENT_READ)
            def stan_oczekiwania(program_WARTOŚĆ=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while program_WARTOŚĆ not in LOG_zapis[처음:]:
                    if time.monotonic() > 끝 or Proces_WARTOŚĆ.poll() is not None:
                        raise AssertionError('Missing ' + repr(program_WARTOŚĆ) + '\n' + LOG_zapis[처음:].decode('utf-8', 'replace'))
                    for wpis_WARTOŚĆ, _ in zaznaczenie_WARTOŚĆ.select(.1):
                        dane = wpis_WARTOŚĆ.fileobj.read(65536)
                        if dane:
                            LOG_zapis.extend(dane)
                return bytes(LOG_zapis[처음:])
            def wysłać(Word_SMS, program_WARTOŚĆ=b'jkoros-native> '):
                처음 = len(LOG_zapis)
                Proces_WARTOŚĆ.stdin.write(Word_SMS.encode() + b'\n')
                Proces_WARTOŚĆ.stdin.flush()
                return stan_oczekiwania(program_WARTOŚĆ, 처음)
            try:
                stan_oczekiwania()
                testy = '#include <Plik_ABI.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return zapis_Plik_dane(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                wysłać('load /relink.c', b'hex> ')
                for indeks_pozycji in range(0, len(testy), 64):
                    wysłać(testy[indeks_pozycji:indeks_pozycji+64].hex(), b'hex> ')
                assert b'LOADED' in wysłać('.')
                WYNIK = wysłać('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in WYNIK, WYNIK
                WYNIK = wysłać('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in WYNIK and b'exit 0' in WYNIK, WYNIK
                Raport_WARTOŚĆ['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                zaznaczenie_WARTOŚĆ.close()
                if Proces_WARTOŚĆ.poll() is None:
                    Proces_WARTOŚĆ.terminate()
                    try:
                        Proces_WARTOŚĆ.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proces_WARTOŚĆ.kill()
                        Proces_WARTOŚĆ.wait()
                (pozycja_wyjścia / 'guest.log').write_bytes(LOG_zapis)
        Raport_WARTOŚĆ['passed'] = True
        print(json.dumps(Raport_WARTOŚĆ, ensure_ascii=False, indent=2))
    finally:
        (pozycja_wyjścia / 'report.json').write_text(json.dumps(Raport_WARTOŚĆ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Uruchom_2()
