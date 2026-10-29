#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 واقعی_داده_ها 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from اجرا_فرمان import نمایش_دادن_جذر, فرمان


def اجرا_2():
    مفسر_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    مفسر_48ee4b1b.add_argument('--sdk', type=Path, default=نمایش_دادن_جذر.parent / 'rpi4/build/rootfs')
    نشانوندها = مفسر_48ee4b1b.parse_args()
    خروجی = نمایش_دادن_جذر / 'build/verification/cosl-relink'
    خروجی.mkdir(parents=True, exist_ok=True)
    گزارش_مقدار = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((نمایش_دادن_جذر / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            مسیر = Path(임시)
            with tarfile.open(str(نمایش_دادن_جذر / 'dist/jkoros-native-relink.tar.gz')) as گروه_مقدار:
                for ورودی_مقدار in گروه_مقدار.getmembers():
                    if مسیر not in (مسیر / ورودی_مقدار.name).resolve().parents or ورودی_مقدار.issym() or ورودی_مقدار.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ورودی_مقدار.name)
                گروه_مقدار.extractall(str(مسیر))
            مبداء = مسیر / 'jkoros-native-relink'
            def 재연결(نام, 인수들):
                with (خروجی / نام).open('wb') as واقعه_نگار_ردیف:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(مبداء),
                                   stdout=واقعه_نگار_ردیف, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            گزارش_مقدار['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = مبداء / 'vendor/tinycc/libtcc.c'
            متن_اصلی = 번역기.read_text()
            مرتب_کردن = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert متن_اصلی.count(مرتب_کردن) == 1
            번역기.write_text(متن_اصلی.replace(مرتب_کردن, مرتب_کردن + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(نشانوندها.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            عکس_مقدار = مبداء / 'build/relinked/kernel8.img'
            گزارش_مقدار['modified_kernel_sha256'] = hashlib.sha256(عکس_مقدار.read_bytes()).hexdigest()
            assert گزارش_مقدار['modified_kernel_sha256'] != گزارش_مقدار['kernel_sha256']
            گزارش_مقدار['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = فرمان()
            인수들[인수들.index('-kernel') + 1] = str(عکس_مقدار)
            فرآیند_مقدار = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            واقعه_نگار_ردیف = bytearray()
            مورد_انتخابی_مقدار = selectors.DefaultSelector()
            مورد_انتخابی_مقدار.register(فرآیند_مقدار.stdout, selectors.EVENT_READ)
            def منتظر_ماندن_وضعیت(نمایش_مقدار=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while نمایش_مقدار not in واقعه_نگار_ردیف[처음:]:
                    if time.monotonic() > 끝 or فرآیند_مقدار.poll() is not None:
                        raise AssertionError('Missing ' + repr(نمایش_مقدار) + '\n' + واقعه_نگار_ردیف[처음:].decode('utf-8', 'replace'))
                    for ورودی_مقدار, _ in مورد_انتخابی_مقدار.select(.1):
                        داده_ها = ورودی_مقدار.fileobj.read(65536)
                        if داده_ها:
                            واقعه_نگار_ردیف.extend(داده_ها)
                return bytes(واقعه_نگار_ردیف[처음:])
            def ارسال(کلمات_متن, نمایش_مقدار=b'jkoros-native> '):
                처음 = len(واقعه_نگار_ردیف)
                فرآیند_مقدار.stdin.write(کلمات_متن.encode() + b'\n')
                فرآیند_مقدار.stdin.flush()
                return منتظر_ماندن_وضعیت(نمایش_مقدار, 처음)
            try:
                منتظر_ماندن_وضعیت()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return نوشتن_فایل_داده_ها(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                ارسال('load /relink.c', b'hex> ')
                for مرتب_کردن_فهرست in range(0, len(시험), 64):
                    ارسال(시험[مرتب_کردن_فهرست:مرتب_کردن_فهرست+64].hex(), b'hex> ')
                assert b'LOADED' in ارسال('.')
                سنجش = ارسال('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in سنجش, سنجش
                سنجش = ارسال('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in سنجش and b'exit 0' in سنجش, سنجش
                گزارش_مقدار['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                مورد_انتخابی_مقدار.close()
                if فرآیند_مقدار.poll() is None:
                    فرآیند_مقدار.terminate()
                    try:
                        فرآیند_مقدار.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        فرآیند_مقدار.kill()
                        فرآیند_مقدار.wait()
                (خروجی / 'guest.log').write_bytes(واقعه_نگار_ردیف)
        گزارش_مقدار['passed'] = True
        print(json.dumps(گزارش_مقدار, ensure_ascii=False, indent=2))
    finally:
        (خروجی / 'report.json').write_text(json.dumps(گزارش_مقدار, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    اجرا_2()
