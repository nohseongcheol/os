#!/usr/bin/env python3
"""libclang 선언·참조 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class стринг_вриједност(씨.Structure): _fields_ = [('подаци',씨.c_void_p),('приказати_вриједност',씨.c_uint)]
class курсор_вриједност(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('подаци',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('подаци',씨.c_void_p*2),('변위',씨.c_uint)]
def функција_вриједност(назив, 반환, *인수):
    унос_вриједност = getattr(구현, назив); унос_вриједност.restype = 반환; унос_вриједност.argtypes = list(인수); return унос_вриједност
글얻기 = функција_вриједност('clang_getCString',씨.c_char_p,стринг_вриједност)
издање_текст = функција_вриједност('clang_disposeString',None,стринг_вриједност)
def текст(вриједност):
    결과 = (글얻기(вриједност) or b'').decode('utf-8'); издање_текст(вриједност); return 결과
이름얻기 = функција_вриједност('clang_getCursorSpelling',стринг_вриједност,курсор_вриједност)
참조얻기 = функција_вриједност('clang_getCursorReferenced',курсор_вриједност,курсор_вриједност)
위치얻기 = функција_вриједност('clang_getCursorLocation',위치,курсор_вриједност)
파일위치 = функција_вриједност('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
фајл_унос_назив = функција_вриједност('clang_getFileName',стринг_вриједност,씨.c_void_p)
고유이름 = функција_вриједност('clang_getCursorUSR',стринг_вриједност,курсор_вриједност)
연결종류 = функција_вриједност('clang_getCursorLinkage',씨.c_uint,курсор_вриједност)
방문형 = 씨.CFUNCTYPE(씨.c_uint,курсор_вриједност,курсор_вриједност,씨.c_void_p)
방문 = функција_вриједност('clang_visitChildren',씨.c_uint,курсор_вриједност,방문형,씨.c_void_p)
생성 = функција_вриједност('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = функција_вриједност('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = функција_вриједност('clang_getTranslationUnitCursor',курсор_вриједност,씨.c_void_p)
끝내기 = функција_вриједност('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = функција_вриједност('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = функција_вриједност('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
심각도 = функција_вриједност('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = функција_вриједност('clang_getDiagnosticSpelling',стринг_вриједност,씨.c_void_p)
진단해제 = функција_вриједност('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(унос_вриједност):
    фајл = 씨.c_void_p(); редак = 씨.c_uint(); 칸 = 씨.c_uint(); 변위 = 씨.c_uint()
    파일위치(위치얻기(унос_вриједност),씨.byref(фајл),씨.byref(редак),씨.byref(칸),씨.byref(변위))
    return (текст(фајл_унос_назив(фајл)) if фајл else '', 변위.value, редак.value)

def 실행():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 번역 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, стваран_подаци 빌드에서는 계속 컴파일한다.
    소유파일 = {str(пут.resolve()) for пут in 기준.rglob('*') if пут.suffix in ('.c','.h','.cpp','.inc')
              and not set(пут.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and пут.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'корисник'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'통신망'),
          '-I'+str(기준/'удаљено_вриједност'),'-I'+str(기준/'시언어번역기')]
    for пут in sorted(Path(назив) for назив in 소유파일 if назив.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if пут.suffix=='.cpp' else '-std=c11']
        if '통신망' in пут.parts: 인수 += ['-I'+str(기준/'통신망'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in пут.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in пут.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'удаљено_вриједност' in пут.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in пут.parts: 인수 += ['-D__JKOROS__=1']
        if пут.name=='пакет.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        група_вриједност = (씨.c_char_p*len(인수))(*[унос_вриједност.encode() for унос_вриједност in 인수])
        번역단위 = 분석(색인,str(пут).encode(),група_вриједност,len(인수),None,0,1)
        for индекс in range(진단수(번역단위)):
            진단 = 진단얻기(번역단위,индекс)
            if 심각도(진단)>=3: 오류들.append((str(пут.relative_to(기준)),текст(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(унос_вриједност,부모,подаци):
            фајл,변위,редак = 자리(унос_вриједност)
            if фајл not in 소유파일: return 2 if унос_вриједност.종류==300 else 1
            낱말 = текст(이름얻기(унос_вриједност))
            if not 낱말 or any(ord(знак_вриједност)>127 for знак_вриједност in 낱말): return 2
            if унос_вриједност.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = текст(고유이름(унос_вриједност)) or фајл+':'+str(변위)
                선언들[고유] = {'фајл':фајл,'변위':변위,'줄':редак,'종류':унос_вриједност.종류,'назив':낱말,'повезати':연결종류(унос_вриједност)}
                참조들.append((фајл,변위,낱말,고유))
            else:
                참조 = 참조얻기(унос_вриједност)
                참조파일,_,_ = 자리(참조)
                if 참조파일 in 소유파일:
                    고유 = текст(고유이름(참조)); 참조들.append((фајл,변위,текст(이름얻기(참조)),고유))
            return 2
        방문(뿌리(번역단위),살피기,None)
        끝내기(번역단위)
    одредиште_вриједност = 기준/'build/한국어화/시언어분석.json'
    одредиште_вриједност.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {фајл:hashlib.sha256(Path(фајл).read_bytes()).hexdigest() for фајл in sorted(소유파일)}
    одредиште_вриједност.write_text(json.dumps({'선언':선언들,'참조':참조들,'грешка':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'참조',len(참조들),'грешка',len(오류들))
    for грешка in 오류들: print(*грешка)

if __name__=='__main__': 실행()
