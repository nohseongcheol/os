#!/usr/bin/env python3
"""libclang 선언·Salgylanma 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class setir_baha_6ca8363c(씨.Structure): _fields_ = [('maglumat',씨.c_void_p),('görkez_baha_487749b8',씨.c_uint)]
class kursor_baha(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('maglumat',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('maglumat',씨.c_void_p*2),('Süýşüriş_baha',씨.c_uint)]
def FUNCTION_baha(Ad, 반환, *인수):
    girizmeklik_baha = getattr(구현, Ad); girizmeklik_baha.restype = 반환; girizmeklik_baha.argtypes = list(인수); return girizmeklik_baha
글얻기 = FUNCTION_baha('clang_getCString',씨.c_char_p,setir_baha_6ca8363c)
goýbermek_SMS = FUNCTION_baha('clang_disposeString',None,setir_baha_6ca8363c)
def Metin(baha):
    결과 = (글얻기(baha) or b'').decode('utf-8'); goýbermek_SMS(baha); return 결과
이름얻기 = FUNCTION_baha('clang_getCursorSpelling',setir_baha_6ca8363c,kursor_baha)
참조얻기 = FUNCTION_baha('clang_getCursorReferenced',kursor_baha,kursor_baha)
위치얻기 = FUNCTION_baha('clang_getCursorLocation',위치,kursor_baha)
파일위치 = FUNCTION_baha('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
faýl_girizmeklik_at = FUNCTION_baha('clang_getFileName',setir_baha_6ca8363c,씨.c_void_p)
UNIQUE_at = FUNCTION_baha('clang_getCursorUSR',setir_baha_6ca8363c,kursor_baha)
연결종류 = FUNCTION_baha('clang_getCursorLinkage',씨.c_uint,kursor_baha)
방문형 = 씨.CFUNCTYPE(씨.c_uint,kursor_baha,kursor_baha,씨.c_void_p)
방문 = FUNCTION_baha('clang_visitChildren',씨.c_uint,kursor_baha,방문형,씨.c_void_p)
생성 = FUNCTION_baha('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = FUNCTION_baha('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = FUNCTION_baha('clang_getTranslationUnitCursor',kursor_baha,씨.c_void_p)
끝내기 = FUNCTION_baha('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = FUNCTION_baha('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = FUNCTION_baha('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
ähmiýet_baha = FUNCTION_baha('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = FUNCTION_baha('clang_getDiagnosticSpelling',setir_baha_6ca8363c,씨.c_void_p)
진단해제 = FUNCTION_baha('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(girizmeklik_baha):
    Faýl = 씨.c_void_p(); setir = 씨.c_uint(); ýer_girizmeklik = 씨.c_uint(); Süýşüriş_baha = 씨.c_uint()
    파일위치(위치얻기(girizmeklik_baha),씨.byref(Faýl),씨.byref(setir),씨.byref(ýer_girizmeklik),씨.byref(Süýşüriş_baha))
    return (Metin(faýl_girizmeklik_at(Faýl)) if Faýl else '', Süýşüriş_baha.value, setir.value)

def ýerine_ýetir_buýruk():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 Terjime_gor 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, hakyky_maglumat 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Ýol.resolve()) for Ýol in 기준.rglob('*') if Ýol.suffix in ('.c','.h','.cpp','.inc')
              and not set(Ýol.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and Ýol.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'ulanyjy'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'Tor_Desse'),
          '-I'+str(기준/'uzakdan_baha'),'-I'+str(기준/'시언어번역기')]
    for Ýol in sorted(Path(Ad) for Ad in 소유파일 if Ad.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if Ýol.suffix=='.cpp' else '-std=c11']
        if 'Tor_Desse' in Ýol.parts: 인수 += ['-I'+str(기준/'Tor_Desse'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in Ýol.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in Ýol.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'uzakdan_baha' in Ýol.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in Ýol.parts: 인수 += ['-D__JKOROS__=1']
        if Ýol.name=='toplum.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        topar_baha = (씨.c_char_p*len(인수))(*[girizmeklik_baha.encode() for girizmeklik_baha in 인수])
        Terjime_sapak = 분석(색인,str(Ýol).encode(),topar_baha,len(인수),None,0,1)
        for indeks in range(진단수(Terjime_sapak)):
            진단 = 진단얻기(Terjime_sapak,indeks)
            if ähmiýet_baha(진단)>=3: 오류들.append((str(Ýol.relative_to(기준)),Metin(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(girizmeklik_baha,부모,maglumat):
            Faýl,Süýşüriş_baha,setir = 자리(girizmeklik_baha)
            if Faýl not in 소유파일: return 2 if girizmeklik_baha.종류==300 else 1
            낱말 = Metin(이름얻기(girizmeklik_baha))
            if not 낱말 or any(ord(nyşan_baha_068c2631)>127 for nyşan_baha_068c2631 in 낱말): return 2
            if girizmeklik_baha.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_baha = Metin(UNIQUE_at(girizmeklik_baha)) or Faýl+':'+str(Süýşüriş_baha)
                선언들[UNIQUE_baha] = {'Faýl':Faýl,'Süýşüriş_baha':Süýşüriş_baha,'줄':setir,'종류':girizmeklik_baha.종류,'Ad':낱말,'Birikme':연결종류(girizmeklik_baha)}
                참조들.append((Faýl,Süýşüriş_baha,낱말,UNIQUE_baha))
            else:
                Salgylanma = 참조얻기(girizmeklik_baha)
                Salgylanma_faýl,_,_ = 자리(Salgylanma)
                if Salgylanma_faýl in 소유파일:
                    UNIQUE_baha = Metin(UNIQUE_at(Salgylanma)); 참조들.append((Faýl,Süýşüriş_baha,Metin(이름얻기(Salgylanma)),UNIQUE_baha))
            return 2
        방문(뿌리(Terjime_sapak),살피기,None)
        끝내기(Terjime_sapak)
    barylmaly_ýer_baha = 기준/'build/한국어화/시언어분석.json'
    barylmaly_ýer_baha.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Faýl:hashlib.sha256(Path(Faýl).read_bytes()).hexdigest() for Faýl in sorted(소유파일)}
    barylmaly_ýer_baha.write_text(json.dumps({'선언':선언들,'Salgylanma':참조들,'Hata':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Salgylanma',len(참조들),'Hata',len(오류들))
    for Hata in 오류들: print(*Hata)

if __name__=='__main__': ýerine_ýetir_buýruk()
