#!/usr/bin/env python3
"""libclang мәлімдеме·Анықтамалық 위치를 수집한다. сыртқы_мән 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

жоба_түбір = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class жол_мән_6ca8363c(씨.Structure): _fields_ = [('деректер',씨.c_void_p),('көрсету_мән',씨.c_uint)]
class курсор_мән(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('деректер',씨.c_void_p*3)]
class Орны(씨.Structure): _fields_ = [('деректер',씨.c_void_p*2),('жылжыту_мән_450fc799',씨.c_uint)]
def функция_мән(Аты, қайтару_өлшем, *Аргументтер):
    енгізу_мән = getattr(구현, Аты); енгізу_мән.restype = қайтару_өлшем; енгізу_мән.argtypes = list(Аргументтер); return енгізу_мән
алу_Мәтін = функция_мән('clang_getCString',씨.c_char_p,жол_мән_6ca8363c)
шығарылым_Мәтін = функция_мән('clang_disposeString',None,жол_мән_6ca8363c)
def Мәтін(мән):
    НӘТИЖЕ = (алу_Мәтін(мән) or b'').decode('utf-8'); шығарылым_Мәтін(мән); return НӘТИЖЕ
алу_аты = функция_мән('clang_getCursorSpelling',жол_мән_6ca8363c,курсор_мән)
алу_Анықтамалық = функция_мән('clang_getCursorReferenced',курсор_мән,курсор_мән)
алу_лауазым = функция_мән('clang_getCursorLocation',Орны,курсор_мән)
файл_лауазым = функция_мән('clang_getFileLocation',None,Орны,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
файл_енгізу_аты = функция_мән('clang_getFileName',жол_мән_6ca8363c,씨.c_void_p)
고유이름 = функция_мән('clang_getCursorUSR',жол_мән_6ca8363c,курсор_мән)
연결종류 = функция_мән('clang_getCursorLinkage',씨.c_uint,курсор_мән)
방문형 = 씨.CFUNCTYPE(씨.c_uint,курсор_мән,курсор_мән,씨.c_void_p)
방문 = функция_мән('clang_visitChildren',씨.c_uint,курсор_мән,방문형,씨.c_void_p)
жасау = функция_мән('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
Талдау_мән = функция_мән('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
түбір_мән = функция_мән('clang_getTranslationUnitCursor',курсор_мән,씨.c_void_p)
шығу_бағдарлама = функция_мән('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = функция_мән('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = функция_мән('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
қиындық_мән = функция_мән('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = функция_мән('clang_getDiagnosticSpelling',жол_мән_6ca8363c,씨.c_void_p)
진단해제 = функция_мән('clang_disposeDiagnostic',None,씨.c_void_p)

def лауазым_индекс(енгізу_мән):
    Файл = 씨.c_void_p(); Жол = 씨.c_uint(); 칸 = 씨.c_uint(); жылжыту_мән_450fc799 = 씨.c_uint()
    файл_лауазым(алу_лауазым(енгізу_мән),씨.byref(Файл),씨.byref(Жол),씨.byref(칸),씨.byref(жылжыту_мән_450fc799))
    return (Мәтін(файл_енгізу_аты(Файл)) if Файл else '', жылжыту_мән_450fc799.value, Жол.value)

def орындау_пәрмен():
    Іздеу_индекс = жасау(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 мәлімдеме 없이 TinyCC сыртқы_мән 단일 Аудару_көз 단위만 포함한다.
    # сыртқы_мән 선언을 자체 이름으로 세지 않으며, нақты_деректер 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Жол_2.resolve()) for Жол_2 in жоба_түбір.rglob('*') if Жол_2.suffix in ('.c','.h','.cpp','.inc')
              and not set(Жол_2.relative_to(жоба_түбір).parts)&{'build','dist','vendor','__pycache__'}
              and Жол_2.relative_to(жоба_түбір).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(жоба_түбір/'пайдаланушы'),
          '-I'+str(жоба_түбір.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(жоба_түбір/'build'),'-I'+str(жоба_түбір/'build/user'),
          '-I'+str(жоба_түбір/'build/remote'),'-I'+str(жоба_түбір/'vendor/bearssl/inc'),
          '-I'+str(жоба_түбір/'vendor/bearssl/src'),'-I'+str(жоба_түбір/'vendor/libassh/src'),
          '-I'+str(жоба_түбір/'vendor/lwip/src/include'),'-I'+str(жоба_түбір/'желі_Бума'),
          '-I'+str(жоба_түбір/'원격'),'-I'+str(жоба_түбір/'시언어번역기')]
    for Жол_2 in sorted(Path(Аты) for Аты in 소유파일 if Аты.endswith(('.c','.cpp'))):
        Аргументтер = 공통 + ['-std=c++11' if Жол_2.suffix=='.cpp' else '-std=c11']
        if 'желі_Бума' in Жол_2.parts: Аргументтер += ['-I'+str(жоба_түбір/'желі_Бума'),'-I'+str(жоба_түбір/'vendor/lwip/src/include')]
        if '시언어번역기' in Жол_2.parts:
            Аргументтер += ['-I'+str(жоба_түбір/'시언어번역기'),'-I'+str(жоба_түбір/'vendor/tinycc'),'-I'+str(жоба_түбір/'build/ccompiler'),
                    '-isystem',str(жоба_түбір.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in Жол_2.parts:
            Аргументтер += ['-I'+str(жоба_түбір/'파이썬연결'),'-I'+str(жоба_түбір/'build/micropython-1.24.1'),'-I'+str(жоба_түбір/'build/python'),'-isystem','/usr/include/newlib']
        if '원격' in Жол_2.parts:
            Аргументтер += ['-isystem', '/usr/include/newlib']
        if '배포' in Жол_2.parts: Аргументтер += ['-D__JKOROS__=1']
        if Жол_2.name=='жинау.c': Аргументтер += ['-I'+str(жоба_түбір/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Топ_мән = (씨.c_char_p*len(Аргументтер))(*[енгізу_мән.encode() for енгізу_мән in Аргументтер])
        Аударма_сабақ = Талдау_мән(Іздеу_индекс,str(Жол_2).encode(),Топ_мән,len(Аргументтер),None,0,1)
        for индекс in range(진단수(Аударма_сабақ)):
            진단 = 진단얻기(Аударма_сабақ,индекс)
            if қиындық_мән(진단)>=3: 오류들.append((str(Жол_2.relative_to(жоба_түбір)),Мәтін(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(енгізу_мән,басты_мән,деректер):
            Файл,жылжыту_мән_450fc799,Жол = лауазым_индекс(енгізу_мән)
            if Файл not in 소유파일: return 2 if енгізу_мән.종류==300 else 1
            낱말 = Мәтін(алу_аты(енгізу_мән))
            if not 낱말 or any(ord(таңба_мән)>127 for таңба_мән in 낱말): return 2
            if енгізу_мән.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = Мәтін(고유이름(енгізу_мән)) or Файл+':'+str(жылжыту_мән_450fc799)
                선언들[고유] = {'Файл':Файл,'жылжыту_мән_450fc799':жылжыту_мән_450fc799,'Жол':Жол,'종류':енгізу_мән.종류,'Аты':낱말,'Байланысу':연결종류(енгізу_мән)}
                참조들.append((Файл,жылжыту_мән_450fc799,낱말,고유))
            else:
                Анықтамалық = алу_Анықтамалық(енгізу_мән)
                Анықтамалық_файл,_,_ = лауазым_индекс(Анықтамалық)
                if Анықтамалық_файл in 소유파일:
                    고유 = Мәтін(고유이름(Анықтамалық)); 참조들.append((Файл,жылжыту_мән_450fc799,Мәтін(алу_аты(Анықтамалық)),고유))
            return 2
        방문(түбір_мән(Аударма_сабақ),살피기,None)
        шығу_бағдарлама(Аударма_сабақ)
    тағайындау_мән = жоба_түбір/'build/한국어화/시언어분석.json'
    тағайындау_мән.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Файл:hashlib.sha256(Path(Файл).read_bytes()).hexdigest() for Файл in sorted(소유파일)}
    тағайындау_мән.write_text(json.dumps({'мәлімдеме':선언들,'Анықтамалық':참조들,'Қате':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('мәлімдеме',len(선언들),'Анықтамалық',len(참조들),'Қате',len(오류들))
    for Қате in 오류들: print(*Қате)

if __name__=='__main__': орындау_пәрмен()
