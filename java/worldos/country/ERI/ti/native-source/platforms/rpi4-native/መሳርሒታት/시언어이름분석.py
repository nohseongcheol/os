#!/usr/bin/env python3
"""libclang 선언·መወከሲ 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class ሕብረ_ቁምፊ_ዋጋ(씨.Structure): _fields_ = [('ሓበሬታ',씨.c_void_p),('ኣርእይ_ዋጋ',씨.c_uint)]
class ኣመልካቲ_ዋጋ(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('ሓበሬታ',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('ሓበሬታ',씨.c_void_p*2),('ሽፋን_ዋጋ',씨.c_uint)]
def ተግባር_ዋጋ(ሽም, 반환, *인수):
    ምእታው_ዋጋ = getattr(구현, ሽም); ምእታው_ዋጋ.restype = 반환; ምእታው_ዋጋ.argtypes = list(인수); return ምእታው_ዋጋ
글얻기 = ተግባር_ዋጋ('clang_getCString',씨.c_char_p,ሕብረ_ቁምፊ_ዋጋ)
ፍታሕ_ጽሑፍ = ተግባር_ዋጋ('clang_disposeString',None,ሕብረ_ቁምፊ_ዋጋ)
def ጽሑፍ(ዋጋ):
    결과 = (글얻기(ዋጋ) or b'').decode('utf-8'); ፍታሕ_ጽሑፍ(ዋጋ); return 결과
이름얻기 = ተግባር_ዋጋ('clang_getCursorSpelling',ሕብረ_ቁምፊ_ዋጋ,ኣመልካቲ_ዋጋ)
참조얻기 = ተግባር_ዋጋ('clang_getCursorReferenced',ኣመልካቲ_ዋጋ,ኣመልካቲ_ዋጋ)
위치얻기 = ተግባር_ዋጋ('clang_getCursorLocation',위치,ኣመልካቲ_ዋጋ)
파일위치 = ተግባር_ዋጋ('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ፋይል_ምእታው_ሽም = ተግባር_ዋጋ('clang_getFileName',ሕብረ_ቁምፊ_ዋጋ,씨.c_void_p)
고유이름 = ተግባር_ዋጋ('clang_getCursorUSR',ሕብረ_ቁምፊ_ዋጋ,ኣመልካቲ_ዋጋ)
연결종류 = ተግባር_ዋጋ('clang_getCursorLinkage',씨.c_uint,ኣመልካቲ_ዋጋ)
방문형 = 씨.CFUNCTYPE(씨.c_uint,ኣመልካቲ_ዋጋ,ኣመልካቲ_ዋጋ,씨.c_void_p)
방문 = ተግባር_ዋጋ('clang_visitChildren',씨.c_uint,ኣመልካቲ_ዋጋ,방문형,씨.c_void_p)
생성 = ተግባር_ዋጋ('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = ተግባር_ዋጋ('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = ተግባር_ዋጋ('clang_getTranslationUnitCursor',ኣመልካቲ_ዋጋ,씨.c_void_p)
끝내기 = ተግባር_ዋጋ('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ተግባር_ዋጋ('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ተግባር_ዋጋ('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
ናይ_ኽብደት_ደረጃ_ዋጋ = ተግባር_ዋጋ('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ተግባር_ዋጋ('clang_getDiagnosticSpelling',ሕብረ_ቁምፊ_ዋጋ,씨.c_void_p)
진단해제 = ተግባር_ዋጋ('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(ምእታው_ዋጋ):
    ፋይል = 씨.c_void_p(); መስመር = 씨.c_uint(); መሰኩዒ_ምእታው = 씨.c_uint(); ሽፋን_ዋጋ = 씨.c_uint()
    파일위치(위치얻기(ምእታው_ዋጋ),씨.byref(ፋይል),씨.byref(መስመር),씨.byref(መሰኩዒ_ምእታው),씨.byref(ሽፋን_ዋጋ))
    return (ጽሑፍ(ፋይል_ምእታው_ሽም(ፋይል)) if ፋይል else '', ሽፋን_ዋጋ.value, መስመር.value)

def ተግብር_ትእዛዝ():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 ተርጉም_ምንጪ 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, ትኽክለኛ_ሓበሬታ 빌드에서는 계속 컴파일한다.
    소유파일 = {str(መገዲ.resolve()) for መገዲ in 기준.rglob('*') if መገዲ.suffix in ('.c','.h','.cpp','.inc')
              and not set(መገዲ.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and መገዲ.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'ተጠቃሚ'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'ማሕበራዊ_ኔትወርክ_ድርደራ'),
          '-I'+str(기준/'ርሑቕ_ዋጋ'),'-I'+str(기준/'시언어번역기')]
    for መገዲ in sorted(Path(ሽም) for ሽም in 소유파일 if ሽም.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if መገዲ.suffix=='.cpp' else '-std=c11']
        if 'ማሕበራዊ_ኔትወርክ_ድርደራ' in መገዲ.parts: 인수 += ['-I'+str(기준/'ማሕበራዊ_ኔትወርክ_ድርደራ'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in መገዲ.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in መገዲ.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'ርሑቕ_ዋጋ' in መገዲ.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in መገዲ.parts: 인수 += ['-D__JKOROS__=1']
        if መገዲ.name=='ጥማር.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        ጉጅለ_ዋጋ = (씨.c_char_p*len(인수))(*[ምእታው_ዋጋ.encode() for ምእታው_ዋጋ in 인수])
        ትርጉም_ትምህርቲ = 분석(색인,str(መገዲ).encode(),ጉጅለ_ዋጋ,len(인수),None,0,1)
        for መሐበሪ in range(진단수(ትርጉም_ትምህርቲ)):
            진단 = 진단얻기(ትርጉም_ትምህርቲ,መሐበሪ)
            if ናይ_ኽብደት_ደረጃ_ዋጋ(진단)>=3: 오류들.append((str(መገዲ.relative_to(기준)),ጽሑፍ(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ምእታው_ዋጋ,부모,ሓበሬታ):
            ፋይል,ሽፋን_ዋጋ,መስመር = 자리(ምእታው_ዋጋ)
            if ፋይል not in 소유파일: return 2 if ምእታው_ዋጋ.종류==300 else 1
            낱말 = ጽሑፍ(이름얻기(ምእታው_ዋጋ))
            if not 낱말 or any(ord(ፊደል_ዋጋ)>127 for ፊደል_ዋጋ in 낱말): return 2
            if ምእታው_ዋጋ.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = ጽሑፍ(고유이름(ምእታው_ዋጋ)) or ፋይል+':'+str(ሽፋን_ዋጋ)
                선언들[고유] = {'ፋይል':ፋይል,'ሽፋን_ዋጋ':ሽፋን_ዋጋ,'줄':መስመር,'종류':ምእታው_ዋጋ.종류,'ሽም':낱말,'ኣላግብ':연결종류(ምእታው_ዋጋ)}
                참조들.append((ፋይል,ሽፋን_ዋጋ,낱말,고유))
            else:
                መወከሲ = 참조얻기(ምእታው_ዋጋ)
                መወከሲ_ፋይል,_,_ = 자리(መወከሲ)
                if መወከሲ_ፋይል in 소유파일:
                    고유 = ጽሑፍ(고유이름(መወከሲ)); 참조들.append((ፋይል,ሽፋን_ዋጋ,ጽሑፍ(이름얻기(መወከሲ)),고유))
            return 2
        방문(뿌리(ትርጉም_ትምህርቲ),살피기,None)
        끝내기(ትርጉም_ትምህርቲ)
    መዓልቦ_ዋጋ = 기준/'build/한국어화/시언어분석.json'
    መዓልቦ_ዋጋ.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {ፋይል:hashlib.sha256(Path(ፋይል).read_bytes()).hexdigest() for ፋይል in sorted(소유파일)}
    መዓልቦ_ዋጋ.write_text(json.dumps({'선언':선언들,'መወከሲ':참조들,'ጌጋ':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'መወከሲ',len(참조들),'ጌጋ',len(오류들))
    for ጌጋ in 오류들: print(*ጌጋ)

if __name__=='__main__': ተግብር_ትእዛዝ()
