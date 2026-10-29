#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 aktual_të_dhëna 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from zbatoj_komandë import Project_rrënjë, Komanda


def Ekzekuto():
    analizues_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizues_48ee4b1b.add_argument('--sdk', type=Path, default=Project_rrënjë.parent / 'rpi4/build/rootfs')
    Argumente = analizues_48ee4b1b.parse_args()
    출력 = Project_rrënjë / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    raport_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_rrënjë / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            POZICIONI = Path(임시)
            with tarfile.open(str(Project_rrënjë / 'dist/jkoros-native-relink.tar.gz')) as grup_VALUE:
                for futje_VALUE in grup_VALUE.getmembers():
                    if POZICIONI not in (POZICIONI / futje_VALUE.name).resolve().parents or futje_VALUE.issym() or futje_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + futje_VALUE.name)
                grup_VALUE.extractall(str(POZICIONI))
            BURIMI = POZICIONI / 'jkoros-native-relink'
            def 재연결(Emër, 인수들):
                with (출력 / Emër).open('wb') as LOG_RECORD:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(BURIMI),
                                   stdout=LOG_RECORD, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            raport_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = BURIMI / 'vendor/tinycc/libtcc.c'
            trupi_i_tekstit = 번역기.read_text()
            Pozicioni = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert trupi_i_tekstit.count(Pozicioni) == 1
            번역기.write_text(trupi_i_tekstit.replace(Pozicioni, Pozicioni + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Argumente.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = BURIMI / 'build/relinked/kernel8.img'
            raport_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert raport_VALUE['modified_kernel_sha256'] != raport_VALUE['kernel_sha256']
            raport_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Komanda()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            Proces_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_RECORD = bytearray()
            përzgjedhje_VALUE = selectors.DefaultSelector()
            përzgjedhje_VALUE.register(Proces_VALUE.stdout, selectors.EVENT_READ)
            def Prit_status(shfaq_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while shfaq_VALUE not in LOG_RECORD[처음:]:
                    if time.monotonic() > 끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(shfaq_VALUE) + '\n' + LOG_RECORD[처음:].decode('utf-8', 'replace'))
                    for futje_VALUE, _ in përzgjedhje_VALUE.select(.1):
                        të_dhëna = futje_VALUE.fileobj.read(65536)
                        if të_dhëna:
                            LOG_RECORD.extend(të_dhëna)
                return bytes(LOG_RECORD[처음:])
            def dërgoj(Word_SMS, shfaq_VALUE=b'jkoros-native> '):
                처음 = len(LOG_RECORD)
                Proces_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Proces_VALUE.stdin.flush()
                return Prit_status(shfaq_VALUE, 처음)
            try:
                Prit_status()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return shkruaj_skedar_të_dhëna(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                dërgoj('load /relink.c', b'hex> ')
                for pozicioni_INDEX in range(0, len(시험), 64):
                    dërgoj(시험[pozicioni_INDEX:pozicioni_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in dërgoj('.')
                llogaritje = dërgoj('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in llogaritje, llogaritje
                llogaritje = dërgoj('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in llogaritje and b'exit 0' in llogaritje, llogaritje
                raport_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                përzgjedhje_VALUE.close()
                if Proces_VALUE.poll() is None:
                    Proces_VALUE.terminate()
                    try:
                        Proces_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proces_VALUE.kill()
                        Proces_VALUE.wait()
                (출력 / 'guest.log').write_bytes(LOG_RECORD)
        raport_VALUE['passed'] = True
        print(json.dumps(raport_VALUE, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(raport_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Ekzekuto()
