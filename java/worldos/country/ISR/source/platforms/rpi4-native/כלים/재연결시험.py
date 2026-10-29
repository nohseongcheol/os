#!/usr/bin/env python3
"""הפצה_ערך 자료만으로 LGPL 재연결과 수정한 TinyCC의 בפועל_נתונים 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from לבצע_פקודה import לשקף_בסיס, פקודה


def הפעלה():
    מנתח_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    מנתח_48ee4b1b.add_argument('--sdk', type=Path, default=לשקף_בסיס.parent / 'rpi4/build/rootfs')
    ארגומנטים = מנתח_48ee4b1b.parse_args()
    פלטטקסט = לשקף_בסיס / 'build/verification/cosl-relink'
    פלטטקסט.mkdir(parents=True, exist_ok=True)
    דוח_ערך_ddf2aaf3 = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((לשקף_בסיס / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            נתיב = Path(임시)
            with tarfile.open(str(לשקף_בסיס / 'dist/jkoros-native-relink.tar.gz')) as לקבץ_ערך:
                for ערך_ערך in לקבץ_ערך.getmembers():
                    if נתיב not in (נתיב / ערך_ערך.name).resolve().parents or ערך_ערך.issym() or ערך_ערך.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ערך_ערך.name)
                לקבץ_ערך.extractall(str(נתיב))
            קודמקור = נתיב / 'jkoros-native-relink'
            def 재연결(שם, 인수들):
                with (פלטטקסט / שם).open('wb') as לרשום_שיא:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(קודמקור),
                                   stdout=לרשום_שיא, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            דוח_ערך_ddf2aaf3['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            מהדר_כלי = קודמקור / 'vendor/tinycc/libtcc.c'
            גוף_הטקסט = מהדר_כלי.read_text()
            מיקום = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert גוף_הטקסט.count(מיקום) == 1
            מהדר_כלי.write_text(גוף_הטקסט.replace(מיקום, מיקום + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(ארגומנטים.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            תמונה_ערך = קודמקור / 'build/relinked/kernel8.img'
            דוח_ערך_ddf2aaf3['modified_kernel_sha256'] = hashlib.sha256(תמונה_ערך.read_bytes()).hexdigest()
            assert דוח_ערך_ddf2aaf3['modified_kernel_sha256'] != דוח_ערך_ddf2aaf3['kernel_sha256']
            דוח_ערך_ddf2aaf3['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = פקודה()
            인수들[인수들.index('-kernel') + 1] = str(תמונה_ערך)
            תהליך_ערך = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            לרשום_שיא = bytearray()
            קטע_נבחר_ערך = selectors.DefaultSelector()
            קטע_נבחר_ערך.register(תהליך_ערך.stdout, selectors.EVENT_READ)
            def מצב_המתנה(הופעה_ערך=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while הופעה_ערך not in לרשום_שיא[처음:]:
                    if time.monotonic() > 끝 or תהליך_ערך.poll() is not None:
                        raise AssertionError('Missing ' + repr(הופעה_ערך) + '\n' + לרשום_שיא[처음:].decode('utf-8', 'replace'))
                    for ערך_ערך, _ in קטע_נבחר_ערך.select(.1):
                        נתונים = ערך_ערך.fileobj.read(65536)
                        if נתונים:
                            לרשום_שיא.extend(נתונים)
                return bytes(לרשום_שיא[처음:])
            def שלח(מילים_טקסט, הופעה_ערך=b'jkoros-native> '):
                처음 = len(לרשום_שיא)
                תהליך_ערך.stdin.write(מילים_טקסט.encode() + b'\n')
                תהליך_ערך.stdin.flush()
                return מצב_המתנה(הופעה_ערך, 처음)
            try:
                מצב_המתנה()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return כתיבה_קובץ_נתונים(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                שלח('load /relink.c', b'hex> ')
                for עמדה_מדד in range(0, len(시험), 64):
                    שלח(시험[עמדה_מדד:עמדה_מדד+64].hex(), b'hex> ')
                assert b'LOADED' in שלח('.')
                תוצאה = שלח('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in תוצאה, תוצאה
                תוצאה = שלח('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in תוצאה and b'exit 0' in תוצאה, תוצאה
                דוח_ערך_ddf2aaf3['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                קטע_נבחר_ערך.close()
                if תהליך_ערך.poll() is None:
                    תהליך_ערך.terminate()
                    try:
                        תהליך_ערך.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        תהליך_ערך.kill()
                        תהליך_ערך.wait()
                (פלטטקסט / 'guest.log').write_bytes(לרשום_שיא)
        דוח_ערך_ddf2aaf3['passed'] = True
        print(json.dumps(דוח_ערך_ddf2aaf3, ensure_ascii=False, indent=2))
    finally:
        (פלטטקסט / 'report.json').write_text(json.dumps(דוח_ערך_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    הפעלה()
