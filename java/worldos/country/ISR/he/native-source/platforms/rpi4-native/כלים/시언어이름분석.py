#!/usr/bin/env python3
"""libclang הצהרה·הפנה 위치를 수집한다. חיצוני_ערך 헤더의 멤버는 변환하지 않는다."""
import ctypes as מ_מקור
import hashlib
import json
from pathlib import Path

לשקף_בסיס = Path(__file__).resolve().parents[1]
구현 = מ_מקור.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class מחרוזת_ערך(מ_מקור.Structure): _fields_ = [('נתונים',מ_מקור.c_void_p),('הופעה_ערך',מ_מקור.c_uint)]
class סמן_ערך_04ee3e20(מ_מקור.Structure): _fields_ = [('종류',מ_מקור.c_uint),('보조',מ_מקור.c_int),('נתונים',מ_מקור.c_void_p*3)]
class מיקום(מ_מקור.Structure): _fields_ = [('נתונים',מ_מקור.c_void_p*2),('היסט_ערך',מ_מקור.c_uint)]
def פונקציה_ערך(שם, החזר_תוצאה, *ארגומנטים):
    ערך_ערך = getattr(구현, שם); ערך_ערך.restype = החזר_תוצאה; ערך_ערך.argtypes = list(ארגומנטים); return ערך_ערך
לקבל_טקסט = פונקציה_ערך('clang_getCString',מ_מקור.c_char_p,מחרוזת_ערך)
לשחרר_טקסט = פונקציה_ערך('clang_disposeString',None,מחרוזת_ערך)
def טקסט(ערך):
    תוצאה = (לקבל_טקסט(ערך) or b'').decode('utf-8'); לשחרר_טקסט(ערך); return תוצאה
לקבל_שם = פונקציה_ערך('clang_getCursorSpelling',מחרוזת_ערך,סמן_ערך_04ee3e20)
לקבל_הפנה_10d0a960 = פונקציה_ערך('clang_getCursorReferenced',סמן_ערך_04ee3e20,סמן_ערך_04ee3e20)
לקבל_עמדה_9492ef84 = פונקציה_ערך('clang_getCursorLocation',מיקום,סמן_ערך_04ee3e20)
קובץ_עמדה = פונקציה_ערך('clang_getFileLocation',None,מיקום,מ_מקור.POINTER(מ_מקור.c_void_p),מ_מקור.POINTER(מ_מקור.c_uint),מ_מקור.POINTER(מ_מקור.c_uint),מ_מקור.POINTER(מ_מקור.c_uint))
קובץ_ערך_שם = פונקציה_ערך('clang_getFileName',מחרוזת_ערך,מ_מקור.c_void_p)
고유이름 = פונקציה_ערך('clang_getCursorUSR',מחרוזת_ערך,סמן_ערך_04ee3e20)
연결종류 = פונקציה_ערך('clang_getCursorLinkage',מ_מקור.c_uint,סמן_ערך_04ee3e20)
방문형 = מ_מקור.CFUNCTYPE(מ_מקור.c_uint,סמן_ערך_04ee3e20,סמן_ערך_04ee3e20,מ_מקור.c_void_p)
방문 = פונקציה_ערך('clang_visitChildren',מ_מקור.c_uint,סמן_ערך_04ee3e20,방문형,מ_מקור.c_void_p)
יצר = פונקציה_ערך('clang_createIndex',מ_מקור.c_void_p,מ_מקור.c_int,מ_מקור.c_int)
לנתח_ערך = פונקציה_ערך('clang_parseTranslationUnit',מ_מקור.c_void_p,מ_מקור.c_void_p,מ_מקור.c_char_p,מ_מקור.POINTER(מ_מקור.c_char_p),מ_מקור.c_int,מ_מקור.c_void_p,מ_מקור.c_uint,מ_מקור.c_uint)
בסיס_ערך = פונקציה_ערך('clang_getTranslationUnitCursor',סמן_ערך_04ee3e20,מ_מקור.c_void_p)
יציאה_תוכנית_55b3a1cd = פונקציה_ערך('clang_disposeTranslationUnit',None,מ_מקור.c_void_p)
진단수 = פונקציה_ערך('clang_getNumDiagnostics',מ_מקור.c_uint,מ_מקור.c_void_p)
진단얻기 = פונקציה_ערך('clang_getDiagnostic',מ_מקור.c_void_p,מ_מקור.c_void_p,מ_מקור.c_uint)
חומרה_ערך = פונקציה_ערך('clang_getDiagnosticSeverity',מ_מקור.c_uint,מ_מקור.c_void_p)
진단문 = פונקציה_ערך('clang_getDiagnosticSpelling',מחרוזת_ערך,מ_מקור.c_void_p)
진단해제 = פונקציה_ערך('clang_disposeDiagnostic',None,מ_מקור.c_void_p)

def עמדה_מדד(ערך_ערך):
    קובץ = מ_מקור.c_void_p(); שורה = מ_מקור.c_uint(); חריץ_ערך = מ_מקור.c_uint(); היסט_ערך = מ_מקור.c_uint()
    קובץ_עמדה(לקבל_עמדה_9492ef84(ערך_ערך),מ_מקור.byref(קובץ),מ_מקור.byref(שורה),מ_מקור.byref(חריץ_ערך),מ_מקור.byref(היסט_ערך))
    return (טקסט(קובץ_ערך_שם(קובץ)) if קובץ else '', היסט_ערך.value, שורה.value)

