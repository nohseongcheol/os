"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def Cコンパイラ作成(根経路, 保管庫経路, Cコンパイラ, 連結器道具要素, 構成設定ビット列, 命令実行):
    結果データ = 根経路 / 'build/ccompiler'; 結果データ.mkdir(exist_ok=True)
    原本データ = 根経路 / 'Cコンパイラ'
    上流 = 根経路 / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    開発道具一式 = 根経路 / 'vendor/sdk'
    if not (開発道具一式/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    組込要素群 = sorted((開発道具一式/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 組込要素群: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    構成設定ビット列 = [設定値値 for 設定値値 in 構成設定ビット列 if 設定値値 != '-mgeneral-regs-only']
    包含引数 = ['-I', 原本データ, '-I', 上流, '-I', 根経路/'利用者', '-I', 結果データ, '-isystem', 開発道具一式/'usr/include']
    命令実行([Cコンパイラ]+構成設定ビット列+['-ffunction-sections','-fdata-sections']+包含引数+['-c',原本データ/'始動支援.c','-o',結果データ/'crt.o'])
    命令実行([Cコンパイラ]+構成設定ビット列+['-I',保管庫経路/'posix-kor/arm64-native/ヘッダー']+包含引数+['-c',原本データ/'事前翻訳実行環境.c','-o',結果データ/'aot-runtime.o'])
    素材一覧 = [('/sdk/include/'+データ位置.name,データ位置) for データ位置 in sorted((保管庫経路/'posix-kor/arm64-native/ヘッダー').glob('*.h'))]
    素材一覧 += [('/sdk/include/'+データ位置.name,データ位置) for データ位置 in sorted((上流/'include').glob('*.h'))]
    素材一覧 += [('/sdk/include/'+データ位置.name,データ位置) for データ位置 in sorted((原本データ/'開発ヘッダー群').glob('*.h'))]
    素材一覧 += [('/sdk/lib/start.o',根経路/'build/user/start.o'),('/sdk/lib/crt.o',結果データ/'crt.o'),('/sdk/lib/aot-runtime.o',結果データ/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',根経路/'build/libposix-kor-user.a')]
    ヘッダー値=['typedef struct { const char *名前; const unsigned char *データ; unsigned 容量; } コンパイラ資源;']
    for 序数添字,(_,経路) in enumerate(素材一覧):
        ヘッダー値.append('static const unsigned char 탑재자원_%d[] = {%s};'%(序数添字,','.join(str(一時データ) for 一時データ in 経路.read_bytes())))
    ヘッダー値.append('static const コンパイラ資源 コンパイラ資源一覧[] = {')
    for 序数添字,(名前,経路) in enumerate(素材一覧): ヘッダー値.append('{%s, 탑재자원_%d, %d},'%(json.dumps(名前,ensure_ascii=False),序数添字,経路.stat().st_size))
    ヘッダー値.append('};');(結果データ/'resources.h').write_text('\n'.join(ヘッダー値)+'\n',encoding='utf-8')
    宛先ファイル群=[]
    for 名前 in ('コンパイラ道具要素.c','実行環境支援.c','起動処理.c','事前用時間.c','復帰橋渡し.S'):
        宛先ファイル=結果データ/(Path(名前).stem+'.o');宛先ファイル群.append(宛先ファイル)
        命令実行([Cコンパイラ]+構成設定ビット列+['-ffunction-sections','-fdata-sections']+包含引数+['-c',原本データ/名前,'-o',宛先ファイル])
    実行形式ファイル=根経路/'build/user/cc.elf'
    命令実行([連結器道具要素,'--gc-sections','-T',根経路/'利用者/連結配置.ld','-z','max-page-size=4096','-o',実行形式ファイル,
         根経路/'build/user/start.o',根経路/'build/user/runtime.o']+宛先ファイル群+
         [根経路/'build/user'/名前 for 名前 in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[組込要素群[-1]])
