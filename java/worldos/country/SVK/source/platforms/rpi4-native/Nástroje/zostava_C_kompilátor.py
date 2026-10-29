"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def Create_C_kompilátor(koreň_cesta, odkladací_priestor_cesta, C_kompilátor, 연결편집기, konfigurácia_Background_Intelligent_Transfer_Service, Vykonať_príkaz):
    KR_údaje = koreň_cesta / 'build/ccompiler'; KR_údaje.mkdir(exist_ok=True)
    원본자료 = koreň_cesta / 'C_kompilátor'
    upstreamový = koreň_cesta / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    Development_Kit = koreň_cesta / 'vendor/sdk'
    if not (Development_Kit/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((Development_Kit/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfigurácia_Background_Intelligent_Transfer_Service = [Nastavenia_VALUE for Nastavenia_VALUE in konfigurácia_Background_Intelligent_Transfer_Service if Nastavenia_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', upstreamový, '-I', koreň_cesta/'používateľ', '-I', KR_údaje, '-isystem', Development_Kit/'usr/include']
    Vykonať_príkaz([C_kompilátor]+konfigurácia_Background_Intelligent_Transfer_Service+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'spustenie_Podpora.c','-o',KR_údaje/'crt.o'])
    Vykonať_príkaz([C_kompilátor]+konfigurácia_Background_Intelligent_Transfer_Service+['-I',odkladací_priestor_cesta/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',KR_údaje/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+údaje_pozícia.name,údaje_pozícia) for údaje_pozícia in sorted((odkladací_priestor_cesta/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+údaje_pozícia.name,údaje_pozícia) for údaje_pozícia in sorted((upstreamový/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+údaje_pozícia.name,údaje_pozícia) for údaje_pozícia in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',koreň_cesta/'build/user/start.o'),('/sdk/lib/crt.o',KR_údaje/'crt.o'),('/sdk/lib/aot-runtime.o',KR_údaje/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',koreň_cesta/'build/libposix-kor-user.a')]
    Nadpis_VALUE=['typedef struct { const char *Názov; const unsigned char *údaje; unsigned Veľkosť; } kompilátor_zdroj;']
    for 순번,(_,Cesta) in enumerate(탑재자료):
        Nadpis_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Cesta.read_bytes())))
    Nadpis_VALUE.append('static const kompilátor_zdroj kompilátor_Zdroje[] = {')
    for 순번,(Názov,Cesta) in enumerate(탑재자료): Nadpis_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Názov,ensure_ascii=False),순번,Cesta.stat().st_size))
    Nadpis_VALUE.append('};');(KR_údaje/'resources.h').write_text('\n'.join(Nadpis_VALUE)+'\n',encoding='utf-8')
    cieľ_Súbory=[]
    for Názov in ('kompilátor_nástroj.c','CLR_Podpora.c','Spustiť_2.c','미리번역.c','vrátiť_most.S'):
        cieľový_súbor=KR_údaje/(Path(Názov).stem+'.o');cieľ_Súbory.append(cieľový_súbor)
        Vykonať_príkaz([C_kompilátor]+konfigurácia_Background_Intelligent_Transfer_Service+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Názov,'-o',cieľový_súbor])
    spustiteľný_súbor=koreň_cesta/'build/user/cc.elf'
    Vykonať_príkaz([연결편집기,'--gc-sections','-T',koreň_cesta/'používateľ/odkaz_Navigácia.ld','-z','max-page-size=4096','-o',spustiteľný_súbor,
         koreň_cesta/'build/user/start.o',koreň_cesta/'build/user/runtime.o']+cieľ_Súbory+
         [koreň_cesta/'build/user'/Názov for Názov in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
