#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 iarbhír_sonraí 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Rith_ordú import teilgean_fréamh, Ordú


def Rith_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=teilgean_fréamh.parent / 'rpi4/build/rootfs')
    Argóintí = 해석기.parse_args()
    Aschur = teilgean_fréamh / 'build/verification/cosl-relink'
    Aschur.mkdir(parents=True, exist_ok=True)
    tuairisc_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((teilgean_fréamh / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            CONAIR = Path(임시)
            with tarfile.open(str(teilgean_fréamh / 'dist/jkoros-native-relink.tar.gz')) as Grúpa_VALUE:
                for iontráil_VALUE in Grúpa_VALUE.getmembers():
                    if CONAIR not in (CONAIR / iontráil_VALUE.name).resolve().parents or iontráil_VALUE.issym() or iontráil_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + iontráil_VALUE.name)
                Grúpa_VALUE.extractall(str(CONAIR))
            FOINSE = CONAIR / 'jkoros-native-relink'
            def 재연결(Ainm, 인수들):
                with (Aschur / Ainm).open('wb') as LOG_ró:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(FOINSE),
                                   stdout=LOG_ró, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            tuairisc_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = FOINSE / 'vendor/tinycc/libtcc.c'
            corpthéacs = 번역기.read_text()
            suíomh = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert corpthéacs.count(suíomh) == 1
            번역기.write_text(corpthéacs.replace(suíomh, suíomh + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Argóintí.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = FOINSE / 'build/relinked/kernel8.img'
            tuairisc_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert tuairisc_VALUE['modified_kernel_sha256'] != tuairisc_VALUE['kernel_sha256']
            tuairisc_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Ordú()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            Próiseas_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_ró = bytearray()
            roghnú_VALUE = selectors.DefaultSelector()
            roghnú_VALUE.register(Próiseas_VALUE.stdout, selectors.EVENT_READ)
            def 기다림(seó_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while seó_VALUE not in LOG_ró[처음:]:
                    if time.monotonic() > 끝 or Próiseas_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(seó_VALUE) + '\n' + LOG_ró[처음:].decode('utf-8', 'replace'))
                    for iontráil_VALUE, _ in roghnú_VALUE.select(.1):
                        sonraí = iontráil_VALUE.fileobj.read(65536)
                        if sonraí:
                            LOG_ró.extend(sonraí)
                return bytes(LOG_ró[처음:])
            def seol(Word_SMS, seó_VALUE=b'jkoros-native> '):
                처음 = len(LOG_ró)
                Próiseas_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Próiseas_VALUE.stdin.flush()
                return 기다림(seó_VALUE, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return scríobh_comhad_sonraí(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                seol('load /relink.c', b'hex> ')
                for suíomh_INDEX in range(0, len(시험), 64):
                    seol(시험[suíomh_INDEX:suíomh_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in seol('.')
                tomhas = seol('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in tomhas, tomhas
                tomhas = seol('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in tomhas and b'exit 0' in tomhas, tomhas
                tuairisc_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                roghnú_VALUE.close()
                if Próiseas_VALUE.poll() is None:
                    Próiseas_VALUE.terminate()
                    try:
                        Próiseas_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Próiseas_VALUE.kill()
                        Próiseas_VALUE.wait()
                (Aschur / 'guest.log').write_bytes(LOG_ró)
        tuairisc_VALUE['passed'] = True
        print(json.dumps(tuairisc_VALUE, ensure_ascii=False, indent=2))
    finally:
        (Aschur / 'report.json').write_text(json.dumps(tuairisc_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Rith_2()
