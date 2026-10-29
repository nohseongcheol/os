#!/usr/bin/env python3
"""libclang 선언·Шилтемелер 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class сап_маани(씨.Structure): _fields_ = [('берилмелер',씨.c_void_p),('көрсөтүү_маани',씨.c_uint)]
class курсор_маани(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('берилмелер',씨.c_void_p*3)]
class Турган_жери(씨.Structure): _fields_ = [('берилмелер',씨.c_void_p*2),('Жылбышуу_маани',씨.c_uint)]
def функция_маани(Аты, 반환, *인수):
    киргизме_жазуу_маани = getattr(구현, Аты); киргизме_жазуу_маани.restype = 반환; киргизме_жазуу_маани.argtypes = list(인수); return киргизме_жазуу_маани
글얻기 = функция_маани('clang_getCString',씨.c_char_p,сап_маани)
чыгаруу_СМС = функция_маани('clang_disposeString',None,сап_маани)
def Текст(маани):
    결과 = (글얻기(маани) or b'').decode('utf-8'); чыгаруу_СМС(маани); return 결과
이름얻기 = функция_маани('clang_getCursorSpelling',сап_маани,курсор_маани)
참조얻기 = функция_маани('clang_getCursorReferenced',курсор_маани,курсор_маани)
위치얻기 = функция_маани('clang_getCursorLocation',Турган_жери,курсор_маани)
파일위치 = функция_маани('clang_getFileLocation',None,Турган_жери,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
файл_киргизме_жазуу_аты = функция_маани('clang_getFileName',сап_маани,씨.c_void_p)
ОКШОШТУКЖОК_аты = функция_маани('clang_getCursorUSR',сап_маани,курсор_маани)
연결종류 = функция_маани('clang_getCursorLinkage',씨.c_uint,курсор_маани)
방문형 = 씨.CFUNCTYPE(씨.c_uint,курсор_маани,курсор_маани,씨.c_void_p)
방문 = функция_маани('clang_visitChildren',씨.c_uint,курсор_маани,방문형,씨.c_void_p)
생성 = функция_маани('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = функция_маани('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = функция_маани('clang_getTranslationUnitCursor',курсор_маани,씨.c_void_p)
끝내기 = функция_маани('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = функция_маани('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = функция_маани('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
чындыкка_дал_келүүсү_маани = функция_маани('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = функция_маани('clang_getDiagnosticSpelling',сап_маани,씨.c_void_p)
진단해제 = функция_маани('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(киргизме_жазуу_маани):
    Файл = 씨.c_void_p(); сап = 씨.c_uint(); оюкча_киргизме_жазуу = 씨.c_uint(); Жылбышуу_маани = 씨.c_uint()
    파일위치(위치얻기(киргизме_жазуу_маани),씨.byref(Файл),씨.byref(сап),씨.byref(оюкча_киргизме_жазуу),씨.byref(Жылбышуу_маани))
    return (Текст(файл_киргизме_жазуу_аты(Файл)) if Файл else '', Жылбышуу_маани.value, сап.value)

def аткаруу_буйрук():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 Которуу_башат 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, актуалдуу_берилмелер 빌드에서는 계속 컴파일한다.
    소유파일 = {str(ЖОЛ.resolve()) for ЖОЛ in 기준.rglob('*') if ЖОЛ.suffix in ('.c','.h','.cpp','.inc')
              and not set(ЖОЛ.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and ЖОЛ.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'колдонуучу'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'Желе_стек'),
          '-I'+str(기준/'алыскы_маани'),'-I'+str(기준/'시언어번역기')]
    for ЖОЛ in sorted(Path(Аты) for Аты in 소유파일 if Аты.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if ЖОЛ.suffix=='.cpp' else '-std=c11']
        if 'Желе_стек' in ЖОЛ.parts: 인수 += ['-I'+str(기준/'Желе_стек'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in ЖОЛ.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in ЖОЛ.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'алыскы_маани' in ЖОЛ.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in ЖОЛ.parts: 인수 += ['-D__JKOROS__=1']
        if ЖОЛ.name=='пакет.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        топ_маани = (씨.c_char_p*len(인수))(*[киргизме_жазуу_маани.encode() for киргизме_жазуу_маани in 인수])
        Которуу_сабак = 분석(색인,str(ЖОЛ).encode(),топ_маани,len(인수),None,0,1)
        for индекс in range(진단수(Которуу_сабак)):
            진단 = 진단얻기(Которуу_сабак,индекс)
            if чындыкка_дал_келүүсү_маани(진단)>=3: 오류들.append((str(ЖОЛ.relative_to(기준)),Текст(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(киргизме_жазуу_маани,부모,берилмелер):
            Файл,Жылбышуу_маани,сап = 자리(киргизме_жазуу_маани)
            if Файл not in 소유파일: return 2 if киргизме_жазуу_маани.종류==300 else 1
            낱말 = Текст(이름얻기(киргизме_жазуу_маани))
            if not 낱말 or any(ord(символ_маани_068c2631)>127 for символ_маани_068c2631 in 낱말): return 2
            if киргизме_жазуу_маани.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                ОКШОШТУКЖОК_маани = Текст(ОКШОШТУКЖОК_аты(киргизме_жазуу_маани)) or Файл+':'+str(Жылбышуу_маани)
                선언들[ОКШОШТУКЖОК_маани] = {'Файл':Файл,'Жылбышуу_маани':Жылбышуу_маани,'줄':сап,'종류':киргизме_жазуу_маани.종류,'Аты':낱말,'Туташуу':연결종류(киргизме_жазуу_маани)}
                참조들.append((Файл,Жылбышуу_маани,낱말,ОКШОШТУКЖОК_маани))
            else:
                Шилтемелер = 참조얻기(киргизме_жазуу_маани)
                Шилтемелер_файл,_,_ = 자리(Шилтемелер)
                if Шилтемелер_файл in 소유파일:
                    ОКШОШТУКЖОК_маани = Текст(ОКШОШТУКЖОК_аты(Шилтемелер)); 참조들.append((Файл,Жылбышуу_маани,Текст(이름얻기(Шилтемелер)),ОКШОШТУКЖОК_маани))
            return 2
        방문(뿌리(Которуу_сабак),살피기,None)
        끝내기(Которуу_сабак)
    көздөө_жайы_маани = 기준/'build/한국어화/시언어분석.json'
    көздөө_жайы_маани.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Файл:hashlib.sha256(Path(Файл).read_bytes()).hexdigest() for Файл in sorted(소유파일)}
    көздөө_жайы_маани.write_text(json.dumps({'선언':선언들,'Шилтемелер':참조들,'Ката':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Шилтемелер',len(참조들),'Ката',len(오류들))
    for Ката in 오류들: print(*Ката)

if __name__=='__main__': аткаруу_буйрук()