def לבצע_פקודה():
    חפושׂ_מדד = יצר(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # מהדר_כלי.c는 עצמי הצהרה 없이 TinyCC חיצוני_ערך 단일 תרגם_מקור 단위만 포함한다.
    # חיצוני_ערך 선언을 עצמי 이름으로 세지 않으며, בפועל_נתונים 빌드에서는 계속 컴파일한다.
    소유파일 = {str(נתיב.resolve()) for נתיב in לשקף_בסיס.rglob('*') if נתיב.suffix in ('.c','.h','.cpp','.inc')
              and not set(נתיב.relative_to(לשקף_בסיס).parts)&{'build','dist','vendor','__pycache__'}
              and נתיב.relative_to(לשקף_בסיס).as_posix() != 'מ_מהדר/מהדר_כלי.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(לשקף_בסיס/'משתמש'),
          '-I'+str(לשקף_בסיס.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(לשקף_בסיס/'build'),'-I'+str(לשקף_בסיס/'build/user'),
          '-I'+str(לשקף_בסיס/'build/remote'),'-I'+str(לשקף_בסיס/'vendor/bearssl/inc'),
          '-I'+str(לשקף_בסיס/'vendor/bearssl/src'),'-I'+str(לשקף_בסיס/'vendor/libassh/src'),
          '-I'+str(לשקף_בסיס/'vendor/lwip/src/include'),'-I'+str(לשקף_בסיס/'רשת_רמז'),
          '-I'+str(לשקף_בסיס/'מרוחק_ערך'),'-I'+str(לשקף_בסיס/'מ_מהדר')]
    for נתיב in sorted(Path(שם) for שם in 소유파일 if שם.endswith(('.c','.cpp'))):
        ארגומנטים = 공통 + ['-std=c++11' if נתיב.suffix=='.cpp' else '-std=c11']
        if 'רשת_רמז' in נתיב.parts: ארגומנטים += ['-I'+str(לשקף_בסיס/'רשת_רמז'),'-I'+str(לשקף_בסיס/'vendor/lwip/src/include')]
        if 'מ_מהדר' in נתיב.parts:
            ארגומנטים += ['-I'+str(לשקף_בסיס/'מ_מהדר'),'-I'+str(לשקף_בסיס/'vendor/tinycc'),'-I'+str(לשקף_בסיס/'build/ccompiler'),
                    '-isystem',str(לשקף_בסיס.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in נתיב.parts:
            ארגומנטים += ['-I'+str(לשקף_בסיס/'파이썬연결'),'-I'+str(לשקף_בסיס/'build/micropython-1.24.1'),'-I'+str(לשקף_בסיס/'build/python'),'-isystem','/usr/include/newlib']
        if 'מרוחק_ערך' in נתיב.parts:
            ארגומנטים += ['-isystem', '/usr/include/newlib']
        if 'הפצה_ערך' in נתיב.parts: ארגומנטים += ['-D__JKOROS__=1']
        if נתיב.name=='חבילה.c': ארגומנטים += ['-I'+str(לשקף_בסיס/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        לקבץ_ערך = (מ_מקור.c_char_p*len(ארגומנטים))(*[ערך_ערך.encode() for ערך_ערך in ארגומנטים])
        תרגום_יחידה = לנתח_ערך(חפושׂ_מדד,str(נתיב).encode(),לקבץ_ערך,len(ארגומנטים),None,0,1)
        for מדד in range(진단수(תרגום_יחידה)):
            진단 = 진단얻기(תרגום_יחידה,מדד)
            if חומרה_ערך(진단)>=3: 오류들.append((str(נתיב.relative_to(לשקף_בסיס)),טקסט(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ערך_ערך,אב_ערך,נתונים):
            קובץ,היסט_ערך,שורה = עמדה_מדד(ערך_ערך)
            if קובץ not in 소유파일: return 2 if ערך_ערך.종류==300 else 1
            낱말 = טקסט(לקבל_שם(ערך_ערך))
            if not 낱말 or any(ord(תו_ערך)>127 for תו_ערך in 낱말): return 2
            if ערך_ערך.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = טקסט(고유이름(ערך_ערך)) or קובץ+':'+str(היסט_ערך)
                선언들[고유] = {'קובץ':קובץ,'היסט_ערך':היסט_ערך,'שורה':שורה,'종류':ערך_ערך.종류,'שם':낱말,'חיבור':연결종류(ערך_ערך)}
                참조들.append((קובץ,היסט_ערך,낱말,고유))
            else:
                הפנה = לקבל_הפנה_10d0a960(ערך_ערך)
                הפנה_קובץ,_,_ = עמדה_מדד(הפנה)
                if הפנה_קובץ in 소유파일:
                    고유 = טקסט(고유이름(הפנה)); 참조들.append((קובץ,היסט_ערך,טקסט(לקבל_שם(הפנה)),고유))
            return 2
        방문(בסיס_ערך(תרגום_יחידה),살피기,None)
        יציאה_תוכנית_55b3a1cd(תרגום_יחידה)
    יעד_ערך = לשקף_בסיס/'build/한국어화/시언어분석.json'
    יעד_ערך.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {קובץ:hashlib.sha256(Path(קובץ).read_bytes()).hexdigest() for קובץ in sorted(소유파일)}
    יעד_ערך.write_text(json.dumps({'הצהרה':선언들,'הפנה':참조들,'שגיאה':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('הצהרה',len(선언들),'הפנה',len(참조들),'שגיאה',len(오류들))
    for שגיאה in 오류들: print(*שגיאה)

if __name__=='__main__': לבצע_פקודה()
