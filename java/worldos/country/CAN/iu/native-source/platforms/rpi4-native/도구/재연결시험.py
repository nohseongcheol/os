#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 taannallarik_titiqqat 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from 실행 import 기준, piqujijjut


def 시작():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    unikkaaq_atuutilik = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            aqqut = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as katinngajut_atuutilik:
                for Iliniku_atuutilik in katinngajut_atuutilik.getmembers():
                    if aqqut not in (aqqut / Iliniku_atuutilik.name).resolve().parents or Iliniku_atuutilik.issym() or Iliniku_atuutilik.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + Iliniku_atuutilik.name)
                katinngajut_atuutilik.extractall(str(aqqut))
            pivviujuq = aqqut / 'jkoros-native-relink'
            def 재연결(atiq, 인수들):
                with (출력 / atiq).open('wb') as papattivik_sanimukutaak:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(pivviujuq),
                                   stdout=papattivik_sanimukutaak, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            unikkaaq_atuutilik['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = pivviujuq / 'vendor/tinycc/libtcc.c'
            Titiqqaup_ilulilluataa = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert Titiqqaup_ilulilluataa.count(위치) == 1
            번역기.write_text(Titiqqaup_ilulilluataa.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            ajjinnguaq_atuutilik = pivviujuq / 'build/relinked/kernel8.img'
            unikkaaq_atuutilik['modified_kernel_sha256'] = hashlib.sha256(ajjinnguaq_atuutilik.read_bytes()).hexdigest()
            assert unikkaaq_atuutilik['modified_kernel_sha256'] != unikkaaq_atuutilik['kernel_sha256']
            unikkaaq_atuutilik['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = piqujijjut()
            인수들[인수들.index('-kernel') + 1] = str(ajjinnguaq_atuutilik)
            Pivallianiq_atuutilik = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            papattivik_sanimukutaak = bytearray()
            nirulussimaniq_atuutilik = selectors.DefaultSelector()
            nirulussimaniq_atuutilik.register(Pivallianiq_atuutilik.stdout, selectors.EVENT_READ)
            def 기다림(saqqilli_atuutilik=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while saqqilli_atuutilik not in papattivik_sanimukutaak[처음:]:
                    if time.monotonic() > 끝 or Pivallianiq_atuutilik.poll() is not None:
                        raise AssertionError('Missing ' + repr(saqqilli_atuutilik) + '\n' + papattivik_sanimukutaak[처음:].decode('utf-8', 'replace'))
                    for Iliniku_atuutilik, _ in nirulussimaniq_atuutilik.select(.1):
                        titiqqat = Iliniku_atuutilik.fileobj.read(65536)
                        if titiqqat:
                            papattivik_sanimukutaak.extend(titiqqat)
                return bytes(papattivik_sanimukutaak[처음:])
            def nassiutili(말, saqqilli_atuutilik=b'jkoros-native> '):
                처음 = len(papattivik_sanimukutaak)
                Pivallianiq_atuutilik.stdin.write(말.encode() + b'\n')
                Pivallianiq_atuutilik.stdin.flush()
                return 기다림(saqqilli_atuutilik, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return titiraq_ini_titiqqat(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                nassiutili('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    nassiutili(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in nassiutili('.')
                결과 = nassiutili('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = nassiutili('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                unikkaaq_atuutilik['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                nirulussimaniq_atuutilik.close()
                if Pivallianiq_atuutilik.poll() is None:
                    Pivallianiq_atuutilik.terminate()
                    try:
                        Pivallianiq_atuutilik.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Pivallianiq_atuutilik.kill()
                        Pivallianiq_atuutilik.wait()
                (출력 / 'guest.log').write_bytes(papattivik_sanimukutaak)
        unikkaaq_atuutilik['passed'] = True
        print(json.dumps(unikkaaq_atuutilik, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(unikkaaq_atuutilik, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    시작()
