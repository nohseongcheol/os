"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def maken_C_compiler(wortel_pad, opslagplaats_pad, C_compiler, linker_hulpmiddel, configuratie_BITS, Uitvoeren_opdracht):
    HR_gegevens = wortel_pad / 'build/ccompiler'; HR_gegevens.mkdir(exist_ok=True)
    원본자료 = wortel_pad / 'C_compiler'
    upstream = wortel_pad / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    Development_Kit = wortel_pad / 'vendor/sdk'
    if not (Development_Kit/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((Development_Kit/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    configuratie_BITS = [Instellingen_WAARDE for Instellingen_WAARDE in configuratie_BITS if Instellingen_WAARDE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', upstream, '-I', wortel_pad/'gebruikersruimte', '-I', HR_gegevens, '-isystem', Development_Kit/'usr/include']
    Uitvoeren_opdracht([C_compiler]+configuratie_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'bootstrap_steun.c','-o',HR_gegevens/'crt.o'])
    Uitvoeren_opdracht([C_compiler]+configuratie_BITS+['-I',opslagplaats_pad/'posix-kor/arm64-native/declaraties']+포함인수+['-c',원본자료/'AOT_CLR.c','-o',HR_gegevens/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+gegevens_functie.name,gegevens_functie) for gegevens_functie in sorted((opslagplaats_pad/'posix-kor/arm64-native/declaraties').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+gegevens_functie.name,gegevens_functie) for gegevens_functie in sorted((upstream/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+gegevens_functie.name,gegevens_functie) for gegevens_functie in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',wortel_pad/'build/user/start.o'),('/sdk/lib/crt.o',HR_gegevens/'crt.o'),('/sdk/lib/aot-runtime.o',HR_gegevens/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',wortel_pad/'build/libposix-kor-user.a')]
    header_WAARDE=['typedef struct { const char *Naam; const unsigned char *gegevens; unsigned Grootte; } compiler_bron;']
    for 순번,(_,pad) in enumerate(탑재자료):
        header_WAARDE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in pad.read_bytes())))
    header_WAARDE.append('static const compiler_bron compiler_Bronnen[] = {')
    for 순번,(Naam,pad) in enumerate(탑재자료): header_WAARDE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Naam,ensure_ascii=False),순번,pad.stat().st_size))
    header_WAARDE.append('};');(HR_gegevens/'resources.h').write_text('\n'.join(header_WAARDE)+'\n',encoding='utf-8')
    doel_Files=[]
    for Naam in ('compiler_hulpmiddel.c','CLR_steun.c','starten.c','미리번역.c','Retour_brug.S'):
        doelbestand=HR_gegevens/(Path(Naam).stem+'.o');doel_Files.append(doelbestand)
        Uitvoeren_opdracht([C_compiler]+configuratie_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Naam,'-o',doelbestand])
    uitvoerbaar_bestand=wortel_pad/'build/user/cc.elf'
    Uitvoeren_opdracht([linker_hulpmiddel,'--gc-sections','-T',wortel_pad/'gebruikersruimte/koppelindeling.ld','-z','max-page-size=4096','-o',uitvoerbaar_bestand,
         wortel_pad/'build/user/start.o',wortel_pad/'build/user/runtime.o']+doel_Files+
         [wortel_pad/'build/user'/Naam for Naam in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
