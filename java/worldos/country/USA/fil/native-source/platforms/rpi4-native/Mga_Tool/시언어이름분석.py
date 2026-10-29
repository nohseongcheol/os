#!/usr/bin/env python3
"""libclang declaration·Sanggunian 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

Project_root = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class string_VALUE(씨.Structure): _fields_ = [('data',씨.c_void_p),('ipakita_VALUE',씨.c_uint)]
class kursor_VALUE(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('data',씨.c_void_p*3)]
class posisyon(씨.Structure): _fields_ = [('data',씨.c_void_p*2),('OFFSET_VALUE',씨.c_uint)]
def pormula_VALUE(pangalan, 반환, *인수):
    pagpasok_VALUE = getattr(구현, pangalan); pagpasok_VALUE.restype = 반환; pagpasok_VALUE.argtypes = list(인수); return pagpasok_VALUE
get_SMS = pormula_VALUE('clang_getCString',씨.c_char_p,string_VALUE)
release_SMS = pormula_VALUE('clang_disposeString',None,string_VALUE)
def SMS(VALUE):
    sukat = (get_SMS(VALUE) or b'').decode('utf-8'); release_SMS(VALUE); return sukat
get_pangalan = pormula_VALUE('clang_getCursorSpelling',string_VALUE,kursor_VALUE)
get_Sanggunian = pormula_VALUE('clang_getCursorReferenced',kursor_VALUE,kursor_VALUE)
get_posisyon = pormula_VALUE('clang_getCursorLocation',posisyon,kursor_VALUE)
file_posisyon = pormula_VALUE('clang_getFileLocation',None,posisyon,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
file_pagpasok_pangalan = pormula_VALUE('clang_getFileName',string_VALUE,씨.c_void_p)
UNIQUE_pangalan = pormula_VALUE('clang_getCursorUSR',string_VALUE,kursor_VALUE)
연결종류 = pormula_VALUE('clang_getCursorLinkage',씨.c_uint,kursor_VALUE)
방문형 = 씨.CFUNCTYPE(씨.c_uint,kursor_VALUE,kursor_VALUE,씨.c_void_p)
방문 = pormula_VALUE('clang_visitChildren',씨.c_uint,kursor_VALUE,방문형,씨.c_void_p)
mag_generate = pormula_VALUE('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = pormula_VALUE('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
root_VALUE = pormula_VALUE('clang_getTranslationUnitCursor',kursor_VALUE,씨.c_void_p)
lumabas_app = pormula_VALUE('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = pormula_VALUE('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = pormula_VALUE('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
kalalaan_VALUE = pormula_VALUE('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = pormula_VALUE('clang_getDiagnosticSpelling',string_VALUE,씨.c_void_p)
진단해제 = pormula_VALUE('clang_disposeDiagnostic',None,씨.c_void_p)

def posisyon_INDEX(pagpasok_VALUE):
    file = 씨.c_void_p(); linya = 씨.c_uint(); espasyo_pagpasok = 씨.c_uint(); OFFSET_VALUE = 씨.c_uint()
    file_posisyon(get_posisyon(pagpasok_VALUE),씨.byref(file),씨.byref(linya),씨.byref(espasyo_pagpasok),씨.byref(OFFSET_VALUE))
    return (SMS(file_pagpasok_pangalan(file)) if file else '', OFFSET_VALUE.value, linya.value)

def Mag_execute_utos():
    LOOKUP_INDEX = mag_generate(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 declaration 없이 TinyCC 외부 단일 TRANSLATE_pinagmulan 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, totoo_data 빌드에서는 계속 컴파일한다.
    소유파일 = {str(path.resolve()) for path in Project_root.rglob('*') if path.suffix in ('.c','.h','.cpp','.inc')
              and not set(path.relative_to(Project_root).parts)&{'build','dist','vendor','__pycache__'}
              and path.relative_to(Project_root).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(Project_root/'gumagamit'),
          '-I'+str(Project_root.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(Project_root/'build'),'-I'+str(Project_root/'build/user'),
          '-I'+str(Project_root/'build/remote'),'-I'+str(Project_root/'vendor/bearssl/inc'),
          '-I'+str(Project_root/'vendor/bearssl/src'),'-I'+str(Project_root/'vendor/libassh/src'),
          '-I'+str(Project_root/'vendor/lwip/src/include'),'-I'+str(Project_root/'Network_Stack'),
          '-I'+str(Project_root/'malayuan_VALUE'),'-I'+str(Project_root/'시언어번역기')]
    for path in sorted(Path(pangalan) for pangalan in 소유파일 if pangalan.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if path.suffix=='.cpp' else '-std=c11']
        if 'Network_Stack' in path.parts: 인수 += ['-I'+str(Project_root/'Network_Stack'),'-I'+str(Project_root/'vendor/lwip/src/include')]
        if '시언어번역기' in path.parts:
            인수 += ['-I'+str(Project_root/'시언어번역기'),'-I'+str(Project_root/'vendor/tinycc'),'-I'+str(Project_root/'build/ccompiler'),
                    '-isystem',str(Project_root.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_bridge' in path.parts:
            인수 += ['-I'+str(Project_root/'PYTHON_bridge'),'-I'+str(Project_root/'build/micropython-1.24.1'),'-I'+str(Project_root/'build/python'),'-isystem','/usr/include/newlib']
        if 'malayuan_VALUE' in path.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in path.parts: 인수 += ['-D__JKOROS__=1']
        if path.name=='bundle.c': 인수 += ['-I'+str(Project_root/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Grupo_VALUE = (씨.c_char_p*len(인수))(*[pagpasok_VALUE.encode() for pagpasok_VALUE in 인수])
        Translation_aralin = 분석(LOOKUP_INDEX,str(path).encode(),Grupo_VALUE,len(인수),None,0,1)
        for INDEX in range(진단수(Translation_aralin)):
            진단 = 진단얻기(Translation_aralin,INDEX)
            if kalalaan_VALUE(진단)>=3: 오류들.append((str(path.relative_to(Project_root)),SMS(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(pagpasok_VALUE,부모,data):
            file,OFFSET_VALUE,linya = posisyon_INDEX(pagpasok_VALUE)
            if file not in 소유파일: return 2 if pagpasok_VALUE.종류==300 else 1
            낱말 = SMS(get_pangalan(pagpasok_VALUE))
            if not 낱말 or any(ord(karakter_VALUE)>127 for karakter_VALUE in 낱말): return 2
            if pagpasok_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = SMS(UNIQUE_pangalan(pagpasok_VALUE)) or file+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'file':file,'OFFSET_VALUE':OFFSET_VALUE,'줄':linya,'종류':pagpasok_VALUE.종류,'pangalan':낱말,'CONNECT':연결종류(pagpasok_VALUE)}
                참조들.append((file,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                Sanggunian = get_Sanggunian(pagpasok_VALUE)
                Sanggunian_file,_,_ = posisyon_INDEX(Sanggunian)
                if Sanggunian_file in 소유파일:
                    UNIQUE_VALUE = SMS(UNIQUE_pangalan(Sanggunian)); 참조들.append((file,OFFSET_VALUE,SMS(get_pangalan(Sanggunian)),UNIQUE_VALUE))
            return 2
        방문(root_VALUE(Translation_aralin),살피기,None)
        lumabas_app(Translation_aralin)
    patutunguhan_VALUE = Project_root/'build/한국어화/시언어분석.json'
    patutunguhan_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {file:hashlib.sha256(Path(file).read_bytes()).hexdigest() for file in sorted(소유파일)}
    patutunguhan_VALUE.write_text(json.dumps({'declaration':선언들,'Sanggunian':참조들,'error':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('declaration',len(선언들),'Sanggunian',len(참조들),'error',len(오류들))
    for error in 오류들: print(*error)

if __name__=='__main__': Mag_execute_utos()
