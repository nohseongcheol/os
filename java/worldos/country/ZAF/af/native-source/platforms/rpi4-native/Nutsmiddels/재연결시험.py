#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 werklik_data 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from uitvoer_bevel import Project_wortel, Opdrag


def Loop():
    ontleder_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ontleder_48ee4b1b.add_argument('--sdk', type=Path, default=Project_wortel.parent / 'rpi4/build/rootfs')
    인수 = ontleder_48ee4b1b.parse_args()
    Afvoer = Project_wortel / 'build/verification/cosl-relink'
    Afvoer.mkdir(parents=True, exist_ok=True)
    verslag_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_wortel / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Pad = Path(임시)
            with tarfile.open(str(Project_wortel / 'dist/jkoros-native-relink.tar.gz')) as Groep_VALUE:
                for inskrywing_VALUE in Groep_VALUE.getmembers():
                    if Pad not in (Pad / inskrywing_VALUE.name).resolve().parents or inskrywing_VALUE.issym() or inskrywing_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + inskrywing_VALUE.name)
                Groep_VALUE.extractall(str(Pad))
            Bron = Pad / 'jkoros-native-relink'
            def 재연결(Naam, 인수들):
                with (Afvoer / Naam).open('wb') as LOG_ry:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(Bron),
                                   stdout=LOG_ry, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            verslag_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = Bron / 'vendor/tinycc/libtcc.c'
            inhoudteks = 번역기.read_text()
            Posisie = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert inhoudteks.count(Posisie) == 1
            번역기.write_text(inhoudteks.replace(Posisie, Posisie + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            foto_VALUE = Bron / 'build/relinked/kernel8.img'
            verslag_VALUE['modified_kernel_sha256'] = hashlib.sha256(foto_VALUE.read_bytes()).hexdigest()
            assert verslag_VALUE['modified_kernel_sha256'] != verslag_VALUE['kernel_sha256']
            verslag_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Opdrag()
            인수들[인수들.index('-kernel') + 1] = str(foto_VALUE)
            Proses_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_ry = bytearray()
            seleksie_VALUE = selectors.DefaultSelector()
            seleksie_VALUE.register(Proses_VALUE.stdout, selectors.EVENT_READ)
            def wag_stand(wys_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while wys_VALUE not in LOG_ry[처음:]:
                    if time.monotonic() > 끝 or Proses_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(wys_VALUE) + '\n' + LOG_ry[처음:].decode('utf-8', 'replace'))
                    for inskrywing_VALUE, _ in seleksie_VALUE.select(.1):
                        data = inskrywing_VALUE.fileobj.read(65536)
                        if data:
                            LOG_ry.extend(data)
                return bytes(LOG_ry[처음:])
            def e_pos(Word_SMS, wys_VALUE=b'jkoros-native> '):
                처음 = len(LOG_ry)
                Proses_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Proses_VALUE.stdin.flush()
                return wag_stand(wys_VALUE, 처음)
            try:
                wag_stand()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return skryf_lêer_data(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                e_pos('load /relink.c', b'hex> ')
                for plaas_INDEX in range(0, len(시험), 64):
                    e_pos(시험[plaas_INDEX:plaas_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in e_pos('.')
                maatreël = e_pos('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in maatreël, maatreël
                maatreël = e_pos('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in maatreël and b'exit 0' in maatreël, maatreël
                verslag_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                seleksie_VALUE.close()
                if Proses_VALUE.poll() is None:
                    Proses_VALUE.terminate()
                    try:
                        Proses_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proses_VALUE.kill()
                        Proses_VALUE.wait()
                (Afvoer / 'guest.log').write_bytes(LOG_ry)
        verslag_VALUE['passed'] = True
        print(json.dumps(verslag_VALUE, ensure_ascii=False, indent=2))
    finally:
        (Afvoer / 'report.json').write_text(json.dumps(verslag_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Loop()
