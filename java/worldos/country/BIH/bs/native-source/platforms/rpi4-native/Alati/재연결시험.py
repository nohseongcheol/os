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
from Izvrši_komanda import projicirati_koijen, Naredba


def Pokreni():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=projicirati_koijen.parent / 'rpi4/build/rootfs')
    Argumenti = 해석기.parse_args()
    Ispis = projicirati_koijen / 'build/verification/cosl-relink'
    Ispis.mkdir(parents=True, exist_ok=True)
    izvještaj_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((projicirati_koijen / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Putanja = Path(임시)
            with tarfile.open(str(projicirati_koijen / 'dist/jkoros-native-relink.tar.gz')) as Grupa_VALUE:
                for unos_VALUE in Grupa_VALUE.getmembers():
                    if Putanja not in (Putanja / unos_VALUE.name).resolve().parents or unos_VALUE.issym() or unos_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + unos_VALUE.name)
                Grupa_VALUE.extractall(str(Putanja))
            IZVOR = Putanja / 'jkoros-native-relink'
            def 재연결(Naziv, 인수들):
                with (Ispis / Naziv).open('wb') as LOG_red:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(IZVOR),
                                   stdout=LOG_red, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            izvještaj_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = IZVOR / 'vendor/tinycc/libtcc.c'
            tijelo_teksta = 번역기.read_text()
            Pozicija = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert tijelo_teksta.count(Pozicija) == 1
            번역기.write_text(tijelo_teksta.replace(Pozicija, Pozicija + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Argumenti.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = IZVOR / 'build/relinked/kernel8.img'
            izvještaj_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert izvještaj_VALUE['modified_kernel_sha256'] != izvještaj_VALUE['kernel_sha256']
            izvještaj_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Naredba()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            proces_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_red = bytearray()
            izbor_VALUE = selectors.DefaultSelector()
            izbor_VALUE.register(proces_VALUE.stdout, selectors.EVENT_READ)
            def čekaj_stanje(program_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while program_VALUE not in LOG_red[처음:]:
                    if time.monotonic() > 끝 or proces_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(program_VALUE) + '\n' + LOG_red[처음:].decode('utf-8', 'replace'))
                    for unos_VALUE, _ in izbor_VALUE.select(.1):
                        podaci = unos_VALUE.fileobj.read(65536)
                        if podaci:
                            LOG_red.extend(podaci)
                return bytes(LOG_red[처음:])
            def poslati(Word_SMS, program_VALUE=b'jkoros-native> '):
                처음 = len(LOG_red)
                proces_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                proces_VALUE.stdin.flush()
                return čekaj_stanje(program_VALUE, 처음)
            try:
                čekaj_stanje()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return pisati_fajl_podaci(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                poslati('load /relink.c', b'hex> ')
                for položaj_INDEX in range(0, len(시험), 64):
                    poslati(시험[položaj_INDEX:položaj_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in poslati('.')
                mjera = poslati('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in mjera, mjera
                mjera = poslati('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in mjera and b'exit 0' in mjera, mjera
                izvještaj_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                izbor_VALUE.close()
                if proces_VALUE.poll() is None:
                    proces_VALUE.terminate()
                    try:
                        proces_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        proces_VALUE.kill()
                        proces_VALUE.wait()
                (Ispis / 'guest.log').write_bytes(LOG_red)
        izvještaj_VALUE['passed'] = True
        print(json.dumps(izvještaj_VALUE, ensure_ascii=False, indent=2))
    finally:
        (Ispis / 'report.json').write_text(json.dumps(izvještaj_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Pokreni()
