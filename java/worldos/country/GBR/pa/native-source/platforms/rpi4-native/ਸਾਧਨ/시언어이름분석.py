#!/usr/bin/env python3
"""libclang 선언·ਸੰਦਰਭ 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ(씨.Structure): _fields_ = [('ਸਮੱਗਰੀ',씨.c_void_p),('ਸ਼ੋਅ_ਕੀਮਤ',씨.c_uint)]
class ਕਰਸਰ_ਕੀਮਤ(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('ਸਮੱਗਰੀ',씨.c_void_p*3)]
class ਸਥਿਤੀ(씨.Structure): _fields_ = [('ਸਮੱਗਰੀ',씨.c_void_p*2),('ਔਫਸੈਟ_ਕੀਮਤ',씨.c_uint)]
def ਫੰਗਸ਼ਨ_ਕੀਮਤ(ਨਾਂ, 반환, *ਆਰਗੂਮੈਂਟ):
    ਦਾਖਲਾ_ਕੀਮਤ = getattr(구현, ਨਾਂ); ਦਾਖਲਾ_ਕੀਮਤ.restype = 반환; ਦਾਖਲਾ_ਕੀਮਤ.argtypes = list(ਆਰਗੂਮੈਂਟ); return ਦਾਖਲਾ_ਕੀਮਤ
글얻기 = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_getCString',씨.c_char_p,ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ)
ਰਿਲੀਜ_ਪਾਠ = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_disposeString',None,ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ)
def ਟੈਕਸਟ(ਕੀਮਤ):
    ਮਾਪ = (글얻기(ਕੀਮਤ) or b'').decode('utf-8'); ਰਿਲੀਜ_ਪਾਠ(ਕੀਮਤ); return ਮਾਪ
이름얻기 = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_getCursorSpelling',ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ,ਕਰਸਰ_ਕੀਮਤ)
참조얻기 = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_getCursorReferenced',ਕਰਸਰ_ਕੀਮਤ,ਕਰਸਰ_ਕੀਮਤ)
위치얻기 = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_getCursorLocation',ਸਥਿਤੀ,ਕਰਸਰ_ਕੀਮਤ)
ਲਿਖਤ_ਪੱਤਰ_ਸਥਿਤੀ_ਬਦਲੋ = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_getFileLocation',None,ਸਥਿਤੀ,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_getFileName',ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ,씨.c_void_p)
고유이름 = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_getCursorUSR',ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ,ਕਰਸਰ_ਕੀਮਤ)
연결종류 = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_getCursorLinkage',씨.c_uint,ਕਰਸਰ_ਕੀਮਤ)
방문형 = 씨.CFUNCTYPE(씨.c_uint,ਕਰਸਰ_ਕੀਮਤ,ਕਰਸਰ_ਕੀਮਤ,씨.c_void_p)
방문 = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_visitChildren',씨.c_uint,ਕਰਸਰ_ਕੀਮਤ,방문형,씨.c_void_p)
ਜਨਰੇਟ_ਕਰੋ = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
ਰੂਟ_ਕੀਮਤ = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_getTranslationUnitCursor',ਕਰਸਰ_ਕੀਮਤ,씨.c_void_p)
ਬੰਦ_ਕਰੋ_ਐਪਲੀਕੇਸ਼ = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
ਤੀਬਰਤਾ_ਕੀਮਤ = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_getDiagnosticSpelling',ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ,씨.c_void_p)
진단해제 = ਫੰਗਸ਼ਨ_ਕੀਮਤ('clang_disposeDiagnostic',None,씨.c_void_p)

def ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ(ਦਾਖਲਾ_ਕੀਮਤ):
    ਫਾਇਲ = 씨.c_void_p(); ਲਾਈਨ = 씨.c_uint(); ਸਲੌਟ_ਦਾਖਲਾ = 씨.c_uint(); ਔਫਸੈਟ_ਕੀਮਤ = 씨.c_uint()
    ਲਿਖਤ_ਪੱਤਰ_ਸਥਿਤੀ_ਬਦਲੋ(위치얻기(ਦਾਖਲਾ_ਕੀਮਤ),씨.byref(ਫਾਇਲ),씨.byref(ਲਾਈਨ),씨.byref(ਸਲੌਟ_ਦਾਖਲਾ),씨.byref(ਔਫਸੈਟ_ਕੀਮਤ))
    return (ਟੈਕਸਟ(ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ(ਫਾਇਲ)) if ਫਾਇਲ else '', ਔਫਸੈਟ_ਕੀਮਤ.value, ਲਾਈਨ.value)

def ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼():
    ਲੱਭਣਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ = ਜਨਰੇਟ_ਕਰੋ(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 ਅਨੁਵਾਦ_ਸਰੋਤ 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, ਅਸਲ_ਸਮੱਗਰੀ 빌드에서는 계속 컴파일한다.
    소유파일 = {str(ਮਾਰਗ.resolve()) for ਮਾਰਗ in ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.rglob('*') if ਮਾਰਗ.suffix in ('.c','.h','.cpp','.inc')
              and not set(ਮਾਰਗ.relative_to(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ).parts)&{'build','dist','vendor','__pycache__'}
              and ਮਾਰਗ.relative_to(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਉਪਭੋਗਤਾ'),
          '-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build'),'-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/user'),
          '-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/remote'),'-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'vendor/bearssl/inc'),
          '-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'vendor/bearssl/src'),'-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'vendor/libassh/src'),
          '-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'vendor/lwip/src/include'),'-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਨੈਟਵਰਕ_ਸਟੈਕ'),
          '-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਰਿਮੋਟ_ਕੀਮਤ'),'-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'시언어번역기')]
    for ਮਾਰਗ in sorted(Path(ਨਾਂ) for ਨਾਂ in 소유파일 if ਨਾਂ.endswith(('.c','.cpp'))):
        ਆਰਗੂਮੈਂਟ = 공통 + ['-std=c++11' if ਮਾਰਗ.suffix=='.cpp' else '-std=c11']
        if 'ਨੈਟਵਰਕ_ਸਟੈਕ' in ਮਾਰਗ.parts: ਆਰਗੂਮੈਂਟ += ['-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਨੈਟਵਰਕ_ਸਟੈਕ'),'-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'vendor/lwip/src/include')]
        if '시언어번역기' in ਮਾਰਗ.parts:
            ਆਰਗੂਮੈਂਟ += ['-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'시언어번역기'),'-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'vendor/tinycc'),'-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/ccompiler'),
                    '-isystem',str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in ਮਾਰਗ.parts:
            ਆਰਗੂਮੈਂਟ += ['-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'파이썬연결'),'-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/micropython-1.24.1'),'-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/python'),'-isystem','/usr/include/newlib']
        if 'ਰਿਮੋਟ_ਕੀਮਤ' in ਮਾਰਗ.parts:
            ਆਰਗੂਮੈਂਟ += ['-isystem', '/usr/include/newlib']
        if '배포' in ਮਾਰਗ.parts: ਆਰਗੂਮੈਂਟ += ['-D__JKOROS__=1']
        if ਮਾਰਗ.name=='ਬੰਡਲ.c': ਆਰਗੂਮੈਂਟ += ['-I'+str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        ਸਮੂਹ_ਕੀਮਤ = (씨.c_char_p*len(ਆਰਗੂਮੈਂਟ))(*[ਦਾਖਲਾ_ਕੀਮਤ.encode() for ਦਾਖਲਾ_ਕੀਮਤ in ਆਰਗੂਮੈਂਟ])
        ਅਨੁਵਾਦ_ਪਾਠ = 분석(ਲੱਭਣਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ,str(ਮਾਰਗ).encode(),ਸਮੂਹ_ਕੀਮਤ,len(ਆਰਗੂਮੈਂਟ),None,0,1)
        for ਅਨੁਕ੍ਰਮਣਿਕਾ in range(진단수(ਅਨੁਵਾਦ_ਪਾਠ)):
            진단 = 진단얻기(ਅਨੁਵਾਦ_ਪਾਠ,ਅਨੁਕ੍ਰਮਣਿਕਾ)
            if ਤੀਬਰਤਾ_ਕੀਮਤ(진단)>=3: 오류들.append((str(ਮਾਰਗ.relative_to(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ)),ਟੈਕਸਟ(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ਦਾਖਲਾ_ਕੀਮਤ,부모,ਸਮੱਗਰੀ):
            ਫਾਇਲ,ਔਫਸੈਟ_ਕੀਮਤ,ਲਾਈਨ = ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ(ਦਾਖਲਾ_ਕੀਮਤ)
            if ਫਾਇਲ not in 소유파일: return 2 if ਦਾਖਲਾ_ਕੀਮਤ.종류==300 else 1
            낱말 = ਟੈਕਸਟ(이름얻기(ਦਾਖਲਾ_ਕੀਮਤ))
            if not 낱말 or any(ord(ਵਰਣ_ਕੀਮਤ)>127 for ਵਰਣ_ਕੀਮਤ in 낱말): return 2
            if ਦਾਖਲਾ_ਕੀਮਤ.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = ਟੈਕਸਟ(고유이름(ਦਾਖਲਾ_ਕੀਮਤ)) or ਫਾਇਲ+':'+str(ਔਫਸੈਟ_ਕੀਮਤ)
                선언들[고유] = {'ਫਾਇਲ':ਫਾਇਲ,'ਔਫਸੈਟ_ਕੀਮਤ':ਔਫਸੈਟ_ਕੀਮਤ,'ਲਾਈਨ':ਲਾਈਨ,'종류':ਦਾਖਲਾ_ਕੀਮਤ.종류,'ਨਾਂ':낱말,'ਕੁਨੈਕਸ਼ਨ_ਕਰੋ':연결종류(ਦਾਖਲਾ_ਕੀਮਤ)}
                참조들.append((ਫਾਇਲ,ਔਫਸੈਟ_ਕੀਮਤ,낱말,고유))
            else:
                ਸੰਦਰਭ = 참조얻기(ਦਾਖਲਾ_ਕੀਮਤ)
                ਸੰਦਰਭ_ਲਿਖਤ_ਪੱਤਰ,_,_ = ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ(ਸੰਦਰਭ)
                if ਸੰਦਰਭ_ਲਿਖਤ_ਪੱਤਰ in 소유파일:
                    고유 = ਟੈਕਸਟ(고유이름(ਸੰਦਰਭ)); 참조들.append((ਫਾਇਲ,ਔਫਸੈਟ_ਕੀਮਤ,ਟੈਕਸਟ(이름얻기(ਸੰਦਰਭ)),고유))
            return 2
        방문(ਰੂਟ_ਕੀਮਤ(ਅਨੁਵਾਦ_ਪਾਠ),살피기,None)
        ਬੰਦ_ਕਰੋ_ਐਪਲੀਕੇਸ਼(ਅਨੁਵਾਦ_ਪਾਠ)
    ਮੰਜਿਲ_ਕੀਮਤ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/한국어화/시언어분석.json'
    ਮੰਜਿਲ_ਕੀਮਤ.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {ਫਾਇਲ:hashlib.sha256(Path(ਫਾਇਲ).read_bytes()).hexdigest() for ਫਾਇਲ in sorted(소유파일)}
    ਮੰਜਿਲ_ਕੀਮਤ.write_text(json.dumps({'선언':선언들,'ਸੰਦਰਭ':참조들,'ਗਲਤੀ':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'ਸੰਦਰਭ',len(참조들),'ਗਲਤੀ',len(오류들))
    for ਗਲਤੀ in 오류들: print(*ਗਲਤੀ)

if __name__=='__main__': ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
