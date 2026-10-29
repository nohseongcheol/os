#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 real_date 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from executa_comandă import Project_rădăcină, Comandă


def Pornește():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--sdk', type=Path, default=Project_rădăcină.parent / 'rpi4/build/rootfs')
    Argumente = parser_48ee4b1b.parse_args()
    Rezultat = Project_rădăcină / 'build/verification/cosl-relink'
    Rezultat.mkdir(parents=True, exist_ok=True)
    raport_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_rădăcină / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Cale = Path(임시)
            with tarfile.open(str(Project_rădăcină / 'dist/jkoros-native-relink.tar.gz')) as grup_VALUE:
                for intrare_VALUE in grup_VALUE.getmembers():
                    if Cale not in (Cale / intrare_VALUE.name).resolve().parents or intrare_VALUE.issym() or intrare_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + intrare_VALUE.name)
                grup_VALUE.extractall(str(Cale))
            SURSĂ = Cale / 'jkoros-native-relink'
            def 재연결(Nume, 인수들):
                with (Rezultat / Nume).open('wb') as LOG_RECORD:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(SURSĂ),
                                   stdout=LOG_RECORD, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            raport_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            compilator_instrument = SURSĂ / 'vendor/tinycc/libtcc.c'
            text_corp = compilator_instrument.read_text()
            Poziție = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert text_corp.count(Poziție) == 1
            compilator_instrument.write_text(text_corp.replace(Poziție, Poziție + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Argumente.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = SURSĂ / 'build/relinked/kernel8.img'
            raport_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert raport_VALUE['modified_kernel_sha256'] != raport_VALUE['kernel_sha256']
            raport_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Comandă()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            Proces_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_RECORD = bytearray()
            selecție_VALUE = selectors.DefaultSelector()
            selecție_VALUE.register(Proces_VALUE.stdout, selectors.EVENT_READ)
            def stare_de_așteptare(afișa_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while afișa_VALUE not in LOG_RECORD[처음:]:
                    if time.monotonic() > 끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(afișa_VALUE) + '\n' + LOG_RECORD[처음:].decode('utf-8', 'replace'))
                    for intrare_VALUE, _ in selecție_VALUE.select(.1):
                        date = intrare_VALUE.fileobj.read(65536)
                        if date:
                            LOG_RECORD.extend(date)
                return bytes(LOG_RECORD[처음:])
            def trimite(Word_SMS, afișa_VALUE=b'jkoros-native> '):
                처음 = len(LOG_RECORD)
                Proces_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Proces_VALUE.stdin.flush()
                return stare_de_așteptare(afișa_VALUE, 처음)
            try:
                stare_de_așteptare()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return scriere_Fișier_date(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                trimite('load /relink.c', b'hex> ')
                for index_de_poziție in range(0, len(시험), 64):
                    trimite(시험[index_de_poziție:index_de_poziție+64].hex(), b'hex> ')
                assert b'LOADED' in trimite('.')
                KR = trimite('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in KR, KR
                KR = trimite('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in KR and b'exit 0' in KR, KR
                raport_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                selecție_VALUE.close()
                if Proces_VALUE.poll() is None:
                    Proces_VALUE.terminate()
                    try:
                        Proces_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proces_VALUE.kill()
                        Proces_VALUE.wait()
                (Rezultat / 'guest.log').write_bytes(LOG_RECORD)
        raport_VALUE['passed'] = True
        print(json.dumps(raport_VALUE, ensure_ascii=False, indent=2))
    finally:
        (Rezultat / 'report.json').write_text(json.dumps(raport_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Pornește()
