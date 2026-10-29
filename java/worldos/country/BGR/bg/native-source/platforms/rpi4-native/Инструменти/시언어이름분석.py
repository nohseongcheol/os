#!/usr/bin/env python3
"""libclang декларация·препратка 위치를 수집한다. външен_стойност 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

проект_корен = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class низ_стойност(씨.Structure): _fields_ = [('данни',씨.c_void_p),('показвам_стойност',씨.c_uint)]
class курсор_стойност(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('данни',씨.c_void_p*3)]
class Позиция(씨.Structure): _fields_ = [('данни',씨.c_void_p*2),('Изместване_стойност',씨.c_uint)]
def функция_стойност(Име, връщам_мярка, *Параметри):
    запис_стойност = getattr(구현, Име); запис_стойност.restype = връщам_мярка; запис_стойност.argtypes = list(Параметри); return запис_стойност
получавам_Текст = функция_стойност('clang_getCString',씨.c_char_p,низ_стойност)
издание_Текст = функция_стойност('clang_disposeString',None,низ_стойност)
def Текст(стойност):
    РЕЗУЛТАТ = (получавам_Текст(стойност) or b'').decode('utf-8'); издание_Текст(стойност); return РЕЗУЛТАТ
получавам_препратка_към_клетка = функция_стойност('clang_getCursorSpelling',низ_стойност,курсор_стойност)
получавам_препратка_10d0a960 = функция_стойност('clang_getCursorReferenced',курсор_стойност,курсор_стойност)
получавам_позиция_9492ef84 = функция_стойност('clang_getCursorLocation',Позиция,курсор_стойност)
Файл_позиция = функция_стойност('clang_getFileLocation',None,Позиция,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
Файл_запис_препратка_към_клетка = функция_стойност('clang_getFileName',низ_стойност,씨.c_void_p)
고유이름 = функция_стойност('clang_getCursorUSR',низ_стойност,курсор_стойност)
연결종류 = функция_стойност('clang_getCursorLinkage',씨.c_uint,курсор_стойност)
방문형 = 씨.CFUNCTYPE(씨.c_uint,курсор_стойност,курсор_стойност,씨.c_void_p)
방문 = функция_стойност('clang_visitChildren',씨.c_uint,курсор_стойност,방문형,씨.c_void_p)
генерирам = функция_стойност('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
Анализ_стойност = функция_стойност('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
корен_стойност = функция_стойност('clang_getTranslationUnitCursor',курсор_стойност,씨.c_void_p)
изход_програма = функция_стойност('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = функция_стойност('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = функция_стойност('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
степен_стойност = функция_стойност('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = функция_стойност('clang_getDiagnosticSpelling',низ_стойност,씨.c_void_p)
진단해제 = функция_стойност('clang_disposeDiagnostic',None,씨.c_void_p)

def позиционен_указател(запис_стойност):
    Файл = 씨.c_void_p(); ред = 씨.c_uint(); 칸 = 씨.c_uint(); Изместване_стойност = 씨.c_uint()
    Файл_позиция(получавам_позиция_9492ef84(запис_стойност),씨.byref(Файл),씨.byref(ред),씨.byref(칸),씨.byref(Изместване_стойност))
    return (Текст(Файл_запис_препратка_към_клетка(Файл)) if Файл else '', Изместване_стойност.value, ред.value)

def изпълнявам_команда():
    Търсене_индекс = генерирам(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # компилатор_инструмент.c는 자체 декларация 없이 TinyCC външен_стойност 단일 Превод_източник 단위만 포함한다.
    # външен_стойност 선언을 자체 이름으로 세지 않으며, действителен_данни 빌드에서는 계속 컴파일한다.
    소유파일 = {str(ПЪТ.resolve()) for ПЪТ in проект_корен.rglob('*') if ПЪТ.suffix in ('.c','.h','.cpp','.inc')
              and not set(ПЪТ.relative_to(проект_корен).parts)&{'build','dist','vendor','__pycache__'}
              and ПЪТ.relative_to(проект_корен).as_posix() != '시언어번역기/компилатор_инструмент.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(проект_корен/'потребител'),
          '-I'+str(проект_корен.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(проект_корен/'build'),'-I'+str(проект_корен/'build/user'),
          '-I'+str(проект_корен/'build/remote'),'-I'+str(проект_корен/'vendor/bearssl/inc'),
          '-I'+str(проект_корен/'vendor/bearssl/src'),'-I'+str(проект_корен/'vendor/libassh/src'),
          '-I'+str(проект_корен/'vendor/lwip/src/include'),'-I'+str(проект_корен/'мрежа_стек'),
          '-I'+str(проект_корен/'отдалечен_стойност'),'-I'+str(проект_корен/'시언어번역기')]
    for ПЪТ in sorted(Path(Име) for Име in 소유파일 if Име.endswith(('.c','.cpp'))):
        Параметри = 공통 + ['-std=c++11' if ПЪТ.suffix=='.cpp' else '-std=c11']
        if 'мрежа_стек' in ПЪТ.parts: Параметри += ['-I'+str(проект_корен/'мрежа_стек'),'-I'+str(проект_корен/'vendor/lwip/src/include')]
        if '시언어번역기' in ПЪТ.parts:
            Параметри += ['-I'+str(проект_корен/'시언어번역기'),'-I'+str(проект_корен/'vendor/tinycc'),'-I'+str(проект_корен/'build/ccompiler'),
                    '-isystem',str(проект_корен.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in ПЪТ.parts:
            Параметри += ['-I'+str(проект_корен/'파이썬연결'),'-I'+str(проект_корен/'build/micropython-1.24.1'),'-I'+str(проект_корен/'build/python'),'-isystem','/usr/include/newlib']
        if 'отдалечен_стойност' in ПЪТ.parts:
            Параметри += ['-isystem', '/usr/include/newlib']
        if '배포' in ПЪТ.parts: Параметри += ['-D__JKOROS__=1']
        if ПЪТ.name=='пакет.c': Параметри += ['-I'+str(проект_корен/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Група_стойност = (씨.c_char_p*len(Параметри))(*[запис_стойност.encode() for запис_стойност in Параметри])
        Превод_урок = Анализ_стойност(Търсене_индекс,str(ПЪТ).encode(),Група_стойност,len(Параметри),None,0,1)
        for индекс in range(진단수(Превод_урок)):
            진단 = 진단얻기(Превод_урок,индекс)
            if степен_стойност(진단)>=3: 오류들.append((str(ПЪТ.relative_to(проект_корен)),Текст(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(запис_стойност,родител_стойност,данни):
            Файл,Изместване_стойност,ред = позиционен_указател(запис_стойност)
            if Файл not in 소유파일: return 2 if запис_стойност.종류==300 else 1
            낱말 = Текст(получавам_препратка_към_клетка(запис_стойност))
            if not 낱말 or any(ord(знак_стойност)>127 for знак_стойност in 낱말): return 2
            if запис_стойност.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = Текст(고유이름(запис_стойност)) or Файл+':'+str(Изместване_стойност)
                선언들[고유] = {'Файл':Файл,'Изместване_стойност':Изместване_стойност,'줄':ред,'종류':запис_стойност.종류,'Име':낱말,'Свързване':연결종류(запис_стойност)}
                참조들.append((Файл,Изместване_стойност,낱말,고유))
            else:
                препратка = получавам_препратка_10d0a960(запис_стойност)
                препратка_Файл,_,_ = позиционен_указател(препратка)
                if препратка_Файл in 소유파일:
                    고유 = Текст(고유이름(препратка)); 참조들.append((Файл,Изместване_стойност,Текст(получавам_препратка_към_клетка(препратка)),고유))
            return 2
        방문(корен_стойност(Превод_урок),살피기,None)
        изход_програма(Превод_урок)
    местоназначение_стойност = проект_корен/'build/한국어화/시언어분석.json'
    местоназначение_стойност.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Файл:hashlib.sha256(Path(Файл).read_bytes()).hexdigest() for Файл in sorted(소유파일)}
    местоназначение_стойност.write_text(json.dumps({'декларация':선언들,'препратка':참조들,'ГРЕШКА':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('декларация',len(선언들),'препратка',len(참조들),'ГРЕШКА',len(오류들))
    for ГРЕШКА in 오류들: print(*ГРЕШКА)

if __name__=='__main__': изпълнявам_команда()
