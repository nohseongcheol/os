#!/usr/bin/env python3
"""turustus_VALUE 자료만으로 LGPL 재연결과 수정한 TinyCC의 tegelik_andmed 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Täida_käsk import Project_juur, Käsk


def Käivita_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--sdk', type=Path, default=Project_juur.parent / 'rpi4/build/rootfs')
    Argumendid = parser_48ee4b1b.parse_args()
    Väljund = Project_juur / 'build/verification/cosl-relink'
    Väljund.mkdir(parents=True, exist_ok=True)
    aruanne_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_juur / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            RADA = Path(임시)
            with tarfile.open(str(Project_juur / 'dist/jkoros-native-relink.tar.gz')) as Rühm_VALUE:
                for kirje_VALUE in Rühm_VALUE.getmembers():
                    if RADA not in (RADA / kirje_VALUE.name).resolve().parents or kirje_VALUE.issym() or kirje_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + kirje_VALUE.name)
                Rühm_VALUE.extractall(str(RADA))
            ALLIKAS = RADA / 'jkoros-native-relink'
            def 재연결(Nimi_2, 인수들):
                with (Väljund / Nimi_2).open('wb') as LOG_kirje:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ALLIKAS),
                                   stdout=LOG_kirje, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            aruanne_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            kompilaator_tööriist = ALLIKAS / 'vendor/tinycc/libtcc.c'
            sisu_SMS = kompilaator_tööriist.read_text()
            Asukoht = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert sisu_SMS.count(Asukoht) == 1
            kompilaator_tööriist.write_text(sisu_SMS.replace(Asukoht, Asukoht + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Argumendid.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            pilt_VALUE = ALLIKAS / 'build/relinked/kernel8.img'
            aruanne_VALUE['modified_kernel_sha256'] = hashlib.sha256(pilt_VALUE.read_bytes()).hexdigest()
            assert aruanne_VALUE['modified_kernel_sha256'] != aruanne_VALUE['kernel_sha256']
            aruanne_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Käsk()
            인수들[인수들.index('-kernel') + 1] = str(pilt_VALUE)
            Joonis_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_kirje = bytearray()
            valim_VALUE = selectors.DefaultSelector()
            valim_VALUE.register(Joonis_VALUE.stdout, selectors.EVENT_READ)
            def ooteolek(saade_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while saade_VALUE not in LOG_kirje[처음:]:
                    if time.monotonic() > 끝 or Joonis_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(saade_VALUE) + '\n' + LOG_kirje[처음:].decode('utf-8', 'replace'))
                    for kirje_VALUE, _ in valim_VALUE.select(.1):
                        andmed = kirje_VALUE.fileobj.read(65536)
                        if andmed:
                            LOG_kirje.extend(andmed)
                return bytes(LOG_kirje[처음:])
            def saatma(Word_SMS, saade_VALUE=b'jkoros-native> '):
                처음 = len(LOG_kirje)
                Joonis_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Joonis_VALUE.stdin.flush()
                return ooteolek(saade_VALUE, 처음)
            try:
                ooteolek()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return kirjutamine_Fail_andmed(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                saatma('load /relink.c', b'hex> ')
                for asukohaindeks in range(0, len(시험), 64):
                    saatma(시험[asukohaindeks:asukohaindeks+64].hex(), b'hex> ')
                assert b'LOADED' in saatma('.')
                TULEMUS = saatma('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in TULEMUS, TULEMUS
                TULEMUS = saatma('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in TULEMUS and b'exit 0' in TULEMUS, TULEMUS
                aruanne_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                valim_VALUE.close()
                if Joonis_VALUE.poll() is None:
                    Joonis_VALUE.terminate()
                    try:
                        Joonis_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Joonis_VALUE.kill()
                        Joonis_VALUE.wait()
                (Väljund / 'guest.log').write_bytes(LOG_kirje)
        aruanne_VALUE['passed'] = True
        print(json.dumps(aruanne_VALUE, ensure_ascii=False, indent=2))
    finally:
        (Väljund / 'report.json').write_text(json.dumps(aruanne_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Käivita_2()
