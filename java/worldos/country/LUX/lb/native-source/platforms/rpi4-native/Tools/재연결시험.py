#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 aktuell_Daten 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from ausféieren_Befeel import projezéieren_Racinn, Befeel


def Laf():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=projezéieren_Racinn.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = projezéieren_Racinn / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    mellen_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((projezéieren_Racinn / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Wee = Path(임시)
            with tarfile.open(str(projezéieren_Racinn / 'dist/jkoros-native-relink.tar.gz')) as Grupp_VALUE:
                for Agab_VALUE in Grupp_VALUE.getmembers():
                    if Wee not in (Wee / Agab_VALUE.name).resolve().parents or Agab_VALUE.issym() or Agab_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + Agab_VALUE.name)
                Grupp_VALUE.extractall(str(Wee))
            Quell = Wee / 'jkoros-native-relink'
            def 재연결(Numm, 인수들):
                with (출력 / Numm).open('wb') as LOG_Rei:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(Quell),
                                   stdout=LOG_Rei, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            mellen_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = Quell / 'vendor/tinycc/libtcc.c'
            Textkierper = 번역기.read_text()
            positionéieren = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert Textkierper.count(positionéieren) == 1
            번역기.write_text(Textkierper.replace(positionéieren, positionéieren + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            Bild_VALUE = Quell / 'build/relinked/kernel8.img'
            mellen_VALUE['modified_kernel_sha256'] = hashlib.sha256(Bild_VALUE.read_bytes()).hexdigest()
            assert mellen_VALUE['modified_kernel_sha256'] != mellen_VALUE['kernel_sha256']
            mellen_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Befeel()
            인수들[인수들.index('-kernel') + 1] = str(Bild_VALUE)
            Prozess_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_Rei = bytearray()
            Auswiel_VALUE = selectors.DefaultSelector()
            Auswiel_VALUE.register(Prozess_VALUE.stdout, selectors.EVENT_READ)
            def Waart_Status(Show_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while Show_VALUE not in LOG_Rei[처음:]:
                    if time.monotonic() > 끝 or Prozess_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(Show_VALUE) + '\n' + LOG_Rei[처음:].decode('utf-8', 'replace'))
                    for Agab_VALUE, _ in Auswiel_VALUE.select(.1):
                        Daten = Agab_VALUE.fileobj.read(65536)
                        if Daten:
                            LOG_Rei.extend(Daten)
                return bytes(LOG_Rei[처음:])
            def mailen(Word_SMS, Show_VALUE=b'jkoros-native> '):
                처음 = len(LOG_Rei)
                Prozess_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Prozess_VALUE.stdin.flush()
                return Waart_Status(Show_VALUE, 처음)
            try:
                Waart_Status()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return schreiwen_Fichier_Daten(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                mailen('load /relink.c', b'hex> ')
                for positionéieren_INDEX in range(0, len(시험), 64):
                    mailen(시험[positionéieren_INDEX:positionéieren_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in mailen('.')
                Mooss = mailen('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in Mooss, Mooss
                Mooss = mailen('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in Mooss and b'exit 0' in Mooss, Mooss
                mellen_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                Auswiel_VALUE.close()
                if Prozess_VALUE.poll() is None:
                    Prozess_VALUE.terminate()
                    try:
                        Prozess_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Prozess_VALUE.kill()
                        Prozess_VALUE.wait()
                (출력 / 'guest.log').write_bytes(LOG_Rei)
        mellen_VALUE['passed'] = True
        print(json.dumps(mellen_VALUE, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(mellen_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Laf()
