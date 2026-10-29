#!/usr/bin/env python3
"""libclang 聲明·引用 위치를 수집한다. 外部值 헤더의 멤버는 변환하지 않는다."""
import ctypes as C原始碼
import hashlib
import json
from pathlib import Path

項目根 = Path(__file__).resolve().parents[1]
實現 = C原始碼.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class 字符串(C原始碼.Structure): _fields_ = [('資料',C原始碼.c_void_p),('顯示值',C原始碼.c_uint)]
class 光標值(C原始碼.Structure): _fields_ = [('種類值',C原始碼.c_uint),('輔助值',C原始碼.c_int),('資料',C原始碼.c_void_p*3)]
class 位置(C原始碼.Structure): _fields_ = [('資料',C原始碼.c_void_p*2),('偏移值',C原始碼.c_uint)]
def 函數(名稱, 發回結果, *實參):
    條目值 = getattr(實現, 名稱); 條目值.restype = 發回結果; 條目值.argtypes = list(實參); return 條目值
獲取文本 = 函數('clang_getCString',C原始碼.c_char_p,字符串)
釋放文本 = 函數('clang_disposeString',None,字符串)
def 文本(值):
    結果 = (獲取文本(值) or b'').decode('utf-8'); 釋放文本(值); return 結果
獲取名稱 = 函數('clang_getCursorSpelling',字符串,光標值)
獲取引用 = 函數('clang_getCursorReferenced',光標值,光標值)
獲取位置 = 函數('clang_getCursorLocation',位置,光標值)
檔案位置 = 函數('clang_getFileLocation',None,位置,C原始碼.POINTER(C原始碼.c_void_p),C原始碼.POINTER(C原始碼.c_uint),C原始碼.POINTER(C原始碼.c_uint),C原始碼.POINTER(C原始碼.c_uint))
檔案條目名稱 = 函數('clang_getFileName',字符串,C原始碼.c_void_p)
唯一名稱 = 函數('clang_getCursorUSR',字符串,光標值)
連接狀態種類 = 函數('clang_getCursorLinkage',C原始碼.c_uint,光標值)
已訪問類型 = C原始碼.CFUNCTYPE(C原始碼.c_uint,光標值,光標值,C原始碼.c_void_p)
訪問值 = 函數('clang_visitChildren',C原始碼.c_uint,光標值,已訪問類型,C原始碼.c_void_p)
生成 = 函數('clang_createIndex',C原始碼.c_void_p,C原始碼.c_int,C原始碼.c_int)
分析值 = 函數('clang_parseTranslationUnit',C原始碼.c_void_p,C原始碼.c_void_p,C原始碼.c_char_p,C原始碼.POINTER(C原始碼.c_char_p),C原始碼.c_int,C原始碼.c_void_p,C原始碼.c_uint,C原始碼.c_uint)
根值 = 函數('clang_getTranslationUnitCursor',光標值,C原始碼.c_void_p)
結束程序 = 函數('clang_disposeTranslationUnit',None,C原始碼.c_void_p)
診斷個數 = 函數('clang_getNumDiagnostics',C原始碼.c_uint,C原始碼.c_void_p)
獲取診斷 = 函數('clang_getDiagnostic',C原始碼.c_void_p,C原始碼.c_void_p,C原始碼.c_uint)
嚴重性值 = 函數('clang_getDiagnosticSeverity',C原始碼.c_uint,C原始碼.c_void_p)
診斷消息 = 函數('clang_getDiagnosticSpelling',字符串,C原始碼.c_void_p)
釋放診斷 = 函數('clang_disposeDiagnostic',None,C原始碼.c_void_p)

def 位置索引(條目值):
    檔案 = C原始碼.c_void_p(); 行 = C原始碼.c_uint(); 槽條目 = C原始碼.c_uint(); 偏移值 = C原始碼.c_uint()
    檔案位置(獲取位置(條目值),C原始碼.byref(檔案),C原始碼.byref(行),C原始碼.byref(槽條目),C原始碼.byref(偏移值))
    return (文本(檔案條目名稱(檔案)) if 檔案 else '', 偏移值.value, 行.value)

