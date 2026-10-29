#!/usr/bin/env python3
"""dreifing_VALUE 자료만으로 LGPL 재연결과 수정한 TinyCC의 raun_gögn 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from keyra_skipun import verk_rót, Skipun


def Keyra_2():
    þáttari_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    þáttari_48ee4b1b.add_argument('--sdk', type=Path, default=verk_rót.parent / 'rpi4/build/rootfs')
    Viðföng = þáttari_48ee4b1b.parse_args()
    úttak = verk_rót / 'build/verification/cosl-relink'
    úttak.mkdir(parents=True, exist_ok=True)
    skrá_VALUE_ddf2aaf3 = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((verk_rót / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            SLÓÐ = Path(임시)
            with tarfile.open(str(verk_rót / 'dist/jkoros-native-relink.tar.gz')) as Hópur_VALUE:
                for færsla_VALUE in Hópur_VALUE.getmembers():
                    if SLÓÐ not in (SLÓÐ / færsla_VALUE.name).resolve().parents or færsla_VALUE.issym() or færsla_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + færsla_VALUE.name)
                Hópur_VALUE.extractall(str(SLÓÐ))
            Uppruni = SLÓÐ / 'jkoros-native-relink'
            def 재연결(Heiti, 인수들):
                with (úttak / Heiti).open('wb') as LOG_lína:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(Uppruni),
                                   stdout=LOG_lína, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            skrá_VALUE_ddf2aaf3['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = Uppruni / 'vendor/tinycc/libtcc.c'
            meginmál = 번역기.read_text()
            Staðsetning = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert meginmál.count(Staðsetning) == 1
            번역기.write_text(meginmál.replace(Staðsetning, Staðsetning + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Viðföng.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            mynd_VALUE = Uppruni / 'build/relinked/kernel8.img'
            skrá_VALUE_ddf2aaf3['modified_kernel_sha256'] = hashlib.sha256(mynd_VALUE.read_bytes()).hexdigest()
            assert skrá_VALUE_ddf2aaf3['modified_kernel_sha256'] != skrá_VALUE_ddf2aaf3['kernel_sha256']
            skrá_VALUE_ddf2aaf3['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Skipun()
            인수들[인수들.index('-kernel') + 1] = str(mynd_VALUE)
            Ferli_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_lína = bytearray()
            val_VALUE = selectors.DefaultSelector()
            val_VALUE.register(Ferli_VALUE.stdout, selectors.EVENT_READ)
            def Bíddu_staða(sýna_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while sýna_VALUE not in LOG_lína[처음:]:
                    if time.monotonic() > 끝 or Ferli_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(sýna_VALUE) + '\n' + LOG_lína[처음:].decode('utf-8', 'replace'))
                    for færsla_VALUE, _ in val_VALUE.select(.1):
                        gögn = færsla_VALUE.fileobj.read(65536)
                        if gögn:
                            LOG_lína.extend(gögn)
                return bytes(LOG_lína[처음:])
            def senda(Word_SMS, sýna_VALUE=b'jkoros-native> '):
                처음 = len(LOG_lína)
                Ferli_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Ferli_VALUE.stdin.flush()
                return Bíddu_staða(sýna_VALUE, 처음)
            try:
                Bíddu_staða()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return skrifa_skrá_gögn(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                senda('load /relink.c', b'hex> ')
                for staða_INDEX in range(0, len(시험), 64):
                    senda(시험[staða_INDEX:staða_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in senda('.')
                NIÐURSTAÐA = senda('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in NIÐURSTAÐA, NIÐURSTAÐA
                NIÐURSTAÐA = senda('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in NIÐURSTAÐA and b'exit 0' in NIÐURSTAÐA, NIÐURSTAÐA
                skrá_VALUE_ddf2aaf3['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                val_VALUE.close()
                if Ferli_VALUE.poll() is None:
                    Ferli_VALUE.terminate()
                    try:
                        Ferli_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Ferli_VALUE.kill()
                        Ferli_VALUE.wait()
                (úttak / 'guest.log').write_bytes(LOG_lína)
        skrá_VALUE_ddf2aaf3['passed'] = True
        print(json.dumps(skrá_VALUE_ddf2aaf3, ensure_ascii=False, indent=2))
    finally:
        (úttak / 'report.json').write_text(json.dumps(skrá_VALUE_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Keyra_2()
