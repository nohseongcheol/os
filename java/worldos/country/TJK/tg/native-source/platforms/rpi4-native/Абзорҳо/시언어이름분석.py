#!/usr/bin/env python3
"""libclang 선언·Маълумотнома 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class сатр_қимат_6ca8363c(씨.Structure): _fields_ = [('иттилоот',씨.c_void_p),('намоиш_додан_қимат',씨.c_uint)]
class курсор_қимат(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('иттилоот',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('иттилоот',씨.c_void_p*2),('Интиқолшавӣ_қимат',씨.c_uint)]
def функсия_қимат(Ном, 반환, *인수):
    ворида_қимат = getattr(구현, Ном); ворида_қимат.restype = 반환; ворида_қимат.argtypes = list(인수); return ворида_қимат
글얻기 = функсия_қимат('clang_getCString',씨.c_char_p,сатр_қимат_6ca8363c)
нашр_Матн = функсия_қимат('clang_disposeString',None,сатр_қимат_6ca8363c)
def Матн(қимат):
    결과 = (글얻기(қимат) or b'').decode('utf-8'); нашр_Матн(қимат); return 결과
이름얻기 = функсия_қимат('clang_getCursorSpelling',сатр_қимат_6ca8363c,курсор_қимат)
참조얻기 = функсия_қимат('clang_getCursorReferenced',курсор_қимат,курсор_қимат)
위치얻기 = функсия_қимат('clang_getCursorLocation',위치,курсор_қимат)
파일위치 = функсия_қимат('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
файл_ворида_ном = функсия_қимат('clang_getFileName',сатр_қимат_6ca8363c,씨.c_void_p)
고유이름 = функсия_қимат('clang_getCursorUSR',сатр_қимат_6ca8363c,курсор_қимат)
연결종류 = функсия_қимат('clang_getCursorLinkage',씨.c_uint,курсор_қимат)
방문형 = 씨.CFUNCTYPE(씨.c_uint,курсор_қимат,курсор_қимат,씨.c_void_p)
방문 = функсия_қимат('clang_visitChildren',씨.c_uint,курсор_қимат,방문형,씨.c_void_p)
생성 = функсия_қимат('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = функсия_қимат('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = функсия_қимат('clang_getTranslationUnitCursor',курсор_қимат,씨.c_void_p)
끝내기 = функсия_қимат('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = функсия_қимат('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = функсия_қимат('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
шадидият_қимат = функсия_қимат('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = функсия_қимат('clang_getDiagnosticSpelling',сатр_қимат_6ca8363c,씨.c_void_p)
진단해제 = функсия_қимат('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(ворида_қимат):
    Файл = 씨.c_void_p(); хат = 씨.c_uint(); ковокӣ_ворида = 씨.c_uint(); Интиқолшавӣ_қимат = 씨.c_uint()
    파일위치(위치얻기(ворида_қимат),씨.byref(Файл),씨.byref(хат),씨.byref(ковокӣ_ворида),씨.byref(Интиқолшавӣ_қимат))
    return (Матн(файл_ворида_ном(Файл)) if Файл else '', Интиқолшавӣ_қимат.value, хат.value)

def иҷро_кардан_фармон():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 Тарҷума_манбаъ 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, воқеӣ_иттилоот 빌드에서는 계속 컴파일한다.
    소유파일 = {str(масир.resolve()) for масир in 기준.rglob('*') if масир.suffix in ('.c','.h','.cpp','.inc')
              and not set(масир.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and масир.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'корбар'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'Шабака_ҷамъ'),
          '-I'+str(기준/'дурдаст_қимат'),'-I'+str(기준/'시언어번역기')]
    for масир in sorted(Path(Ном) for Ном in 소유파일 if Ном.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if масир.suffix=='.cpp' else '-std=c11']
        if 'Шабака_ҷамъ' in масир.parts: 인수 += ['-I'+str(기준/'Шабака_ҷамъ'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in масир.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in масир.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'дурдаст_қимат' in масир.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in масир.parts: 인수 += ['-D__JKOROS__=1']
        if масир.name=='баста.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        гуруҳ_қимат = (씨.c_char_p*len(인수))(*[ворида_қимат.encode() for ворида_қимат in 인수])
        Тарҷума_дарс = 분석(색인,str(масир).encode(),гуруҳ_қимат,len(인수),None,0,1)
        for индекс in range(진단수(Тарҷума_дарс)):
            진단 = 진단얻기(Тарҷума_дарс,индекс)
            if шадидият_қимат(진단)>=3: 오류들.append((str(масир.relative_to(기준)),Матн(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ворида_қимат,부모,иттилоот):
            Файл,Интиқолшавӣ_қимат,хат = 자리(ворида_қимат)
            if Файл not in 소유파일: return 2 if ворида_қимат.종류==300 else 1
            낱말 = Матн(이름얻기(ворида_қимат))
            if not 낱말 or any(ord(аломат_қимат_068c2631)>127 for аломат_қимат_068c2631 in 낱말): return 2
            if ворида_қимат.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = Матн(고유이름(ворида_қимат)) or Файл+':'+str(Интиқолшавӣ_қимат)
                선언들[고유] = {'Файл':Файл,'Интиқолшавӣ_қимат':Интиқолшавӣ_қимат,'줄':хат,'종류':ворида_қимат.종류,'Ном':낱말,'ПАЙВАСТ':연결종류(ворида_қимат)}
                참조들.append((Файл,Интиқолшавӣ_қимат,낱말,고유))
            else:
                Маълумотнома = 참조얻기(ворида_қимат)
                Маълумотнома_файл,_,_ = 자리(Маълумотнома)
                if Маълумотнома_файл in 소유파일:
                    고유 = Матн(고유이름(Маълумотнома)); 참조들.append((Файл,Интиқолшавӣ_қимат,Матн(이름얻기(Маълумотнома)),고유))
            return 2
        방문(뿌리(Тарҷума_дарс),살피기,None)
        끝내기(Тарҷума_дарс)
    ҷои_таъинот_қимат = 기준/'build/한국어화/시언어분석.json'
    ҷои_таъинот_қимат.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Файл:hashlib.sha256(Path(Файл).read_bytes()).hexdigest() for Файл in sorted(소유파일)}
    ҷои_таъинот_қимат.write_text(json.dumps({'선언':선언들,'Маълумотнома':참조들,'Хато':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Маълумотнома',len(참조들),'Хато',len(오류들))
    for Хато in 오류들: print(*Хато)

if __name__=='__main__': иҷро_кардан_фармон()
