"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def Skapa_C_kompilerare(rot_väg, centrallager_väg, C_kompilerare, länkare_verktyg, konfiguration_BITS, köra_kommando):
    KR_data = rot_väg / 'build/ccompiler'; KR_data.mkdir(exist_ok=True)
    원본자료 = rot_väg / 'C_kompilerare'
    uppström = rot_väg / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    development_kit = rot_väg / 'vendor/sdk'
    if not (development_kit/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((development_kit/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfiguration_BITS = [Inställningar_värde for Inställningar_värde in konfiguration_BITS if Inställningar_värde != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', uppström, '-I', rot_väg/'användarutrymme', '-I', KR_data, '-isystem', development_kit/'usr/include']
    köra_kommando([C_kompilerare]+konfiguration_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'start_stöd.c','-o',KR_data/'crt.o'])
    köra_kommando([C_kompilerare]+konfiguration_BITS+['-I',centrallager_väg/'posix-kor/arm64-native/deklarationer']+포함인수+['-c',원본자료/'AOT_CLR.c','-o',KR_data/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+data_placera.name,data_placera) for data_placera in sorted((centrallager_väg/'posix-kor/arm64-native/deklarationer').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_placera.name,data_placera) for data_placera in sorted((uppström/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_placera.name,data_placera) for data_placera in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',rot_väg/'build/user/start.o'),('/sdk/lib/crt.o',KR_data/'crt.o'),('/sdk/lib/aot-runtime.o',KR_data/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',rot_väg/'build/libposix-kor-user.a')]
    huvud_värde=['typedef struct { const char *Namn; const unsigned char *data; unsigned Storlek; } kompilerare_resurs;']
    for 순번,(_,sökväg_2) in enumerate(탑재자료):
        huvud_värde.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in sökväg_2.read_bytes())))
    huvud_värde.append('static const kompilerare_resurs kompilerare_Resurser[] = {')
    for 순번,(Namn,sökväg_2) in enumerate(탑재자료): huvud_värde.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Namn,ensure_ascii=False),순번,sökväg_2.stat().st_size))
    huvud_värde.append('};');(KR_data/'resources.h').write_text('\n'.join(huvud_värde)+'\n',encoding='utf-8')
    mål_Filer=[]
    for Namn in ('kompilerare_verktyg.c','CLR_stöd.c','Kör.c','미리번역.c','Retur_brygga.S'):
        målfil=KR_data/(Path(Namn).stem+'.o');mål_Filer.append(målfil)
        köra_kommando([C_kompilerare]+konfiguration_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Namn,'-o',målfil])
    körbar_fil_fil=rot_väg/'build/user/cc.elf'
    köra_kommando([länkare_verktyg,'--gc-sections','-T',rot_väg/'användarutrymme/länkningslayout.ld','-z','max-page-size=4096','-o',körbar_fil_fil,
         rot_väg/'build/user/start.o',rot_väg/'build/user/runtime.o']+mål_Filer+
         [rot_väg/'build/user'/Namn for Namn in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
