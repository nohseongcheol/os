#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 ǹdịnezie_datà 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from mee_nnyemiwu import 기준, Ntiiwu


def Bido():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    akụkọ_valuu = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ụzọ_ozi = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as otu_valuu:
                for ndebà_valuu in otu_valuu.getmembers():
                    if ụzọ_ozi not in (ụzọ_ozi / ndebà_valuu.name).resolve().parents or ndebà_valuu.issym() or ndebà_valuu.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ndebà_valuu.name)
                otu_valuu.extractall(str(ụzọ_ozi))
            ebensìbịa = ụzọ_ozi / 'jkoros-native-relink'
            def 재연결(Aha, 인수들):
                with (출력 / Aha).open('wb') as ndekọ_NDEKỌ:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ebensìbịa),
                                   stdout=ndekọ_NDEKỌ, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            akụkọ_valuu['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ebensìbịa / 'vendor/tinycc/libtcc.c'
            àhụngwè = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert àhụngwè.count(위치) == 1
            번역기.write_text(àhụngwè.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            foto_valuu = ebensìbịa / 'build/relinked/kernel8.img'
            akụkọ_valuu['modified_kernel_sha256'] = hashlib.sha256(foto_valuu.read_bytes()).hexdigest()
            assert akụkọ_valuu['modified_kernel_sha256'] != akụkọ_valuu['kernel_sha256']
            akụkọ_valuu['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Ntiiwu()
            인수들[인수들.index('-kernel') + 1] = str(foto_valuu)
            ùsòrò_valuu_6712bde7 = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ndekọ_NDEKỌ = bytearray()
            ebenhọrọ_valuu = selectors.DefaultSelector()
            ebenhọrọ_valuu.register(ùsòrò_valuu_6712bde7.stdout, selectors.EVENT_READ)
            def 기다림(gòsi_valuu=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while gòsi_valuu not in ndekọ_NDEKỌ[처음:]:
                    if time.monotonic() > 끝 or ùsòrò_valuu_6712bde7.poll() is not None:
                        raise AssertionError('Missing ' + repr(gòsi_valuu) + '\n' + ndekọ_NDEKỌ[처음:].decode('utf-8', 'replace'))
                    for ndebà_valuu, _ in ebenhọrọ_valuu.select(.1):
                        datà = ndebà_valuu.fileobj.read(65536)
                        if datà:
                            ndekọ_NDEKỌ.extend(datà)
                return bytes(ndekọ_NDEKỌ[처음:])
            def zìga(Mkpụrụokwu_SMS, gòsi_valuu=b'jkoros-native> '):
                처음 = len(ndekọ_NDEKỌ)
                ùsòrò_valuu_6712bde7.stdin.write(Mkpụrụokwu_SMS.encode() + b'\n')
                ùsòrò_valuu_6712bde7.stdin.flush()
                return 기다림(gòsi_valuu, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return dee_ọbọakwụkwọ_datà(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                zìga('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    zìga(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in zìga('.')
                결과 = zìga('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = zìga('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                akụkọ_valuu['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                ebenhọrọ_valuu.close()
                if ùsòrò_valuu_6712bde7.poll() is None:
                    ùsòrò_valuu_6712bde7.terminate()
                    try:
                        ùsòrò_valuu_6712bde7.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        ùsòrò_valuu_6712bde7.kill()
                        ùsòrò_valuu_6712bde7.wait()
                (출력 / 'guest.log').write_bytes(ndekọ_NDEKỌ)
        akụkọ_valuu['passed'] = True
        print(json.dumps(akụkọ_valuu, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(akụkọ_valuu, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Bido()
