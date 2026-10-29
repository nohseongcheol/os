#!/usr/bin/env python3
"""libclang абвяшчэнне·Даведачныя_матэрыялы 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class радок_значэнне(씨.Structure): _fields_ = [('дадзеныя',씨.c_void_p),('паказаць_значэнне',씨.c_uint)]
class курсор_значэнне(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('дадзеныя',씨.c_void_p*3)]
class Пазіцыя(씨.Structure): _fields_ = [('дадзеныя',씨.c_void_p*2),('Зрух_значэнне',씨.c_uint)]
def функцыя_значэнне(Назва, 반환, *인수):
    увядзенне_значэнне = getattr(구현, Назва); увядзенне_значэнне.restype = 반환; увядзенне_значэнне.argtypes = list(인수); return увядзенне_значэнне
атрымаць_Тэкст = функцыя_значэнне('clang_getCString',씨.c_char_p,радок_значэнне)
выпуск_Тэкст = функцыя_значэнне('clang_disposeString',None,радок_значэнне)
def Тэкст(значэнне):
    결과 = (атрымаць_Тэкст(значэнне) or b'').decode('utf-8'); выпуск_Тэкст(значэнне); return 결과
атрымаць_імя = функцыя_значэнне('clang_getCursorSpelling',радок_значэнне,курсор_значэнне)
атрымаць_Даведачныя_матэрыялы = функцыя_значэнне('clang_getCursorReferenced',курсор_значэнне,курсор_значэнне)
위치얻기 = функцыя_значэнне('clang_getCursorLocation',Пазіцыя,курсор_значэнне)
파일위치 = функцыя_значэнне('clang_getFileLocation',None,Пазіцыя,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
файл_увядзенне_імя = функцыя_значэнне('clang_getFileName',радок_значэнне,씨.c_void_p)
고유이름 = функцыя_значэнне('clang_getCursorUSR',радок_значэнне,курсор_значэнне)
연결종류 = функцыя_значэнне('clang_getCursorLinkage',씨.c_uint,курсор_значэнне)
방문형 = 씨.CFUNCTYPE(씨.c_uint,курсор_значэнне,курсор_значэнне,씨.c_void_p)
방문 = функцыя_значэнне('clang_visitChildren',씨.c_uint,курсор_значэнне,방문형,씨.c_void_p)
생성 = функцыя_значэнне('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = функцыя_значэнне('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = функцыя_значэнне('clang_getTranslationUnitCursor',курсор_значэнне,씨.c_void_p)
끝내기 = функцыя_значэнне('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = функцыя_значэнне('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = функцыя_значэнне('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
узровень_важнасці_значэнне = функцыя_значэнне('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = функцыя_значэнне('clang_getDiagnosticSpelling',радок_значэнне,씨.c_void_p)
진단해제 = функцыя_значэнне('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(увядзенне_значэнне):
    Файл = 씨.c_void_p(); лінія = 씨.c_uint(); слот_увядзенне = 씨.c_uint(); Зрух_значэнне = 씨.c_uint()
    파일위치(위치얻기(увядзенне_значэнне),씨.byref(Файл),씨.byref(лінія),씨.byref(слот_увядзенне),씨.byref(Зрух_значэнне))
    return (Тэкст(файл_увядзенне_імя(Файл)) if Файл else '', Зрух_значэнне.value, лінія.value)

def выканаць_каманда():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 абвяшчэнне 없이 TinyCC 외부 단일 Пераклад_крыніца 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, фактычны_дадзеныя 빌드에서는 계속 컴파일한다.
    소유파일 = {str(ШЛЯХ.resolve()) for ШЛЯХ in 기준.rglob('*') if ШЛЯХ.suffix in ('.c','.h','.cpp','.inc')
              and not set(ШЛЯХ.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and ШЛЯХ.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'карыстальнік'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'Сетка_Стэк'),
          '-I'+str(기준/'аддалены_значэнне'),'-I'+str(기준/'시언어번역기')]
    for ШЛЯХ in sorted(Path(Назва) for Назва in 소유파일 if Назва.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if ШЛЯХ.suffix=='.cpp' else '-std=c11']
        if 'Сетка_Стэк' in ШЛЯХ.parts: 인수 += ['-I'+str(기준/'Сетка_Стэк'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in ШЛЯХ.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in ШЛЯХ.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'аддалены_значэнне' in ШЛЯХ.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in ШЛЯХ.parts: 인수 += ['-D__JKOROS__=1']
        if ШЛЯХ.name=='пакет.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Група_значэнне = (씨.c_char_p*len(인수))(*[увядзенне_значэнне.encode() for увядзенне_значэнне in 인수])
        Пераклад_урок = 분석(색인,str(ШЛЯХ).encode(),Група_значэнне,len(인수),None,0,1)
        for індэкс in range(진단수(Пераклад_урок)):
            진단 = 진단얻기(Пераклад_урок,індэкс)
            if узровень_важнасці_значэнне(진단)>=3: 오류들.append((str(ШЛЯХ.relative_to(기준)),Тэкст(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(увядзенне_значэнне,부모,дадзеныя):
            Файл,Зрух_значэнне,лінія = 자리(увядзенне_значэнне)
            if Файл not in 소유파일: return 2 if увядзенне_значэнне.종류==300 else 1
            낱말 = Тэкст(атрымаць_імя(увядзенне_значэнне))
            if not 낱말 or any(ord(сімвал_значэнне_068c2631)>127 for сімвал_значэнне_068c2631 in 낱말): return 2
            if увядзенне_значэнне.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = Тэкст(고유이름(увядзенне_значэнне)) or Файл+':'+str(Зрух_значэнне)
                선언들[고유] = {'Файл':Файл,'Зрух_значэнне':Зрух_значэнне,'줄':лінія,'종류':увядзенне_значэнне.종류,'Назва':낱말,'Злучыцца':연결종류(увядзенне_значэнне)}
                참조들.append((Файл,Зрух_значэнне,낱말,고유))
            else:
                Даведачныя_матэрыялы = атрымаць_Даведачныя_матэрыялы(увядзенне_значэнне)
                Даведачныя_матэрыялы_файл,_,_ = 자리(Даведачныя_матэрыялы)
                if Даведачныя_матэрыялы_файл in 소유파일:
                    고유 = Тэкст(고유이름(Даведачныя_матэрыялы)); 참조들.append((Файл,Зрух_значэнне,Тэкст(атрымаць_імя(Даведачныя_матэрыялы)),고유))
            return 2
        방문(뿌리(Пераклад_урок),살피기,None)
        끝내기(Пераклад_урок)
    прызначэнне_значэнне_a0fbc067 = 기준/'build/한국어화/시언어분석.json'
    прызначэнне_значэнне_a0fbc067.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Файл:hashlib.sha256(Path(Файл).read_bytes()).hexdigest() for Файл in sorted(소유파일)}
    прызначэнне_значэнне_a0fbc067.write_text(json.dumps({'абвяшчэнне':선언들,'Даведачныя_матэрыялы':참조들,'ПАМЫЛКА':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('абвяшчэнне',len(선언들),'Даведачныя_матэрыялы',len(참조들),'ПАМЫЛКА',len(오류들))
    for ПАМЫЛКА in 오류들: print(*ПАМЫЛКА)

if __name__=='__main__': выканаць_каманда()
