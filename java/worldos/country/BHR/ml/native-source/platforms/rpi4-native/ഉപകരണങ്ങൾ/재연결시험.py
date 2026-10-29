#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 വാസ്തവമായ_ഡാറ്റാ 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം, ആജ്ഞ


def നടപ്പിലാക്കുക():
    പാഴ്_സർ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    പാഴ്_സർ_48ee4b1b.add_argument('--sdk', type=Path, default=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parent / 'rpi4/build/rootfs')
    인수 = പാഴ്_സർ_48ee4b1b.parse_args()
    ഫലം = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/verification/cosl-relink'
    ഫലം.mkdir(parents=True, exist_ok=True)
    నివేదిక_മൂല്യം = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            വഴി = Path(임시)
            with tarfile.open(str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'dist/jkoros-native-relink.tar.gz')) as സംഘം_മൂല്യം:
                for എന്_ട്രി_മൂല്യം in സംഘം_മൂല്യം.getmembers():
                    if വഴി not in (വഴി / എന്_ട്രി_മൂല്യം.name).resolve().parents or എന്_ട്രി_മൂല്യം.issym() or എന്_ട്രി_മൂല്യം.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + എന്_ട്രി_മൂല്യം.name)
                സംഘം_മൂല്യം.extractall(str(വഴി))
            ഉറവിടം = വഴി / 'jkoros-native-relink'
            def 재연결(പേരു്, 인수들):
                with (ഫലം / പേരു്).open('wb') as ലോഗ്_രേഖ:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ഉറവിടം),
                                   stdout=ലോഗ്_രേഖ, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            నివేదిక_മൂല്യം['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ഉറവിടം / 'vendor/tinycc/libtcc.c'
            മുഖ്യ_പാഠം = 번역기.read_text()
            സ്ഥാനം = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert മുഖ്യ_പാഠം.count(സ്ഥാനം) == 1
            번역기.write_text(മുഖ്യ_പാഠം.replace(സ്ഥാനം, സ്ഥാനം + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            ഇമേജ്_മൂല്യം = ഉറവിടം / 'build/relinked/kernel8.img'
            నివేదిక_മൂല്യം['modified_kernel_sha256'] = hashlib.sha256(ഇമേജ്_മൂല്യം.read_bytes()).hexdigest()
            assert నివేదిక_മൂല്യം['modified_kernel_sha256'] != నివేదిక_മൂല്യം['kernel_sha256']
            నివేదిక_മൂല്യം['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = ആജ്ഞ()
            인수들[인수들.index('-kernel') + 1] = str(ഇമേജ്_മൂല്യം)
            പ്രോസസ്_മൂല്യം = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ലോഗ്_രേഖ = bytearray()
            തിരഞ്ഞെടുക്കല്_മൂല്യം = selectors.DefaultSelector()
            തിരഞ്ഞെടുക്കല്_മൂല്യം.register(പ്രോസസ്_മൂല്യം.stdout, selectors.EVENT_READ)
            def കാക്കുക_അവസ്ഥ(പ്രദർശനം_മൂല്യം=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while പ്രദർശനം_മൂല്യം not in ലോഗ്_രേഖ[처음:]:
                    if time.monotonic() > 끝 or പ്രോസസ്_മൂല്യം.poll() is not None:
                        raise AssertionError('Missing ' + repr(പ്രദർശനം_മൂല്യം) + '\n' + ലോഗ്_രേഖ[처음:].decode('utf-8', 'replace'))
                    for എന്_ട്രി_മൂല്യം, _ in തിരഞ്ഞെടുക്കല്_മൂല്യം.select(.1):
                        ഡാറ്റാ = എന്_ട്രി_മൂല്യം.fileobj.read(65536)
                        if ഡാറ്റാ:
                            ലോഗ്_രേഖ.extend(ഡാറ്റാ)
                return bytes(ലോഗ്_രേഖ[처음:])
            def അയയ്ക്കുക(വാക്ക്_ലിഖിതം, പ്രദർശനം_മൂല്യം=b'jkoros-native> '):
                처음 = len(ലോഗ്_രേഖ)
                പ്രോസസ്_മൂല്യം.stdin.write(വാക്ക്_ലിഖിതം.encode() + b'\n')
                പ്രോസസ്_മൂല്യം.stdin.flush()
                return കാക്കുക_അവസ്ഥ(പ്രദർശനം_മൂല്യം, 처음)
            try:
                കാക്കുക_അവസ്ഥ()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return റൈറ്റ്_ചെയ്യുക_ഫയല്_ഡാറ്റാ(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                അയയ്ക്കുക('load /relink.c', b'hex> ')
                for പദവി_സൂചിക in range(0, len(시험), 64):
                    അയയ്ക്കുക(시험[പദവി_സൂചിക:പദവി_സൂചിക+64].hex(), b'hex> ')
                assert b'LOADED' in അയയ്ക്കുക('.')
                അളവ് = അയയ്ക്കുക('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in അളവ്, അളവ്
                അളവ് = അയയ്ക്കുക('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in അളവ് and b'exit 0' in അളവ്, അളവ്
                నివేదిక_മൂല്യം['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                തിരഞ്ഞെടുക്കല്_മൂല്യം.close()
                if പ്രോസസ്_മൂല്യം.poll() is None:
                    പ്രോസസ്_മൂല്യം.terminate()
                    try:
                        പ്രോസസ്_മൂല്യം.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        പ്രോസസ്_മൂല്യം.kill()
                        പ്രോസസ്_മൂല്യം.wait()
                (ഫലം / 'guest.log').write_bytes(ലോഗ്_രേഖ)
        నివేదిక_മൂല്യം['passed'] = True
        print(json.dumps(నివేదిక_മൂല്യം, ensure_ascii=False, indent=2))
    finally:
        (ഫലം / 'report.json').write_text(json.dumps(నివేదిక_മൂല്യം, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    നടപ്പിലാക്കുക()
