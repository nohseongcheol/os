#!/usr/bin/env python3
"""elosztás_ÉRTÉK 자료만으로 LGPL 재연결과 수정한 TinyCC의 tényleges_adat 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from végrehajt_parancs import teendő_gyök, Parancs


def Futtatás():
    elemző_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    elemző_48ee4b1b.add_argument('--sdk', type=Path, default=teendő_gyök.parent / 'rpi4/build/rootfs')
    Argumentumok = elemző_48ee4b1b.parse_args()
    Kimenet = teendő_gyök / 'build/verification/cosl-relink'
    Kimenet.mkdir(parents=True, exist_ok=True)
    jelent_ÉRTÉK = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((teendő_gyök / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ÚTVONAL = Path(임시)
            with tarfile.open(str(teendő_gyök / 'dist/jkoros-native-relink.tar.gz')) as Csoport_ÉRTÉK:
                for bejegyzés_ÉRTÉK in Csoport_ÉRTÉK.getmembers():
                    if ÚTVONAL not in (ÚTVONAL / bejegyzés_ÉRTÉK.name).resolve().parents or bejegyzés_ÉRTÉK.issym() or bejegyzés_ÉRTÉK.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + bejegyzés_ÉRTÉK.name)
                Csoport_ÉRTÉK.extractall(str(ÚTVONAL))
            FORRÁS = ÚTVONAL / 'jkoros-native-relink'
            def 재연결(Név, 인수들):
                with (Kimenet / Név).open('wb') as LOG_REKORD:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(FORRÁS),
                                   stdout=LOG_REKORD, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            jelent_ÉRTÉK['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            fordítóprogram_eszköz = FORRÁS / 'vendor/tinycc/libtcc.c'
            törzsszöveg = fordítóprogram_eszköz.read_text()
            Pozíció = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert törzsszöveg.count(Pozíció) == 1
            fordítóprogram_eszköz.write_text(törzsszöveg.replace(Pozíció, Pozíció + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Argumentumok.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            KÉP_ÉRTÉK = FORRÁS / 'build/relinked/kernel8.img'
            jelent_ÉRTÉK['modified_kernel_sha256'] = hashlib.sha256(KÉP_ÉRTÉK.read_bytes()).hexdigest()
            assert jelent_ÉRTÉK['modified_kernel_sha256'] != jelent_ÉRTÉK['kernel_sha256']
            jelent_ÉRTÉK['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Parancs()
            인수들[인수들.index('-kernel') + 1] = str(KÉP_ÉRTÉK)
            folyamat_ÉRTÉK = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_REKORD = bytearray()
            kijelölés_ÉRTÉK = selectors.DefaultSelector()
            kijelölés_ÉRTÉK.register(folyamat_ÉRTÉK.stdout, selectors.EVENT_READ)
            def várakozóállapot(bemutató_ÉRTÉK=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while bemutató_ÉRTÉK not in LOG_REKORD[처음:]:
                    if time.monotonic() > 끝 or folyamat_ÉRTÉK.poll() is not None:
                        raise AssertionError('Missing ' + repr(bemutató_ÉRTÉK) + '\n' + LOG_REKORD[처음:].decode('utf-8', 'replace'))
                    for bejegyzés_ÉRTÉK, _ in kijelölés_ÉRTÉK.select(.1):
                        adat = bejegyzés_ÉRTÉK.fileobj.read(65536)
                        if adat:
                            LOG_REKORD.extend(adat)
                return bytes(LOG_REKORD[처음:])
            def küld(szó_SMS, bemutató_ÉRTÉK=b'jkoros-native> '):
                처음 = len(LOG_REKORD)
                folyamat_ÉRTÉK.stdin.write(szó_SMS.encode() + b'\n')
                folyamat_ÉRTÉK.stdin.flush()
                return várakozóállapot(bemutató_ÉRTÉK, 처음)
            try:
                várakozóállapot()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ír_Fájl_adat(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                küld('load /relink.c', b'hex> ')
                for helyzetindex in range(0, len(시험), 64):
                    küld(시험[helyzetindex:helyzetindex+64].hex(), b'hex> ')
                assert b'LOADED' in küld('.')
                KR = küld('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in KR, KR
                KR = küld('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in KR and b'exit 0' in KR, KR
                jelent_ÉRTÉK['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                kijelölés_ÉRTÉK.close()
                if folyamat_ÉRTÉK.poll() is None:
                    folyamat_ÉRTÉK.terminate()
                    try:
                        folyamat_ÉRTÉK.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        folyamat_ÉRTÉK.kill()
                        folyamat_ÉRTÉK.wait()
                (Kimenet / 'guest.log').write_bytes(LOG_REKORD)
        jelent_ÉRTÉK['passed'] = True
        print(json.dumps(jelent_ÉRTÉK, ensure_ascii=False, indent=2))
    finally:
        (Kimenet / 'report.json').write_text(json.dumps(jelent_ÉRTÉK, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Futtatás()
