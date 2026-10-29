#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 dejanski_podatki 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Izvedi_ukaz import pobuda_koren, Ukaz


def Zaženi():
    razčlenjevalnik_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    razčlenjevalnik_48ee4b1b.add_argument('--sdk', type=Path, default=pobuda_koren.parent / 'rpi4/build/rootfs')
    Argumenti = razčlenjevalnik_48ee4b1b.parse_args()
    Izpis = pobuda_koren / 'build/verification/cosl-relink'
    Izpis.mkdir(parents=True, exist_ok=True)
    prijavi_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((pobuda_koren / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            POT = Path(임시)
            with tarfile.open(str(pobuda_koren / 'dist/jkoros-native-relink.tar.gz')) as Skupina_VALUE:
                for vnos_VALUE in Skupina_VALUE.getmembers():
                    if POT not in (POT / vnos_VALUE.name).resolve().parents or vnos_VALUE.issym() or vnos_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + vnos_VALUE.name)
                Skupina_VALUE.extractall(str(POT))
            VIR = POT / 'jkoros-native-relink'
            def 재연결(Ime, 인수들):
                with (Izpis / Ime).open('wb') as LOG_zapis:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(VIR),
                                   stdout=LOG_zapis, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            prijavi_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            prevajalnik_orodje = VIR / 'vendor/tinycc/libtcc.c'
            telo_besedila = prevajalnik_orodje.read_text()
            Položaj = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert telo_besedila.count(Položaj) == 1
            prevajalnik_orodje.write_text(telo_besedila.replace(Položaj, Položaj + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Argumenti.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = VIR / 'build/relinked/kernel8.img'
            prijavi_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert prijavi_VALUE['modified_kernel_sha256'] != prijavi_VALUE['kernel_sha256']
            prijavi_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Ukaz()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            Proces_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_zapis = bytearray()
            izbor_VALUE = selectors.DefaultSelector()
            izbor_VALUE.register(Proces_VALUE.stdout, selectors.EVENT_READ)
            def čakalno_stanje(oddaja_VALUE_487749b8=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while oddaja_VALUE_487749b8 not in LOG_zapis[처음:]:
                    if time.monotonic() > 끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(oddaja_VALUE_487749b8) + '\n' + LOG_zapis[처음:].decode('utf-8', 'replace'))
                    for vnos_VALUE, _ in izbor_VALUE.select(.1):
                        podatki = vnos_VALUE.fileobj.read(65536)
                        if podatki:
                            LOG_zapis.extend(podatki)
                return bytes(LOG_zapis[처음:])
            def poslati(Word_SMS, oddaja_VALUE_487749b8=b'jkoros-native> '):
                처음 = len(LOG_zapis)
                Proces_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Proces_VALUE.stdin.flush()
                return čakalno_stanje(oddaja_VALUE_487749b8, 처음)
            try:
                čakalno_stanje()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return pisati_Datoteka_podatki(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                poslati('load /relink.c', b'hex> ')
                for kazalec_mesta in range(0, len(시험), 64):
                    poslati(시험[kazalec_mesta:kazalec_mesta+64].hex(), b'hex> ')
                assert b'LOADED' in poslati('.')
                REZULTAT = poslati('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in REZULTAT, REZULTAT
                REZULTAT = poslati('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in REZULTAT and b'exit 0' in REZULTAT, REZULTAT
                prijavi_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                izbor_VALUE.close()
                if Proces_VALUE.poll() is None:
                    Proces_VALUE.terminate()
                    try:
                        Proces_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proces_VALUE.kill()
                        Proces_VALUE.wait()
                (Izpis / 'guest.log').write_bytes(LOG_zapis)
        prijavi_VALUE['passed'] = True
        print(json.dumps(prijavi_VALUE, ensure_ascii=False, indent=2))
    finally:
        (Izpis / 'report.json').write_text(json.dumps(prijavi_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Zaženi()
