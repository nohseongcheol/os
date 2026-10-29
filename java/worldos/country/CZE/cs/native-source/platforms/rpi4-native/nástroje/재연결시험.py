#!/usr/bin/env python3
"""distribuce_HODNOTA 자료만으로 LGPL 재연결과 수정한 TinyCC의 skutečný_data 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Provést_příkaz import akce_kořen, příkaz


def Spustit_2():
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('--sdk', type=Path, default=akce_kořen.parent / 'rpi4/build/rootfs')
    argumenty = analyzátor_48ee4b1b.parse_args()
    výstupní_pozice = akce_kořen / 'build/verification/cosl-relink'
    výstupní_pozice.mkdir(parents=True, exist_ok=True)
    Zpráva_HODNOTA = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((akce_kořen / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            cesta_2 = Path(임시)
            with tarfile.open(str(akce_kořen / 'dist/jkoros-native-relink.tar.gz')) as Skupina_HODNOTA:
                for položka_HODNOTA in Skupina_HODNOTA.getmembers():
                    if cesta_2 not in (cesta_2 / položka_HODNOTA.name).resolve().parents or položka_HODNOTA.issym() or položka_HODNOTA.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + položka_HODNOTA.name)
                Skupina_HODNOTA.extractall(str(cesta_2))
            zdrojový_soubor = cesta_2 / 'jkoros-native-relink'
            def 재연결(Název, 인수들):
                with (výstupní_pozice / Název).open('wb') as LOGZ_ZÁZNAM:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(zdrojový_soubor),
                                   stdout=LOGZ_ZÁZNAM, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            Zpráva_HODNOTA['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            kompilátor_nástroj = zdrojový_soubor / 'vendor/tinycc/libtcc.c'
            základní_text = kompilátor_nástroj.read_text()
            pozice = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert základní_text.count(pozice) == 1
            kompilátor_nástroj.write_text(základní_text.replace(pozice, pozice + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(argumenty.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            image_HODNOTA = zdrojový_soubor / 'build/relinked/kernel8.img'
            Zpráva_HODNOTA['modified_kernel_sha256'] = hashlib.sha256(image_HODNOTA.read_bytes()).hexdigest()
            assert Zpráva_HODNOTA['modified_kernel_sha256'] != Zpráva_HODNOTA['kernel_sha256']
            Zpráva_HODNOTA['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = příkaz()
            인수들[인수들.index('-kernel') + 1] = str(image_HODNOTA)
            Proces_HODNOTA = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOGZ_ZÁZNAM = bytearray()
            výběr_HODNOTA = selectors.DefaultSelector()
            výběr_HODNOTA.register(Proces_HODNOTA.stdout, selectors.EVENT_READ)
            def čekací_stav(zobrazit_HODNOTA=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while zobrazit_HODNOTA not in LOGZ_ZÁZNAM[처음:]:
                    if time.monotonic() > 끝 or Proces_HODNOTA.poll() is not None:
                        raise AssertionError('Missing ' + repr(zobrazit_HODNOTA) + '\n' + LOGZ_ZÁZNAM[처음:].decode('utf-8', 'replace'))
                    for položka_HODNOTA, _ in výběr_HODNOTA.select(.1):
                        data = položka_HODNOTA.fileobj.read(65536)
                        if data:
                            LOGZ_ZÁZNAM.extend(data)
                return bytes(LOGZ_ZÁZNAM[처음:])
            def poslat(Word_SMS, zobrazit_HODNOTA=b'jkoros-native> '):
                처음 = len(LOGZ_ZÁZNAM)
                Proces_HODNOTA.stdin.write(Word_SMS.encode() + b'\n')
                Proces_HODNOTA.stdin.flush()
                return čekací_stav(zobrazit_HODNOTA, 처음)
            try:
                čekací_stav()
                zkoušky = '#include <Soubor_ABI.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return zápis_Soubor_data(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                poslat('load /relink.c', b'hex> ')
                for poziční_index in range(0, len(zkoušky), 64):
                    poslat(zkoušky[poziční_index:poziční_index+64].hex(), b'hex> ')
                assert b'LOADED' in poslat('.')
                VÝSLEDEK = poslat('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in VÝSLEDEK, VÝSLEDEK
                VÝSLEDEK = poslat('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in VÝSLEDEK and b'exit 0' in VÝSLEDEK, VÝSLEDEK
                Zpráva_HODNOTA['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                výběr_HODNOTA.close()
                if Proces_HODNOTA.poll() is None:
                    Proces_HODNOTA.terminate()
                    try:
                        Proces_HODNOTA.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proces_HODNOTA.kill()
                        Proces_HODNOTA.wait()
                (výstupní_pozice / 'guest.log').write_bytes(LOGZ_ZÁZNAM)
        Zpráva_HODNOTA['passed'] = True
        print(json.dumps(Zpráva_HODNOTA, ensure_ascii=False, indent=2))
    finally:
        (výstupní_pozice / 'report.json').write_text(json.dumps(Zpráva_HODNOTA, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Spustit_2()
