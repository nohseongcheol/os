#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 πραγματικός_δεδομένα 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from εκτελώ_εντολή import έργο_ρίζα, Εντολή


def Εκτέλεση_2():
    ανάλυση_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ανάλυση_48ee4b1b.add_argument('--sdk', type=Path, default=έργο_ρίζα.parent / 'rpi4/build/rootfs')
    Παράμετροι = ανάλυση_48ee4b1b.parse_args()
    Έξοδος = έργο_ρίζα / 'build/verification/cosl-relink'
    Έξοδος.mkdir(parents=True, exist_ok=True)
    έκθεση_τιμή = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((έργο_ρίζα / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ΔΙΑΔΡΟΜΗ = Path(임시)
            with tarfile.open(str(έργο_ρίζα / 'dist/jkoros-native-relink.tar.gz')) as Ομάδα_τιμή:
                for καταχώρηση_τιμή in Ομάδα_τιμή.getmembers():
                    if ΔΙΑΔΡΟΜΗ not in (ΔΙΑΔΡΟΜΗ / καταχώρηση_τιμή.name).resolve().parents or καταχώρηση_τιμή.issym() or καταχώρηση_τιμή.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + καταχώρηση_τιμή.name)
                Ομάδα_τιμή.extractall(str(ΔΙΑΔΡΟΜΗ))
            ΠΗΓΗ = ΔΙΑΔΡΟΜΗ / 'jkoros-native-relink'
            def 재연결(Όνομα, 인수들):
                with (Έξοδος / Όνομα).open('wb') as καταγράφω_ρεκόρ:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ΠΗΓΗ),
                                   stdout=καταγράφω_ρεκόρ, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            έκθεση_τιμή['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            πρόγραμμα_μεταγλώττισης_εργαλείο = ΠΗΓΗ / 'vendor/tinycc/libtcc.c'
            σώμα_κειμένου = πρόγραμμα_μεταγλώττισης_εργαλείο.read_text()
            Θέση = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert σώμα_κειμένου.count(Θέση) == 1
            πρόγραμμα_μεταγλώττισης_εργαλείο.write_text(σώμα_κειμένου.replace(Θέση, Θέση + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Παράμετροι.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            εικόνα_τιμή = ΠΗΓΗ / 'build/relinked/kernel8.img'
            έκθεση_τιμή['modified_kernel_sha256'] = hashlib.sha256(εικόνα_τιμή.read_bytes()).hexdigest()
            assert έκθεση_τιμή['modified_kernel_sha256'] != έκθεση_τιμή['kernel_sha256']
            έκθεση_τιμή['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Εντολή()
            인수들[인수들.index('-kernel') + 1] = str(εικόνα_τιμή)
            διεργασία_τιμή = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            καταγράφω_ρεκόρ = bytearray()
            επιλογή_τιμή = selectors.DefaultSelector()
            επιλογή_τιμή.register(διεργασία_τιμή.stdout, selectors.EVENT_READ)
            def κατάσταση_αναμονής(εμφανίζω_τιμή=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while εμφανίζω_τιμή not in καταγράφω_ρεκόρ[처음:]:
                    if time.monotonic() > 끝 or διεργασία_τιμή.poll() is not None:
                        raise AssertionError('Missing ' + repr(εμφανίζω_τιμή) + '\n' + καταγράφω_ρεκόρ[처음:].decode('utf-8', 'replace'))
                    for καταχώρηση_τιμή, _ in επιλογή_τιμή.select(.1):
                        δεδομένα = καταχώρηση_τιμή.fileobj.read(65536)
                        if δεδομένα:
                            καταγράφω_ρεκόρ.extend(δεδομένα)
                return bytes(καταγράφω_ρεκόρ[처음:])
            def στέλνω(λέξη_μήνυμα, εμφανίζω_τιμή=b'jkoros-native> '):
                처음 = len(καταγράφω_ρεκόρ)
                διεργασία_τιμή.stdin.write(λέξη_μήνυμα.encode() + b'\n')
                διεργασία_τιμή.stdin.flush()
                return κατάσταση_αναμονής(εμφανίζω_τιμή, 처음)
            try:
                κατάσταση_αναμονής()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return εγγράφω_Αρχείο_δεδομένα(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                στέλνω('load /relink.c', b'hex> ')
                for δείκτης_θέσης in range(0, len(시험), 64):
                    στέλνω(시험[δείκτης_θέσης:δείκτης_θέσης+64].hex(), b'hex> ')
                assert b'LOADED' in στέλνω('.')
                μέτρηση = στέλνω('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in μέτρηση, μέτρηση
                μέτρηση = στέλνω('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in μέτρηση and b'exit 0' in μέτρηση, μέτρηση
                έκθεση_τιμή['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                επιλογή_τιμή.close()
                if διεργασία_τιμή.poll() is None:
                    διεργασία_τιμή.terminate()
                    try:
                        διεργασία_τιμή.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        διεργασία_τιμή.kill()
                        διεργασία_τιμή.wait()
                (Έξοδος / 'guest.log').write_bytes(καταγράφω_ρεκόρ)
        έκθεση_τιμή['passed'] = True
        print(json.dumps(έκθεση_τιμή, ensure_ascii=False, indent=2))
    finally:
        (Έξοδος / 'report.json').write_text(json.dumps(έκθεση_τιμή, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Εκτέλεση_2()
