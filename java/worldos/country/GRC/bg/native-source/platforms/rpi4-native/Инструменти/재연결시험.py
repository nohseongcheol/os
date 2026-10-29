#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 действителен_данни 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from изпълнявам_команда import проект_корен, Команда


def Стартиране():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--sdk', type=Path, default=проект_корен.parent / 'rpi4/build/rootfs')
    Параметри = анализатор_48ee4b1b.parse_args()
    Изход = проект_корен / 'build/verification/cosl-relink'
    Изход.mkdir(parents=True, exist_ok=True)
    отчет_стойност = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((проект_корен / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ПЪТ = Path(임시)
            with tarfile.open(str(проект_корен / 'dist/jkoros-native-relink.tar.gz')) as Група_стойност:
                for запис_стойност in Група_стойност.getmembers():
                    if ПЪТ not in (ПЪТ / запис_стойност.name).resolve().parents or запис_стойност.issym() or запис_стойност.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + запис_стойност.name)
                Група_стойност.extractall(str(ПЪТ))
            ИЗТОЧНИК = ПЪТ / 'jkoros-native-relink'
            def 재연결(Име, 인수들):
                with (Изход / Име).open('wb') as регистрирам_запис:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ИЗТОЧНИК),
                                   stdout=регистрирам_запис, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            отчет_стойност['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            компилатор_инструмент = ИЗТОЧНИК / 'vendor/tinycc/libtcc.c'
            основен_текст = компилатор_инструмент.read_text()
            Позиция = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert основен_текст.count(Позиция) == 1
            компилатор_инструмент.write_text(основен_текст.replace(Позиция, Позиция + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Параметри.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            снимка_стойност = ИЗТОЧНИК / 'build/relinked/kernel8.img'
            отчет_стойност['modified_kernel_sha256'] = hashlib.sha256(снимка_стойност.read_bytes()).hexdigest()
            assert отчет_стойност['modified_kernel_sha256'] != отчет_стойност['kernel_sha256']
            отчет_стойност['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Команда()
            인수들[인수들.index('-kernel') + 1] = str(снимка_стойност)
            Процес_стойност = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            регистрирам_запис = bytearray()
            избор_стойност = selectors.DefaultSelector()
            избор_стойност.register(Процес_стойност.stdout, selectors.EVENT_READ)
            def състояние_на_изчакване(показвам_стойност=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while показвам_стойност not in регистрирам_запис[처음:]:
                    if time.monotonic() > 끝 or Процес_стойност.poll() is not None:
                        raise AssertionError('Missing ' + repr(показвам_стойност) + '\n' + регистрирам_запис[처음:].decode('utf-8', 'replace'))
                    for запис_стойност, _ in избор_стойност.select(.1):
                        данни = запис_стойност.fileobj.read(65536)
                        if данни:
                            регистрирам_запис.extend(данни)
                return bytes(регистрирам_запис[처음:])
            def изпращам(Игри_с_думи_Текст, показвам_стойност=b'jkoros-native> '):
                처음 = len(регистрирам_запис)
                Процес_стойност.stdin.write(Игри_с_думи_Текст.encode() + b'\n')
                Процес_стойност.stdin.flush()
                return състояние_на_изчакване(показвам_стойност, 처음)
            try:
                състояние_на_изчакване()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return записване_Файл_данни(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                изпращам('load /relink.c', b'hex> ')
                for позиционен_указател in range(0, len(시험), 64):
                    изпращам(시험[позиционен_указател:позиционен_указател+64].hex(), b'hex> ')
                assert b'LOADED' in изпращам('.')
                РЕЗУЛТАТ = изпращам('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in РЕЗУЛТАТ, РЕЗУЛТАТ
                РЕЗУЛТАТ = изпращам('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in РЕЗУЛТАТ and b'exit 0' in РЕЗУЛТАТ, РЕЗУЛТАТ
                отчет_стойност['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                избор_стойност.close()
                if Процес_стойност.poll() is None:
                    Процес_стойност.terminate()
                    try:
                        Процес_стойност.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Процес_стойност.kill()
                        Процес_стойност.wait()
                (Изход / 'guest.log').write_bytes(регистрирам_запис)
        отчет_стойност['passed'] = True
        print(json.dumps(отчет_стойност, ensure_ascii=False, indent=2))
    finally:
        (Изход / 'report.json').write_text(json.dumps(отчет_стойност, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Стартиране()
