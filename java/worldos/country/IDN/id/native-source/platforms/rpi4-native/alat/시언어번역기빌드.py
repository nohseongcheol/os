"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(akar_jalur, repositori_jalur, 시언어번역기, 연결편집기, konfigurasi_Background_Intelligent_Transfer_Service, Jalankan_perintah):
    KR_data = akar_jalur / 'build/ccompiler'; KR_data.mkdir(exist_ok=True)
    원본자료 = akar_jalur / '시언어번역기'
    upstram = akar_jalur / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = akar_jalur / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfigurasi_Background_Intelligent_Transfer_Service = [Pengaturan_VALUE for Pengaturan_VALUE in konfigurasi_Background_Intelligent_Transfer_Service if Pengaturan_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', upstram, '-I', akar_jalur/'ruang_pengguna', '-I', KR_data, '-isystem', 개발꾸러미/'usr/include']
    Jalankan_perintah([시언어번역기]+konfigurasi_Background_Intelligent_Transfer_Service+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'mulai_dukung.c','-o',KR_data/'crt.o'])
    Jalankan_perintah([시언어번역기]+konfigurasi_Background_Intelligent_Transfer_Service+['-I',repositori_jalur/'posix-kor/arm64-native/deklarasi']+포함인수+['-c',원본자료/'미리번역실행.c','-o',KR_data/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+data_posisi.name,data_posisi) for data_posisi in sorted((repositori_jalur/'posix-kor/arm64-native/deklarasi').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_posisi.name,data_posisi) for data_posisi in sorted((upstram/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_posisi.name,data_posisi) for data_posisi in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',akar_jalur/'build/user/start.o'),('/sdk/lib/crt.o',KR_data/'crt.o'),('/sdk/lib/aot-runtime.o',KR_data/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',akar_jalur/'build/libposix-kor-user.a')]
    judul_VALUE=['typedef struct { const char *Nama_2; const unsigned char *data; unsigned Ukuran; } 번역기자원;']
    for 순번,(_,jalur) in enumerate(탑재자료):
        judul_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in jalur.read_bytes())))
    judul_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Nama_2,jalur) in enumerate(탑재자료): judul_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Nama_2,ensure_ascii=False),순번,jalur.stat().st_size))
    judul_VALUE.append('};');(KR_data/'resources.h').write_text('\n'.join(judul_VALUE)+'\n',encoding='utf-8')
    tujuan_File=[]
    for Nama_2 in ('번역기.c','runtime_bahasa_umum_dukung.c','jalankan.c','미리번역.c','kembalikan_bridge.S'):
        file_tujuan=KR_data/(Path(Nama_2).stem+'.o');tujuan_File.append(file_tujuan)
        Jalankan_perintah([시언어번역기]+konfigurasi_Background_Intelligent_Transfer_Service+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Nama_2,'-o',file_tujuan])
    실행파일=akar_jalur/'build/user/cc.elf'
    Jalankan_perintah([연결편집기,'--gc-sections','-T',akar_jalur/'ruang_pengguna/tata_letak_penautan.ld','-z','max-page-size=4096','-o',실행파일,
         akar_jalur/'build/user/start.o',akar_jalur/'build/user/runtime.o']+tujuan_File+
         [akar_jalur/'build/user'/Nama_2 for Nama_2 in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
