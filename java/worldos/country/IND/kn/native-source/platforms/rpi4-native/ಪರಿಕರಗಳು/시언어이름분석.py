#!/usr/bin/env python3
"""libclang ದೃಢೀಕರಣ·ಉಲ್ಲೇಖ 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

ಬಿಂಬಿಸು_ಮೂಲ = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ(씨.Structure): _fields_ = [('ಡೇಟಾ',씨.c_void_p),('ಶೋ_ಮೌಲ್ಯ',씨.c_uint)]
class ಕರ್ಸರ್_ಮೌಲ್ಯ(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('ಡೇಟಾ',씨.c_void_p*3)]
class ಸ್ಥಾನ(씨.Structure): _fields_ = [('ಡೇಟಾ',씨.c_void_p*2),('ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ',씨.c_uint)]
def ಕಾರ್ಯ_ಮೌಲ್ಯ(ಹೆಸರು, 반환, *인수):
    ನಮೂದು_ಮೌಲ್ಯ = getattr(구현, ಹೆಸರು); ನಮೂದು_ಮೌಲ್ಯ.restype = 반환; ನಮೂದು_ಮೌಲ್ಯ.argtypes = list(인수); return ನಮೂದು_ಮೌಲ್ಯ
ಪಡೆದುಕೊಳ್ಳಿ_ಪಠ್ಯ = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_getCString',씨.c_char_p,ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ)
ಬಿಡುಗಡೆ_ಪಠ್ಯ = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_disposeString',None,ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ)
def ಪಠ್ಯ(ಮೌಲ್ಯ):
    ಮಾಪನ = (ಪಡೆದುಕೊಳ್ಳಿ_ಪಠ್ಯ(ಮೌಲ್ಯ) or b'').decode('utf-8'); ಬಿಡುಗಡೆ_ಪಠ್ಯ(ಮೌಲ್ಯ); return ಮಾಪನ
ಪಡೆದುಕೊಳ್ಳಿ_ಹೆಸರು = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_getCursorSpelling',ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ,ಕರ್ಸರ್_ಮೌಲ್ಯ)
ಪಡೆದುಕೊಳ್ಳಿ_ಉಲ್ಲೇಖ = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_getCursorReferenced',ಕರ್ಸರ್_ಮೌಲ್ಯ,ಕರ್ಸರ್_ಮೌಲ್ಯ)
ಪಡೆದುಕೊಳ್ಳಿ_ಹುದ್ದೆ = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_getCursorLocation',ಸ್ಥಾನ,ಕರ್ಸರ್_ಮೌಲ್ಯ)
ಫೈಲ್_ಹುದ್ದೆ = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_getFileLocation',None,ಸ್ಥಾನ,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ಫೈಲ್_ನಮೂದು_ಹೆಸರು = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_getFileName',ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ,씨.c_void_p)
고유이름 = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_getCursorUSR',ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ,ಕರ್ಸರ್_ಮೌಲ್ಯ)
연결종류 = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_getCursorLinkage',씨.c_uint,ಕರ್ಸರ್_ಮೌಲ್ಯ)
방문형 = 씨.CFUNCTYPE(씨.c_uint,ಕರ್ಸರ್_ಮೌಲ್ಯ,ಕರ್ಸರ್_ಮೌಲ್ಯ,씨.c_void_p)
방문 = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_visitChildren',씨.c_uint,ಕರ್ಸರ್_ಮೌಲ್ಯ,방문형,씨.c_void_p)
ರಚಿಸಿ = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
ಮೂಲ_ಮೌಲ್ಯ = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_getTranslationUnitCursor',ಕರ್ಸರ್_ಮೌಲ್ಯ,씨.c_void_p)
ತೊರೆಯಿರಿ_ಅಪ್ಲಿ = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
ತೀವ್ರತೆ_ಮೌಲ್ಯ = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_getDiagnosticSpelling',ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ,씨.c_void_p)
진단해제 = ಕಾರ್ಯ_ಮೌಲ್ಯ('clang_disposeDiagnostic',None,씨.c_void_p)

def ಹುದ್ದೆ_ಪದಸೂಚಿ(ನಮೂದು_ಮೌಲ್ಯ):
    ಕಡತ = 씨.c_void_p(); ಸಾಲು = 씨.c_uint(); ಸ್ಲಾಟ್_ನಮೂದು = 씨.c_uint(); ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ = 씨.c_uint()
    ಫೈಲ್_ಹುದ್ದೆ(ಪಡೆದುಕೊಳ್ಳಿ_ಹುದ್ದೆ(ನಮೂದು_ಮೌಲ್ಯ),씨.byref(ಕಡತ),씨.byref(ಸಾಲು),씨.byref(ಸ್ಲಾಟ್_ನಮೂದು),씨.byref(ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ))
    return (ಪಠ್ಯ(ಫೈಲ್_ನಮೂದು_ಹೆಸರು(ಕಡತ)) if ಕಡತ else '', ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ.value, ಸಾಲು.value)

def ಪೂರೈಸು_ಆದೇಶ():
    ನೋಡುವ_ಪದಸೂಚಿ = ರಚಿಸಿ(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 ದೃಢೀಕರಣ 없이 TinyCC 외부 단일 ಅನುವಾದಿಸು_ಮೂಲ 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, ನಿಜವಾದ_ಡೇಟಾ 빌드에서는 계속 컴파일한다.
    소유파일 = {str(ಮಾರ್ಗ.resolve()) for ಮಾರ್ಗ in ಬಿಂಬಿಸು_ಮೂಲ.rglob('*') if ಮಾರ್ಗ.suffix in ('.c','.h','.cpp','.inc')
              and not set(ಮಾರ್ಗ.relative_to(ಬಿಂಬಿಸು_ಮೂಲ).parts)&{'build','dist','vendor','__pycache__'}
              and ಮಾರ್ಗ.relative_to(ಬಿಂಬಿಸು_ಮೂಲ).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'ಬಳಕೆದಾರ'),
          '-I'+str(ಬಿಂಬಿಸು_ಮೂಲ.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'build'),'-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'build/user'),
          '-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'build/remote'),'-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'vendor/bearssl/inc'),
          '-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'vendor/bearssl/src'),'-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'vendor/libassh/src'),
          '-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'vendor/lwip/src/include'),'-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್'),
          '-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'ರಿಮೋಟ್_ಮೌಲ್ಯ'),'-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'시언어번역기')]
    for ಮಾರ್ಗ in sorted(Path(ಹೆಸರು) for ಹೆಸರು in 소유파일 if ಹೆಸರು.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if ಮಾರ್ಗ.suffix=='.cpp' else '-std=c11']
        if 'ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್' in ಮಾರ್ಗ.parts: 인수 += ['-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್'),'-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'vendor/lwip/src/include')]
        if '시언어번역기' in ಮಾರ್ಗ.parts:
            인수 += ['-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'시언어번역기'),'-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'vendor/tinycc'),'-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'build/ccompiler'),
                    '-isystem',str(ಬಿಂಬಿಸು_ಮೂಲ.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in ಮಾರ್ಗ.parts:
            인수 += ['-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'파이썬연결'),'-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'build/micropython-1.24.1'),'-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'build/python'),'-isystem','/usr/include/newlib']
        if 'ರಿಮೋಟ್_ಮೌಲ್ಯ' in ಮಾರ್ಗ.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in ಮಾರ್ಗ.parts: 인수 += ['-D__JKOROS__=1']
        if ಮಾರ್ಗ.name=='ಬಂಡಲ್.c': 인수 += ['-I'+str(ಬಿಂಬಿಸು_ಮೂಲ/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        ಸಮೂಹ_ಮೌಲ್ಯ = (씨.c_char_p*len(인수))(*[ನಮೂದು_ಮೌಲ್ಯ.encode() for ನಮೂದು_ಮೌಲ್ಯ in 인수])
        ಅನುವಾದ_ಅಧ್ಯಯನ = 분석(ನೋಡುವ_ಪದಸೂಚಿ,str(ಮಾರ್ಗ).encode(),ಸಮೂಹ_ಮೌಲ್ಯ,len(인수),None,0,1)
        for ಪದಸೂಚಿ in range(진단수(ಅನುವಾದ_ಅಧ್ಯಯನ)):
            진단 = 진단얻기(ಅನುವಾದ_ಅಧ್ಯಯನ,ಪದಸೂಚಿ)
            if ತೀವ್ರತೆ_ಮೌಲ್ಯ(진단)>=3: 오류들.append((str(ಮಾರ್ಗ.relative_to(ಬಿಂಬಿಸು_ಮೂಲ)),ಪಠ್ಯ(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ನಮೂದು_ಮೌಲ್ಯ,부모,ಡೇಟಾ):
            ಕಡತ,ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ,ಸಾಲು = ಹುದ್ದೆ_ಪದಸೂಚಿ(ನಮೂದು_ಮೌಲ್ಯ)
            if ಕಡತ not in 소유파일: return 2 if ನಮೂದು_ಮೌಲ್ಯ.종류==300 else 1
            낱말 = ಪಠ್ಯ(ಪಡೆದುಕೊಳ್ಳಿ_ಹೆಸರು(ನಮೂದು_ಮೌಲ್ಯ))
            if not 낱말 or any(ord(ಅಕ್ಷರ_ಮೌಲ್ಯ)>127 for ಅಕ್ಷರ_ಮೌಲ್ಯ in 낱말): return 2
            if ನಮೂದು_ಮೌಲ್ಯ.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = ಪಠ್ಯ(고유이름(ನಮೂದು_ಮೌಲ್ಯ)) or ಕಡತ+':'+str(ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
                선언들[고유] = {'ಕಡತ':ಕಡತ,'ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ':ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ,'줄':ಸಾಲು,'종류':ನಮೂದು_ಮೌಲ್ಯ.종류,'ಹೆಸರು':낱말,'ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು':연결종류(ನಮೂದು_ಮೌಲ್ಯ)}
                참조들.append((ಕಡತ,ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ,낱말,고유))
            else:
                ಉಲ್ಲೇಖ = ಪಡೆದುಕೊಳ್ಳಿ_ಉಲ್ಲೇಖ(ನಮೂದು_ಮೌಲ್ಯ)
                ಉಲ್ಲೇಖ_ಫೈಲ್,_,_ = ಹುದ್ದೆ_ಪದಸೂಚಿ(ಉಲ್ಲೇಖ)
                if ಉಲ್ಲೇಖ_ಫೈಲ್ in 소유파일:
                    고유 = ಪಠ್ಯ(고유이름(ಉಲ್ಲೇಖ)); 참조들.append((ಕಡತ,ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ,ಪಠ್ಯ(ಪಡೆದುಕೊಳ್ಳಿ_ಹೆಸರು(ಉಲ್ಲೇಖ)),고유))
            return 2
        방문(ಮೂಲ_ಮೌಲ್ಯ(ಅನುವಾದ_ಅಧ್ಯಯನ),살피기,None)
        ತೊರೆಯಿರಿ_ಅಪ್ಲಿ(ಅನುವಾದ_ಅಧ್ಯಯನ)
    ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ = ಬಿಂಬಿಸು_ಮೂಲ/'build/한국어화/시언어분석.json'
    ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {ಕಡತ:hashlib.sha256(Path(ಕಡತ).read_bytes()).hexdigest() for ಕಡತ in sorted(소유파일)}
    ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ.write_text(json.dumps({'ದೃಢೀಕರಣ':선언들,'ಉಲ್ಲೇಖ':참조들,'ದೋಷ':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('ದೃಢೀಕರಣ',len(선언들),'ಉಲ್ಲೇಖ',len(참조들),'ದೋಷ',len(오류들))
    for ದೋಷ in 오류들: print(*ದೋಷ)

if __name__=='__main__': ಪೂರೈಸು_ಆದೇಶ()
