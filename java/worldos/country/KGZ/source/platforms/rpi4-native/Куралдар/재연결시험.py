#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 актуалдуу_берилмелер 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from аткаруу_буйрук import 기준, Команда


def Жүргүзүү():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    Чыгыш = 기준 / 'build/verification/cosl-relink'
    Чыгыш.mkdir(parents=True, exist_ok=True)
    отчет_маани_ddf2aaf3 = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ЖОЛ = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as топ_маани:
                for киргизме_жазуу_маани in топ_маани.getmembers():
                    if ЖОЛ not in (ЖОЛ / киргизме_жазуу_маани.name).resolve().parents or киргизме_жазуу_маани.issym() or киргизме_жазуу_маани.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + киргизме_жазуу_маани.name)
                топ_маани.extractall(str(ЖОЛ))
            Булак = ЖОЛ / 'jkoros-native-relink'
            def 재연결(Аты, 인수들):
                with (Чыгыш / Аты).open('wb') as жазуу_катар:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(Булак),
                                   stdout=жазуу_катар, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            отчет_маани_ddf2aaf3['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = Булак / 'vendor/tinycc/libtcc.c'
            негизги_текст = 번역기.read_text()
            Турган_жери = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert негизги_текст.count(Турган_жери) == 1
            번역기.write_text(негизги_текст.replace(Турган_жери, Турган_жери + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            сүрөт_маани = Булак / 'build/relinked/kernel8.img'
            отчет_маани_ddf2aaf3['modified_kernel_sha256'] = hashlib.sha256(сүрөт_маани.read_bytes()).hexdigest()
            assert отчет_маани_ddf2aaf3['modified_kernel_sha256'] != отчет_маани_ddf2aaf3['kernel_sha256']
            отчет_маани_ddf2aaf3['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Команда()
            인수들[인수들.index('-kernel') + 1] = str(сүрөт_маани)
            Процесс_маани = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            жазуу_катар = bytearray()
            белгилөө_маани = selectors.DefaultSelector()
            белгилөө_маани.register(Процесс_маани.stdout, selectors.EVENT_READ)
            def 기다림(көрсөтүү_маани=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while көрсөтүү_маани not in жазуу_катар[처음:]:
                    if time.monotonic() > 끝 or Процесс_маани.poll() is not None:
                        raise AssertionError('Missing ' + repr(көрсөтүү_маани) + '\n' + жазуу_катар[처음:].decode('utf-8', 'replace'))
                    for киргизме_жазуу_маани, _ in белгилөө_маани.select(.1):
                        берилмелер = киргизме_жазуу_маани.fileobj.read(65536)
                        if берилмелер:
                            жазуу_катар.extend(берилмелер)
                return bytes(жазуу_катар[처음:])
            def жөнөтүү(Сөз_СМС, көрсөтүү_маани=b'jkoros-native> '):
                처음 = len(жазуу_катар)
                Процесс_маани.stdin.write(Сөз_СМС.encode() + b'\n')
                Процесс_маани.stdin.flush()
                return 기다림(көрсөтүү_маани, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return жазуу_файл_берилмелер(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                жөнөтүү('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    жөнөтүү(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in жөнөтүү('.')
                결과 = жөнөтүү('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = жөнөтүү('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                отчет_маани_ddf2aaf3['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                белгилөө_маани.close()
                if Процесс_маани.poll() is None:
                    Процесс_маани.terminate()
                    try:
                        Процесс_маани.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Процесс_маани.kill()
                        Процесс_маани.wait()
                (Чыгыш / 'guest.log').write_bytes(жазуу_катар)
        отчет_маани_ddf2aaf3['passed'] = True
        print(json.dumps(отчет_маани_ddf2aaf3, ensure_ascii=False, indent=2))
    finally:
        (Чыгыш / 'report.json').write_text(json.dumps(отчет_маани_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Жүргүзүү()
