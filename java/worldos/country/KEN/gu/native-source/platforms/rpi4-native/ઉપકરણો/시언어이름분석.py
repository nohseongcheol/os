#!/usr/bin/env python3
"""libclang 선언·સંદર્ભ 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

પ્રોજેક્ટ_રૂટ = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class સ્ટ્રિંગ_મૂલ્ય(씨.Structure): _fields_ = [('ડેટા',씨.c_void_p),('શૉ_મૂલ્ય',씨.c_uint)]
class કર્સર_મૂલ્ય(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('ડેટા',씨.c_void_p*3)]
class સ્થાન(씨.Structure): _fields_ = [('ડેટા',씨.c_void_p*2),('ઑફસેટ_મૂલ્ય',씨.c_uint)]
def ફંક્શંસ_મૂલ્ય(નામ, 반환, *દલીલો):
    પ્રવેશ_મૂલ્ય = getattr(구현, નામ); પ્રવેશ_મૂલ્ય.restype = 반환; પ્રવેશ_મૂલ્ય.argtypes = list(દલીલો); return પ્રવેશ_મૂલ્ય
글얻기 = ફંક્શંસ_મૂલ્ય('clang_getCString',씨.c_char_p,સ્ટ્રિંગ_મૂલ્ય)
રિલીઝ_પાઠ = ફંક્શંસ_મૂલ્ય('clang_disposeString',None,સ્ટ્રિંગ_મૂલ્ય)
def લખાણ(મૂલ્ય):
    પરિમાણ = (글얻기(મૂલ્ય) or b'').decode('utf-8'); રિલીઝ_પાઠ(મૂલ્ય); return પરિમાણ
이름얻기 = ફંક્શંસ_મૂલ્ય('clang_getCursorSpelling',સ્ટ્રિંગ_મૂલ્ય,કર્સર_મૂલ્ય)
참조얻기 = ફંક્શંસ_મૂલ્ય('clang_getCursorReferenced',કર્સર_મૂલ્ય,કર્સર_મૂલ્ય)
위치얻기 = ફંક્શંસ_મૂલ્ય('clang_getCursorLocation',સ્થાન,કર્સર_મૂલ્ય)
ફાઇલ_સ્થિતિ_2aa21a9a = ફંક્શંસ_મૂલ્ય('clang_getFileLocation',None,સ્થાન,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ફાઇલ_પ્રવેશ_નામ = ફંક્શંસ_મૂલ્ય('clang_getFileName',સ્ટ્રિંગ_મૂલ્ય,씨.c_void_p)
고유이름 = ફંક્શંસ_મૂલ્ય('clang_getCursorUSR',સ્ટ્રિંગ_મૂલ્ય,કર્સર_મૂલ્ય)
연결종류 = ફંક્શંસ_મૂલ્ય('clang_getCursorLinkage',씨.c_uint,કર્સર_મૂલ્ય)
방문형 = 씨.CFUNCTYPE(씨.c_uint,કર્સર_મૂલ્ય,કર્સર_મૂલ્ય,씨.c_void_p)
방문 = ફંક્શંસ_મૂલ્ય('clang_visitChildren',씨.c_uint,કર્સર_મૂલ્ય,방문형,씨.c_void_p)
જનરેટ_કરો = ફંક્શંસ_મૂલ્ય('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = ફંક્શંસ_મૂલ્ય('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
રૂટ_મૂલ્ય = ફંક્શંસ_મૂલ્ય('clang_getTranslationUnitCursor',કર્સર_મૂલ્ય,씨.c_void_p)
છોડી_દો_એપ્લિકેશન = ફંક્શંસ_મૂલ્ય('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ફંક્શંસ_મૂલ્ય('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ફંક્શંસ_મૂલ્ય('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
તીવ્રતા_મૂલ્ય = ફંક્શંસ_મૂલ્ય('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ફંક્શંસ_મૂલ્ય('clang_getDiagnosticSpelling',સ્ટ્રિંગ_મૂલ્ય,씨.c_void_p)
진단해제 = ફંક્શંસ_મૂલ્ય('clang_disposeDiagnostic',None,씨.c_void_p)

def સ્થિતિ_અનુક્રમણિકા(પ્રવેશ_મૂલ્ય):
    ફાઈલ = 씨.c_void_p(); લાઇન = 씨.c_uint(); સ્લૉટ_પ્રવેશ = 씨.c_uint(); ઑફસેટ_મૂલ્ય = 씨.c_uint()
    ફાઇલ_સ્થિતિ_2aa21a9a(위치얻기(પ્રવેશ_મૂલ્ય),씨.byref(ફાઈલ),씨.byref(લાઇન),씨.byref(સ્લૉટ_પ્રવેશ),씨.byref(ઑફસેટ_મૂલ્ય))
    return (લખાણ(ફાઇલ_પ્રવેશ_નામ(ફાઈલ)) if ફાઈલ else '', ઑફસેટ_મૂલ્ય.value, લાઇન.value)

def અમલ_કરો_આદેશ():
    લુકઅપ_અનુક્રમણિકા = જનરેટ_કરો(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 અનુવાદ_કરો_સ્રોત 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, વાસ્તવિક_ડેટા 빌드에서는 계속 컴파일한다.
    소유파일 = {str(પથ.resolve()) for પથ in પ્રોજેક્ટ_રૂટ.rglob('*') if પથ.suffix in ('.c','.h','.cpp','.inc')
              and not set(પથ.relative_to(પ્રોજેક્ટ_રૂટ).parts)&{'build','dist','vendor','__pycache__'}
              and પથ.relative_to(પ્રોજેક્ટ_રૂટ).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(પ્રોજેક્ટ_રૂટ/'ઉપયોગકર્તા'),
          '-I'+str(પ્રોજેક્ટ_રૂટ.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(પ્રોજેક્ટ_રૂટ/'build'),'-I'+str(પ્રોજેક્ટ_રૂટ/'build/user'),
          '-I'+str(પ્રોજેક્ટ_રૂટ/'build/remote'),'-I'+str(પ્રોજેક્ટ_રૂટ/'vendor/bearssl/inc'),
          '-I'+str(પ્રોજેક્ટ_રૂટ/'vendor/bearssl/src'),'-I'+str(પ્રોજેક્ટ_રૂટ/'vendor/libassh/src'),
          '-I'+str(પ્રોજેક્ટ_રૂટ/'vendor/lwip/src/include'),'-I'+str(પ્રોજેક્ટ_રૂટ/'નેટવર્ક_સ્ટેક'),
          '-I'+str(પ્રોજેક્ટ_રૂટ/'રિમોટ_મૂલ્ય'),'-I'+str(પ્રોજેક્ટ_રૂટ/'시언어번역기')]
    for પથ in sorted(Path(નામ) for નામ in 소유파일 if નામ.endswith(('.c','.cpp'))):
        દલીલો = 공통 + ['-std=c++11' if પથ.suffix=='.cpp' else '-std=c11']
        if 'નેટવર્ક_સ્ટેક' in પથ.parts: દલીલો += ['-I'+str(પ્રોજેક્ટ_રૂટ/'નેટવર્ક_સ્ટેક'),'-I'+str(પ્રોજેક્ટ_રૂટ/'vendor/lwip/src/include')]
        if '시언어번역기' in પથ.parts:
            દલીલો += ['-I'+str(પ્રોજેક્ટ_રૂટ/'시언어번역기'),'-I'+str(પ્રોજેક્ટ_રૂટ/'vendor/tinycc'),'-I'+str(પ્રોજેક્ટ_રૂટ/'build/ccompiler'),
                    '-isystem',str(પ્રોજેક્ટ_રૂટ.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in પથ.parts:
            દલીલો += ['-I'+str(પ્રોજેક્ટ_રૂટ/'파이썬연결'),'-I'+str(પ્રોજેક્ટ_રૂટ/'build/micropython-1.24.1'),'-I'+str(પ્રોજેક્ટ_રૂટ/'build/python'),'-isystem','/usr/include/newlib']
        if 'રિમોટ_મૂલ્ય' in પથ.parts:
            દલીલો += ['-isystem', '/usr/include/newlib']
        if '배포' in પથ.parts: દલીલો += ['-D__JKOROS__=1']
        if પથ.name=='બન્ડલ.c': દલીલો += ['-I'+str(પ્રોજેક્ટ_રૂટ/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        સમૂહ_મૂલ્ય = (씨.c_char_p*len(દલીલો))(*[પ્રવેશ_મૂલ્ય.encode() for પ્રવેશ_મૂલ્ય in દલીલો])
        અનુવાદ_એકમ = 분석(લુકઅપ_અનુક્રમણિકા,str(પથ).encode(),સમૂહ_મૂલ્ય,len(દલીલો),None,0,1)
        for અનુક્રમણિકા in range(진단수(અનુવાદ_એકમ)):
            진단 = 진단얻기(અનુવાદ_એકમ,અનુક્રમણિકા)
            if તીવ્રતા_મૂલ્ય(진단)>=3: 오류들.append((str(પથ.relative_to(પ્રોજેક્ટ_રૂટ)),લખાણ(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(પ્રવેશ_મૂલ્ય,부모,ડેટા):
            ફાઈલ,ઑફસેટ_મૂલ્ય,લાઇન = સ્થિતિ_અનુક્રમણિકા(પ્રવેશ_મૂલ્ય)
            if ફાઈલ not in 소유파일: return 2 if પ્રવેશ_મૂલ્ય.종류==300 else 1
            낱말 = લખાણ(이름얻기(પ્રવેશ_મૂલ્ય))
            if not 낱말 or any(ord(વર્ણ_મૂલ્ય)>127 for વર્ણ_મૂલ્ય in 낱말): return 2
            if પ્રવેશ_મૂલ્ય.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = લખાણ(고유이름(પ્રવેશ_મૂલ્ય)) or ફાઈલ+':'+str(ઑફસેટ_મૂલ્ય)
                선언들[고유] = {'ફાઈલ':ફાઈલ,'ઑફસેટ_મૂલ્ય':ઑફસેટ_મૂલ્ય,'줄':લાઇન,'종류':પ્રવેશ_મૂલ્ય.종류,'નામ':낱말,'સંપર્ક_કરો':연결종류(પ્રવેશ_મૂલ્ય)}
                참조들.append((ફાઈલ,ઑફસેટ_મૂલ્ય,낱말,고유))
            else:
                સંદર્ભ = 참조얻기(પ્રવેશ_મૂલ્ય)
                સંદર્ભ_ફાઇલ,_,_ = સ્થિતિ_અનુક્રમણિકા(સંદર્ભ)
                if સંદર્ભ_ફાઇલ in 소유파일:
                    고유 = લખાણ(고유이름(સંદર્ભ)); 참조들.append((ફાઈલ,ઑફસેટ_મૂલ્ય,લખાણ(이름얻기(સંદર્ભ)),고유))
            return 2
        방문(રૂટ_મૂલ્ય(અનુવાદ_એકમ),살피기,None)
        છોડી_દો_એપ્લિકેશન(અનુવાદ_એકમ)
    ગંતવ્ય_મૂલ્ય = પ્રોજેક્ટ_રૂટ/'build/한국어화/시언어분석.json'
    ગંતવ્ય_મૂલ્ય.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {ફાઈલ:hashlib.sha256(Path(ફાઈલ).read_bytes()).hexdigest() for ફાઈલ in sorted(소유파일)}
    ગંતવ્ય_મૂલ્ય.write_text(json.dumps({'선언':선언들,'સંદર્ભ':참조들,'ભૂલ':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'સંદર્ભ',len(참조들),'ભૂલ',len(오류들))
    for ભૂલ in 오류들: print(*ભૂલ)

if __name__=='__main__': અમલ_કરો_આદેશ()
