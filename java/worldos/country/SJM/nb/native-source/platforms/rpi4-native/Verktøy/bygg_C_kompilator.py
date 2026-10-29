"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def åpne_C_kompilator(rot_bane, repositorium_bane, C_kompilator, koblingsprogram_verktøy, konfigurasjon_BITS, Utfør_kommando):
    KR_data = rot_bane / 'build/ccompiler'; KR_data.mkdir(exist_ok=True)
    원본자료 = rot_bane / 'C_kompilator'
    oppstrøms = rot_bane / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    utviklingspakke = rot_bane / 'vendor/sdk'
    if not (utviklingspakke/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((utviklingspakke/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfigurasjon_BITS = [Innstillinger_VERDI for Innstillinger_VERDI in konfigurasjon_BITS if Innstillinger_VERDI != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', oppstrøms, '-I', rot_bane/'bruker', '-I', KR_data, '-isystem', utviklingspakke/'usr/include']
    Utfør_kommando([C_kompilator]+konfigurasjon_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'oppstart_støtte.c','-o',KR_data/'crt.o'])
    Utfør_kommando([C_kompilator]+konfigurasjon_BITS+['-I',repositorium_bane/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'applikasjonsobjekttre_CLR.c','-o',KR_data/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+data_plassere.name,data_plassere) for data_plassere in sorted((repositorium_bane/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_plassere.name,data_plassere) for data_plassere in sorted((oppstrøms/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_plassere.name,data_plassere) for data_plassere in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',rot_bane/'build/user/start.o'),('/sdk/lib/crt.o',KR_data/'crt.o'),('/sdk/lib/aot-runtime.o',KR_data/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',rot_bane/'build/libposix-kor-user.a')]
    Topptekst_VERDI=['typedef struct { const char *Navn; const unsigned char *data; unsigned Størrelse; } kompilator_ressurs;']
    for 순번,(_,Sti) in enumerate(탑재자료):
        Topptekst_VERDI.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Sti.read_bytes())))
    Topptekst_VERDI.append('static const kompilator_ressurs kompilator_Ressurser[] = {')
    for 순번,(Navn,Sti) in enumerate(탑재자료): Topptekst_VERDI.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Navn,ensure_ascii=False),순번,Sti.stat().st_size))
    Topptekst_VERDI.append('};');(KR_data/'resources.h').write_text('\n'.join(Topptekst_VERDI)+'\n',encoding='utf-8')
    mål_Filer=[]
    for Navn in ('kompilator_verktøy.c','CLR_støtte.c','Kjør_2.c','미리번역.c','return_bro.S'):
        målfil=KR_data/(Path(Navn).stem+'.o');mål_Filer.append(målfil)
        Utfør_kommando([C_kompilator]+konfigurasjon_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Navn,'-o',målfil])
    kjørbar_fil=rot_bane/'build/user/cc.elf'
    Utfør_kommando([koblingsprogram_verktøy,'--gc-sections','-T',rot_bane/'bruker/koble_Oppsett.ld','-z','max-page-size=4096','-o',kjørbar_fil,
         rot_bane/'build/user/start.o',rot_bane/'build/user/runtime.o']+mål_Filer+
         [rot_bane/'build/user'/Navn for Navn in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
