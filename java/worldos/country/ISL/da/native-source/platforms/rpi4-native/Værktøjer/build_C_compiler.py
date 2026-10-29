"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def åbne_C_compiler(rod_sti, lager_sti, C_compiler, linker_værktøj, konfiguration_BITS, Udfør_kommando):
    KR_data = rod_sti / 'build/ccompiler'; KR_data.mkdir(exist_ok=True)
    원본자료 = rod_sti / 'C_compiler'
    upstream = rod_sti / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    Development_Kit = rod_sti / 'vendor/sdk'
    if not (Development_Kit/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((Development_Kit/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfiguration_BITS = [Indstillinger_VÆRDI for Indstillinger_VÆRDI in konfiguration_BITS if Indstillinger_VÆRDI != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', upstream, '-I', rod_sti/'bruger', '-I', KR_data, '-isystem', Development_Kit/'usr/include']
    Udfør_kommando([C_compiler]+konfiguration_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'IPL_støtte.c','-o',KR_data/'crt.o'])
    Udfør_kommando([C_compiler]+konfiguration_BITS+['-I',lager_sti/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'AOT_CLR.c','-o',KR_data/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+data_placere.name,data_placere) for data_placere in sorted((lager_sti/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_placere.name,data_placere) for data_placere in sorted((upstream/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_placere.name,data_placere) for data_placere in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',rod_sti/'build/user/start.o'),('/sdk/lib/crt.o',KR_data/'crt.o'),('/sdk/lib/aot-runtime.o',KR_data/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',rod_sti/'build/libposix-kor-user.a')]
    Header_VÆRDI=['typedef struct { const char *Navn; const unsigned char *data; unsigned Størrelse; } compiler_ressource;']
    for 순번,(_,Sti) in enumerate(탑재자료):
        Header_VÆRDI.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Sti.read_bytes())))
    Header_VÆRDI.append('static const compiler_ressource compiler_Ressourcer[] = {')
    for 순번,(Navn,Sti) in enumerate(탑재자료): Header_VÆRDI.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Navn,ensure_ascii=False),순번,Sti.stat().st_size))
    Header_VÆRDI.append('};');(KR_data/'resources.h').write_text('\n'.join(Header_VÆRDI)+'\n',encoding='utf-8')
    destination_Filer=[]
    for Navn in ('compiler_værktøj.c','CLR_støtte.c','Kør_2.c','미리번역.c','returnere_bro.S'):
        destinationsfil=KR_data/(Path(Navn).stem+'.o');destination_Filer.append(destinationsfil)
        Udfør_kommando([C_compiler]+konfiguration_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Navn,'-o',destinationsfil])
    eksekverbar_fil=rod_sti/'build/user/cc.elf'
    Udfør_kommando([linker_værktøj,'--gc-sections','-T',rod_sti/'bruger/Link_Layout.ld','-z','max-page-size=4096','-o',eksekverbar_fil,
         rod_sti/'build/user/start.o',rod_sti/'build/user/runtime.o']+destination_Filer+
         [rod_sti/'build/user'/Navn for Navn in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
