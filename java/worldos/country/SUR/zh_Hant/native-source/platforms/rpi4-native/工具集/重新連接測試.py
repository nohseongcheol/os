#!/usr/bin/env python3
"""分發值 자료만으로 LGPL 재연결과 수정한 TinyCC의 實際資料 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from 執行命令 import 項目根, 命令


def 運行():
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('--sdk', type=Path, default=項目根.parent / 'rpi4/build/rootfs')
    實參 = 解析器.parse_args()
    輸出 = 項目根 / 'build/verification/cosl-relink'
    輸出.mkdir(parents=True, exist_ok=True)
    報告值 = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((項目根 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 臨時值:
            路徑 = Path(臨時值)
            with tarfile.open(str(項目根 / 'dist/jkoros-native-relink.tar.gz')) as 組值:
                for 條目值 in 組值.getmembers():
                    if 路徑 not in (路徑 / 條目值.name).resolve().parents or 條目值.issym() or 條目值.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + 條目值.name)
                組值.extractall(str(路徑))
            原始碼 = 路徑 / 'jkoros-native-relink'
            def 重新連接端點(名稱, 參數列列表):
                with (輸出 / 名稱).open('wb') as 日誌記錄:
                    subprocess.run(['python3', 'relink.py'] + 參數列列表, cwd=str(原始碼),
                                   stdout=日誌記錄, stderr=subprocess.STDOUT, check=True, timeout=180)
            重新連接端點('original.log', ['--verify'])
            報告值['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            編譯器工具 = 原始碼 / 'vendor/tinycc/libtcc.c'
            主體文本 = 編譯器工具.read_text()
            位置 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert 主體文本.count(位置) == 1
            編譯器工具.write_text(主體文本.replace(位置, 位置 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            重新連接端點('modified-tinycc.log', ['--tinycc', '--sdk', str(實參.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            映像值 = 原始碼 / 'build/relinked/kernel8.img'
            報告值['modified_kernel_sha256'] = hashlib.sha256(映像值.read_bytes()).hexdigest()
            assert 報告值['modified_kernel_sha256'] != 報告值['kernel_sha256']
            報告值['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            參數列列表 = 命令()
            參數列列表[參數列列表.index('-kernel') + 1] = str(映像值)
            程序值 = subprocess.Popen(參數列列表 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            日誌記錄 = bytearray()
            選中狀態值 = selectors.DefaultSelector()
            選中狀態值.register(程序值.stdout, selectors.EVENT_READ)
            def 等待狀態狀態(顯示值=b'jkoros-native> ', 初始項目=0):
                結尾 = time.monotonic() + 40
                while 顯示值 not in 日誌記錄[初始項目:]:
                    if time.monotonic() > 結尾 or 程序值.poll() is not None:
                        raise AssertionError('Missing ' + repr(顯示值) + '\n' + 日誌記錄[初始項目:].decode('utf-8', 'replace'))
                    for 條目值, _ in 選中狀態值.select(.1):
                        資料 = 條目值.fileobj.read(65536)
                        if 資料:
                            日誌記錄.extend(資料)
                return bytes(日誌記錄[初始項目:])
            def 發送(機器字文本, 顯示值=b'jkoros-native> '):
                初始項目 = len(日誌記錄)
                程序值.stdin.write(機器字文本.encode() + b'\n')
                程序值.stdin.flush()
                return 等待狀態狀態(顯示值, 初始項目)
            try:
                等待狀態狀態()
                測試 = '#include <檔案ABI.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return 寫入檔案資料(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                發送('load /relink.c', b'hex> ')
                for 位置索引 in range(0, len(測試), 64):
                    發送(測試[位置索引:位置索引+64].hex(), b'hex> ')
                assert b'LOADED' in 發送('.')
                結果 = 發送('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 結果, 結果
                結果 = 發送('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 結果 and b'exit 0' in 結果, 結果
                報告值['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                選中狀態值.close()
                if 程序值.poll() is None:
                    程序值.terminate()
                    try:
                        程序值.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        程序值.kill()
                        程序值.wait()
                (輸出 / 'guest.log').write_bytes(日誌記錄)
        報告值['passed'] = True
        print(json.dumps(報告值, ensure_ascii=False, indent=2))
    finally:
        (輸出 / 'report.json').write_text(json.dumps(報告值, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    運行()
