#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 faktiki_verilənlər 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from icra_etmək_əmr import Project_kök, Əmr


def İcra_Et():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--sdk', type=Path, default=Project_kök.parent / 'rpi4/build/rootfs')
    인수 = parser_48ee4b1b.parse_args()
    출력 = Project_kök / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    hesabat_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_kök / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Cığır = Path(임시)
            with tarfile.open(str(Project_kök / 'dist/jkoros-native-relink.tar.gz')) as Qrup_VALUE:
                for daxiletmə_VALUE in Qrup_VALUE.getmembers():
                    if Cığır not in (Cığır / daxiletmə_VALUE.name).resolve().parents or daxiletmə_VALUE.issym() or daxiletmə_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + daxiletmə_VALUE.name)
                Qrup_VALUE.extractall(str(Cığır))
            QAYNAQ = Cığır / 'jkoros-native-relink'
            def 재연결(Ad, 인수들):
                with (출력 / Ad).open('wb') as LOG_yaz:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(QAYNAQ),
                                   stdout=LOG_yaz, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            hesabat_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = QAYNAQ / 'vendor/tinycc/libtcc.c'
            əsas_mətn = 번역기.read_text()
            yerinə_qoymaq = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert əsas_mətn.count(yerinə_qoymaq) == 1
            번역기.write_text(əsas_mətn.replace(yerinə_qoymaq, yerinə_qoymaq + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = QAYNAQ / 'build/relinked/kernel8.img'
            hesabat_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert hesabat_VALUE['modified_kernel_sha256'] != hesabat_VALUE['kernel_sha256']
            hesabat_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Əmr()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            Proses_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_yaz = bytearray()
            seçilmiş_sahə_VALUE = selectors.DefaultSelector()
            seçilmiş_sahə_VALUE.register(Proses_VALUE.stdout, selectors.EVENT_READ)
            def gözlə_vəziyyət(göstərmək_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while göstərmək_VALUE not in LOG_yaz[처음:]:
                    if time.monotonic() > 끝 or Proses_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(göstərmək_VALUE) + '\n' + LOG_yaz[처음:].decode('utf-8', 'replace'))
                    for daxiletmə_VALUE, _ in seçilmiş_sahə_VALUE.select(.1):
                        verilənlər = daxiletmə_VALUE.fileobj.read(65536)
                        if verilənlər:
                            LOG_yaz.extend(verilənlər)
                return bytes(LOG_yaz[처음:])
            def göndərmək(Söz_SMS, göstərmək_VALUE=b'jkoros-native> '):
                처음 = len(LOG_yaz)
                Proses_VALUE.stdin.write(Söz_SMS.encode() + b'\n')
                Proses_VALUE.stdin.flush()
                return gözlə_vəziyyət(göstərmək_VALUE, 처음)
            try:
                gözlə_vəziyyət()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return yazmaq_fayl_verilənlər(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                göndərmək('load /relink.c', b'hex> ')
                for yerinə_qoymaq_INDEX in range(0, len(시험), 64):
                    göndərmək(시험[yerinə_qoymaq_INDEX:yerinə_qoymaq_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in göndərmək('.')
                ölçü = göndərmək('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in ölçü, ölçü
                ölçü = göndərmək('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in ölçü and b'exit 0' in ölçü, ölçü
                hesabat_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                seçilmiş_sahə_VALUE.close()
                if Proses_VALUE.poll() is None:
                    Proses_VALUE.terminate()
                    try:
                        Proses_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proses_VALUE.kill()
                        Proses_VALUE.wait()
                (출력 / 'guest.log').write_bytes(LOG_yaz)
        hesabat_VALUE['passed'] = True
        print(json.dumps(hesabat_VALUE, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(hesabat_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    İcra_Et()
