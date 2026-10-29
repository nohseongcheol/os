#!/usr/bin/env python3
"""libclang bildirim·Başvuru 위치를 수집한다. dış_değer 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_kaynak
import hashlib
import json
from pathlib import Path

işlem_kök = Path(__file__).resolve().parents[1]
gerçekleme = C_kaynak.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class dize_değer(C_kaynak.Structure): _fields_ = [('veri',C_kaynak.c_void_p),('şov_değer',C_kaynak.c_uint)]
class imleç_değer(C_kaynak.Structure): _fields_ = [('Tip_değer',C_kaynak.c_uint),('보조',C_kaynak.c_int),('veri',C_kaynak.c_void_p*3)]
class konum(C_kaynak.Structure): _fields_ = [('veri',C_kaynak.c_void_p*2),('Ofset_değer',C_kaynak.c_uint)]
def işlev_değer(İsim, İade_KR, *bağımsız_değişkenler):
    girdi_değer = getattr(gerçekleme, İsim); girdi_değer.restype = İade_KR; girdi_değer.argtypes = list(bağımsız_değişkenler); return girdi_değer
get_SMS = işlev_değer('clang_getCString',C_kaynak.c_char_p,dize_değer)
sürüm_SMS = işlev_değer('clang_disposeString',None,dize_değer)
def metin(değer):
    sonuç = (get_SMS(değer) or b'').decode('utf-8'); sürüm_SMS(değer); return sonuç
get_ad = işlev_değer('clang_getCursorSpelling',dize_değer,imleç_değer)
get_Başvuru = işlev_değer('clang_getCursorReferenced',imleç_değer,imleç_değer)
get_konum = işlev_değer('clang_getCursorLocation',konum,imleç_değer)
Dosya_konum = işlev_değer('clang_getFileLocation',None,konum,C_kaynak.POINTER(C_kaynak.c_void_p),C_kaynak.POINTER(C_kaynak.c_uint),C_kaynak.POINTER(C_kaynak.c_uint),C_kaynak.POINTER(C_kaynak.c_uint))
Dosya_girdi_ad = işlev_değer('clang_getFileName',dize_değer,C_kaynak.c_void_p)
BENZERSİZ_ad = işlev_değer('clang_getCursorUSR',dize_değer,imleç_değer)
cxn_Tip = işlev_değer('clang_getCursorLinkage',C_kaynak.c_uint,imleç_değer)
방문형 = C_kaynak.CFUNCTYPE(C_kaynak.c_uint,imleç_değer,imleç_değer,C_kaynak.c_void_p)
방문 = işlev_değer('clang_visitChildren',C_kaynak.c_uint,imleç_değer,방문형,C_kaynak.c_void_p)
oluşturmak = işlev_değer('clang_createIndex',C_kaynak.c_void_p,C_kaynak.c_int,C_kaynak.c_int)
Analiz_değer = işlev_değer('clang_parseTranslationUnit',C_kaynak.c_void_p,C_kaynak.c_void_p,C_kaynak.c_char_p,C_kaynak.POINTER(C_kaynak.c_char_p),C_kaynak.c_int,C_kaynak.c_void_p,C_kaynak.c_uint,C_kaynak.c_uint)
kök_değer = işlev_değer('clang_getTranslationUnitCursor',imleç_değer,C_kaynak.c_void_p)
çıkış_program = işlev_değer('clang_disposeTranslationUnit',None,C_kaynak.c_void_p)
진단수 = işlev_değer('clang_getNumDiagnostics',C_kaynak.c_uint,C_kaynak.c_void_p)
진단얻기 = işlev_değer('clang_getDiagnostic',C_kaynak.c_void_p,C_kaynak.c_void_p,C_kaynak.c_uint)
önem_düzeyi_değer = işlev_değer('clang_getDiagnosticSeverity',C_kaynak.c_uint,C_kaynak.c_void_p)
진단문 = işlev_değer('clang_getDiagnosticSpelling',dize_değer,C_kaynak.c_void_p)
진단해제 = işlev_değer('clang_disposeDiagnostic',None,C_kaynak.c_void_p)

def konum_dizini(girdi_değer):
    dosya = C_kaynak.c_void_p(); girdi_satırı = C_kaynak.c_uint(); yuva_girdi = C_kaynak.c_uint(); Ofset_değer = C_kaynak.c_uint()
    Dosya_konum(get_konum(girdi_değer),C_kaynak.byref(dosya),C_kaynak.byref(girdi_satırı),C_kaynak.byref(yuva_girdi),C_kaynak.byref(Ofset_değer))
    return (metin(Dosya_girdi_ad(dosya)) if dosya else '', Ofset_değer.value, girdi_satırı.value)

def yürütmek_komut():
    ARA_Dizin = oluşturmak(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # derleyici_araç.c는 Öz bildirim 없이 TinyCC dış_değer 단일 çevir_kaynak 단위만 포함한다.
    # dış_değer 선언을 Öz 이름으로 세지 않으며, fiili_veri 빌드에서는 계속 컴파일한다.
    소유파일 = {str(yol.resolve()) for yol in işlem_kök.rglob('*') if yol.suffix in ('.c','.h','.cpp','.inc')
              and not set(yol.relative_to(işlem_kök).parts)&{'build','dist','vendor','__pycache__'}
              and yol.relative_to(işlem_kök).as_posix() != 'C_derleyici/derleyici_araç.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(işlem_kök/'kullanıcı_alanı'),
          '-I'+str(işlem_kök.parents[1]/'posix-kor/arm64-native/bildirimler'),'-I'+str(işlem_kök/'build'),'-I'+str(işlem_kök/'build/user'),
          '-I'+str(işlem_kök/'build/remote'),'-I'+str(işlem_kök/'vendor/bearssl/inc'),
          '-I'+str(işlem_kök/'vendor/bearssl/src'),'-I'+str(işlem_kök/'vendor/libassh/src'),
          '-I'+str(işlem_kök/'vendor/lwip/src/include'),'-I'+str(işlem_kök/'ağ_Yığın'),
          '-I'+str(işlem_kök/'uzak_değer'),'-I'+str(işlem_kök/'C_derleyici')]
    for yol in sorted(Path(İsim) for İsim in 소유파일 if İsim.endswith(('.c','.cpp'))):
        bağımsız_değişkenler = 공통 + ['-std=c++11' if yol.suffix=='.cpp' else '-std=c11']
        if 'ağ_Yığın' in yol.parts: bağımsız_değişkenler += ['-I'+str(işlem_kök/'ağ_Yığın'),'-I'+str(işlem_kök/'vendor/lwip/src/include')]
        if 'C_derleyici' in yol.parts:
            bağımsız_değişkenler += ['-I'+str(işlem_kök/'C_derleyici'),'-I'+str(işlem_kök/'vendor/tinycc'),'-I'+str(işlem_kök/'build/ccompiler'),
                    '-isystem',str(işlem_kök.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_köprü' in yol.parts:
            bağımsız_değişkenler += ['-I'+str(işlem_kök/'PYTHON_köprü'),'-I'+str(işlem_kök/'build/micropython-1.24.1'),'-I'+str(işlem_kök/'build/python'),'-isystem','/usr/include/newlib']
        if 'uzak_değer' in yol.parts:
            bağımsız_değişkenler += ['-isystem', '/usr/include/newlib']
        if 'dağıtım_değer' in yol.parts: bağımsız_değişkenler += ['-D__JKOROS__=1']
        if yol.name=='paket_iş.c': bağımsız_değişkenler += ['-I'+str(işlem_kök/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Grup_değer = (C_kaynak.c_char_p*len(bağımsız_değişkenler))(*[girdi_değer.encode() for girdi_değer in bağımsız_değişkenler])
        çeviri_birimi = Analiz_değer(ARA_Dizin,str(yol).encode(),Grup_değer,len(bağımsız_değişkenler),None,0,1)
        for Dizin in range(진단수(çeviri_birimi)):
            진단 = 진단얻기(çeviri_birimi,Dizin)
            if önem_düzeyi_değer(진단)>=3: 오류들.append((str(yol.relative_to(işlem_kök)),metin(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(girdi_değer,ana_değer,veri):
            dosya,Ofset_değer,girdi_satırı = konum_dizini(girdi_değer)
            if dosya not in 소유파일: return 2 if girdi_değer.Tip_değer==300 else 1
            낱말 = metin(get_ad(girdi_değer))
            if not 낱말 or any(ord(karakter_değer)>127 for karakter_değer in 낱말): return 2
            if girdi_değer.Tip_değer in (2,3,4,5,6,7,8,9,10,20,21,501):
                BENZERSİZ_değer = metin(BENZERSİZ_ad(girdi_değer)) or dosya+':'+str(Ofset_değer)
                선언들[BENZERSİZ_değer] = {'dosya':dosya,'Ofset_değer':Ofset_değer,'girdi_satırı':girdi_satırı,'Tip_değer':girdi_değer.Tip_değer,'İsim':낱말,'Bağlan':cxn_Tip(girdi_değer)}
                참조들.append((dosya,Ofset_değer,낱말,BENZERSİZ_değer))
            else:
                Başvuru = get_Başvuru(girdi_değer)
                Başvuru_Dosya,_,_ = konum_dizini(Başvuru)
                if Başvuru_Dosya in 소유파일:
                    BENZERSİZ_değer = metin(BENZERSİZ_ad(Başvuru)); 참조들.append((dosya,Ofset_değer,metin(get_ad(Başvuru)),BENZERSİZ_değer))
            return 2
        방문(kök_değer(çeviri_birimi),살피기,None)
        çıkış_program(çeviri_birimi)
    hedef_değer = işlem_kök/'build/한국어화/시언어분석.json'
    hedef_değer.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {dosya:hashlib.sha256(Path(dosya).read_bytes()).hexdigest() for dosya in sorted(소유파일)}
    hedef_değer.write_text(json.dumps({'bildirim':선언들,'Başvuru':참조들,'hata':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('bildirim',len(선언들),'Başvuru',len(참조들),'hata',len(오류들))
    for hata in 오류들: print(*hata)

if __name__=='__main__': yürütmek_komut()
