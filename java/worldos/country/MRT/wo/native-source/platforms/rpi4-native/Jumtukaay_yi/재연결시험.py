#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 liteew_mbir 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from def_ndigel import 기준, ndigel


def daw():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    tënk_xëyma = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Yoonu_jëmale = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as mboolo_xëyma:
                for dugal_xabaar_xëyma in mboolo_xëyma.getmembers():
                    if Yoonu_jëmale not in (Yoonu_jëmale / dugal_xabaar_xëyma.name).resolve().parents or dugal_xabaar_xëyma.issym() or dugal_xabaar_xëyma.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + dugal_xabaar_xëyma.name)
                mboolo_xëyma.extractall(str(Yoonu_jëmale))
            Cosaan = Yoonu_jëmale / 'jkoros-native-relink'
            def 재연결(tur_253d1510, 인수들):
                with (출력 / tur_253d1510).open('wb') as làq_Dënk:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(Cosaan),
                                   stdout=làq_Dënk, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            tënk_xëyma['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = Cosaan / 'vendor/tinycc/libtcc.c'
            yaxub_mool = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert yaxub_mool.count(위치) == 1
            번역기.write_text(yaxub_mool.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            nataal_xëyma = Cosaan / 'build/relinked/kernel8.img'
            tënk_xëyma['modified_kernel_sha256'] = hashlib.sha256(nataal_xëyma.read_bytes()).hexdigest()
            assert tënk_xëyma['modified_kernel_sha256'] != tënk_xëyma['kernel_sha256']
            tënk_xëyma['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = ndigel()
            인수들[인수들.index('-kernel') + 1] = str(nataal_xëyma)
            yokkute_xëyma = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            làq_Dënk = bytearray()
            tanneef_xëyma = selectors.DefaultSelector()
            tanneef_xëyma.register(yokkute_xëyma.stdout, selectors.EVENT_READ)
            def 기다림(féeñal_xëyma=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while féeñal_xëyma not in làq_Dënk[처음:]:
                    if time.monotonic() > 끝 or yokkute_xëyma.poll() is not None:
                        raise AssertionError('Missing ' + repr(féeñal_xëyma) + '\n' + làq_Dënk[처음:].decode('utf-8', 'replace'))
                    for dugal_xabaar_xëyma, _ in tanneef_xëyma.select(.1):
                        mbir = dugal_xabaar_xëyma.fileobj.read(65536)
                        if mbir:
                            làq_Dënk.extend(mbir)
                return bytes(làq_Dënk[처음:])
            def Yónnee(Word_SMS, féeñal_xëyma=b'jkoros-native> '):
                처음 = len(làq_Dënk)
                yokkute_xëyma.stdin.write(Word_SMS.encode() + b'\n')
                yokkute_xëyma.stdin.flush()
                return 기다림(féeñal_xëyma, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return biir_bara_denc_mbir(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                Yónnee('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    Yónnee(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in Yónnee('.')
                결과 = Yónnee('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = Yónnee('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                tënk_xëyma['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                tanneef_xëyma.close()
                if yokkute_xëyma.poll() is None:
                    yokkute_xëyma.terminate()
                    try:
                        yokkute_xëyma.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        yokkute_xëyma.kill()
                        yokkute_xëyma.wait()
                (출력 / 'guest.log').write_bytes(làq_Dënk)
        tënk_xëyma['passed'] = True
        print(json.dumps(tënk_xëyma, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(tënk_xëyma, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    daw()
