#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 faktisk_data 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Utfør_kommando import spegle_rot, Kommando


def Køyr_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=spegle_rot.parent / 'rpi4/build/rootfs')
    Argument = 해석기.parse_args()
    Utdata = spegle_rot / 'build/verification/cosl-relink'
    Utdata.mkdir(parents=True, exist_ok=True)
    rapport_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((spegle_rot / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            STIGE = Path(임시)
            with tarfile.open(str(spegle_rot / 'dist/jkoros-native-relink.tar.gz')) as gruppe_VALUE:
                for oppføring_VALUE in gruppe_VALUE.getmembers():
                    if STIGE not in (STIGE / oppføring_VALUE.name).resolve().parents or oppføring_VALUE.issym() or oppføring_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + oppføring_VALUE.name)
                gruppe_VALUE.extractall(str(STIGE))
            KJELDE = STIGE / 'jkoros-native-relink'
            def 재연결(Namn, 인수들):
                with (Utdata / Namn).open('wb') as LOG_rad:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(KJELDE),
                                   stdout=LOG_rad, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            rapport_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = KJELDE / 'vendor/tinycc/libtcc.c'
            brødtekst = 번역기.read_text()
            Posisjon = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert brødtekst.count(Posisjon) == 1
            번역기.write_text(brødtekst.replace(Posisjon, Posisjon + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Argument.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = KJELDE / 'build/relinked/kernel8.img'
            rapport_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert rapport_VALUE['modified_kernel_sha256'] != rapport_VALUE['kernel_sha256']
            rapport_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Kommando()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            Prosess_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_rad = bytearray()
            merkt_område_VALUE = selectors.DefaultSelector()
            merkt_område_VALUE.register(Prosess_VALUE.stdout, selectors.EVENT_READ)
            def vent_status(vise_VALUE_487749b8=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while vise_VALUE_487749b8 not in LOG_rad[처음:]:
                    if time.monotonic() > 끝 or Prosess_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(vise_VALUE_487749b8) + '\n' + LOG_rad[처음:].decode('utf-8', 'replace'))
                    for oppføring_VALUE, _ in merkt_område_VALUE.select(.1):
                        data = oppføring_VALUE.fileobj.read(65536)
                        if data:
                            LOG_rad.extend(data)
                return bytes(LOG_rad[처음:])
            def sende(Word_SMS, vise_VALUE_487749b8=b'jkoros-native> '):
                처음 = len(LOG_rad)
                Prosess_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Prosess_VALUE.stdin.flush()
                return vent_status(vise_VALUE_487749b8, 처음)
            try:
                vent_status()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return skrive_fil_data(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                sende('load /relink.c', b'hex> ')
                for plassere_INDEX in range(0, len(시험), 64):
                    sende(시험[plassere_INDEX:plassere_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in sende('.')
                forretningsmål = sende('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in forretningsmål, forretningsmål
                forretningsmål = sende('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in forretningsmål and b'exit 0' in forretningsmål, forretningsmål
                rapport_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                merkt_område_VALUE.close()
                if Prosess_VALUE.poll() is None:
                    Prosess_VALUE.terminate()
                    try:
                        Prosess_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Prosess_VALUE.kill()
                        Prosess_VALUE.wait()
                (Utdata / 'guest.log').write_bytes(LOG_rad)
        rapport_VALUE['passed'] = True
        print(json.dumps(rapport_VALUE, ensure_ascii=False, indent=2))
    finally:
        (Utdata / 'report.json').write_text(json.dumps(rapport_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Køyr_2()
