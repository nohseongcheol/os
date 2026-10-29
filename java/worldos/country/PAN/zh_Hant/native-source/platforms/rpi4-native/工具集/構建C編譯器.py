"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 創建C編譯器(根路徑, 代碼庫路徑, C編譯器, 鏈接器工具, 配置項位元列, 執行命令):
    結果資料 = 根路徑 / 'build/ccompiler'; 結果資料.mkdir(exist_ok=True)
    原始資料 = 根路徑 / 'C編譯器'
    上游 = 根路徑 / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    開發工具套件 = 根路徑 / 'vendor/sdk'
    if not (開發工具套件/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    內建項集 = sorted((開發工具套件/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 內建項集: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    配置項位元列 = [設置值 for 設置值 in 配置項位元列 if 設置值 != '-mgeneral-regs-only']
    包含項 = ['-I', 原始資料, '-I', 上游, '-I', 根路徑/'使用者', '-I', 結果資料, '-isystem', 開發工具套件/'usr/include']
    執行命令([C編譯器]+配置項位元列+['-ffunction-sections','-fdata-sections']+包含項+['-c',原始資料/'啓動支持.c','-o',結果資料/'crt.o'])
    執行命令([C編譯器]+配置項位元列+['-I',代碼庫路徑/'posix-kor/arm64-native/頭文件']+包含項+['-c',原始資料/'提前編譯運行時.c','-o',結果資料/'aot-runtime.o'])
    資源素材 = [('/sdk/include/'+資料位置.name,資料位置) for 資料位置 in sorted((代碼庫路徑/'posix-kor/arm64-native/頭文件').glob('*.h'))]
    資源素材 += [('/sdk/include/'+資料位置.name,資料位置) for 資料位置 in sorted((上游/'include').glob('*.h'))]
    資源素材 += [('/sdk/include/'+資料位置.name,資料位置) for 資料位置 in sorted((原始資料/'開發標頭集').glob('*.h'))]
    資源素材 += [('/sdk/lib/start.o',根路徑/'build/user/start.o'),('/sdk/lib/crt.o',結果資料/'crt.o'),('/sdk/lib/aot-runtime.o',結果資料/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',根路徑/'build/libposix-kor-user.a')]
    標頭值=['typedef struct { const char *名稱; const unsigned char *資料; unsigned 大小; } 編譯器資源;']
    for 序數索引,(_,路徑) in enumerate(資源素材):
        標頭值.append('static const unsigned char 탑재자원_%d[] = {%s};'%(序數索引,','.join(str(臨時資料) for 臨時資料 in 路徑.read_bytes())))
    標頭值.append('static const 編譯器資源 編譯器資源集[] = {')
    for 序數索引,(名稱,路徑) in enumerate(資源素材): 標頭值.append('{%s, 탑재자원_%d, %d},'%(json.dumps(名稱,ensure_ascii=False),序數索引,路徑.stat().st_size))
    標頭值.append('};');(結果資料/'resources.h').write_text('\n'.join(標頭值)+'\n',encoding='utf-8')
    目的地址檔案集=[]
    for 名稱 in ('編譯器工具.c','運行時支持.c','運行.c','提前所屬時間.c','發回橋接.S'):
        目的地址檔案=結果資料/(Path(名稱).stem+'.o');目的地址檔案集.append(目的地址檔案)
        執行命令([C編譯器]+配置項位元列+['-ffunction-sections','-fdata-sections']+包含項+['-c',原始資料/名稱,'-o',目的地址檔案])
    可執行文件檔案=根路徑/'build/user/cc.elf'
    執行命令([鏈接器工具,'--gc-sections','-T',根路徑/'使用者/鏈接佈局.ld','-z','max-page-size=4096','-o',可執行文件檔案,
         根路徑/'build/user/start.o',根路徑/'build/user/runtime.o']+目的地址檔案集+
         [根路徑/'build/user'/名稱 for 名稱 in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[內建項集[-1]])
