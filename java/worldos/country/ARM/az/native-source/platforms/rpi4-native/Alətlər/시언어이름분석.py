#!/usr/bin/env python3
"""libclang bəyannamə·İstinad 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

Project_kök = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class sətir_VALUE(씨.Structure): _fields_ = [('verilənlər',씨.c_void_p),('göstərmək_VALUE',씨.c_uint)]
class kursor_VALUE(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('verilənlər',씨.c_void_p*3)]
class yerinə_qoymaq(씨.Structure): _fields_ = [('verilənlər',씨.c_void_p*2),('OFFSET_VALUE',씨.c_uint)]
def FUNCTION_VALUE(Ad, geri_qaytarmaq_ölçü, *인수):
    daxiletmə_VALUE = getattr(구현, Ad); daxiletmə_VALUE.restype = geri_qaytarmaq_ölçü; daxiletmə_VALUE.argtypes = list(인수); return daxiletmə_VALUE
əldə_et_SMS = FUNCTION_VALUE('clang_getCString',씨.c_char_p,sətir_VALUE)
burax_SMS = FUNCTION_VALUE('clang_disposeString',None,sətir_VALUE)
def Mətn(VALUE):
    ölçü = (əldə_et_SMS(VALUE) or b'').decode('utf-8'); burax_SMS(VALUE); return ölçü
əldə_et_ad = FUNCTION_VALUE('clang_getCursorSpelling',sətir_VALUE,kursor_VALUE)
əldə_et_İstinad = FUNCTION_VALUE('clang_getCursorReferenced',kursor_VALUE,kursor_VALUE)
əldə_et_yerinə_qoymaq = FUNCTION_VALUE('clang_getCursorLocation',yerinə_qoymaq,kursor_VALUE)
fayl_yerinə_qoymaq = FUNCTION_VALUE('clang_getFileLocation',None,yerinə_qoymaq,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
fayl_daxiletmə_ad = FUNCTION_VALUE('clang_getFileName',sətir_VALUE,씨.c_void_p)
UNIQUE_ad = FUNCTION_VALUE('clang_getCursorUSR',sətir_VALUE,kursor_VALUE)
연결종류 = FUNCTION_VALUE('clang_getCursorLinkage',씨.c_uint,kursor_VALUE)
방문형 = 씨.CFUNCTYPE(씨.c_uint,kursor_VALUE,kursor_VALUE,씨.c_void_p)
방문 = FUNCTION_VALUE('clang_visitChildren',씨.c_uint,kursor_VALUE,방문형,씨.c_void_p)
yarat = FUNCTION_VALUE('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = FUNCTION_VALUE('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
kök_VALUE = FUNCTION_VALUE('clang_getTranslationUnitCursor',kursor_VALUE,씨.c_void_p)
çıxış_proqram = FUNCTION_VALUE('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = FUNCTION_VALUE('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = FUNCTION_VALUE('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
səviyyə_VALUE = FUNCTION_VALUE('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = FUNCTION_VALUE('clang_getDiagnosticSpelling',sətir_VALUE,씨.c_void_p)
진단해제 = FUNCTION_VALUE('clang_disposeDiagnostic',None,씨.c_void_p)

def yerinə_qoymaq_INDEX(daxiletmə_VALUE):
    FAYL = 씨.c_void_p(); Giriş = 씨.c_uint(); slot_daxiletmə = 씨.c_uint(); OFFSET_VALUE = 씨.c_uint()
    fayl_yerinə_qoymaq(əldə_et_yerinə_qoymaq(daxiletmə_VALUE),씨.byref(FAYL),씨.byref(Giriş),씨.byref(slot_daxiletmə),씨.byref(OFFSET_VALUE))
    return (Mətn(fayl_daxiletmə_ad(FAYL)) if FAYL else '', OFFSET_VALUE.value, Giriş.value)

def icra_etmək_əmr():
    LOOKUP_INDEX = yarat(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 bəyannamə 없이 TinyCC 외부 단일 TRANSLATE_mənbə 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, faktiki_verilənlər 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Cığır.resolve()) for Cığır in Project_kök.rglob('*') if Cığır.suffix in ('.c','.h','.cpp','.inc')
              and not set(Cığır.relative_to(Project_kök).parts)&{'build','dist','vendor','__pycache__'}
              and Cığır.relative_to(Project_kök).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(Project_kök/'istifadəçi'),
          '-I'+str(Project_kök.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(Project_kök/'build'),'-I'+str(Project_kök/'build/user'),
          '-I'+str(Project_kök/'build/remote'),'-I'+str(Project_kök/'vendor/bearssl/inc'),
          '-I'+str(Project_kök/'vendor/bearssl/src'),'-I'+str(Project_kök/'vendor/libassh/src'),
          '-I'+str(Project_kök/'vendor/lwip/src/include'),'-I'+str(Project_kök/'Şəbəkə_Yığın'),
          '-I'+str(Project_kök/'uzaq_VALUE'),'-I'+str(Project_kök/'시언어번역기')]
    for Cığır in sorted(Path(Ad) for Ad in 소유파일 if Ad.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if Cığır.suffix=='.cpp' else '-std=c11']
        if 'Şəbəkə_Yığın' in Cığır.parts: 인수 += ['-I'+str(Project_kök/'Şəbəkə_Yığın'),'-I'+str(Project_kök/'vendor/lwip/src/include')]
        if '시언어번역기' in Cığır.parts:
            인수 += ['-I'+str(Project_kök/'시언어번역기'),'-I'+str(Project_kök/'vendor/tinycc'),'-I'+str(Project_kök/'build/ccompiler'),
                    '-isystem',str(Project_kök.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_körpü' in Cığır.parts:
            인수 += ['-I'+str(Project_kök/'PYTHON_körpü'),'-I'+str(Project_kök/'build/micropython-1.24.1'),'-I'+str(Project_kök/'build/python'),'-isystem','/usr/include/newlib']
        if 'uzaq_VALUE' in Cığır.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in Cığır.parts: 인수 += ['-D__JKOROS__=1']
        if Cığır.name=='paket.c': 인수 += ['-I'+str(Project_kök/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Qrup_VALUE = (씨.c_char_p*len(인수))(*[daxiletmə_VALUE.encode() for daxiletmə_VALUE in 인수])
        Tərcümə_dərs = 분석(LOOKUP_INDEX,str(Cığır).encode(),Qrup_VALUE,len(인수),None,0,1)
        for INDEX in range(진단수(Tərcümə_dərs)):
            진단 = 진단얻기(Tərcümə_dərs,INDEX)
            if səviyyə_VALUE(진단)>=3: 오류들.append((str(Cığır.relative_to(Project_kök)),Mətn(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(daxiletmə_VALUE,부모,verilənlər):
            FAYL,OFFSET_VALUE,Giriş = yerinə_qoymaq_INDEX(daxiletmə_VALUE)
            if FAYL not in 소유파일: return 2 if daxiletmə_VALUE.종류==300 else 1
            낱말 = Mətn(əldə_et_ad(daxiletmə_VALUE))
            if not 낱말 or any(ord(simvol_VALUE_068c2631)>127 for simvol_VALUE_068c2631 in 낱말): return 2
            if daxiletmə_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Mətn(UNIQUE_ad(daxiletmə_VALUE)) or FAYL+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'FAYL':FAYL,'OFFSET_VALUE':OFFSET_VALUE,'Giriş':Giriş,'종류':daxiletmə_VALUE.종류,'Ad':낱말,'Bağlan':연결종류(daxiletmə_VALUE)}
                참조들.append((FAYL,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                İstinad = əldə_et_İstinad(daxiletmə_VALUE)
                İstinad_fayl,_,_ = yerinə_qoymaq_INDEX(İstinad)
                if İstinad_fayl in 소유파일:
                    UNIQUE_VALUE = Mətn(UNIQUE_ad(İstinad)); 참조들.append((FAYL,OFFSET_VALUE,Mətn(əldə_et_ad(İstinad)),UNIQUE_VALUE))
            return 2
        방문(kök_VALUE(Tərcümə_dərs),살피기,None)
        çıxış_proqram(Tərcümə_dərs)
    təyinat_VALUE_a0fbc067 = Project_kök/'build/한국어화/시언어분석.json'
    təyinat_VALUE_a0fbc067.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {FAYL:hashlib.sha256(Path(FAYL).read_bytes()).hexdigest() for FAYL in sorted(소유파일)}
    təyinat_VALUE_a0fbc067.write_text(json.dumps({'bəyannamə':선언들,'İstinad':참조들,'XƏTA':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('bəyannamə',len(선언들),'İstinad',len(참조들),'XƏTA',len(오류들))
    for XƏTA in 오류들: print(*XƏTA)

if __name__=='__main__': icra_etmək_əmr()
