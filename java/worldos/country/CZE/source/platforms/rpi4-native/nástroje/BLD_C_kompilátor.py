"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def Create_C_kompilátor(kořen_cesta, úložiště_cesta, C_kompilátor, linker_nástroj, konfigurace_BITS, Provést_příkaz):
    KV_data = kořen_cesta / 'build/ccompiler'; KV_data.mkdir(exist_ok=True)
    원본자료 = kořen_cesta / 'C_kompilátor'
    upstream = kořen_cesta / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    Development_Kit = kořen_cesta / 'vendor/sdk'
    if not (Development_Kit/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((Development_Kit/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfigurace_BITS = [Nastavení_HODNOTA for Nastavení_HODNOTA in konfigurace_BITS if Nastavení_HODNOTA != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', upstream, '-I', kořen_cesta/'uživatelský_prostor', '-I', KV_data, '-isystem', Development_Kit/'usr/include']
    Provést_příkaz([C_kompilátor]+konfigurace_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'spuštění_vzpěra.c','-o',KV_data/'crt.o'])
    Provést_příkaz([C_kompilátor]+konfigurace_BITS+['-I',úložiště_cesta/'posix-kor/arm64-native/deklarace']+포함인수+['-c',원본자료/'AOT_CLR.c','-o',KV_data/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+data_pozice.name,data_pozice) for data_pozice in sorted((úložiště_cesta/'posix-kor/arm64-native/deklarace').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_pozice.name,data_pozice) for data_pozice in sorted((upstream/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_pozice.name,data_pozice) for data_pozice in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',kořen_cesta/'build/user/start.o'),('/sdk/lib/crt.o',KV_data/'crt.o'),('/sdk/lib/aot-runtime.o',KV_data/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',kořen_cesta/'build/libposix-kor-user.a')]
    Nadpis_HODNOTA=['typedef struct { const char *Název; const unsigned char *data; unsigned Velikost; } kompilátor_zdroj;']
    for 순번,(_,cesta_2) in enumerate(탑재자료):
        Nadpis_HODNOTA.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in cesta_2.read_bytes())))
    Nadpis_HODNOTA.append('static const kompilátor_zdroj kompilátor_Prostředky[] = {')
    for 순번,(Název,cesta_2) in enumerate(탑재자료): Nadpis_HODNOTA.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Název,ensure_ascii=False),순번,cesta_2.stat().st_size))
    Nadpis_HODNOTA.append('};');(KV_data/'resources.h').write_text('\n'.join(Nadpis_HODNOTA)+'\n',encoding='utf-8')
    cíl_Files=[]
    for Název in ('kompilátor_nástroj.c','CLR_vzpěra.c','Spustit_2.c','미리번역.c','Vratka_most.S'):
        cílový_soubor=KV_data/(Path(Název).stem+'.o');cíl_Files.append(cílový_soubor)
        Provést_příkaz([C_kompilátor]+konfigurace_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Název,'-o',cílový_soubor])
    spustitelný_soubor=kořen_cesta/'build/user/cc.elf'
    Provést_příkaz([linker_nástroj,'--gc-sections','-T',kořen_cesta/'uživatelský_prostor/rozvržení_spojování.ld','-z','max-page-size=4096','-o',spustitelný_soubor,
         kořen_cesta/'build/user/start.o',kořen_cesta/'build/user/runtime.o']+cíl_Files+
         [kořen_cesta/'build/user'/Název for Název in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
