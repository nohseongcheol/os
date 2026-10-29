#!/usr/bin/env python3
"""libclang 선언·Տեղեկատուներ 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

արձակել_արմատ = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class տող_արժեք_6ca8363c(씨.Structure): _fields_ = [('տվյալ',씨.c_void_p),('ցուցադրել_արժեք',씨.c_uint)]
class նշորդ_արժեք(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('տվյալ',씨.c_void_p*3)]
class Դիրք(씨.Structure): _fields_ = [('տվյալ',씨.c_void_p*2),('Տեղաշարժում_արժեք',씨.c_uint)]
def ՖՈՒՆԿՑԻԱ_արժեք(Անուն, վերադարձնել_չափ, *인수):
    մուտքագրում_արժեք = getattr(구현, Անուն); մուտքագրում_արժեք.restype = վերադարձնել_չափ; մուտքագրում_արժեք.argtypes = list(인수); return մուտքագրում_արժեք
글얻기 = ՖՈՒՆԿՑԻԱ_արժեք('clang_getCString',씨.c_char_p,տող_արժեք_6ca8363c)
արձակել_Գրվածք = ՖՈՒՆԿՑԻԱ_արժեք('clang_disposeString',None,տող_արժեք_6ca8363c)
def Տեքստ(արժեք):
    չափ = (글얻기(արժեք) or b'').decode('utf-8'); արձակել_Գրվածք(արժեք); return չափ
이름얻기 = ՖՈՒՆԿՑԻԱ_արժեք('clang_getCursorSpelling',տող_արժեք_6ca8363c,նշորդ_արժեք)
참조얻기 = ՖՈՒՆԿՑԻԱ_արժեք('clang_getCursorReferenced',նշորդ_արժեք,նշորդ_արժեք)
위치얻기 = ՖՈՒՆԿՑԻԱ_արժեք('clang_getCursorLocation',Դիրք,նշորդ_արժեք)
նիշք_դիրք = ՖՈՒՆԿՑԻԱ_արժեք('clang_getFileLocation',None,Դիրք,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
նիշք_մուտքագրում_անուն = ՖՈՒՆԿՑԻԱ_արժեք('clang_getFileName',տող_արժեք_6ca8363c,씨.c_void_p)
고유이름 = ՖՈՒՆԿՑԻԱ_արժեք('clang_getCursorUSR',տող_արժեք_6ca8363c,նշորդ_արժեք)
연결종류 = ՖՈՒՆԿՑԻԱ_արժեք('clang_getCursorLinkage',씨.c_uint,նշորդ_արժեք)
방문형 = 씨.CFUNCTYPE(씨.c_uint,նշորդ_արժեք,նշորդ_արժեք,씨.c_void_p)
방문 = ՖՈՒՆԿՑԻԱ_արժեք('clang_visitChildren',씨.c_uint,նշորդ_արժեք,방문형,씨.c_void_p)
արտադրել = ՖՈՒՆԿՑԻԱ_արժեք('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = ՖՈՒՆԿՑԻԱ_արժեք('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
արմատ_արժեք = ՖՈՒՆԿՑԻԱ_արժեք('clang_getTranslationUnitCursor',նշորդ_արժեք,씨.c_void_p)
լքում_ծրագիր = ՖՈՒՆԿՑԻԱ_արժեք('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ՖՈՒՆԿՑԻԱ_արժեք('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ՖՈՒՆԿՑԻԱ_արժեք('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
Խստություն_արժեք = ՖՈՒՆԿՑԻԱ_արժեք('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ՖՈՒՆԿՑԻԱ_արժեք('clang_getDiagnosticSpelling',տող_արժեք_6ca8363c,씨.c_void_p)
진단해제 = ՖՈՒՆԿՑԻԱ_արժեք('clang_disposeDiagnostic',None,씨.c_void_p)

def դիրք_դասիչ(մուտքագրում_արժեք):
    Ֆայլ = 씨.c_void_p(); կապ = 씨.c_uint(); փորակ_մուտքագրում = 씨.c_uint(); Տեղաշարժում_արժեք = 씨.c_uint()
    նիշք_դիրք(위치얻기(մուտքագրում_արժեք),씨.byref(Ֆայլ),씨.byref(կապ),씨.byref(փորակ_մուտքագրում),씨.byref(Տեղաշարժում_արժեք))
    return (Տեքստ(նիշք_մուտքագրում_անուն(Ֆայլ)) if Ֆայլ else '', Տեղաշարժում_արժեք.value, կապ.value)

def կատարել_հրաման():
    Փնտրում_դասիչ = արտադրել(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 Թարգմանել_աղբյուր 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, իրական_տվյալ 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Ճանապարհ.resolve()) for Ճանապարհ in արձակել_արմատ.rglob('*') if Ճանապարհ.suffix in ('.c','.h','.cpp','.inc')
              and not set(Ճանապարհ.relative_to(արձակել_արմատ).parts)&{'build','dist','vendor','__pycache__'}
              and Ճանապարհ.relative_to(արձակել_արմատ).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(արձակել_արմատ/'օգտվող'),
          '-I'+str(արձակել_արմատ.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(արձակել_արմատ/'build'),'-I'+str(արձակել_արմատ/'build/user'),
          '-I'+str(արձակել_արմատ/'build/remote'),'-I'+str(արձակել_արմատ/'vendor/bearssl/inc'),
          '-I'+str(արձակել_արմատ/'vendor/bearssl/src'),'-I'+str(արձակել_արմատ/'vendor/libassh/src'),
          '-I'+str(արձակել_արմատ/'vendor/lwip/src/include'),'-I'+str(արձակել_արմատ/'Ցանց_Շեղջ'),
          '-I'+str(արձակել_արմատ/'հեռակա_արժեք'),'-I'+str(արձակել_արմատ/'시언어번역기')]
    for Ճանապարհ in sorted(Path(Անուն) for Անուն in 소유파일 if Անուն.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if Ճանապարհ.suffix=='.cpp' else '-std=c11']
        if 'Ցանց_Շեղջ' in Ճանապարհ.parts: 인수 += ['-I'+str(արձակել_արմատ/'Ցանց_Շեղջ'),'-I'+str(արձակել_արմատ/'vendor/lwip/src/include')]
        if '시언어번역기' in Ճանապարհ.parts:
            인수 += ['-I'+str(արձակել_արմատ/'시언어번역기'),'-I'+str(արձակել_արմատ/'vendor/tinycc'),'-I'+str(արձակել_արմատ/'build/ccompiler'),
                    '-isystem',str(արձակել_արմատ.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in Ճանապարհ.parts:
            인수 += ['-I'+str(արձակել_արմատ/'파이썬연결'),'-I'+str(արձակել_արմատ/'build/micropython-1.24.1'),'-I'+str(արձակել_արմատ/'build/python'),'-isystem','/usr/include/newlib']
        if 'հեռակա_արժեք' in Ճանապարհ.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in Ճանապարհ.parts: 인수 += ['-D__JKOROS__=1']
        if Ճանապարհ.name=='փաթեթ.c': 인수 += ['-I'+str(արձակել_արմատ/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        խումբ_արժեք = (씨.c_char_p*len(인수))(*[մուտքագրում_արժեք.encode() for մուտքագրում_արժեք in 인수])
        Թարգմանություն_դասընթաց = 분석(Փնտրում_դասիչ,str(Ճանապարհ).encode(),խումբ_արժեք,len(인수),None,0,1)
        for դասիչ in range(진단수(Թարգմանություն_դասընթաց)):
            진단 = 진단얻기(Թարգմանություն_դասընթաց,դասիչ)
            if Խստություն_արժեք(진단)>=3: 오류들.append((str(Ճանապարհ.relative_to(արձակել_արմատ)),Տեքստ(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(մուտքագրում_արժեք,부모,տվյալ):
            Ֆայլ,Տեղաշարժում_արժեք,կապ = դիրք_դասիչ(մուտքագրում_արժեք)
            if Ֆայլ not in 소유파일: return 2 if մուտքագրում_արժեք.종류==300 else 1
            낱말 = Տեքստ(이름얻기(մուտքագրում_արժեք))
            if not 낱말 or any(ord(գրանշան_արժեք)>127 for գրանշան_արժեք in 낱말): return 2
            if մուտքագրում_արժեք.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = Տեքստ(고유이름(մուտքագրում_արժեք)) or Ֆայլ+':'+str(Տեղաշարժում_արժեք)
                선언들[고유] = {'Ֆայլ':Ֆայլ,'Տեղաշարժում_արժեք':Տեղաշարժում_արժեք,'줄':կապ,'종류':մուտքագրում_արժեք.종류,'Անուն':낱말,'Միացնել':연결종류(մուտքագրում_արժեք)}
                참조들.append((Ֆայլ,Տեղաշարժում_արժեք,낱말,고유))
            else:
                Տեղեկատուներ = 참조얻기(մուտքագրում_արժեք)
                Տեղեկատուներ_նիշք,_,_ = դիրք_դասիչ(Տեղեկատուներ)
                if Տեղեկատուներ_նիշք in 소유파일:
                    고유 = Տեքստ(고유이름(Տեղեկատուներ)); 참조들.append((Ֆայլ,Տեղաշարժում_արժեք,Տեքստ(이름얻기(Տեղեկատուներ)),고유))
            return 2
        방문(արմատ_արժեք(Թարգմանություն_դասընթաց),살피기,None)
        լքում_ծրագիր(Թարգմանություն_դասընթաց)
    նպատակակետ_արժեք = արձակել_արմատ/'build/한국어화/시언어분석.json'
    նպատակակետ_արժեք.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Ֆայլ:hashlib.sha256(Path(Ֆայլ).read_bytes()).hexdigest() for Ֆայլ in sorted(소유파일)}
    նպատակակետ_արժեք.write_text(json.dumps({'선언':선언들,'Տեղեկատուներ':참조들,'Սխալ':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Տեղեկատուներ',len(참조들),'Սխալ',len(오류들))
    for Սխալ in 오류들: print(*Սխալ)

if __name__=='__main__': կատարել_հրաման()
