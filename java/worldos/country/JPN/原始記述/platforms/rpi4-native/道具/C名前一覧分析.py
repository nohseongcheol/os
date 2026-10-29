#!/usr/bin/env python3
"""libclang 宣言·参照 위치를 수집한다. 外部値 헤더의 멤버는 변환하지 않는다."""
import ctypes as Cソース
import hashlib
import json
from pathlib import Path

計画根 = Path(__file__).resolve().parents[1]
実装 = Cソース.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class 文字列(Cソース.Structure): _fields_ = [('データ',Cソース.c_void_p),('値表示',Cソース.c_uint)]
class カーソル値(Cソース.Structure): _fields_ = [('種別値',Cソース.c_uint),('補助値',Cソース.c_int),('データ',Cソース.c_void_p*3)]
class 位置(Cソース.Structure): _fields_ = [('データ',Cソース.c_void_p*2),('変位量値',Cソース.c_uint)]
def 関数(名前, 復帰結果, *引数):
    入口値 = getattr(実装, 名前); 入口値.restype = 復帰結果; 入口値.argtypes = list(引数); return 入口値
本文取得 = 関数('clang_getCString',Cソース.c_char_p,文字列)
本文解放 = 関数('clang_disposeString',None,文字列)
def 文(値):
    結果 = (本文取得(値) or b'').decode('utf-8'); 本文解放(値); return 結果
名前取得 = 関数('clang_getCursorSpelling',文字列,カーソル値)
参照取得 = 関数('clang_getCursorReferenced',カーソル値,カーソル値)
位置取得 = 関数('clang_getCursorLocation',位置,カーソル値)
ファイル位置 = 関数('clang_getFileLocation',None,位置,Cソース.POINTER(Cソース.c_void_p),Cソース.POINTER(Cソース.c_uint),Cソース.POINTER(Cソース.c_uint),Cソース.POINTER(Cソース.c_uint))
ファイル入口名前 = 関数('clang_getFileName',文字列,Cソース.c_void_p)
一意名前 = 関数('clang_getCursorUSR',文字列,カーソル値)
接続状態種別 = 関数('clang_getCursorLinkage',Cソース.c_uint,カーソル値)
訪問済み型 = Cソース.CFUNCTYPE(Cソース.c_uint,カーソル値,カーソル値,Cソース.c_void_p)
値訪問 = 関数('clang_visitChildren',Cソース.c_uint,カーソル値,訪問済み型,Cソース.c_void_p)
生成 = 関数('clang_createIndex',Cソース.c_void_p,Cソース.c_int,Cソース.c_int)
値分析 = 関数('clang_parseTranslationUnit',Cソース.c_void_p,Cソース.c_void_p,Cソース.c_char_p,Cソース.POINTER(Cソース.c_char_p),Cソース.c_int,Cソース.c_void_p,Cソース.c_uint,Cソース.c_uint)
根値 = 関数('clang_getTranslationUnitCursor',カーソル値,Cソース.c_void_p)
脱出プログラム = 関数('clang_disposeTranslationUnit',None,Cソース.c_void_p)
診断個数 = 関数('clang_getNumDiagnostics',Cソース.c_uint,Cソース.c_void_p)
診断取得 = 関数('clang_getDiagnostic',Cソース.c_void_p,Cソース.c_void_p,Cソース.c_uint)
重大度値 = 関数('clang_getDiagnosticSeverity',Cソース.c_uint,Cソース.c_void_p)
診断メッセージ = 関数('clang_getDiagnosticSpelling',文字列,Cソース.c_void_p)
診断解放 = 関数('clang_disposeDiagnostic',None,Cソース.c_void_p)

def 位置添字(入口値):
    ファイル = Cソース.c_void_p(); 行 = Cソース.c_uint(); 槽入口 = Cソース.c_uint(); 変位量値 = Cソース.c_uint()
    ファイル位置(位置取得(入口値),Cソース.byref(ファイル),Cソース.byref(行),Cソース.byref(槽入口),Cソース.byref(変位量値))
    return (文(ファイル入口名前(ファイル)) if ファイル else '', 変位量値.value, 行.value)

