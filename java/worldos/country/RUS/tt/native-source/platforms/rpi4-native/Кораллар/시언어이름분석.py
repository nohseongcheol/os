#!/usr/bin/env python3
"""libclang 선언·Белешмәлекләр 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

экранга_җибәрү_тамыр = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class юл_VALUE_6ca8363c(씨.Structure): _fields_ = [('мәгълүмат',씨.c_void_p),('күрсәтү_VALUE',씨.c_uint)]
class курсор_VALUE(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('мәгълүмат',씨.c_void_p*3)]
class урнаштыру(씨.Structure): _fields_ = [('мәгълүмат',씨.c_void_p*2),('OFFSET_VALUE',씨.c_uint)]
def ФУНКЦИЯ_VALUE(исем, кайтару_үлчәм, *인수):
    кертү_VALUE = getattr(구현, исем); кертү_VALUE.restype = кайтару_үлчәм; кертү_VALUE.argtypes = list(인수); return кертү_VALUE
글얻기 = ФУНКЦИЯ_VALUE('clang_getCString',씨.c_char_p,юл_VALUE_6ca8363c)
Чыгарылыш_СМС = ФУНКЦИЯ_VALUE('clang_disposeString',None,юл_VALUE_6ca8363c)
def Mäten(VALUE):
    үлчәм = (글얻기(VALUE) or b'').decode('utf-8'); Чыгарылыш_СМС(VALUE); return үлчәм
이름얻기 = ФУНКЦИЯ_VALUE('clang_getCursorSpelling',юл_VALUE_6ca8363c,курсор_VALUE)
참조얻기 = ФУНКЦИЯ_VALUE('clang_getCursorReferenced',курсор_VALUE,курсор_VALUE)
위치얻기 = ФУНКЦИЯ_VALUE('clang_getCursorLocation',урнаштыру,курсор_VALUE)
файл_урнаштыру = ФУНКЦИЯ_VALUE('clang_getFileLocation',None,урнаштыру,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
файл_кертү_исем = ФУНКЦИЯ_VALUE('clang_getFileName',юл_VALUE_6ca8363c,씨.c_void_p)
UNIQUE_исем = ФУНКЦИЯ_VALUE('clang_getCursorUSR',юл_VALUE_6ca8363c,курсор_VALUE)
연결종류 = ФУНКЦИЯ_VALUE('clang_getCursorLinkage',씨.c_uint,курсор_VALUE)
방문형 = 씨.CFUNCTYPE(씨.c_uint,курсор_VALUE,курсор_VALUE,씨.c_void_p)
방문 = ФУНКЦИЯ_VALUE('clang_visitChildren',씨.c_uint,курсор_VALUE,방문형,씨.c_void_p)
булдыру = ФУНКЦИЯ_VALUE('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = ФУНКЦИЯ_VALUE('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
тамыр_VALUE = ФУНКЦИЯ_VALUE('clang_getTranslationUnitCursor',курсор_VALUE,씨.c_void_p)
чыгу_кушымта = ФУНКЦИЯ_VALUE('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ФУНКЦИЯ_VALUE('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ФУНКЦИЯ_VALUE('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
җитдилек_VALUE = ФУНКЦИЯ_VALUE('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ФУНКЦИЯ_VALUE('clang_getDiagnosticSpelling',юл_VALUE_6ca8363c,씨.c_void_p)
진단해제 = ФУНКЦИЯ_VALUE('clang_disposeDiagnostic',None,씨.c_void_p)

def урнаштыру_INDEX(кертү_VALUE):
    Birem = 씨.c_void_p(); юл = 씨.c_uint(); оя_кертү = 씨.c_uint(); OFFSET_VALUE = 씨.c_uint()
    файл_урнаштыру(위치얻기(кертү_VALUE),씨.byref(Birem),씨.byref(юл),씨.byref(оя_кертү),씨.byref(OFFSET_VALUE))
    return (Mäten(файл_кертү_исем(Birem)) if Birem else '', OFFSET_VALUE.value, юл.value)

def үтәргә_команда():
    Эзләү_INDEX = булдыру(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 TRANSLATE_чыганак 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, фактик_мәгълүмат 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Yul.resolve()) for Yul in экранга_җибәрү_тамыр.rglob('*') if Yul.suffix in ('.c','.h','.cpp','.inc')
              and not set(Yul.relative_to(экранга_җибәрү_тамыр).parts)&{'build','dist','vendor','__pycache__'}
              and Yul.relative_to(экранга_җибәрү_тамыр).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(экранга_җибәрү_тамыр/'кулланучы'),
          '-I'+str(экранга_җибәрү_тамыр.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(экранга_җибәрү_тамыр/'build'),'-I'+str(экранга_җибәрү_тамыр/'build/user'),
          '-I'+str(экранга_җибәрү_тамыр/'build/remote'),'-I'+str(экранга_җибәрү_тамыр/'vendor/bearssl/inc'),
          '-I'+str(экранга_җибәрү_тамыр/'vendor/bearssl/src'),'-I'+str(экранга_җибәрү_тамыр/'vendor/libassh/src'),
          '-I'+str(экранга_җибәрү_тамыр/'vendor/lwip/src/include'),'-I'+str(экранга_җибәрү_тамыр/'Челтәр_Стәк'),
          '-I'+str(экранга_җибәрү_тамыр/'читтәге_VALUE'),'-I'+str(экранга_җибәрү_тамыр/'시언어번역기')]
    for Yul in sorted(Path(исем) for исем in 소유파일 if исем.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if Yul.suffix=='.cpp' else '-std=c11']
        if 'Челтәр_Стәк' in Yul.parts: 인수 += ['-I'+str(экранга_җибәрү_тамыр/'Челтәр_Стәк'),'-I'+str(экранга_җибәрү_тамыр/'vendor/lwip/src/include')]
        if '시언어번역기' in Yul.parts:
            인수 += ['-I'+str(экранга_җибәрү_тамыр/'시언어번역기'),'-I'+str(экранга_җибәрү_тамыр/'vendor/tinycc'),'-I'+str(экранга_җибәрү_тамыр/'build/ccompiler'),
                    '-isystem',str(экранга_җибәрү_тамыр.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_күпер' in Yul.parts:
            인수 += ['-I'+str(экранга_җибәрү_тамыр/'PYTHON_күпер'),'-I'+str(экранга_җибәрү_тамыр/'build/micropython-1.24.1'),'-I'+str(экранга_җибәрү_тамыр/'build/python'),'-isystem','/usr/include/newlib']
        if 'читтәге_VALUE' in Yul.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in Yul.parts: 인수 += ['-D__JKOROS__=1']
        if Yul.name=='пакет.c': 인수 += ['-I'+str(экранга_җибәрү_тамыр/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        төркем_VALUE = (씨.c_char_p*len(인수))(*[кертү_VALUE.encode() for кертү_VALUE in 인수])
        Тәрҗемә_итү_дәрес = 분석(Эзләү_INDEX,str(Yul).encode(),төркем_VALUE,len(인수),None,0,1)
        for INDEX in range(진단수(Тәрҗемә_итү_дәрес)):
            진단 = 진단얻기(Тәрҗемә_итү_дәрес,INDEX)
            if җитдилек_VALUE(진단)>=3: 오류들.append((str(Yul.relative_to(экранга_җибәрү_тамыр)),Mäten(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(кертү_VALUE,부모,мәгълүмат):
            Birem,OFFSET_VALUE,юл = урнаштыру_INDEX(кертү_VALUE)
            if Birem not in 소유파일: return 2 if кертү_VALUE.종류==300 else 1
            낱말 = Mäten(이름얻기(кертү_VALUE))
            if not 낱말 or any(ord(символ_VALUE_068c2631)>127 for символ_VALUE_068c2631 in 낱말): return 2
            if кертү_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Mäten(UNIQUE_исем(кертү_VALUE)) or Birem+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'Birem':Birem,'OFFSET_VALUE':OFFSET_VALUE,'줄':юл,'종류':кертү_VALUE.종류,'исем':낱말,'ялгау':연결종류(кертү_VALUE)}
                참조들.append((Birem,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                Белешмәлекләр = 참조얻기(кертү_VALUE)
                Белешмәлекләр_файл,_,_ = урнаштыру_INDEX(Белешмәлекләр)
                if Белешмәлекләр_файл in 소유파일:
                    UNIQUE_VALUE = Mäten(UNIQUE_исем(Белешмәлекләр)); 참조들.append((Birem,OFFSET_VALUE,Mäten(이름얻기(Белешмәлекләр)),UNIQUE_VALUE))
            return 2
        방문(тамыр_VALUE(Тәрҗемә_итү_дәрес),살피기,None)
        чыгу_кушымта(Тәрҗемә_итү_дәрес)
    күчерү_урыны_VALUE = экранга_җибәрү_тамыр/'build/한국어화/시언어분석.json'
    күчерү_урыны_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Birem:hashlib.sha256(Path(Birem).read_bytes()).hexdigest() for Birem in sorted(소유파일)}
    күчерү_урыны_VALUE.write_text(json.dumps({'선언':선언들,'Белешмәлекләр':참조들,'Хата':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Белешмәлекләр',len(참조들),'Хата',len(오류들))
    for Хата in 오류들: print(*Хата)

if __name__=='__main__': үтәргә_команда()
