#!/usr/bin/env python3
"""libclang deklarasi_4f4f026b·Referensi 위치를 수집한다. eksternal_VALUE 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

Tugas_akar = Path(__file__).resolve().parents[1]
implementasi = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class string_VALUE(씨.Structure): _fields_ = [('data',씨.c_void_p),('show_VALUE',씨.c_uint)]
class kursor_VALUE(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('data',씨.c_void_p*3)]
class posisi(씨.Structure): _fields_ = [('data',씨.c_void_p*2),('OFFSET_VALUE',씨.c_uint)]
def fungsi_VALUE(Nama_2, kembalikan_KR, *argumen):
    entri_VALUE = getattr(implementasi, Nama_2); entri_VALUE.restype = kembalikan_KR; entri_VALUE.argtypes = list(argumen); return entri_VALUE
dapatkan_SMS = fungsi_VALUE('clang_getCString',씨.c_char_p,string_VALUE)
lepas_SMS = fungsi_VALUE('clang_disposeString',None,string_VALUE)
def teks(VALUE):
    hasil = (dapatkan_SMS(VALUE) or b'').decode('utf-8'); lepas_SMS(VALUE); return hasil
dapatkan_nama = fungsi_VALUE('clang_getCursorSpelling',string_VALUE,kursor_VALUE)
dapatkan_Referensi = fungsi_VALUE('clang_getCursorReferenced',kursor_VALUE,kursor_VALUE)
dapatkan_posisi = fungsi_VALUE('clang_getCursorLocation',posisi,kursor_VALUE)
file_posisi = fungsi_VALUE('clang_getFileLocation',None,posisi,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
file_entri_nama = fungsi_VALUE('clang_getFileName',string_VALUE,씨.c_void_p)
UNIQUE_nama = fungsi_VALUE('clang_getCursorUSR',string_VALUE,kursor_VALUE)
연결종류 = fungsi_VALUE('clang_getCursorLinkage',씨.c_uint,kursor_VALUE)
방문형 = 씨.CFUNCTYPE(씨.c_uint,kursor_VALUE,kursor_VALUE,씨.c_void_p)
방문 = fungsi_VALUE('clang_visitChildren',씨.c_uint,kursor_VALUE,방문형,씨.c_void_p)
buat = fungsi_VALUE('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
Analisis_VALUE = fungsi_VALUE('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
akar_VALUE = fungsi_VALUE('clang_getTranslationUnitCursor',kursor_VALUE,씨.c_void_p)
berhenti_apl = fungsi_VALUE('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = fungsi_VALUE('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = fungsi_VALUE('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
keparahan_VALUE = fungsi_VALUE('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = fungsi_VALUE('clang_getDiagnosticSpelling',string_VALUE,씨.c_void_p)
진단해제 = fungsi_VALUE('clang_disposeDiagnostic',None,씨.c_void_p)

def posisi_INDEX(entri_VALUE):
    berkas = 씨.c_void_p(); baris_masukan = 씨.c_uint(); slot_entri = 씨.c_uint(); OFFSET_VALUE = 씨.c_uint()
    file_posisi(dapatkan_posisi(entri_VALUE),씨.byref(berkas),씨.byref(baris_masukan),씨.byref(slot_entri),씨.byref(OFFSET_VALUE))
    return (teks(file_entri_nama(berkas)) if berkas else '', OFFSET_VALUE.value, baris_masukan.value)

def Jalankan_perintah():
    LOOKUP_INDEX = buat(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 Asli deklarasi_4f4f026b 없이 TinyCC eksternal_VALUE 단일 TRANSLATE_sumber 단위만 포함한다.
    # eksternal_VALUE 선언을 Asli 이름으로 세지 않으며, aktual_data 빌드에서는 계속 컴파일한다.
    소유파일 = {str(jalur.resolve()) for jalur in Tugas_akar.rglob('*') if jalur.suffix in ('.c','.h','.cpp','.inc')
              and not set(jalur.relative_to(Tugas_akar).parts)&{'build','dist','vendor','__pycache__'}
              and jalur.relative_to(Tugas_akar).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(Tugas_akar/'ruang_pengguna'),
          '-I'+str(Tugas_akar.parents[1]/'posix-kor/arm64-native/deklarasi'),'-I'+str(Tugas_akar/'build'),'-I'+str(Tugas_akar/'build/user'),
          '-I'+str(Tugas_akar/'build/remote'),'-I'+str(Tugas_akar/'vendor/bearssl/inc'),
          '-I'+str(Tugas_akar/'vendor/bearssl/src'),'-I'+str(Tugas_akar/'vendor/libassh/src'),
          '-I'+str(Tugas_akar/'vendor/lwip/src/include'),'-I'+str(Tugas_akar/'jaringan_tumpuk'),
          '-I'+str(Tugas_akar/'jarak_jauh_VALUE'),'-I'+str(Tugas_akar/'시언어번역기')]
    for jalur in sorted(Path(Nama_2) for Nama_2 in 소유파일 if Nama_2.endswith(('.c','.cpp'))):
        argumen = 공통 + ['-std=c++11' if jalur.suffix=='.cpp' else '-std=c11']
        if 'jaringan_tumpuk' in jalur.parts: argumen += ['-I'+str(Tugas_akar/'jaringan_tumpuk'),'-I'+str(Tugas_akar/'vendor/lwip/src/include')]
        if '시언어번역기' in jalur.parts:
            argumen += ['-I'+str(Tugas_akar/'시언어번역기'),'-I'+str(Tugas_akar/'vendor/tinycc'),'-I'+str(Tugas_akar/'build/ccompiler'),
                    '-isystem',str(Tugas_akar.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_bridge' in jalur.parts:
            argumen += ['-I'+str(Tugas_akar/'PYTHON_bridge'),'-I'+str(Tugas_akar/'build/micropython-1.24.1'),'-I'+str(Tugas_akar/'build/python'),'-isystem','/usr/include/newlib']
        if 'jarak_jauh_VALUE' in jalur.parts:
            argumen += ['-isystem', '/usr/include/newlib']
        if '배포' in jalur.parts: argumen += ['-D__JKOROS__=1']
        if jalur.name=='paket.c': argumen += ['-I'+str(Tugas_akar/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        grup_VALUE = (씨.c_char_p*len(argumen))(*[entri_VALUE.encode() for entri_VALUE in argumen])
        Terjemahan_unit = Analisis_VALUE(LOOKUP_INDEX,str(jalur).encode(),grup_VALUE,len(argumen),None,0,1)
        for INDEX in range(진단수(Terjemahan_unit)):
            진단 = 진단얻기(Terjemahan_unit,INDEX)
            if keparahan_VALUE(진단)>=3: 오류들.append((str(jalur.relative_to(Tugas_akar)),teks(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(entri_VALUE,induk_VALUE,data):
            berkas,OFFSET_VALUE,baris_masukan = posisi_INDEX(entri_VALUE)
            if berkas not in 소유파일: return 2 if entri_VALUE.종류==300 else 1
            낱말 = teks(dapatkan_nama(entri_VALUE))
            if not 낱말 or any(ord(karakter_VALUE)>127 for karakter_VALUE in 낱말): return 2
            if entri_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = teks(UNIQUE_nama(entri_VALUE)) or berkas+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'berkas':berkas,'OFFSET_VALUE':OFFSET_VALUE,'baris_masukan':baris_masukan,'종류':entri_VALUE.종류,'Nama_2':낱말,'Sambung':연결종류(entri_VALUE)}
                참조들.append((berkas,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                Referensi = dapatkan_Referensi(entri_VALUE)
                Referensi_file,_,_ = posisi_INDEX(Referensi)
                if Referensi_file in 소유파일:
                    UNIQUE_VALUE = teks(UNIQUE_nama(Referensi)); 참조들.append((berkas,OFFSET_VALUE,teks(dapatkan_nama(Referensi)),UNIQUE_VALUE))
            return 2
        방문(akar_VALUE(Terjemahan_unit),살피기,None)
        berhenti_apl(Terjemahan_unit)
    tujuan_VALUE = Tugas_akar/'build/한국어화/시언어분석.json'
    tujuan_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {berkas:hashlib.sha256(Path(berkas).read_bytes()).hexdigest() for berkas in sorted(소유파일)}
    tujuan_VALUE.write_text(json.dumps({'deklarasi_4f4f026b':선언들,'Referensi':참조들,'galat':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('deklarasi_4f4f026b',len(선언들),'Referensi',len(참조들),'galat',len(오류들))
    for galat in 오류들: print(*galat)

if __name__=='__main__': Jalankan_perintah()
