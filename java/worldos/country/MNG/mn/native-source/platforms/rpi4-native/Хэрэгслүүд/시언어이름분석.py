#!/usr/bin/env python3
"""libclang 선언·Толь_лавлах 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class мөр_утга_6ca8363c(씨.Structure): _fields_ = [('өгөгдөл',씨.c_void_p),('үзүүлэх_утга',씨.c_uint)]
class курсор_утга(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('өгөгдөл',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('өгөгдөл',씨.c_void_p*2),('Оффсет_утга',씨.c_uint)]
def ФУНКЦ_утга(Нэр, 반환, *인수):
    оролт_утга = getattr(구현, Нэр); оролт_утга.restype = 반환; оролт_утга.argtypes = list(인수); return оролт_утга
글얻기 = ФУНКЦ_утга('clang_getCString',씨.c_char_p,мөр_утга_6ca8363c)
гарц_Бичвэр = ФУНКЦ_утга('clang_disposeString',None,мөр_утга_6ca8363c)
def Бичвэр(утга):
    결과 = (글얻기(утга) or b'').decode('utf-8'); гарц_Бичвэр(утга); return 결과
이름얻기 = ФУНКЦ_утга('clang_getCursorSpelling',мөр_утга_6ca8363c,курсор_утга)
참조얻기 = ФУНКЦ_утга('clang_getCursorReferenced',курсор_утга,курсор_утга)
위치얻기 = ФУНКЦ_утга('clang_getCursorLocation',위치,курсор_утга)
파일위치 = ФУНКЦ_утга('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
файл_оролт_нэр = ФУНКЦ_утга('clang_getFileName',мөр_утга_6ca8363c,씨.c_void_p)
ЦОР_ГАНЦ_нэр = ФУНКЦ_утга('clang_getCursorUSR',мөр_утга_6ca8363c,курсор_утга)
연결종류 = ФУНКЦ_утга('clang_getCursorLinkage',씨.c_uint,курсор_утга)
방문형 = 씨.CFUNCTYPE(씨.c_uint,курсор_утга,курсор_утга,씨.c_void_p)
방문 = ФУНКЦ_утга('clang_visitChildren',씨.c_uint,курсор_утга,방문형,씨.c_void_p)
생성 = ФУНКЦ_утга('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = ФУНКЦ_утга('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = ФУНКЦ_утга('clang_getTranslationUnitCursor',курсор_утга,씨.c_void_p)
끝내기 = ФУНКЦ_утга('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ФУНКЦ_утга('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ФУНКЦ_утга('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
аюулын_түвшин_утга = ФУНКЦ_утга('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ФУНКЦ_утга('clang_getDiagnosticSpelling',мөр_утга_6ca8363c,씨.c_void_p)
진단해제 = ФУНКЦ_утга('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(оролт_утга):
    Файл = 씨.c_void_p(); Шугам = 씨.c_uint(); зай_оролт = 씨.c_uint(); Оффсет_утга = 씨.c_uint()
    파일위치(위치얻기(оролт_утга),씨.byref(Файл),씨.byref(Шугам),씨.byref(зай_оролт),씨.byref(Оффсет_утга))
    return (Бичвэр(файл_оролт_нэр(Файл)) if Файл else '', Оффсет_утга.value, Шугам.value)

def Гүйцэтгэх_команд():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 Орчуулах_эх 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, бодит_өгөгдөл 빌드에서는 계속 컴파일한다.
    소유파일 = {str(ЗАМ.resolve()) for ЗАМ in 기준.rglob('*') if ЗАМ.suffix in ('.c','.h','.cpp','.inc')
              and not set(ЗАМ.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and ЗАМ.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'хэрэглэгч'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'Сүлжээ_давхцал'),
          '-I'+str(기준/'алсын_утга'),'-I'+str(기준/'시언어번역기')]
    for ЗАМ in sorted(Path(Нэр) for Нэр in 소유파일 if Нэр.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if ЗАМ.suffix=='.cpp' else '-std=c11']
        if 'Сүлжээ_давхцал' in ЗАМ.parts: 인수 += ['-I'+str(기준/'Сүлжээ_давхцал'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in ЗАМ.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in ЗАМ.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'алсын_утга' in ЗАМ.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in ЗАМ.parts: 인수 += ['-D__JKOROS__=1']
        if ЗАМ.name=='багц.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        бүлэг_утга = (씨.c_char_p*len(인수))(*[оролт_утга.encode() for оролт_утга in 인수])
        Орчуулга_хичээл = 분석(색인,str(ЗАМ).encode(),бүлэг_утга,len(인수),None,0,1)
        for индекс in range(진단수(Орчуулга_хичээл)):
            진단 = 진단얻기(Орчуулга_хичээл,индекс)
            if аюулын_түвшин_утга(진단)>=3: 오류들.append((str(ЗАМ.relative_to(기준)),Бичвэр(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(оролт_утга,부모,өгөгдөл):
            Файл,Оффсет_утга,Шугам = 자리(оролт_утга)
            if Файл not in 소유파일: return 2 if оролт_утга.종류==300 else 1
            낱말 = Бичвэр(이름얻기(оролт_утга))
            if not 낱말 or any(ord(тэмдэгт_утга)>127 for тэмдэгт_утга in 낱말): return 2
            if оролт_утга.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                ЦОР_ГАНЦ_утга = Бичвэр(ЦОР_ГАНЦ_нэр(оролт_утга)) or Файл+':'+str(Оффсет_утга)
                선언들[ЦОР_ГАНЦ_утга] = {'Файл':Файл,'Оффсет_утга':Оффсет_утга,'Шугам':Шугам,'종류':оролт_утга.종류,'Нэр':낱말,'Холбох':연결종류(оролт_утга)}
                참조들.append((Файл,Оффсет_утга,낱말,ЦОР_ГАНЦ_утга))
            else:
                Толь_лавлах = 참조얻기(оролт_утга)
                Толь_лавлах_файл,_,_ = 자리(Толь_лавлах)
                if Толь_лавлах_файл in 소유파일:
                    ЦОР_ГАНЦ_утга = Бичвэр(ЦОР_ГАНЦ_нэр(Толь_лавлах)); 참조들.append((Файл,Оффсет_утга,Бичвэр(이름얻기(Толь_лавлах)),ЦОР_ГАНЦ_утга))
            return 2
        방문(뿌리(Орчуулга_хичээл),살피기,None)
        끝내기(Орчуулга_хичээл)
    товлосон_газар_утга = 기준/'build/한국어화/시언어분석.json'
    товлосон_газар_утга.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Файл:hashlib.sha256(Path(Файл).read_bytes()).hexdigest() for Файл in sorted(소유파일)}
    товлосон_газар_утга.write_text(json.dumps({'선언':선언들,'Толь_лавлах':참조들,'Алдаа':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Толь_лавлах',len(참조들),'Алдаа',len(오류들))
    for Алдаа in 오류들: print(*Алдаа)

if __name__=='__main__': Гүйцэтгэх_команд()
