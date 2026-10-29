#!/usr/bin/env python3
"""paskirstymas_VALUE 자료만으로 LGPL 재연결과 수정한 TinyCC의 faktinis_duomenys 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Vykdyti_komanda import Project_šaknis, Komanda


def Paleisti():
    analizatorius_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatorius_48ee4b1b.add_argument('--sdk', type=Path, default=Project_šaknis.parent / 'rpi4/build/rootfs')
    Argumentai = analizatorius_48ee4b1b.parse_args()
    Išvestis = Project_šaknis / 'build/verification/cosl-relink'
    Išvestis.mkdir(parents=True, exist_ok=True)
    pranešti_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_šaknis / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            KELIAS = Path(임시)
            with tarfile.open(str(Project_šaknis / 'dist/jkoros-native-relink.tar.gz')) as Grupė_VALUE:
                for įrašas_VALUE in Grupė_VALUE.getmembers():
                    if KELIAS not in (KELIAS / įrašas_VALUE.name).resolve().parents or įrašas_VALUE.issym() or įrašas_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + įrašas_VALUE.name)
                Grupė_VALUE.extractall(str(KELIAS))
            ŠALTINIS = KELIAS / 'jkoros-native-relink'
            def 재연결(Pavadinimas_2, 인수들):
                with (Išvestis / Pavadinimas_2).open('wb') as LOG_RECORD:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ŠALTINIS),
                                   stdout=LOG_RECORD, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            pranešti_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            kompiliatorius_įrankis = ŠALTINIS / 'vendor/tinycc/libtcc.c'
            pagrindinis_tekstas = kompiliatorius_įrankis.read_text()
            Pozicija = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert pagrindinis_tekstas.count(Pozicija) == 1
            kompiliatorius_įrankis.write_text(pagrindinis_tekstas.replace(Pozicija, Pozicija + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Argumentai.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = ŠALTINIS / 'build/relinked/kernel8.img'
            pranešti_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert pranešti_VALUE['modified_kernel_sha256'] != pranešti_VALUE['kernel_sha256']
            pranešti_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Komanda()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            Procesas_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_RECORD = bytearray()
            žymėjimas_VALUE = selectors.DefaultSelector()
            žymėjimas_VALUE.register(Procesas_VALUE.stdout, selectors.EVENT_READ)
            def laukimo_būsena(laida_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while laida_VALUE not in LOG_RECORD[처음:]:
                    if time.monotonic() > 끝 or Procesas_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(laida_VALUE) + '\n' + LOG_RECORD[처음:].decode('utf-8', 'replace'))
                    for įrašas_VALUE, _ in žymėjimas_VALUE.select(.1):
                        duomenys = įrašas_VALUE.fileobj.read(65536)
                        if duomenys:
                            LOG_RECORD.extend(duomenys)
                return bytes(LOG_RECORD[처음:])
            def siųsti(Word_SMS, laida_VALUE=b'jkoros-native> '):
                처음 = len(LOG_RECORD)
                Procesas_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Procesas_VALUE.stdin.flush()
                return laukimo_būsena(laida_VALUE, 처음)
            try:
                laukimo_būsena()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return rašymas_Failas_duomenys(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                siųsti('load /relink.c', b'hex> ')
                for vietos_rodyklė in range(0, len(시험), 64):
                    siųsti(시험[vietos_rodyklė:vietos_rodyklė+64].hex(), b'hex> ')
                assert b'LOADED' in siųsti('.')
                REZULTATAS = siųsti('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in REZULTATAS, REZULTATAS
                REZULTATAS = siųsti('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in REZULTATAS and b'exit 0' in REZULTATAS, REZULTATAS
                pranešti_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                žymėjimas_VALUE.close()
                if Procesas_VALUE.poll() is None:
                    Procesas_VALUE.terminate()
                    try:
                        Procesas_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Procesas_VALUE.kill()
                        Procesas_VALUE.wait()
                (Išvestis / 'guest.log').write_bytes(LOG_RECORD)
        pranešti_VALUE['passed'] = True
        print(json.dumps(pranešti_VALUE, ensure_ascii=False, indent=2))
    finally:
        (Išvestis / 'report.json').write_text(json.dumps(pranešti_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Paleisti()
