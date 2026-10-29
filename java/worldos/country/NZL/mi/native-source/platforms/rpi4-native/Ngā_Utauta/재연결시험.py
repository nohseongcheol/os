#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 tūturu_raraunga 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from kawe_tono import whakaatu_pūtake, tono


def whakahaere():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=whakaatu_pūtake.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = whakaatu_pūtake / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    pūrongo_uara = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((whakaatu_pūtake / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ara = Path(임시)
            with tarfile.open(str(whakaatu_pūtake / 'dist/jkoros-native-relink.tar.gz')) as rōpū_uara:
                for tāurunga_uara in rōpū_uara.getmembers():
                    if ara not in (ara / tāurunga_uara.name).resolve().parents or tāurunga_uara.issym() or tāurunga_uara.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + tāurunga_uara.name)
                rōpū_uara.extractall(str(ara))
            pūtake = ara / 'jkoros-native-relink'
            def 재연결(Ingoa, 인수들):
                with (출력 / Ingoa).open('wb') as LOG_RECORD:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(pūtake),
                                   stdout=LOG_RECORD, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            pūrongo_uara['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = pūtake / 'vendor/tinycc/libtcc.c'
            kuputuhi_tinana = 번역기.read_text()
            tūranga = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert kuputuhi_tinana.count(tūranga) == 1
            번역기.write_text(kuputuhi_tinana.replace(tūranga, tūranga + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_uara = pūtake / 'build/relinked/kernel8.img'
            pūrongo_uara['modified_kernel_sha256'] = hashlib.sha256(IMAGE_uara.read_bytes()).hexdigest()
            assert pūrongo_uara['modified_kernel_sha256'] != pūrongo_uara['kernel_sha256']
            pūrongo_uara['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = tono()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_uara)
            Hātepe_uara = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_RECORD = bytearray()
            tīpakonga_uara = selectors.DefaultSelector()
            tīpakonga_uara.register(Hātepe_uara.stdout, selectors.EVENT_READ)
            def 기다림(whakaatu_uara=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while whakaatu_uara not in LOG_RECORD[처음:]:
                    if time.monotonic() > 끝 or Hātepe_uara.poll() is not None:
                        raise AssertionError('Missing ' + repr(whakaatu_uara) + '\n' + LOG_RECORD[처음:].decode('utf-8', 'replace'))
                    for tāurunga_uara, _ in tīpakonga_uara.select(.1):
                        raraunga = tāurunga_uara.fileobj.read(65536)
                        if raraunga:
                            LOG_RECORD.extend(raraunga)
                return bytes(LOG_RECORD[처음:])
            def tuku(Word_TEXT, whakaatu_uara=b'jkoros-native> '):
                처음 = len(LOG_RECORD)
                Hātepe_uara.stdin.write(Word_TEXT.encode() + b'\n')
                Hātepe_uara.stdin.flush()
                return 기다림(whakaatu_uara, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return tuhi_kōnae_raraunga(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                tuku('load /relink.c', b'hex> ')
                for tūranga_INDEX in range(0, len(시험), 64):
                    tuku(시험[tūranga_INDEX:tūranga_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in tuku('.')
                mēhua = tuku('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in mēhua, mēhua
                mēhua = tuku('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in mēhua and b'exit 0' in mēhua, mēhua
                pūrongo_uara['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                tīpakonga_uara.close()
                if Hātepe_uara.poll() is None:
                    Hātepe_uara.terminate()
                    try:
                        Hātepe_uara.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Hātepe_uara.kill()
                        Hātepe_uara.wait()
                (출력 / 'guest.log').write_bytes(LOG_RECORD)
        pūrongo_uara['passed'] = True
        print(json.dumps(pūrongo_uara, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(pūrongo_uara, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    whakahaere()
