#!/usr/bin/env python3
"""sadale_VALUE 자료만으로 LGPL 재연결과 수정한 TinyCC의 faktisks_dati 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Izpildīt_komanda import Project_sakne, Komanda


def Palaist():
    parsētājs_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parsētājs_48ee4b1b.add_argument('--sdk', type=Path, default=Project_sakne.parent / 'rpi4/build/rootfs')
    Parametri = parsētājs_48ee4b1b.parse_args()
    Izvade = Project_sakne / 'build/verification/cosl-relink'
    Izvade.mkdir(parents=True, exist_ok=True)
    ziņot_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_sakne / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            CEĻŠ = Path(임시)
            with tarfile.open(str(Project_sakne / 'dist/jkoros-native-relink.tar.gz')) as Grupa_VALUE:
                for ievade_VALUE in Grupa_VALUE.getmembers():
                    if CEĻŠ not in (CEĻŠ / ievade_VALUE.name).resolve().parents or ievade_VALUE.issym() or ievade_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ievade_VALUE.name)
                Grupa_VALUE.extractall(str(CEĻŠ))
            AVOTS = CEĻŠ / 'jkoros-native-relink'
            def 재연결(Nosaukums, 인수들):
                with (Izvade / Nosaukums).open('wb') as LOG_RECORD:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(AVOTS),
                                   stdout=LOG_RECORD, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            ziņot_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            kompilators_rīks = AVOTS / 'vendor/tinycc/libtcc.c'
            pamatteksts = kompilators_rīks.read_text()
            Novietojums = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert pamatteksts.count(Novietojums) == 1
            kompilators_rīks.write_text(pamatteksts.replace(Novietojums, Novietojums + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Parametri.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = AVOTS / 'build/relinked/kernel8.img'
            ziņot_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert ziņot_VALUE['modified_kernel_sha256'] != ziņot_VALUE['kernel_sha256']
            ziņot_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Komanda()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            Process_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_RECORD = bytearray()
            atlase_VALUE = selectors.DefaultSelector()
            atlase_VALUE.register(Process_VALUE.stdout, selectors.EVENT_READ)
            def nogaides_stāvoklis(rādīt_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while rādīt_VALUE not in LOG_RECORD[처음:]:
                    if time.monotonic() > 끝 or Process_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(rādīt_VALUE) + '\n' + LOG_RECORD[처음:].decode('utf-8', 'replace'))
                    for ievade_VALUE, _ in atlase_VALUE.select(.1):
                        dati = ievade_VALUE.fileobj.read(65536)
                        if dati:
                            LOG_RECORD.extend(dati)
                return bytes(LOG_RECORD[처음:])
            def sūtīt(Word_SMS, rādīt_VALUE=b'jkoros-native> '):
                처음 = len(LOG_RECORD)
                Process_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Process_VALUE.stdin.flush()
                return nogaides_stāvoklis(rādīt_VALUE, 처음)
            try:
                nogaides_stāvoklis()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return rakstīšana_Fails_dati(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                sūtīt('load /relink.c', b'hex> ')
                for pozīcijas_indekss in range(0, len(시험), 64):
                    sūtīt(시험[pozīcijas_indekss:pozīcijas_indekss+64].hex(), b'hex> ')
                assert b'LOADED' in sūtīt('.')
                mērs = sūtīt('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in mērs, mērs
                mērs = sūtīt('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in mērs and b'exit 0' in mērs, mērs
                ziņot_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                atlase_VALUE.close()
                if Process_VALUE.poll() is None:
                    Process_VALUE.terminate()
                    try:
                        Process_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Process_VALUE.kill()
                        Process_VALUE.wait()
                (Izvade / 'guest.log').write_bytes(LOG_RECORD)
        ziņot_VALUE['passed'] = True
        print(json.dumps(ziņot_VALUE, ensure_ascii=False, indent=2))
    finally:
        (Izvade / 'report.json').write_text(json.dumps(ziņot_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Palaist()
