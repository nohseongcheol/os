#!/usr/bin/env python3
"""توزيع_قيمة 자료만으로 LGPL 재연결과 수정한 TinyCC의 الفعلي_بيانات 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from ينفذ_أمر import يعرض_جذر, أمر


def تشغيل():
    المحلل_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    المحلل_48ee4b1b.add_argument('--sdk', type=Path, default=يعرض_جذر.parent / 'rpi4/build/rootfs')
    وسائط = المحلل_48ee4b1b.parse_args()
    مخرجات = يعرض_جذر / 'build/verification/cosl-relink'
    مخرجات.mkdir(parents=True, exist_ok=True)
    إبلاغ_قيمة = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((يعرض_جذر / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            مسار = Path(임시)
            with tarfile.open(str(يعرض_جذر / 'dist/jkoros-native-relink.tar.gz')) as يجمع_قيمة:
                for إدخال_قيمة_962f286b in يجمع_قيمة.getmembers():
                    if مسار not in (مسار / إدخال_قيمة_962f286b.name).resolve().parents or إدخال_قيمة_962f286b.issym() or إدخال_قيمة_962f286b.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + إدخال_قيمة_962f286b.name)
                يجمع_قيمة.extractall(str(مسار))
            مصدر = مسار / 'jkoros-native-relink'
            def 재연결(اسم, 인수들):
                with (مخرجات / اسم).open('wb') as سجل_سجل:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(مصدر),
                                   stdout=سجل_سجل, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            إبلاغ_قيمة['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            محول_برمجي_أداة = مصدر / 'vendor/tinycc/libtcc.c'
            نص_أساسي = محول_برمجي_أداة.read_text()
            موضع = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert نص_أساسي.count(موضع) == 1
            محول_برمجي_أداة.write_text(نص_أساسي.replace(موضع, موضع + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(وسائط.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            صورة_قيمة = مصدر / 'build/relinked/kernel8.img'
            إبلاغ_قيمة['modified_kernel_sha256'] = hashlib.sha256(صورة_قيمة.read_bytes()).hexdigest()
            assert إبلاغ_قيمة['modified_kernel_sha256'] != إبلاغ_قيمة['kernel_sha256']
            إبلاغ_قيمة['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = أمر()
            인수들[인수들.index('-kernel') + 1] = str(صورة_قيمة)
            عملية_قيمة = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            سجل_سجل = bytearray()
            تحديد_قيمة = selectors.DefaultSelector()
            تحديد_قيمة.register(عملية_قيمة.stdout, selectors.EVENT_READ)
            def حالة_انتظار(عرض_قيمة_487749b8=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while عرض_قيمة_487749b8 not in سجل_سجل[처음:]:
                    if time.monotonic() > 끝 or عملية_قيمة.poll() is not None:
                        raise AssertionError('Missing ' + repr(عرض_قيمة_487749b8) + '\n' + سجل_سجل[처음:].decode('utf-8', 'replace'))
                    for إدخال_قيمة_962f286b, _ in تحديد_قيمة.select(.1):
                        بيانات = إدخال_قيمة_962f286b.fileobj.read(65536)
                        if بيانات:
                            سجل_سجل.extend(بيانات)
                return bytes(سجل_سجل[처음:])
            def يرسل(الكلمات_نص, عرض_قيمة_487749b8=b'jkoros-native> '):
                처음 = len(سجل_سجل)
                عملية_قيمة.stdin.write(الكلمات_نص.encode() + b'\n')
                عملية_قيمة.stdin.flush()
                return حالة_انتظار(عرض_قيمة_487749b8, 처음)
            try:
                حالة_انتظار()
                اختبارات = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return كتابة_ملف_بيانات(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                يرسل('load /relink.c', b'hex> ')
                for منصب_فهرس in range(0, len(اختبارات), 64):
                    يرسل(اختبارات[منصب_فهرس:منصب_فهرس+64].hex(), b'hex> ')
                assert b'LOADED' in يرسل('.')
                نتيجة = يرسل('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in نتيجة, نتيجة
                نتيجة = يرسل('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in نتيجة and b'exit 0' in نتيجة, نتيجة
                إبلاغ_قيمة['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                تحديد_قيمة.close()
                if عملية_قيمة.poll() is None:
                    عملية_قيمة.terminate()
                    try:
                        عملية_قيمة.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        عملية_قيمة.kill()
                        عملية_قيمة.wait()
                (مخرجات / 'guest.log').write_bytes(سجل_سجل)
        إبلاغ_قيمة['passed'] = True
        print(json.dumps(إبلاغ_قيمة, ensure_ascii=False, indent=2))
    finally:
        (مخرجات / 'report.json').write_text(json.dumps(إبلاغ_قيمة, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    تشغيل()
