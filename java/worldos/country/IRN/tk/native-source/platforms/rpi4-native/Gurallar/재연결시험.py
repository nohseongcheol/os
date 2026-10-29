#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 hakyky_maglumat 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from ýerine_ýetir_buýruk import 기준, buýruk


def Bitir():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    hasabat_baha = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Ýol = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as topar_baha:
                for girizmeklik_baha in topar_baha.getmembers():
                    if Ýol not in (Ýol / girizmeklik_baha.name).resolve().parents or girizmeklik_baha.issym() or girizmeklik_baha.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + girizmeklik_baha.name)
                topar_baha.extractall(str(Ýol))
            Çeşme = Ýol / 'jkoros-native-relink'
            def 재연결(Ad, 인수들):
                with (출력 / Ad).open('wb') as hasaba_alyş_setir:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(Çeşme),
                                   stdout=hasaba_alyş_setir, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            hasabat_baha['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = Çeşme / 'vendor/tinycc/libtcc.c'
            göwre_teksti = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert göwre_teksti.count(위치) == 1
            번역기.write_text(göwre_teksti.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            surat_baha = Çeşme / 'build/relinked/kernel8.img'
            hasabat_baha['modified_kernel_sha256'] = hashlib.sha256(surat_baha.read_bytes()).hexdigest()
            assert hasabat_baha['modified_kernel_sha256'] != hasabat_baha['kernel_sha256']
            hasabat_baha['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = buýruk()
            인수들[인수들.index('-kernel') + 1] = str(surat_baha)
            Proses_baha = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            hasaba_alyş_setir = bytearray()
            saýlama_baha = selectors.DefaultSelector()
            saýlama_baha.register(Proses_baha.stdout, selectors.EVENT_READ)
            def 기다림(görkez_baha_487749b8=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while görkez_baha_487749b8 not in hasaba_alyş_setir[처음:]:
                    if time.monotonic() > 끝 or Proses_baha.poll() is not None:
                        raise AssertionError('Missing ' + repr(görkez_baha_487749b8) + '\n' + hasaba_alyş_setir[처음:].decode('utf-8', 'replace'))
                    for girizmeklik_baha, _ in saýlama_baha.select(.1):
                        maglumat = girizmeklik_baha.fileobj.read(65536)
                        if maglumat:
                            hasaba_alyş_setir.extend(maglumat)
                return bytes(hasaba_alyş_setir[처음:])
            def iber(Söz_SMS, görkez_baha_487749b8=b'jkoros-native> '):
                처음 = len(hasaba_alyş_setir)
                Proses_baha.stdin.write(Söz_SMS.encode() + b'\n')
                Proses_baha.stdin.flush()
                return 기다림(görkez_baha_487749b8, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ýaz_faýl_maglumat(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                iber('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    iber(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in iber('.')
                결과 = iber('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = iber('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                hasabat_baha['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                saýlama_baha.close()
                if Proses_baha.poll() is None:
                    Proses_baha.terminate()
                    try:
                        Proses_baha.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proses_baha.kill()
                        Proses_baha.wait()
                (출력 / 'guest.log').write_bytes(hasaba_alyş_setir)
        hasabat_baha['passed'] = True
        print(json.dumps(hasabat_baha, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(hasabat_baha, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Bitir()
