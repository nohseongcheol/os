#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 skutočný_údaje 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Vykonať_príkaz import akcia_koreň, Príkaz


def Spustiť_2():
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('--sdk', type=Path, default=akcia_koreň.parent / 'rpi4/build/rootfs')
    Argumenty = analyzátor_48ee4b1b.parse_args()
    Výstup = akcia_koreň / 'build/verification/cosl-relink'
    Výstup.mkdir(parents=True, exist_ok=True)
    správa_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((akcia_koreň / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Cesta = Path(임시)
            with tarfile.open(str(akcia_koreň / 'dist/jkoros-native-relink.tar.gz')) as Skupina_VALUE:
                for položka_VALUE in Skupina_VALUE.getmembers():
                    if Cesta not in (Cesta / položka_VALUE.name).resolve().parents or položka_VALUE.issym() or položka_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + položka_VALUE.name)
                Skupina_VALUE.extractall(str(Cesta))
            ZDROJ = Cesta / 'jkoros-native-relink'
            def 재연결(Názov, 인수들):
                with (Výstup / Názov).open('wb') as LOG_RECORD:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ZDROJ),
                                   stdout=LOG_RECORD, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            správa_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            kompilátor_nástroj = ZDROJ / 'vendor/tinycc/libtcc.c'
            základný_text = kompilátor_nástroj.read_text()
            Pozícia = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert základný_text.count(Pozícia) == 1
            kompilátor_nástroj.write_text(základný_text.replace(Pozícia, Pozícia + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Argumenty.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = ZDROJ / 'build/relinked/kernel8.img'
            správa_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert správa_VALUE['modified_kernel_sha256'] != správa_VALUE['kernel_sha256']
            správa_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Príkaz()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            Proces_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_RECORD = bytearray()
            výber_VALUE = selectors.DefaultSelector()
            výber_VALUE.register(Proces_VALUE.stdout, selectors.EVENT_READ)
            def stav_čakania(zobraziť_VALUE_487749b8=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while zobraziť_VALUE_487749b8 not in LOG_RECORD[처음:]:
                    if time.monotonic() > 끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(zobraziť_VALUE_487749b8) + '\n' + LOG_RECORD[처음:].decode('utf-8', 'replace'))
                    for položka_VALUE, _ in výber_VALUE.select(.1):
                        údaje = položka_VALUE.fileobj.read(65536)
                        if údaje:
                            LOG_RECORD.extend(údaje)
                return bytes(LOG_RECORD[처음:])
            def odoslať(Word_SMS, zobraziť_VALUE_487749b8=b'jkoros-native> '):
                처음 = len(LOG_RECORD)
                Proces_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Proces_VALUE.stdin.flush()
                return stav_čakania(zobraziť_VALUE_487749b8, 처음)
            try:
                stav_čakania()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return zapísať_Súbor_údaje(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                odoslať('load /relink.c', b'hex> ')
                for pozičný_index in range(0, len(시험), 64):
                    odoslať(시험[pozičný_index:pozičný_index+64].hex(), b'hex> ')
                assert b'LOADED' in odoslať('.')
                KR = odoslať('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in KR, KR
                KR = odoslať('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in KR and b'exit 0' in KR, KR
                správa_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                výber_VALUE.close()
                if Proces_VALUE.poll() is None:
                    Proces_VALUE.terminate()
                    try:
                        Proces_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proces_VALUE.kill()
                        Proces_VALUE.wait()
                (Výstup / 'guest.log').write_bytes(LOG_RECORD)
        správa_VALUE['passed'] = True
        print(json.dumps(správa_VALUE, ensure_ascii=False, indent=2))
    finally:
        (Výstup / 'report.json').write_text(json.dumps(správa_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Spustiť_2()
