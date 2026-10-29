#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 totoo_data 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Mag_execute_utos import Project_root, utos


def run():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--sdk', type=Path, default=Project_root.parent / 'rpi4/build/rootfs')
    인수 = parser_48ee4b1b.parse_args()
    출력 = Project_root / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    ulat_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_root / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            path = Path(임시)
            with tarfile.open(str(Project_root / 'dist/jkoros-native-relink.tar.gz')) as Grupo_VALUE:
                for pagpasok_VALUE in Grupo_VALUE.getmembers():
                    if path not in (path / pagpasok_VALUE.name).resolve().parents or pagpasok_VALUE.issym() or pagpasok_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + pagpasok_VALUE.name)
                Grupo_VALUE.extractall(str(path))
            pinagmulan = path / 'jkoros-native-relink'
            def 재연결(pangalan, 인수들):
                with (출력 / pangalan).open('wb') as LOG_hanay:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(pinagmulan),
                                   stdout=LOG_hanay, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            ulat_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = pinagmulan / 'vendor/tinycc/libtcc.c'
            teksto_ng_nilalaman = 번역기.read_text()
            posisyon = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert teksto_ng_nilalaman.count(posisyon) == 1
            번역기.write_text(teksto_ng_nilalaman.replace(posisyon, posisyon + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = pinagmulan / 'build/relinked/kernel8.img'
            ulat_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert ulat_VALUE['modified_kernel_sha256'] != ulat_VALUE['kernel_sha256']
            ulat_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = utos()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            Proseso_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_hanay = bytearray()
            seleksyon_VALUE = selectors.DefaultSelector()
            seleksyon_VALUE.register(Proseso_VALUE.stdout, selectors.EVENT_READ)
            def maghintay_katayuan(ipakita_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while ipakita_VALUE not in LOG_hanay[처음:]:
                    if time.monotonic() > 끝 or Proseso_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(ipakita_VALUE) + '\n' + LOG_hanay[처음:].decode('utf-8', 'replace'))
                    for pagpasok_VALUE, _ in seleksyon_VALUE.select(.1):
                        data = pagpasok_VALUE.fileobj.read(65536)
                        if data:
                            LOG_hanay.extend(data)
                return bytes(LOG_hanay[처음:])
            def i_email(Word_SMS, ipakita_VALUE=b'jkoros-native> '):
                처음 = len(LOG_hanay)
                Proseso_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Proseso_VALUE.stdin.flush()
                return maghintay_katayuan(ipakita_VALUE, 처음)
            try:
                maghintay_katayuan()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return sumulat_file_data(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                i_email('load /relink.c', b'hex> ')
                for posisyon_INDEX in range(0, len(시험), 64):
                    i_email(시험[posisyon_INDEX:posisyon_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in i_email('.')
                sukat = i_email('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in sukat, sukat
                sukat = i_email('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in sukat and b'exit 0' in sukat, sukat
                ulat_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                seleksyon_VALUE.close()
                if Proseso_VALUE.poll() is None:
                    Proseso_VALUE.terminate()
                    try:
                        Proseso_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proseso_VALUE.kill()
                        Proseso_VALUE.wait()
                (출력 / 'guest.log').write_bytes(LOG_hanay)
        ulat_VALUE['passed'] = True
        print(json.dumps(ulat_VALUE, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(ulat_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    run()
