#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 реален_податоци 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Изврши_наредба import Project_корен, Команда


def Изврши_2():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--sdk', type=Path, default=Project_корен.parent / 'rpi4/build/rootfs')
    Аргументи = анализатор_48ee4b1b.parse_args()
    출력 = Project_корен / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    извештај_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_корен / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ПАТЕКА = Path(임시)
            with tarfile.open(str(Project_корен / 'dist/jkoros-native-relink.tar.gz')) as Група_VALUE:
                for внес_VALUE in Група_VALUE.getmembers():
                    if ПАТЕКА not in (ПАТЕКА / внес_VALUE.name).resolve().parents or внес_VALUE.issym() or внес_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + внес_VALUE.name)
                Група_VALUE.extractall(str(ПАТЕКА))
            ИЗВОР = ПАТЕКА / 'jkoros-native-relink'
            def 재연결(Име, 인수들):
                with (출력 / Име).open('wb') as LOG_ред:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ИЗВОР),
                                   stdout=LOG_ред, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            извештај_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ИЗВОР / 'vendor/tinycc/libtcc.c'
            основен_текст = 번역기.read_text()
            Позиција = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert основен_текст.count(Позиција) == 1
            번역기.write_text(основен_текст.replace(Позиција, Позиција + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Аргументи.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = ИЗВОР / 'build/relinked/kernel8.img'
            извештај_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert извештај_VALUE['modified_kernel_sha256'] != извештај_VALUE['kernel_sha256']
            извештај_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Команда()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            Процес_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_ред = bytearray()
            селекција_VALUE = selectors.DefaultSelector()
            селекција_VALUE.register(Процес_VALUE.stdout, selectors.EVENT_READ)
            def почекај_статус(прикажи_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while прикажи_VALUE not in LOG_ред[처음:]:
                    if time.monotonic() > 끝 or Процес_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(прикажи_VALUE) + '\n' + LOG_ред[처음:].decode('utf-8', 'replace'))
                    for внес_VALUE, _ in селекција_VALUE.select(.1):
                        податоци = внес_VALUE.fileobj.read(65536)
                        if податоци:
                            LOG_ред.extend(податоци)
                return bytes(LOG_ред[처음:])
            def испрати(Word_СМС, прикажи_VALUE=b'jkoros-native> '):
                처음 = len(LOG_ред)
                Процес_VALUE.stdin.write(Word_СМС.encode() + b'\n')
                Процес_VALUE.stdin.flush()
                return почекај_статус(прикажи_VALUE, 처음)
            try:
                почекај_статус()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return запиши_датотека_податоци(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                испрати('load /relink.c', b'hex> ')
                for позиционирање_INDEX in range(0, len(시험), 64):
                    испрати(시험[позиционирање_INDEX:позиционирање_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in испрати('.')
                мерка = испрати('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in мерка, мерка
                мерка = испрати('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in мерка and b'exit 0' in мерка, мерка
                извештај_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                селекција_VALUE.close()
                if Процес_VALUE.poll() is None:
                    Процес_VALUE.terminate()
                    try:
                        Процес_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Процес_VALUE.kill()
                        Процес_VALUE.wait()
                (출력 / 'guest.log').write_bytes(LOG_ред)
        извештај_VALUE['passed'] = True
        print(json.dumps(извештај_VALUE, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(извештај_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Изврши_2()
