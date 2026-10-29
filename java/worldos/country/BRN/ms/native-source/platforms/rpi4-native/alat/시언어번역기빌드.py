"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(akar_laluan, repositori_laluan, 시언어번역기, pemaut_alat, konfigurasi_Background_Intelligent_Transfer_Service, laksanakan_perintah):
    ukuran_data = akar_laluan / 'build/ccompiler'; ukuran_data.mkdir(exist_ok=True)
    원본자료 = akar_laluan / '시언어번역기'
    huluan = akar_laluan / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = akar_laluan / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfigurasi_Background_Intelligent_Transfer_Service = [Seting_VALUE for Seting_VALUE in konfigurasi_Background_Intelligent_Transfer_Service if Seting_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', huluan, '-I', akar_laluan/'ruang_pengguna', '-I', ukuran_data, '-isystem', 개발꾸러미/'usr/include']
    laksanakan_perintah([시언어번역기]+konfigurasi_Background_Intelligent_Transfer_Service+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'butstrap_Sokongan.c','-o',ukuran_data/'crt.o'])
    laksanakan_perintah([시언어번역기]+konfigurasi_Background_Intelligent_Transfer_Service+['-I',repositori_laluan/'posix-kor/arm64-native/pengisytiharan']+포함인수+['-c',원본자료/'미리번역실행.c','-o',ukuran_data/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+data_jawatan.name,data_jawatan) for data_jawatan in sorted((repositori_laluan/'posix-kor/arm64-native/pengisytiharan').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_jawatan.name,data_jawatan) for data_jawatan in sorted((huluan/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_jawatan.name,data_jawatan) for data_jawatan in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',akar_laluan/'build/user/start.o'),('/sdk/lib/crt.o',ukuran_data/'crt.o'),('/sdk/lib/aot-runtime.o',ukuran_data/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',akar_laluan/'build/libposix-kor-user.a')]
    Pengepala_VALUE=['typedef struct { const char *Nama; const unsigned char *data; unsigned Saiz; } 번역기자원;']
    for 순번,(_,LALUAN) in enumerate(탑재자료):
        Pengepala_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in LALUAN.read_bytes())))
    Pengepala_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Nama,LALUAN) in enumerate(탑재자료): Pengepala_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Nama,ensure_ascii=False),순번,LALUAN.stat().st_size))
    Pengepala_VALUE.append('};');(ukuran_data/'resources.h').write_text('\n'.join(Pengepala_VALUE)+'\n',encoding='utf-8')
    destinasi_Fail=[]
    for Nama in ('번역기.c','masa_jalan_bahasa_biasa_Sokongan.c','Jalan.c','미리번역.c','kembalikan_penghubung.S'):
        fail_destinasi=ukuran_data/(Path(Nama).stem+'.o');destinasi_Fail.append(fail_destinasi)
        laksanakan_perintah([시언어번역기]+konfigurasi_Background_Intelligent_Transfer_Service+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Nama,'-o',fail_destinasi])
    fail_boleh_laku=akar_laluan/'build/user/cc.elf'
    laksanakan_perintah([pemaut_alat,'--gc-sections','-T',akar_laluan/'ruang_pengguna/susun_atur_pautan.ld','-z','max-page-size=4096','-o',fail_boleh_laku,
         akar_laluan/'build/user/start.o',akar_laluan/'build/user/runtime.o']+destinasi_Fail+
         [akar_laluan/'build/user'/Nama for Nama in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
