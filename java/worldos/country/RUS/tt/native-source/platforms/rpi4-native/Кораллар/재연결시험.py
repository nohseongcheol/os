#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 фактик_мәгълүмат 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from үтәргә_команда import экранга_җибәрү_тамыр, команда


def эшләтү():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=экранга_җибәрү_тамыр.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = экранга_җибәрү_тамыр / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    отчет_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((экранга_җибәрү_тамыр / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Yul = Path(임시)
            with tarfile.open(str(экранга_җибәрү_тамыр / 'dist/jkoros-native-relink.tar.gz')) as төркем_VALUE:
                for кертү_VALUE in төркем_VALUE.getmembers():
                    if Yul not in (Yul / кертү_VALUE.name).resolve().parents or кертү_VALUE.issym() or кертү_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + кертү_VALUE.name)
                төркем_VALUE.extractall(str(Yul))
            чыганак = Yul / 'jkoros-native-relink'
            def 재연결(исем, 인수들):
                with (출력 / исем).open('wb') as LOG_юл:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(чыганак),
                                   stdout=LOG_юл, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            отчет_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = чыганак / 'vendor/tinycc/libtcc.c'
            төп_текст = 번역기.read_text()
            урнаштыру = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert төп_текст.count(урнаштыру) == 1
            번역기.write_text(төп_текст.replace(урнаштыру, урнаштыру + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = чыганак / 'build/relinked/kernel8.img'
            отчет_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert отчет_VALUE['modified_kernel_sha256'] != отчет_VALUE['kernel_sha256']
            отчет_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = команда()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            Процесс_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_юл = bytearray()
            тамгаланган_өлеш_VALUE = selectors.DefaultSelector()
            тамгаланган_өлеш_VALUE.register(Процесс_VALUE.stdout, selectors.EVENT_READ)
            def 기다림(күрсәтү_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while күрсәтү_VALUE not in LOG_юл[처음:]:
                    if time.monotonic() > 끝 or Процесс_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(күрсәтү_VALUE) + '\n' + LOG_юл[처음:].decode('utf-8', 'replace'))
                    for кертү_VALUE, _ in тамгаланган_өлеш_VALUE.select(.1):
                        мәгълүмат = кертү_VALUE.fileobj.read(65536)
                        if мәгълүмат:
                            LOG_юл.extend(мәгълүмат)
                return bytes(LOG_юл[처음:])
            def җибәрү(Word_СМС, күрсәтү_VALUE=b'jkoros-native> '):
                처음 = len(LOG_юл)
                Процесс_VALUE.stdin.write(Word_СМС.encode() + b'\n')
                Процесс_VALUE.stdin.flush()
                return 기다림(күрсәтү_VALUE, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return язу_файл_мәгълүмат(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                җибәрү('load /relink.c', b'hex> ')
                for урнаштыру_INDEX in range(0, len(시험), 64):
                    җибәрү(시험[урнаштыру_INDEX:урнаштыру_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in җибәрү('.')
                үлчәм = җибәрү('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in үлчәм, үлчәм
                үлчәм = җибәрү('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in үлчәм and b'exit 0' in үлчәм, үлчәм
                отчет_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                тамгаланган_өлеш_VALUE.close()
                if Процесс_VALUE.poll() is None:
                    Процесс_VALUE.terminate()
                    try:
                        Процесс_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Процесс_VALUE.kill()
                        Процесс_VALUE.wait()
                (출력 / 'guest.log').write_bytes(LOG_юл)
        отчет_VALUE['passed'] = True
        print(json.dumps(отчет_VALUE, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(отчет_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    эшләтү()
