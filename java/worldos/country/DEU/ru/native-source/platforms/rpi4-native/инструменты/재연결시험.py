#!/usr/bin/env python3
"""распределение_ЗНАЧЕН 자료만으로 LGPL 재연결과 수정한 TinyCC의 фактический_данные 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from 실행 import задача_корень, команда


def запустить():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--sdk', type=Path, default=задача_корень.parent / 'rpi4/build/rootfs')
    аргументы = анализатор_48ee4b1b.parse_args()
    текстовыйВывод = задача_корень / 'build/verification/cosl-relink'
    текстовыйВывод.mkdir(parents=True, exist_ok=True)
    Отчет_ЗНАЧЕН = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((задача_корень / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            путь = Path(임시)
            with tarfile.open(str(задача_корень / 'dist/jkoros-native-relink.tar.gz')) as Группа_ЗНАЧЕН:
                for ввод_ЗНАЧЕН in Группа_ЗНАЧЕН.getmembers():
                    if путь not in (путь / ввод_ЗНАЧЕН.name).resolve().parents or ввод_ЗНАЧЕН.issym() or ввод_ЗНАЧЕН.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ввод_ЗНАЧЕН.name)
                Группа_ЗНАЧЕН.extractall(str(путь))
            исходныйКод = путь / 'jkoros-native-relink'
            def 재연결(Название, 인수들):
                with (текстовыйВывод / Название).open('wb') as LOG_ЗАПИСЬ:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(исходныйКод),
                                   stdout=LOG_ЗАПИСЬ, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            Отчет_ЗНАЧЕН['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            компилятор_средство = исходныйКод / 'vendor/tinycc/libtcc.c'
            основной_текст = компилятор_средство.read_text()
            позиция = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert основной_текст.count(позиция) == 1
            компилятор_средство.write_text(основной_текст.replace(позиция, позиция + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(аргументы.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            фото_ЗНАЧЕН = исходныйКод / 'build/relinked/kernel8.img'
            Отчет_ЗНАЧЕН['modified_kernel_sha256'] = hashlib.sha256(фото_ЗНАЧЕН.read_bytes()).hexdigest()
            assert Отчет_ЗНАЧЕН['modified_kernel_sha256'] != Отчет_ЗНАЧЕН['kernel_sha256']
            Отчет_ЗНАЧЕН['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = команда()
            인수들[인수들.index('-kernel') + 1] = str(фото_ЗНАЧЕН)
            Процесс_ЗНАЧЕН = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_ЗАПИСЬ = bytearray()
            выделение_ЗНАЧЕН = selectors.DefaultSelector()
            выделение_ЗНАЧЕН.register(Процесс_ЗНАЧЕН.stdout, selectors.EVENT_READ)
            def состояние_ожидания(выпуск_ЗНАЧЕН=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while выпуск_ЗНАЧЕН not in LOG_ЗАПИСЬ[처음:]:
                    if time.monotonic() > 끝 or Процесс_ЗНАЧЕН.poll() is not None:
                        raise AssertionError('Missing ' + repr(выпуск_ЗНАЧЕН) + '\n' + LOG_ЗАПИСЬ[처음:].decode('utf-8', 'replace'))
                    for ввод_ЗНАЧЕН, _ in выделение_ЗНАЧЕН.select(.1):
                        данные = ввод_ЗНАЧЕН.fileobj.read(65536)
                        if данные:
                            LOG_ЗАПИСЬ.extend(данные)
                return bytes(LOG_ЗАПИСЬ[처음:])
            def написать(Word_SMS, выпуск_ЗНАЧЕН=b'jkoros-native> '):
                처음 = len(LOG_ЗАПИСЬ)
                Процесс_ЗНАЧЕН.stdin.write(Word_SMS.encode() + b'\n')
                Процесс_ЗНАЧЕН.stdin.flush()
                return состояние_ожидания(выпуск_ЗНАЧЕН, 처음)
            try:
                состояние_ожидания()
                испытания = '#include <файл_ABI.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return запись_файл_данные(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                написать('load /relink.c', b'hex> ')
                for позиция_ИНДЕКС in range(0, len(испытания), 64):
                    написать(испытания[позиция_ИНДЕКС:позиция_ИНДЕКС+64].hex(), b'hex> ')
                assert b'LOADED' in написать('.')
                результат = написать('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in результат, результат
                результат = написать('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in результат and b'exit 0' in результат, результат
                Отчет_ЗНАЧЕН['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                выделение_ЗНАЧЕН.close()
                if Процесс_ЗНАЧЕН.poll() is None:
                    Процесс_ЗНАЧЕН.terminate()
                    try:
                        Процесс_ЗНАЧЕН.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Процесс_ЗНАЧЕН.kill()
                        Процесс_ЗНАЧЕН.wait()
                (текстовыйВывод / 'guest.log').write_bytes(LOG_ЗАПИСЬ)
        Отчет_ЗНАЧЕН['passed'] = True
        print(json.dumps(Отчет_ЗНАЧЕН, ensure_ascii=False, indent=2))
    finally:
        (текстовыйВывод / 'report.json').write_text(json.dumps(Отчет_ЗНАЧЕН, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    запустить()
