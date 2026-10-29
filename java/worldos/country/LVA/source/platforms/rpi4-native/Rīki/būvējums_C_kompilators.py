"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def atvērt_C_kompilators(sakne_ceļš, repozitorijs_ceļš, C_kompilators, 연결편집기, konfigurācija_Background_Intelligent_Transfer_Service, Izpildīt_komanda):
    mērs_dati = sakne_ceļš / 'build/ccompiler'; mērs_dati.mkdir(exist_ok=True)
    원본자료 = sakne_ceļš / 'C_kompilators'
    iepriekšējs = sakne_ceļš / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    programmizstrādes_komplekts = sakne_ceļš / 'vendor/sdk'
    if not (programmizstrādes_komplekts/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((programmizstrādes_komplekts/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfigurācija_Background_Intelligent_Transfer_Service = [Iestatījumi_VALUE for Iestatījumi_VALUE in konfigurācija_Background_Intelligent_Transfer_Service if Iestatījumi_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', iepriekšējs, '-I', sakne_ceļš/'lietotājs', '-I', mērs_dati, '-isystem', programmizstrādes_komplekts/'usr/include']
    Izpildīt_komanda([C_kompilators]+konfigurācija_Background_Intelligent_Transfer_Service+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'palaišana_Atbalsts.c','-o',mērs_dati/'crt.o'])
    Izpildīt_komanda([C_kompilators]+konfigurācija_Background_Intelligent_Transfer_Service+['-I',repozitorijs_ceļš/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'AOT_CLR.c','-o',mērs_dati/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+dati_amats.name,dati_amats) for dati_amats in sorted((repozitorijs_ceļš/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+dati_amats.name,dati_amats) for dati_amats in sorted((iepriekšējs/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+dati_amats.name,dati_amats) for dati_amats in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',sakne_ceļš/'build/user/start.o'),('/sdk/lib/crt.o',mērs_dati/'crt.o'),('/sdk/lib/aot-runtime.o',mērs_dati/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',sakne_ceļš/'build/libposix-kor-user.a')]
    galvene_VALUE=['typedef struct { const char *Nosaukums; const unsigned char *dati; unsigned Izmērs; } kompilators_resurss;']
    for 순번,(_,CEĻŠ) in enumerate(탑재자료):
        galvene_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in CEĻŠ.read_bytes())))
    galvene_VALUE.append('static const kompilators_resurss kompilators_Resursi[] = {')
    for 순번,(Nosaukums,CEĻŠ) in enumerate(탑재자료): galvene_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Nosaukums,ensure_ascii=False),순번,CEĻŠ.stat().st_size))
    galvene_VALUE.append('};');(mērs_dati/'resources.h').write_text('\n'.join(galvene_VALUE)+'\n',encoding='utf-8')
    mērķis_Faili=[]
    for Nosaukums in ('kompilators_rīks.c','CLR_Atbalsts.c','Palaist.c','미리번역.c','atdot_tilts.S'):
        mērķa_fails=mērs_dati/(Path(Nosaukums).stem+'.o');mērķis_Faili.append(mērķa_fails)
        Izpildīt_komanda([C_kompilators]+konfigurācija_Background_Intelligent_Transfer_Service+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Nosaukums,'-o',mērķa_fails])
    izpildāms_fails=sakne_ceļš/'build/user/cc.elf'
    Izpildīt_komanda([연결편집기,'--gc-sections','-T',sakne_ceļš/'lietotājs/Saite_shēma.ld','-z','max-page-size=4096','-o',izpildāms_fails,
         sakne_ceļš/'build/user/start.o',sakne_ceļš/'build/user/runtime.o']+mērķis_Faili+
         [sakne_ceļš/'build/user'/Nosaukums for Nosaukums in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
