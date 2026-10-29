#!/usr/bin/env python3
"""libclang декларација·Референци 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

Project_корен = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class низа_VALUE_6ca8363c(씨.Structure): _fields_ = [('податоци',씨.c_void_p),('прикажи_VALUE',씨.c_uint)]
class покажувач_VALUE(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('податоци',씨.c_void_p*3)]
class Позиција(씨.Structure): _fields_ = [('податоци',씨.c_void_p*2),('OFFSET_VALUE',씨.c_uint)]
def ФУНКЦИЈА_VALUE(Име, 반환, *Аргументи):
    внес_VALUE = getattr(구현, Име); внес_VALUE.restype = 반환; внес_VALUE.argtypes = list(Аргументи); return внес_VALUE
зема_СМС = ФУНКЦИЈА_VALUE('clang_getCString',씨.c_char_p,низа_VALUE_6ca8363c)
издание_СМС = ФУНКЦИЈА_VALUE('clang_disposeString',None,низа_VALUE_6ca8363c)
def Текст(VALUE):
    мерка = (зема_СМС(VALUE) or b'').decode('utf-8'); издание_СМС(VALUE); return мерка
зема_име = ФУНКЦИЈА_VALUE('clang_getCursorSpelling',низа_VALUE_6ca8363c,покажувач_VALUE)
зема_Референци = ФУНКЦИЈА_VALUE('clang_getCursorReferenced',покажувач_VALUE,покажувач_VALUE)
зема_позиционирање = ФУНКЦИЈА_VALUE('clang_getCursorLocation',Позиција,покажувач_VALUE)
датотека_позиционирање = ФУНКЦИЈА_VALUE('clang_getFileLocation',None,Позиција,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
датотека_внес_име = ФУНКЦИЈА_VALUE('clang_getFileName',низа_VALUE_6ca8363c,씨.c_void_p)
UNIQUE_име = ФУНКЦИЈА_VALUE('clang_getCursorUSR',низа_VALUE_6ca8363c,покажувач_VALUE)
연결종류 = ФУНКЦИЈА_VALUE('clang_getCursorLinkage',씨.c_uint,покажувач_VALUE)
방문형 = 씨.CFUNCTYPE(씨.c_uint,покажувач_VALUE,покажувач_VALUE,씨.c_void_p)
방문 = ФУНКЦИЈА_VALUE('clang_visitChildren',씨.c_uint,покажувач_VALUE,방문형,씨.c_void_p)
генерира = ФУНКЦИЈА_VALUE('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = ФУНКЦИЈА_VALUE('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
корен_VALUE = ФУНКЦИЈА_VALUE('clang_getTranslationUnitCursor',покажувач_VALUE,씨.c_void_p)
излез_програма = ФУНКЦИЈА_VALUE('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ФУНКЦИЈА_VALUE('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ФУНКЦИЈА_VALUE('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
сериозност_VALUE = ФУНКЦИЈА_VALUE('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ФУНКЦИЈА_VALUE('clang_getDiagnosticSpelling',низа_VALUE_6ca8363c,씨.c_void_p)
진단해제 = ФУНКЦИЈА_VALUE('clang_disposeDiagnostic',None,씨.c_void_p)

def позиционирање_INDEX(внес_VALUE):
    Датотека = 씨.c_void_p(); ред = 씨.c_uint(); отвор_внес = 씨.c_uint(); OFFSET_VALUE = 씨.c_uint()
    датотека_позиционирање(зема_позиционирање(внес_VALUE),씨.byref(Датотека),씨.byref(ред),씨.byref(отвор_внес),씨.byref(OFFSET_VALUE))
    return (Текст(датотека_внес_име(Датотека)) if Датотека else '', OFFSET_VALUE.value, ред.value)

def Изврши_наредба():
    LOOKUP_INDEX = генерира(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 декларација 없이 TinyCC 외부 단일 Превод_извор 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, реален_податоци 빌드에서는 계속 컴파일한다.
    소유파일 = {str(ПАТЕКА.resolve()) for ПАТЕКА in Project_корен.rglob('*') if ПАТЕКА.suffix in ('.c','.h','.cpp','.inc')
              and not set(ПАТЕКА.relative_to(Project_корен).parts)&{'build','dist','vendor','__pycache__'}
              and ПАТЕКА.relative_to(Project_корен).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(Project_корен/'корисник'),
          '-I'+str(Project_корен.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(Project_корен/'build'),'-I'+str(Project_корен/'build/user'),
          '-I'+str(Project_корен/'build/remote'),'-I'+str(Project_корен/'vendor/bearssl/inc'),
          '-I'+str(Project_корен/'vendor/bearssl/src'),'-I'+str(Project_корен/'vendor/libassh/src'),
          '-I'+str(Project_корен/'vendor/lwip/src/include'),'-I'+str(Project_корен/'Мрежа_Купче'),
          '-I'+str(Project_корен/'далечинскo_VALUE'),'-I'+str(Project_корен/'시언어번역기')]
    for ПАТЕКА in sorted(Path(Име) for Име in 소유파일 if Име.endswith(('.c','.cpp'))):
        Аргументи = 공통 + ['-std=c++11' if ПАТЕКА.suffix=='.cpp' else '-std=c11']
        if 'Мрежа_Купче' in ПАТЕКА.parts: Аргументи += ['-I'+str(Project_корен/'Мрежа_Купче'),'-I'+str(Project_корен/'vendor/lwip/src/include')]
        if '시언어번역기' in ПАТЕКА.parts:
            Аргументи += ['-I'+str(Project_корен/'시언어번역기'),'-I'+str(Project_корен/'vendor/tinycc'),'-I'+str(Project_корен/'build/ccompiler'),
                    '-isystem',str(Project_корен.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_мост' in ПАТЕКА.parts:
            Аргументи += ['-I'+str(Project_корен/'PYTHON_мост'),'-I'+str(Project_корен/'build/micropython-1.24.1'),'-I'+str(Project_корен/'build/python'),'-isystem','/usr/include/newlib']
        if 'далечинскo_VALUE' in ПАТЕКА.parts:
            Аргументи += ['-isystem', '/usr/include/newlib']
        if '배포' in ПАТЕКА.parts: Аргументи += ['-D__JKOROS__=1']
        if ПАТЕКА.name=='пакет.c': Аргументи += ['-I'+str(Project_корен/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Група_VALUE = (씨.c_char_p*len(Аргументи))(*[внес_VALUE.encode() for внес_VALUE in Аргументи])
        Превод_единици = 분석(LOOKUP_INDEX,str(ПАТЕКА).encode(),Група_VALUE,len(Аргументи),None,0,1)
        for INDEX in range(진단수(Превод_единици)):
            진단 = 진단얻기(Превод_единици,INDEX)
            if сериозност_VALUE(진단)>=3: 오류들.append((str(ПАТЕКА.relative_to(Project_корен)),Текст(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(внес_VALUE,부모,податоци):
            Датотека,OFFSET_VALUE,ред = позиционирање_INDEX(внес_VALUE)
            if Датотека not in 소유파일: return 2 if внес_VALUE.종류==300 else 1
            낱말 = Текст(зема_име(внес_VALUE))
            if not 낱말 or any(ord(знак_VALUE)>127 for знак_VALUE in 낱말): return 2
            if внес_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Текст(UNIQUE_име(внес_VALUE)) or Датотека+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'Датотека':Датотека,'OFFSET_VALUE':OFFSET_VALUE,'줄':ред,'종류':внес_VALUE.종류,'Име':낱말,'Врзи_се':연결종류(внес_VALUE)}
                참조들.append((Датотека,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                Референци = зема_Референци(внес_VALUE)
                Референци_датотека,_,_ = позиционирање_INDEX(Референци)
                if Референци_датотека in 소유파일:
                    UNIQUE_VALUE = Текст(UNIQUE_име(Референци)); 참조들.append((Датотека,OFFSET_VALUE,Текст(зема_име(Референци)),UNIQUE_VALUE))
            return 2
        방문(корен_VALUE(Превод_единици),살피기,None)
        излез_програма(Превод_единици)
    одредиште_VALUE = Project_корен/'build/한국어화/시언어분석.json'
    одредиште_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Датотека:hashlib.sha256(Path(Датотека).read_bytes()).hexdigest() for Датотека in sorted(소유파일)}
    одредиште_VALUE.write_text(json.dumps({'декларација':선언들,'Референци':참조들,'ГРЕШКА':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('декларација',len(선언들),'Референци',len(참조들),'ГРЕШКА',len(오류들))
    for ГРЕШКА in 오류들: print(*ГРЕШКА)

if __name__=='__main__': Изврши_наредба()
