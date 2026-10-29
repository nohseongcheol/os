"""독립된 內建 ABI ELF64와 로더 拒絕值 測試 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 構建Python import 創建Python
from 構建Java庫 import 創建Java庫
from 構建C編譯器 import 創建C編譯器


def 創建用戶空間(根路徑, 代碼庫路徑, C編譯器, Cpp編譯器, 鏈接器工具, 存檔工具, 配置項位元列, 執行命令):
    配置項位元列 = [設置值 for 設置值 in 配置項位元列 if 設置值 != '-mgeneral-regs-only']
    構建路徑 = 根路徑 / 'build'
    輸出結果 = 構建路徑 / 'user'
    輸出結果.mkdir(exist_ok=True)
    原始資料 = 根路徑 / '使用者'
    POSIX = 代碼庫路徑 / 'posix-kor/arm64-native'
    包含路徑 = ['-I', 原始資料, '-I', POSIX / '頭文件', '-I', 輸出結果]
    for 編譯器工具, 附加區域, 路徑, 名稱 in [
            (C編譯器, [], 原始資料 / '運行.S', 'start.o'),
            (C編譯器, ['-std=c11'], 原始資料 / '執行命令.c', 'runtime.o'),
            (C編譯器, ['-std=c11'], POSIX / '用戶橋接.c', 'posix.o'),
            (Cpp編譯器, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 原始資料 / '檔案例.cpp', 'demo.o'),
            (Cpp編譯器, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 原始資料 / '通信範例.cpp', 'network.o'),
            (C編譯器, ['-std=c11'], 原始資料 / '保護測試.c', 'fault.o'),
            (C編譯器, ['-std=c11'], 原始資料 / '編輯器.c', 'vi.o')]:
        執行命令([編譯器工具] + 配置項位元列 + 附加區域 + 包含路徑 + ['-Wall', '-Wextra', '-Werror', '-c', 路徑, '-o', 輸出結果 / 名稱])
    執行命令([存檔工具, 'rcs', 構建路徑 / 'libposix-kor-user.a', 輸出結果 / 'posix.o'])
    for 名稱 in ('demo', 'fault', 'network', 'vi'):
        執行命令([鏈接器工具, '-T', 原始資料 / '鏈接佈局.ld', '-z', 'max-page-size=4096', '-o', 輸出結果 / (名稱 + '.elf'),
             輸出結果 / 'start.o', 輸出結果 / 'runtime.o', 輸出結果 / (名稱 + '.o'), 構建路徑 / 'libposix-kor-user.a'])
    創建Java庫(根路徑, 執行命令)
    # 기존 內建 Java 編譯器/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(構建路徑)) as 工作中路徑:
        類別路徑 = Path(工作中路徑)
        執行命令(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', 類別路徑, '-sourcepath', 類別路徑, '-d', 類別路徑] +
            [資料位置 for 資料位置 in sorted((代碼庫路徑 / 'os/使用者/Java').glob('*.java')) if 資料位置.name != 'Java虛擬機器.java'] + sorted((原始資料 / 'Java').glob('*.java')))
        執行命令(['sh', 代碼庫路徑 / 'compiler/提前所屬時間.sh', '--entry', '工具條目.運行',
             '--profile', 'user', '--heap-words', '1048576', '-o', 輸出結果 / 'java-tools.c'] + sorted(類別路徑.glob('*.class')))
    解壓庫 = 根路徑 / 'vendor/uzlib'
    for 路徑, 名稱 in [(輸出結果 / 'java-tools.c', 'java-tools.o'), (原始資料 / 'Java橋接.c', 'java-link.o'),
                       (原始資料 / '軟件包.c', 'jar.o')] + [(解壓庫 / (名稱 + '.c'), 名稱 + '.o') for 名稱 in ('tinflate', 'crc32', 'adler32')]:
        執行命令([C編譯器] + 配置項位元列 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 解壓庫] + 包含路徑 + ['-c', 路徑, '-o', 輸出結果 / 名稱])
    執行命令([鏈接器工具, '-T', 原始資料 / '鏈接佈局.ld', '-z', 'max-page-size=4096', '-o', 輸出結果 / 'java-tools.elf'] +
        [輸出結果 / 名稱 for 名稱 in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    創建Python(根路徑, C編譯器, 鏈接器工具)
    創建C編譯器(根路徑, 代碼庫路徑, C編譯器, 鏈接器工具, 配置項位元列, 執行命令)
    有效 = (輸出結果 / 'demo.elf').read_bytes()
    程式標頭偏移 = struct.unpack_from('<Q', 有效, 32)[0]
    標頭列表 = [程式標頭偏移 + 項目個數 * 56 for 項目個數 in range(struct.unpack_from('<H', 有效, 56)[0])]
    載入項 = [資料位置 for 資料位置 in 標頭列表 if struct.unpack_from('<I', 有效, 資料位置)[0] == 1]
    文本, 資料 = 載入項[:2]
    命令地址 = struct.unpack_from('<Q', 有效, 文本 + 16)[0]
    資料地址 = struct.unpack_from('<Q', 有效, 資料 + 16)[0]
    呼叫ABI = 有效.index(b'JKOROS\0')
    測試情況 = [('empty', b''), ('short', 有效[:63])]
    修改列 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', 命令地址 + 1), ('data-entry', 24, 'Q', 資料地址),
               ('outside-file', 文本 + 32, 'Q', len(有效) + 1), ('short-memory', 文本 + 40, 'Q', 1),
               ('kernel-address', 文本 + 16, 'Q', 0x80000), ('memory-overflow', 文本 + 40, 'Q', 2**64 - 1),
               ('writable-code', 文本 + 4, 'I', 7), ('missing-abi', 呼叫ABI, 'B', ord('X')),
               ('wrong-abi', 呼叫ABI + 8, 'I', 2), ('dynamic', 文本, 'I', 2),
               ('unaligned-load', 文本 + 16, 'Q', 命令地址 + 8),
               ('overlap', 資料 + 16, 'Q', 命令地址)]
    for 名稱, 偏移值, 資料格式, 值 in 修改列:
        已更改 = bytearray(有效); struct.pack_into('<' + 資料格式, 已更改, 偏移值, 值)
        測試情況.append((名稱, bytes(已更改)))
    二進制塊集 = [(名稱.replace('-', '_'), 輸出結果 / (名稱 + '.elf')) for 名稱 in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 查找索引, (名稱, 載荷數據資料) in enumerate(測試情況):
        路徑 = 輸出結果 / ('invalid-{}.elf'.format(名稱)); 路徑.write_bytes(載荷數據資料)
        二進制塊集.append(('invalid_{}'.format(查找索引), 路徑))
    彙編, 標頭值 = ['.section .rodata.user,"a"'], []
    大小列 = {}
    for 名稱, 路徑 in 二進制塊集:
        符號值 = 'user_blob_' + 名稱
        大小列[名稱] = 路徑.stat().st_size
        # 생성한 對端值 경로만 넣어 프로젝트 경로의 공백/引號 영향을 피한다.
        彙編 += ['.balign 16', '.global ' + 符號值, 符號值 + ':', '.incbin "{}"'.format(路徑.relative_to(根路徑))]
        標頭值.append('extern const unsigned char {}[];'.format(符號值))
    彙編.append('.section .note.GNU-stack,"",%progbits')
    標頭值 += ['static const 執行條目 可執行文件條目列[] = {', '{user_blob_demo, %d, 0},' % 大小列['demo']]
    標頭值 += ['{user_blob_fault, %d, %d},' % (大小列['fault'], 已轉發值) for 已轉發值 in range(8)]
    標頭值 += ['{user_blob_network, %d, 0},' % 大小列['network']]
    標頭值 += ['{user_blob_java_tools, %d, %d},' % (大小列['java_tools'], 方法模式) for 方法模式 in (0, 1)]
    標頭值 += ['{user_blob_python, %d, 0},' % 大小列['python'], '{user_blob_vi, %d, 0},' % 大小列['vi']]
    標頭值 += ['{user_blob_java_tools, %d, 2},' % 大小列['java_tools']]
    標頭值 += ['{user_blob_cc, %d, 0},' % 大小列['cc']]
    標頭值 += ['{user_blob_cc, %d, 1},' % 大小列['cc']]
    標頭值 += ['};', 'static const 執行條目 無效可執行項列[] = {']
    標頭值 += ['{user_blob_invalid_%d, %d, 0},' % (序數索引, len(載荷數據資料)) for 序數索引, (_, 載荷數據資料) in enumerate(測試情況)]
    標頭值 += ['};']
    (構建路徑 / 'programs.S').write_text('\n'.join(彙編) + '\n')
    (構建路徑 / 'programs.h').write_text('\n'.join(標頭值) + '\n')
    (輸出結果 / 'invalid-cases.txt').write_text('\n'.join(名稱 for 名稱, _ in 測試情況) + '\n')
    執行命令([C編譯器] + 配置項位元列 + ['-c', 構建路徑 / 'programs.S', '-o', 構建路徑 / 'programs.o'])
