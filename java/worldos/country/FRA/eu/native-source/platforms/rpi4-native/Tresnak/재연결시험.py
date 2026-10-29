#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 benetako_datuak 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from exekutatu_komando import Project_erro, Komandoa


def Exekutatu_2():
    analizatzaile_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatzaile_48ee4b1b.add_argument('--sdk', type=Path, default=Project_erro.parent / 'rpi4/build/rootfs')
    Argumentuak = analizatzaile_48ee4b1b.parse_args()
    Irteera = Project_erro / 'build/verification/cosl-relink'
    Irteera.mkdir(parents=True, exist_ok=True)
    txosten_balio = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_erro / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Bide_izena = Path(임시)
            with tarfile.open(str(Project_erro / 'dist/jkoros-native-relink.tar.gz')) as talde_balio:
                for sarrera_balio in talde_balio.getmembers():
                    if Bide_izena not in (Bide_izena / sarrera_balio.name).resolve().parents or sarrera_balio.issym() or sarrera_balio.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + sarrera_balio.name)
                talde_balio.extractall(str(Bide_izena))
            ITURBURUA = Bide_izena / 'jkoros-native-relink'
            def 재연결(Izena, 인수들):
                with (Irteera / Izena).open('wb') as LOG_marka:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ITURBURUA),
                                   stdout=LOG_marka, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            txosten_balio['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ITURBURUA / 'vendor/tinycc/libtcc.c'
            testu_nagusi = 번역기.read_text()
            Posizioa = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert testu_nagusi.count(Posizioa) == 1
            번역기.write_text(testu_nagusi.replace(Posizioa, Posizioa + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Argumentuak.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            irudi_balio = ITURBURUA / 'build/relinked/kernel8.img'
            txosten_balio['modified_kernel_sha256'] = hashlib.sha256(irudi_balio.read_bytes()).hexdigest()
            assert txosten_balio['modified_kernel_sha256'] != txosten_balio['kernel_sha256']
            txosten_balio['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Komandoa()
            인수들[인수들.index('-kernel') + 1] = str(irudi_balio)
            prozesu_balio = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_marka = bytearray()
            hautapen_balio = selectors.DefaultSelector()
            hautapen_balio.register(prozesu_balio.stdout, selectors.EVENT_READ)
            def itxaron_Egoera(erakutsi_balio=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while erakutsi_balio not in LOG_marka[처음:]:
                    if time.monotonic() > 끝 or prozesu_balio.poll() is not None:
                        raise AssertionError('Missing ' + repr(erakutsi_balio) + '\n' + LOG_marka[처음:].decode('utf-8', 'replace'))
                    for sarrera_balio, _ in hautapen_balio.select(.1):
                        datuak = sarrera_balio.fileobj.read(65536)
                        if datuak:
                            LOG_marka.extend(datuak)
                return bytes(LOG_marka[처음:])
            def bidali(Word_SMS, erakutsi_balio=b'jkoros-native> '):
                처음 = len(LOG_marka)
                prozesu_balio.stdin.write(Word_SMS.encode() + b'\n')
                prozesu_balio.stdin.flush()
                return itxaron_Egoera(erakutsi_balio, 처음)
            try:
                itxaron_Egoera()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return idatzi_fitxategi_datuak(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                bidali('load /relink.c', b'hex> ')
                for kargu_INDIZE in range(0, len(시험), 64):
                    bidali(시험[kargu_INDIZE:kargu_INDIZE+64].hex(), b'hex> ')
                assert b'LOADED' in bidali('.')
                EMAITZA = bidali('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in EMAITZA, EMAITZA
                EMAITZA = bidali('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in EMAITZA and b'exit 0' in EMAITZA, EMAITZA
                txosten_balio['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                hautapen_balio.close()
                if prozesu_balio.poll() is None:
                    prozesu_balio.terminate()
                    try:
                        prozesu_balio.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        prozesu_balio.kill()
                        prozesu_balio.wait()
                (Irteera / 'guest.log').write_bytes(LOG_marka)
        txosten_balio['passed'] = True
        print(json.dumps(txosten_balio, ensure_ascii=False, indent=2))
    finally:
        (Irteera / 'report.json').write_text(json.dumps(txosten_balio, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Exekutatu_2()