def 命令実行():
    検索添字 = 生成(0,0); 宣言一覧一覧 = {}; 参照一覧一覧 = []; エラー一覧 = []
    # コンパイラ道具要素.c는 内蔵 宣言 없이 TinyCC 外部値 단일 ソース翻訳処理 단위만 포함한다.
    # 外部値 선언을 内蔵 이름으로 세지 않으며, 実際データ 빌드에서는 継続処理工程 컴파일한다.
    所有対象ファイル = {str(経路.resolve()) for 経路 in 計画根.rglob('*') if 経路.suffix in ('.c','.h','.cpp','.inc')
              and not set(経路.relative_to(計画根).parts)&{'build','dist','vendor','__pycache__'}
              and 経路.relative_to(計画根).as_posix() != 'Cコンパイラ/コンパイラ道具要素.c'}
    共通値 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(計画根/'利用者'),
          '-I'+str(計画根.parents[1]/'posix-kor/arm64-native/ヘッダー'),'-I'+str(計画根/'build'),'-I'+str(計画根/'build/user'),
          '-I'+str(計画根/'build/remote'),'-I'+str(計画根/'vendor/bearssl/inc'),
          '-I'+str(計画根/'vendor/bearssl/src'),'-I'+str(計画根/'vendor/libassh/src'),
          '-I'+str(計画根/'vendor/lwip/src/include'),'-I'+str(計画根/'通信網'),
          '-I'+str(計画根/'遠隔値'),'-I'+str(計画根/'Cコンパイラ')]
    for 経路 in sorted(Path(名前) for 名前 in 所有対象ファイル if 名前.endswith(('.c','.cpp'))):
        引数 = 共通値 + ['-std=c++11' if 経路.suffix=='.cpp' else '-std=c11']
        if '通信網' in 経路.parts: 引数 += ['-I'+str(計画根/'通信網'),'-I'+str(計画根/'vendor/lwip/src/include')]
        if 'Cコンパイラ' in 経路.parts:
            引数 += ['-I'+str(計画根/'Cコンパイラ'),'-I'+str(計画根/'vendor/tinycc'),'-I'+str(計画根/'build/ccompiler'),
                    '-isystem',str(計画根.parent/'rpi4/build/rootfs/usr/include')]
        if 'Python橋渡し' in 経路.parts:
            引数 += ['-I'+str(計画根/'Python橋渡し'),'-I'+str(計画根/'build/micropython-1.24.1'),'-I'+str(計画根/'build/python'),'-isystem','/usr/include/newlib']
        if '遠隔値' in 経路.parts:
            引数 += ['-isystem', '/usr/include/newlib']
        if '配布値' in 経路.parts: 引数 += ['-D__JKOROS__=1']
        if 経路.name=='パッケージ.c': 引数 += ['-I'+str(計画根/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        集合値 = (Cソース.c_char_p*len(引数))(*[入口値.encode() for 入口値 in 引数])
        翻訳単位 = 値分析(検索添字,str(経路).encode(),集合値,len(引数),None,0,1)
        for 番号 in range(診断個数(翻訳単位)):
            診断値 = 診断取得(翻訳単位,番号)
            if 重大度値(診断値)>=3: エラー一覧.append((str(経路.relative_to(計画根)),文(診断メッセージ(診断値))))
            診断解放(診断値)
        @訪問済み型
        def 値調査(入口値,親値,データ):
            ファイル,変位量値,行 = 位置添字(入口値)
            if ファイル not in 所有対象ファイル: return 2 if 入口値.種別値==300 else 1
            字句用語 = 文(名前取得(入口値))
            if not 字句用語 or any(ord(文字値)>127 for 文字値 in 字句用語): return 2
            if 入口値.種別値 in (2,3,4,5,6,7,8,9,10,20,21,501):
                一意値 = 文(一意名前(入口値)) or ファイル+':'+str(変位量値)
                宣言一覧一覧[一意値] = {'ファイル':ファイル,'変位量値':変位量値,'行':行,'種別値':入口値.種別値,'名前':字句用語,'接続':接続状態種別(入口値)}
                参照一覧一覧.append((ファイル,変位量値,字句用語,一意値))
            else:
                参照 = 参照取得(入口値)
                参照ファイル,_,_ = 位置添字(参照)
                if 参照ファイル in 所有対象ファイル:
                    一意値 = 文(一意名前(参照)); 参照一覧一覧.append((ファイル,変位量値,文(名前取得(参照)),一意値))
            return 2
        値訪問(根値(翻訳単位),値調査,None)
        脱出プログラム(翻訳単位)
    宛先値 = 計画根/'build/한국어화/시언어분석.json'
    宛先値.parent.mkdir(parents=True, exist_ok=True)
    ハッシュ一覧一覧 = {ファイル:hashlib.sha256(Path(ファイル).read_bytes()).hexdigest() for ファイル in sorted(所有対象ファイル)}
    宛先値.write_text(json.dumps({'宣言':宣言一覧一覧,'参照':参照一覧一覧,'エラー':エラー一覧,'원문해시':ハッシュ一覧一覧},ensure_ascii=False,indent=2)+'\n')
    print('宣言',len(宣言一覧一覧),'参照',len(参照一覧一覧),'エラー',len(エラー一覧))
    for エラー in エラー一覧: print(*エラー)

if __name__=='__main__': 命令実行()
