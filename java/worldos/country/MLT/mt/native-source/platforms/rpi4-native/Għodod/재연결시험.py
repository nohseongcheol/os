#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 attwali_data 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from eżegwixxa_kmand import pprojetta_għerq, kmand


def serje():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=pprojetta_għerq.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = pprojetta_għerq / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    rapport_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((pprojetta_għerq / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            mogħdija = Path(임시)
            with tarfile.open(str(pprojetta_għerq / 'dist/jkoros-native-relink.tar.gz')) as grupp_VALUE:
                for entrata_VALUE in grupp_VALUE.getmembers():
                    if mogħdija not in (mogħdija / entrata_VALUE.name).resolve().parents or entrata_VALUE.issym() or entrata_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + entrata_VALUE.name)
                grupp_VALUE.extractall(str(mogħdija))
            sors = mogħdija / 'jkoros-native-relink'
            def 재연결(isem, 인수들):
                with (출력 / isem).open('wb') as LOG_RECORD:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(sors),
                                   stdout=LOG_RECORD, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            rapport_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = sors / 'vendor/tinycc/libtcc.c'
            il_korp_tat_test = 번역기.read_text()
            pożizzjoni = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert il_korp_tat_test.count(pożizzjoni) == 1
            번역기.write_text(il_korp_tat_test.replace(pożizzjoni, pożizzjoni + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = sors / 'build/relinked/kernel8.img'
            rapport_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert rapport_VALUE['modified_kernel_sha256'] != rapport_VALUE['kernel_sha256']
            rapport_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = kmand()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            Proċess_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_RECORD = bytearray()
            għażla_VALUE = selectors.DefaultSelector()
            għażla_VALUE.register(Proċess_VALUE.stdout, selectors.EVENT_READ)
            def 기다림(wera_VALUE_487749b8=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while wera_VALUE_487749b8 not in LOG_RECORD[처음:]:
                    if time.monotonic() > 끝 or Proċess_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(wera_VALUE_487749b8) + '\n' + LOG_RECORD[처음:].decode('utf-8', 'replace'))
                    for entrata_VALUE, _ in għażla_VALUE.select(.1):
                        data = entrata_VALUE.fileobj.read(65536)
                        if data:
                            LOG_RECORD.extend(data)
                return bytes(LOG_RECORD[처음:])
            def bagħat(Word_SMS, wera_VALUE_487749b8=b'jkoros-native> '):
                처음 = len(LOG_RECORD)
                Proċess_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Proċess_VALUE.stdin.flush()
                return 기다림(wera_VALUE_487749b8, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return kiteb_fajl_data(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                bagħat('load /relink.c', b'hex> ')
                for pożizzjoni_INDEX in range(0, len(시험), 64):
                    bagħat(시험[pożizzjoni_INDEX:pożizzjoni_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in bagħat('.')
                miżura = bagħat('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in miżura, miżura
                miżura = bagħat('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in miżura and b'exit 0' in miżura, miżura
                rapport_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                għażla_VALUE.close()
                if Proċess_VALUE.poll() is None:
                    Proċess_VALUE.terminate()
                    try:
                        Proċess_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proċess_VALUE.kill()
                        Proċess_VALUE.wait()
                (출력 / 'guest.log').write_bytes(LOG_RECORD)
        rapport_VALUE['passed'] = True
        print(json.dumps(rapport_VALUE, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(rapport_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    serje()
