#!/usr/bin/env python3
"""libclang pengisytiharan_4f4f026b·Rujukan 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_sumber
import hashlib
import json
from pathlib import Path

projek_akar = Path(__file__).resolve().parents[1]
pelaksanaan = C_sumber.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class rentetan_VALUE(C_sumber.Structure): _fields_ = [('data',C_sumber.c_void_p),('tayang_VALUE',C_sumber.c_uint)]
class kursor_VALUE(C_sumber.Structure): _fields_ = [('종류',C_sumber.c_uint),('보조',C_sumber.c_int),('data',C_sumber.c_void_p*3)]
class Kedudukan(C_sumber.Structure): _fields_ = [('data',C_sumber.c_void_p*2),('Ofset_VALUE',C_sumber.c_uint)]
def fungsi_VALUE(Nama, kembalikan_ukuran, *인수):
    pemasukan_VALUE = getattr(pelaksanaan, Nama); pemasukan_VALUE.restype = kembalikan_ukuran; pemasukan_VALUE.argtypes = list(인수); return pemasukan_VALUE
dapatkan_SMS = fungsi_VALUE('clang_getCString',C_sumber.c_char_p,rentetan_VALUE)
keluaran_SMS = fungsi_VALUE('clang_disposeString',None,rentetan_VALUE)
def Teks(VALUE):
    ukuran = (dapatkan_SMS(VALUE) or b'').decode('utf-8'); keluaran_SMS(VALUE); return ukuran
dapatkan_nama = fungsi_VALUE('clang_getCursorSpelling',rentetan_VALUE,kursor_VALUE)
dapatkan_Rujukan = fungsi_VALUE('clang_getCursorReferenced',kursor_VALUE,kursor_VALUE)
dapatkan_jawatan = fungsi_VALUE('clang_getCursorLocation',Kedudukan,kursor_VALUE)
fail_jawatan = fungsi_VALUE('clang_getFileLocation',None,Kedudukan,C_sumber.POINTER(C_sumber.c_void_p),C_sumber.POINTER(C_sumber.c_uint),C_sumber.POINTER(C_sumber.c_uint),C_sumber.POINTER(C_sumber.c_uint))
fail_pemasukan_nama = fungsi_VALUE('clang_getFileName',rentetan_VALUE,C_sumber.c_void_p)
UNIQUE_nama = fungsi_VALUE('clang_getCursorUSR',rentetan_VALUE,kursor_VALUE)
연결종류 = fungsi_VALUE('clang_getCursorLinkage',C_sumber.c_uint,kursor_VALUE)
방문형 = C_sumber.CFUNCTYPE(C_sumber.c_uint,kursor_VALUE,kursor_VALUE,C_sumber.c_void_p)
방문 = fungsi_VALUE('clang_visitChildren',C_sumber.c_uint,kursor_VALUE,방문형,C_sumber.c_void_p)
jana = fungsi_VALUE('clang_createIndex',C_sumber.c_void_p,C_sumber.c_int,C_sumber.c_int)
Analisis_VALUE = fungsi_VALUE('clang_parseTranslationUnit',C_sumber.c_void_p,C_sumber.c_void_p,C_sumber.c_char_p,C_sumber.POINTER(C_sumber.c_char_p),C_sumber.c_int,C_sumber.c_void_p,C_sumber.c_uint,C_sumber.c_uint)
akar_VALUE = fungsi_VALUE('clang_getTranslationUnitCursor',kursor_VALUE,C_sumber.c_void_p)
keluar_aplikasi = fungsi_VALUE('clang_disposeTranslationUnit',None,C_sumber.c_void_p)
진단수 = fungsi_VALUE('clang_getNumDiagnostics',C_sumber.c_uint,C_sumber.c_void_p)
진단얻기 = fungsi_VALUE('clang_getDiagnostic',C_sumber.c_void_p,C_sumber.c_void_p,C_sumber.c_uint)
keterukan_VALUE = fungsi_VALUE('clang_getDiagnosticSeverity',C_sumber.c_uint,C_sumber.c_void_p)
진단문 = fungsi_VALUE('clang_getDiagnosticSpelling',rentetan_VALUE,C_sumber.c_void_p)
진단해제 = fungsi_VALUE('clang_disposeDiagnostic',None,C_sumber.c_void_p)

def jawatan_INDEX(pemasukan_VALUE):
    Fail = C_sumber.c_void_p(); baris = C_sumber.c_uint(); 칸 = C_sumber.c_uint(); Ofset_VALUE = C_sumber.c_uint()
    fail_jawatan(dapatkan_jawatan(pemasukan_VALUE),C_sumber.byref(Fail),C_sumber.byref(baris),C_sumber.byref(칸),C_sumber.byref(Ofset_VALUE))
    return (Teks(fail_pemasukan_nama(Fail)) if Fail else '', Ofset_VALUE.value, baris.value)

def laksanakan_perintah():
    Carian_INDEX = jana(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 Asli pengisytiharan_4f4f026b 없이 TinyCC 외부 단일 Terjemah_sumber 단위만 포함한다.
    # 외부 선언을 Asli 이름으로 세지 않으며, sebenar_data 빌드에서는 계속 컴파일한다.
    소유파일 = {str(LALUAN.resolve()) for LALUAN in projek_akar.rglob('*') if LALUAN.suffix in ('.c','.h','.cpp','.inc')
              and not set(LALUAN.relative_to(projek_akar).parts)&{'build','dist','vendor','__pycache__'}
              and LALUAN.relative_to(projek_akar).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(projek_akar/'ruang_pengguna'),
          '-I'+str(projek_akar.parents[1]/'posix-kor/arm64-native/pengisytiharan'),'-I'+str(projek_akar/'build'),'-I'+str(projek_akar/'build/user'),
          '-I'+str(projek_akar/'build/remote'),'-I'+str(projek_akar/'vendor/bearssl/inc'),
          '-I'+str(projek_akar/'vendor/bearssl/src'),'-I'+str(projek_akar/'vendor/libassh/src'),
          '-I'+str(projek_akar/'vendor/lwip/src/include'),'-I'+str(projek_akar/'rangkaian_tindan'),
          '-I'+str(projek_akar/'jauh_VALUE'),'-I'+str(projek_akar/'시언어번역기')]
    for LALUAN in sorted(Path(Nama) for Nama in 소유파일 if Nama.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if LALUAN.suffix=='.cpp' else '-std=c11']
        if 'rangkaian_tindan' in LALUAN.parts: 인수 += ['-I'+str(projek_akar/'rangkaian_tindan'),'-I'+str(projek_akar/'vendor/lwip/src/include')]
        if '시언어번역기' in LALUAN.parts:
            인수 += ['-I'+str(projek_akar/'시언어번역기'),'-I'+str(projek_akar/'vendor/tinycc'),'-I'+str(projek_akar/'build/ccompiler'),
                    '-isystem',str(projek_akar.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_penghubung' in LALUAN.parts:
            인수 += ['-I'+str(projek_akar/'PYTHON_penghubung'),'-I'+str(projek_akar/'build/micropython-1.24.1'),'-I'+str(projek_akar/'build/python'),'-isystem','/usr/include/newlib']
        if 'jauh_VALUE' in LALUAN.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in LALUAN.parts: 인수 += ['-D__JKOROS__=1']
        if LALUAN.name=='pakej.c': 인수 += ['-I'+str(projek_akar/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Kumpulan_VALUE = (C_sumber.c_char_p*len(인수))(*[pemasukan_VALUE.encode() for pemasukan_VALUE in 인수])
        Terjemahan_unit = Analisis_VALUE(Carian_INDEX,str(LALUAN).encode(),Kumpulan_VALUE,len(인수),None,0,1)
        for INDEX in range(진단수(Terjemahan_unit)):
            진단 = 진단얻기(Terjemahan_unit,INDEX)
            if keterukan_VALUE(진단)>=3: 오류들.append((str(LALUAN.relative_to(projek_akar)),Teks(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(pemasukan_VALUE,부모,data):
            Fail,Ofset_VALUE,baris = jawatan_INDEX(pemasukan_VALUE)
            if Fail not in 소유파일: return 2 if pemasukan_VALUE.종류==300 else 1
            낱말 = Teks(dapatkan_nama(pemasukan_VALUE))
            if not 낱말 or any(ord(aksara_VALUE)>127 for aksara_VALUE in 낱말): return 2
            if pemasukan_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Teks(UNIQUE_nama(pemasukan_VALUE)) or Fail+':'+str(Ofset_VALUE)
                선언들[UNIQUE_VALUE] = {'Fail':Fail,'Ofset_VALUE':Ofset_VALUE,'줄':baris,'종류':pemasukan_VALUE.종류,'Nama':낱말,'Sambung':연결종류(pemasukan_VALUE)}
                참조들.append((Fail,Ofset_VALUE,낱말,UNIQUE_VALUE))
            else:
                Rujukan = dapatkan_Rujukan(pemasukan_VALUE)
                Rujukan_fail,_,_ = jawatan_INDEX(Rujukan)
                if Rujukan_fail in 소유파일:
                    UNIQUE_VALUE = Teks(UNIQUE_nama(Rujukan)); 참조들.append((Fail,Ofset_VALUE,Teks(dapatkan_nama(Rujukan)),UNIQUE_VALUE))
            return 2
        방문(akar_VALUE(Terjemahan_unit),살피기,None)
        keluar_aplikasi(Terjemahan_unit)
    destinasi_VALUE = projek_akar/'build/한국어화/시언어분석.json'
    destinasi_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Fail:hashlib.sha256(Path(Fail).read_bytes()).hexdigest() for Fail in sorted(소유파일)}
    destinasi_VALUE.write_text(json.dumps({'pengisytiharan_4f4f026b':선언들,'Rujukan':참조들,'RALAT':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('pengisytiharan_4f4f026b',len(선언들),'Rujukan',len(참조들),'RALAT',len(오류들))
    for RALAT in 오류들: print(*RALAT)

if __name__=='__main__': laksanakan_perintah()
