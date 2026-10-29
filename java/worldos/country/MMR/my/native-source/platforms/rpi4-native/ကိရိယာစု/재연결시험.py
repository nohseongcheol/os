#!/usr/bin/env python3
"""ဖြန့်ချိမှုတန်ဖိုး 자료만으로 LGPL 재연결과 수정한 TinyCC의 တကယ့်ဒေတာ 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from စက်မောင်း import စီမံကိန်းအမြစ်, အမိန့်


def လုပ်ဆောင်():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=စီမံကိန်းအမြစ်.parent / 'rpi4/build/rootfs')
    အချက်များ = 해석기.parse_args()
    အထွက် = စီမံကိန်းအမြစ် / 'build/verification/cosl-relink'
    အထွက်.mkdir(parents=True, exist_ok=True)
    အစီရင်ခံစာတန်ဖိုး = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((စီမံကိန်းအမြစ် / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as ယာယီတန်ဖိုး:
            လမ်း = Path(ယာယီတန်ဖိုး)
            with tarfile.open(str(စီမံကိန်းအမြစ် / 'dist/jkoros-native-relink.tar.gz')) as အုပ်စုတန်ဖိုး:
                for အချက်တန်ဖိုး in အုပ်စုတန်ဖိုး.getmembers():
                    if လမ်း not in (လမ်း / အချက်တန်ဖိုး.name).resolve().parents or အချက်တန်ဖိုး.issym() or အချက်တန်ဖိုး.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + အချက်တန်ဖိုး.name)
                အုပ်စုတန်ဖိုး.extractall(str(လမ်း))
            မူရင်းကုဒ် = လမ်း / 'jkoros-native-relink'
            def 재연결(အမည်, ပေးအချက်များစာရင်း):
                with (အထွက် / အမည်).open('wb') as မှတ်တမ်းမှတ်တမ်းတစ်ခု:
                    subprocess.run(['python3', 'relink.py'] + ပေးအချက်များစာရင်း, cwd=str(မူရင်းကုဒ်),
                                   stdout=မှတ်တမ်းမှတ်တမ်းတစ်ခု, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            အစီရင်ခံစာတန်ဖိုး['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            ဘာသာပြန်စက်ကိရိယာတစ်ခု = မူရင်းကုဒ် / 'vendor/tinycc/libtcc.c'
            ကိုယ်ထည်စာသား = ဘာသာပြန်စက်ကိရိယာတစ်ခု.read_text()
            နေရာ = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert ကိုယ်ထည်စာသား.count(နေရာ) == 1
            ဘာသာပြန်စက်ကိရိယာတစ်ခု.write_text(ကိုယ်ထည်စာသား.replace(နေရာ, နေရာ + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(အချက်များ.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            စက်ပုံရိပ်တန်ဖိုး = မူရင်းကုဒ် / 'build/relinked/kernel8.img'
            အစီရင်ခံစာတန်ဖိုး['modified_kernel_sha256'] = hashlib.sha256(စက်ပုံရိပ်တန်ဖိုး.read_bytes()).hexdigest()
            assert အစီရင်ခံစာတန်ဖိုး['modified_kernel_sha256'] != အစီရင်ခံစာတန်ဖိုး['kernel_sha256']
            အစီရင်ခံစာတန်ဖိုး['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            ပေးအချက်များစာရင်း = အမိန့်()
            ပေးအချက်များစာရင်း[ပေးအချက်များစာရင်း.index('-kernel') + 1] = str(စက်ပုံရိပ်တန်ဖိုး)
            လုပ်ငန်းစဉ် = subprocess.Popen(ပေးအချက်များစာရင်း + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            မှတ်တမ်းမှတ်တမ်းတစ်ခု = bytearray()
            ရွေးချယ်မှုတန်ဖိုး = selectors.DefaultSelector()
            ရွေးချယ်မှုတန်ဖိုး.register(လုပ်ငန်းစဉ်.stdout, selectors.EVENT_READ)
            def အခြေအနေစောင့်(တန်ဖိုးပြသ=b'jkoros-native> ', အစဦးအချက်အလက်တစ်ခု=0):
                အဆုံး = time.monotonic() + 40
                while တန်ဖိုးပြသ not in မှတ်တမ်းမှတ်တမ်းတစ်ခု[အစဦးအချက်အလက်တစ်ခု:]:
                    if time.monotonic() > အဆုံး or လုပ်ငန်းစဉ်.poll() is not None:
                        raise AssertionError('Missing ' + repr(တန်ဖိုးပြသ) + '\n' + မှတ်တမ်းမှတ်တမ်းတစ်ခု[အစဦးအချက်အလက်တစ်ခု:].decode('utf-8', 'replace'))
                    for အချက်တန်ဖိုး, _ in ရွေးချယ်မှုတန်ဖိုး.select(.1):
                        ဒေတာ = အချက်တန်ဖိုး.fileobj.read(65536)
                        if ဒေတာ:
                            မှတ်တမ်းမှတ်တမ်းတစ်ခု.extend(ဒေတာ)
                return bytes(မှတ်တမ်းမှတ်တမ်းတစ်ခု[အစဦးအချက်အလက်တစ်ခု:])
            def ပို့(စကားလုံးစာသား, တန်ဖိုးပြသ=b'jkoros-native> '):
                အစဦးအချက်အလက်တစ်ခု = len(မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                လုပ်ငန်းစဉ်.stdin.write(စကားလုံးစာသား.encode() + b'\n')
                လုပ်ငန်းစဉ်.stdin.flush()
                return အခြေအနေစောင့်(တန်ဖိုးပြသ, အစဦးအချက်အလက်တစ်ခု)
            try:
                အခြေအနေစောင့်()
                စမ်းသပ်မှု = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ဖိုင်ဒေတာရေး(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                ပို့('load /relink.c', b'hex> ')
                for နေရာအညွှန်းကိန်း in range(0, len(စမ်းသပ်မှု), 64):
                    ပို့(စမ်းသပ်မှု[နေရာအညွှန်းကိန်း:နေရာအညွှန်းကိန်း+64].hex(), b'hex> ')
                assert b'LOADED' in ပို့('.')
                ရလဒ် = ပို့('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in ရလဒ်, ရလဒ်
                ရလဒ် = ပို့('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in ရလဒ် and b'exit 0' in ရလဒ်, ရလဒ်
                အစီရင်ခံစာတန်ဖိုး['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                ရွေးချယ်မှုတန်ဖိုး.close()
                if လုပ်ငန်းစဉ်.poll() is None:
                    လုပ်ငန်းစဉ်.terminate()
                    try:
                        လုပ်ငန်းစဉ်.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        လုပ်ငန်းစဉ်.kill()
                        လုပ်ငန်းစဉ်.wait()
                (အထွက် / 'guest.log').write_bytes(မှတ်တမ်းမှတ်တမ်းတစ်ခု)
        အစီရင်ခံစာတန်ဖိုး['passed'] = True
        print(json.dumps(အစီရင်ခံစာတန်ဖိုး, ensure_ascii=False, indent=2))
    finally:
        (အထွက် / 'report.json').write_text(json.dumps(အစီရင်ခံစာတန်ဖိုး, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    လုပ်ဆောင်()
