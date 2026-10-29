#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 real_ma_lumotlar 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from bajarmoq_buyruq import Project_ildiz, Buyruq


def Bajarish():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--sdk', type=Path, default=Project_ildiz.parent / 'rpi4/build/rootfs')
    인수 = parser_48ee4b1b.parse_args()
    출력 = Project_ildiz / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    hisobot_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_ildiz / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            yo_l = Path(임시)
            with tarfile.open(str(Project_ildiz / 'dist/jkoros-native-relink.tar.gz')) as Guruh_VALUE:
                for kiritish_VALUE in Guruh_VALUE.getmembers():
                    if yo_l not in (yo_l / kiritish_VALUE.name).resolve().parents or kiritish_VALUE.issym() or kiritish_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + kiritish_VALUE.name)
                Guruh_VALUE.extractall(str(yo_l))
            manba = yo_l / 'jkoros-native-relink'
            def 재연결(Nomi, 인수들):
                with (출력 / Nomi).open('wb') as LOG_satr:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(manba),
                                   stdout=LOG_satr, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            hisobot_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = manba / 'vendor/tinycc/libtcc.c'
            asosiy_matn = 번역기.read_text()
            Holati = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert asosiy_matn.count(Holati) == 1
            번역기.write_text(asosiy_matn.replace(Holati, Holati + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            rasm_VALUE = manba / 'build/relinked/kernel8.img'
            hisobot_VALUE['modified_kernel_sha256'] = hashlib.sha256(rasm_VALUE.read_bytes()).hexdigest()
            assert hisobot_VALUE['modified_kernel_sha256'] != hisobot_VALUE['kernel_sha256']
            hisobot_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Buyruq()
            인수들[인수들.index('-kernel') + 1] = str(rasm_VALUE)
            Jarayon_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_satr = bytearray()
            tanlanma_VALUE = selectors.DefaultSelector()
            tanlanma_VALUE.register(Jarayon_VALUE.stdout, selectors.EVENT_READ)
            def bir_daqiqa_holat(ko_rsatmoq_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while ko_rsatmoq_VALUE not in LOG_satr[처음:]:
                    if time.monotonic() > 끝 or Jarayon_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(ko_rsatmoq_VALUE) + '\n' + LOG_satr[처음:].decode('utf-8', 'replace'))
                    for kiritish_VALUE, _ in tanlanma_VALUE.select(.1):
                        ma_lumotlar = kiritish_VALUE.fileobj.read(65536)
                        if ma_lumotlar:
                            LOG_satr.extend(ma_lumotlar)
                return bytes(LOG_satr[처음:])
            def yuborish(Word_SMS, ko_rsatmoq_VALUE=b'jkoros-native> '):
                처음 = len(LOG_satr)
                Jarayon_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Jarayon_VALUE.stdin.flush()
                return bir_daqiqa_holat(ko_rsatmoq_VALUE, 처음)
            try:
                bir_daqiqa_holat()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return yozmoq_fayl_ma_lumotlar(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                yuborish('load /relink.c', b'hex> ')
                for holat_INDEX in range(0, len(시험), 64):
                    yuborish(시험[holat_INDEX:holat_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in yuborish('.')
                o_lchov = yuborish('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in o_lchov, o_lchov
                o_lchov = yuborish('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in o_lchov and b'exit 0' in o_lchov, o_lchov
                hisobot_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                tanlanma_VALUE.close()
                if Jarayon_VALUE.poll() is None:
                    Jarayon_VALUE.terminate()
                    try:
                        Jarayon_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Jarayon_VALUE.kill()
                        Jarayon_VALUE.wait()
                (출력 / 'guest.log').write_bytes(LOG_satr)
        hisobot_VALUE['passed'] = True
        print(json.dumps(hisobot_VALUE, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(hisobot_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Bajarish()
