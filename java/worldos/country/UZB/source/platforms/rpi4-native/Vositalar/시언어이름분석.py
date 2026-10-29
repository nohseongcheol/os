#!/usr/bin/env python3
"""libclang e_lon_qilish·Ma_lumotnomalar 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

Project_ildiz = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class satr_VALUE(씨.Structure): _fields_ = [('ma_lumotlar',씨.c_void_p),('ko_rsatmoq_VALUE',씨.c_uint)]
class kursor_VALUE(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('ma_lumotlar',씨.c_void_p*3)]
class Holati(씨.Structure): _fields_ = [('ma_lumotlar',씨.c_void_p*2),('OFFSET_VALUE',씨.c_uint)]
def FUNCTION_VALUE(Nomi, qaytarish_o_lchov, *인수):
    kiritish_VALUE = getattr(구현, Nomi); kiritish_VALUE.restype = qaytarish_o_lchov; kiritish_VALUE.argtypes = list(인수); return kiritish_VALUE
olish_SMS = FUNCTION_VALUE('clang_getCString',씨.c_char_p,satr_VALUE)
nashr_SMS = FUNCTION_VALUE('clang_disposeString',None,satr_VALUE)
def Matn(VALUE):
    o_lchov = (olish_SMS(VALUE) or b'').decode('utf-8'); nashr_SMS(VALUE); return o_lchov
olish_nom = FUNCTION_VALUE('clang_getCursorSpelling',satr_VALUE,kursor_VALUE)
olish_Ma_lumotnomalar = FUNCTION_VALUE('clang_getCursorReferenced',kursor_VALUE,kursor_VALUE)
olish_holat = FUNCTION_VALUE('clang_getCursorLocation',Holati,kursor_VALUE)
fayl_holat_2aa21a9a = FUNCTION_VALUE('clang_getFileLocation',None,Holati,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
fayl_kiritish_nom = FUNCTION_VALUE('clang_getFileName',satr_VALUE,씨.c_void_p)
UNIQUE_nom = FUNCTION_VALUE('clang_getCursorUSR',satr_VALUE,kursor_VALUE)
연결종류 = FUNCTION_VALUE('clang_getCursorLinkage',씨.c_uint,kursor_VALUE)
방문형 = 씨.CFUNCTYPE(씨.c_uint,kursor_VALUE,kursor_VALUE,씨.c_void_p)
방문 = FUNCTION_VALUE('clang_visitChildren',씨.c_uint,kursor_VALUE,방문형,씨.c_void_p)
generatsiiyalash = FUNCTION_VALUE('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = FUNCTION_VALUE('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
ildiz_VALUE = FUNCTION_VALUE('clang_getTranslationUnitCursor',kursor_VALUE,씨.c_void_p)
tugatish_ilova = FUNCTION_VALUE('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = FUNCTION_VALUE('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = FUNCTION_VALUE('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
jiddiylik_darajasi_VALUE = FUNCTION_VALUE('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = FUNCTION_VALUE('clang_getDiagnosticSpelling',satr_VALUE,씨.c_void_p)
진단해제 = FUNCTION_VALUE('clang_disposeDiagnostic',None,씨.c_void_p)

def holat_INDEX(kiritish_VALUE):
    Fayl = 씨.c_void_p(); satr = 씨.c_uint(); in_kiritish = 씨.c_uint(); OFFSET_VALUE = 씨.c_uint()
    fayl_holat_2aa21a9a(olish_holat(kiritish_VALUE),씨.byref(Fayl),씨.byref(satr),씨.byref(in_kiritish),씨.byref(OFFSET_VALUE))
    return (Matn(fayl_kiritish_nom(Fayl)) if Fayl else '', OFFSET_VALUE.value, satr.value)

def bajarmoq_buyruq():
    LOOKUP_INDEX = generatsiiyalash(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 e_lon_qilish 없이 TinyCC 외부 단일 Tarjima_manba 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, real_ma_lumotlar 빌드에서는 계속 컴파일한다.
    소유파일 = {str(yo_l.resolve()) for yo_l in Project_ildiz.rglob('*') if yo_l.suffix in ('.c','.h','.cpp','.inc')
              and not set(yo_l.relative_to(Project_ildiz).parts)&{'build','dist','vendor','__pycache__'}
              and yo_l.relative_to(Project_ildiz).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(Project_ildiz/'foydalanuvchi'),
          '-I'+str(Project_ildiz.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(Project_ildiz/'build'),'-I'+str(Project_ildiz/'build/user'),
          '-I'+str(Project_ildiz/'build/remote'),'-I'+str(Project_ildiz/'vendor/bearssl/inc'),
          '-I'+str(Project_ildiz/'vendor/bearssl/src'),'-I'+str(Project_ildiz/'vendor/libassh/src'),
          '-I'+str(Project_ildiz/'vendor/lwip/src/include'),'-I'+str(Project_ildiz/'Tarmoq_Stack'),
          '-I'+str(Project_ildiz/'masofaviy_VALUE'),'-I'+str(Project_ildiz/'시언어번역기')]
    for yo_l in sorted(Path(Nomi) for Nomi in 소유파일 if Nomi.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if yo_l.suffix=='.cpp' else '-std=c11']
        if 'Tarmoq_Stack' in yo_l.parts: 인수 += ['-I'+str(Project_ildiz/'Tarmoq_Stack'),'-I'+str(Project_ildiz/'vendor/lwip/src/include')]
        if '시언어번역기' in yo_l.parts:
            인수 += ['-I'+str(Project_ildiz/'시언어번역기'),'-I'+str(Project_ildiz/'vendor/tinycc'),'-I'+str(Project_ildiz/'build/ccompiler'),
                    '-isystem',str(Project_ildiz.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in yo_l.parts:
            인수 += ['-I'+str(Project_ildiz/'파이썬연결'),'-I'+str(Project_ildiz/'build/micropython-1.24.1'),'-I'+str(Project_ildiz/'build/python'),'-isystem','/usr/include/newlib']
        if 'masofaviy_VALUE' in yo_l.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in yo_l.parts: 인수 += ['-D__JKOROS__=1']
        if yo_l.name=='to_plam.c': 인수 += ['-I'+str(Project_ildiz/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Guruh_VALUE = (씨.c_char_p*len(인수))(*[kiritish_VALUE.encode() for kiritish_VALUE in 인수])
        Tarjima_dars = 분석(LOOKUP_INDEX,str(yo_l).encode(),Guruh_VALUE,len(인수),None,0,1)
        for INDEX in range(진단수(Tarjima_dars)):
            진단 = 진단얻기(Tarjima_dars,INDEX)
            if jiddiylik_darajasi_VALUE(진단)>=3: 오류들.append((str(yo_l.relative_to(Project_ildiz)),Matn(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(kiritish_VALUE,부모,ma_lumotlar):
            Fayl,OFFSET_VALUE,satr = holat_INDEX(kiritish_VALUE)
            if Fayl not in 소유파일: return 2 if kiritish_VALUE.종류==300 else 1
            낱말 = Matn(olish_nom(kiritish_VALUE))
            if not 낱말 or any(ord(belgi_VALUE)>127 for belgi_VALUE in 낱말): return 2
            if kiritish_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Matn(UNIQUE_nom(kiritish_VALUE)) or Fayl+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'Fayl':Fayl,'OFFSET_VALUE':OFFSET_VALUE,'줄':satr,'종류':kiritish_VALUE.종류,'Nomi':낱말,'Ulanish':연결종류(kiritish_VALUE)}
                참조들.append((Fayl,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                Ma_lumotnomalar = olish_Ma_lumotnomalar(kiritish_VALUE)
                Ma_lumotnomalar_fayl,_,_ = holat_INDEX(Ma_lumotnomalar)
                if Ma_lumotnomalar_fayl in 소유파일:
                    UNIQUE_VALUE = Matn(UNIQUE_nom(Ma_lumotnomalar)); 참조들.append((Fayl,OFFSET_VALUE,Matn(olish_nom(Ma_lumotnomalar)),UNIQUE_VALUE))
            return 2
        방문(ildiz_VALUE(Tarjima_dars),살피기,None)
        tugatish_ilova(Tarjima_dars)
    ko_chirish_joyi_VALUE = Project_ildiz/'build/한국어화/시언어분석.json'
    ko_chirish_joyi_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Fayl:hashlib.sha256(Path(Fayl).read_bytes()).hexdigest() for Fayl in sorted(소유파일)}
    ko_chirish_joyi_VALUE.write_text(json.dumps({'e_lon_qilish':선언들,'Ma_lumotnomalar':참조들,'Xato':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('e_lon_qilish',len(선언들),'Ma_lumotnomalar',len(참조들),'Xato',len(오류들))
    for Xato in 오류들: print(*Xato)

if __name__=='__main__': bajarmoq_buyruq()
