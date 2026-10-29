#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 వాస్తవ_డేటా 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం, ఆదేశము


def నడుపుము():
    పార్సర్_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    పార్సర్_48ee4b1b.add_argument('--sdk', type=Path, default=ప్రొజెక్ట్_మూలం.parent / 'rpi4/build/rootfs')
    인수 = పార్సర్_48ee4b1b.parse_args()
    అవుట్పుట్ = ప్రొజెక్ట్_మూలం / 'build/verification/cosl-relink'
    అవుట్పుట్.mkdir(parents=True, exist_ok=True)
    నివేదిక_మూల్యం = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((ప్రొజెక్ట్_మూలం / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            పాత్ = Path(임시)
            with tarfile.open(str(ప్రొజెక్ట్_మూలం / 'dist/jkoros-native-relink.tar.gz')) as సమూహం_మూల్యం:
                for ప్రవేశం_మూల్యం in సమూహం_మూల్యం.getmembers():
                    if పాత్ not in (పాత్ / ప్రవేశం_మూల్యం.name).resolve().parents or ప్రవేశం_మూల్యం.issym() or ప్రవేశం_మూల్యం.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ప్రవేశం_మూల్యం.name)
                సమూహం_మూల్యం.extractall(str(పాత్))
            వనరు = పాత్ / 'jkoros-native-relink'
            def 재연결(పేరు, 인수들):
                with (అవుట్పుట్ / పేరు).open('wb') as లాగ్_వరుస:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(వనరు),
                                   stdout=లాగ్_వరుస, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            నివేదిక_మూల్యం['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = వనరు / 'vendor/tinycc/libtcc.c'
            ప్రధాన_పాఠం = 번역기.read_text()
            స్థానము = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert ప్రధాన_పాఠం.count(స్థానము) == 1
            번역기.write_text(ప్రధాన_పాఠం.replace(స్థానము, స్థానము + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            చిత్రం_మూల్యం = వనరు / 'build/relinked/kernel8.img'
            నివేదిక_మూల్యం['modified_kernel_sha256'] = hashlib.sha256(చిత్రం_మూల్యం.read_bytes()).hexdigest()
            assert నివేదిక_మూల్యం['modified_kernel_sha256'] != నివేదిక_మూల్యం['kernel_sha256']
            నివేదిక_మూల్యం['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = ఆదేశము()
            인수들[인수들.index('-kernel') + 1] = str(చిత్రం_మూల్యం)
            విధానం_మూల్యం = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            లాగ్_వరుస = bytearray()
            ఎంపిక_మూల్యం = selectors.DefaultSelector()
            ఎంపిక_మూల్యం.register(విధానం_మూల్యం.stdout, selectors.EVENT_READ)
            def వేచియుండు_స్థితి(చూపించు_మూల్యం=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while చూపించు_మూల్యం not in లాగ్_వరుస[처음:]:
                    if time.monotonic() > 끝 or విధానం_మూల్యం.poll() is not None:
                        raise AssertionError('Missing ' + repr(చూపించు_మూల్యం) + '\n' + లాగ్_వరుస[처음:].decode('utf-8', 'replace'))
                    for ప్రవేశం_మూల్యం, _ in ఎంపిక_మూల్యం.select(.1):
                        డేటా = ప్రవేశం_మూల్యం.fileobj.read(65536)
                        if డేటా:
                            లాగ్_వరుస.extend(డేటా)
                return bytes(లాగ్_వరుస[처음:])
            def పంపు(పదం_పాఠం, చూపించు_మూల్యం=b'jkoros-native> '):
                처음 = len(లాగ్_వరుస)
                విధానం_మూల్యం.stdin.write(పదం_పాఠం.encode() + b'\n')
                విధానం_మూల్యం.stdin.flush()
                return వేచియుండు_స్థితి(చూపించు_మూల్యం, 처음)
            try:
                వేచియుండు_స్థితి()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return వ్రాయి_ఫైలు_డేటా(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                పంపు('load /relink.c', b'hex> ')
                for స్థాయి_సూచీ in range(0, len(시험), 64):
                    పంపు(시험[స్థాయి_సూచీ:స్థాయి_సూచీ+64].hex(), b'hex> ')
                assert b'LOADED' in పంపు('.')
                ప్రమాణం = పంపు('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in ప్రమాణం, ప్రమాణం
                ప్రమాణం = పంపు('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in ప్రమాణం and b'exit 0' in ప్రమాణం, ప్రమాణం
                నివేదిక_మూల్యం['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                ఎంపిక_మూల్యం.close()
                if విధానం_మూల్యం.poll() is None:
                    విధానం_మూల్యం.terminate()
                    try:
                        విధానం_మూల్యం.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        విధానం_మూల్యం.kill()
                        విధానం_మూల్యం.wait()
                (అవుట్పుట్ / 'guest.log').write_bytes(లాగ్_వరుస)
        నివేదిక_మూల్యం['passed'] = True
        print(json.dumps(నివేదిక_మూల్యం, ensure_ascii=False, indent=2))
    finally:
        (అవుట్పుట్ / 'report.json').write_text(json.dumps(నివేదిక_మూల్యం, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    నడుపుము()