def 執行命令():
    查找索引 = 生成(0,0); 聲明列列表 = {}; 引用列列表 = []; 錯誤列 = []
    # 編譯器工具.c는 內建 聲明 없이 TinyCC 外部值 단일 翻譯原始碼 단위만 포함한다.
    # 外部值 선언을 內建 이름으로 세지 않으며, 實際資料 빌드에서는 繼續處理 컴파일한다.
    自有檔案 = {str(路徑.resolve()) for 路徑 in 項目根.rglob('*') if 路徑.suffix in ('.c','.h','.cpp','.inc')
              and not set(路徑.relative_to(項目根).parts)&{'build','dist','vendor','__pycache__'}
              and 路徑.relative_to(項目根).as_posix() != 'C編譯器/編譯器工具.c'}
    公用值 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(項目根/'使用者'),
          '-I'+str(項目根.parents[1]/'posix-kor/arm64-native/頭文件'),'-I'+str(項目根/'build'),'-I'+str(項目根/'build/user'),
          '-I'+str(項目根/'build/remote'),'-I'+str(項目根/'vendor/bearssl/inc'),
          '-I'+str(項目根/'vendor/bearssl/src'),'-I'+str(項目根/'vendor/libassh/src'),
          '-I'+str(項目根/'vendor/lwip/src/include'),'-I'+str(項目根/'通信網絡'),
          '-I'+str(項目根/'遠程值'),'-I'+str(項目根/'C編譯器')]
    for 路徑 in sorted(Path(名稱) for 名稱 in 自有檔案 if 名稱.endswith(('.c','.cpp'))):
        實參 = 公用值 + ['-std=c++11' if 路徑.suffix=='.cpp' else '-std=c11']
        if '通信網絡' in 路徑.parts: 實參 += ['-I'+str(項目根/'通信網絡'),'-I'+str(項目根/'vendor/lwip/src/include')]
        if 'C編譯器' in 路徑.parts:
            實參 += ['-I'+str(項目根/'C編譯器'),'-I'+str(項目根/'vendor/tinycc'),'-I'+str(項目根/'build/ccompiler'),
                    '-isystem',str(項目根.parent/'rpi4/build/rootfs/usr/include')]
        if 'Python橋接' in 路徑.parts:
            實參 += ['-I'+str(項目根/'Python橋接'),'-I'+str(項目根/'build/micropython-1.24.1'),'-I'+str(項目根/'build/python'),'-isystem','/usr/include/newlib']
        if '遠程值' in 路徑.parts:
            實參 += ['-isystem', '/usr/include/newlib']
        if '分發值' in 路徑.parts: 實參 += ['-D__JKOROS__=1']
        if 路徑.name=='軟件包.c': 實參 += ['-I'+str(項目根/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        組值 = (C原始碼.c_char_p*len(實參))(*[條目值.encode() for 條目值 in 實參])
        翻譯單位 = 分析值(查找索引,str(路徑).encode(),組值,len(實參),None,0,1)
        for 編號 in range(診斷個數(翻譯單位)):
            診斷值 = 獲取診斷(翻譯單位,編號)
            if 嚴重性值(診斷值)>=3: 錯誤列.append((str(路徑.relative_to(項目根)),文本(診斷消息(診斷值))))
            釋放診斷(診斷值)
        @已訪問類型
        def 審查值(條目值,父值,資料):
            檔案,偏移值,行 = 位置索引(條目值)
            if 檔案 not in 自有檔案: return 2 if 條目值.種類值==300 else 1
            詞法用機器字 = 文本(獲取名稱(條目值))
            if not 詞法用機器字 or any(ord(字元值)>127 for 字元值 in 詞法用機器字): return 2
            if 條目值.種類值 in (2,3,4,5,6,7,8,9,10,20,21,501):
                唯一值 = 文本(唯一名稱(條目值)) or 檔案+':'+str(偏移值)
                聲明列列表[唯一值] = {'檔案':檔案,'偏移值':偏移值,'行':行,'種類值':條目值.種類值,'名稱':詞法用機器字,'連接':連接狀態種類(條目值)}
                引用列列表.append((檔案,偏移值,詞法用機器字,唯一值))
            else:
                引用 = 獲取引用(條目值)
                引用檔案,_,_ = 位置索引(引用)
                if 引用檔案 in 自有檔案:
                    唯一值 = 文本(唯一名稱(引用)); 引用列列表.append((檔案,偏移值,文本(獲取名稱(引用)),唯一值))
            return 2
        訪問值(根值(翻譯單位),審查值,None)
        結束程序(翻譯單位)
    目的地址值 = 項目根/'build/한국어화/시언어분석.json'
    目的地址值.parent.mkdir(parents=True, exist_ok=True)
    散列值列列表 = {檔案:hashlib.sha256(Path(檔案).read_bytes()).hexdigest() for 檔案 in sorted(自有檔案)}
    目的地址值.write_text(json.dumps({'聲明':聲明列列表,'引用':引用列列表,'錯誤':錯誤列,'원문해시':散列值列列表},ensure_ascii=False,indent=2)+'\n')
    print('聲明',len(聲明列列表),'引用',len(引用列列表),'錯誤',len(錯誤列))
    for 錯誤 in 錯誤列: print(*錯誤)

if __name__=='__main__': 執行命令()
