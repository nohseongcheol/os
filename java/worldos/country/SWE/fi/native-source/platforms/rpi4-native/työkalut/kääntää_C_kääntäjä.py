"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def Luo_C_kääntäjä(juuri_polku, säilö_polku, C_kääntäjä, linkitin_työkalu, määritys_Background_Intelligent_Transfer_Service, Suorita_komento):
    KR_data = juuri_polku / 'build/ccompiler'; KR_data.mkdir(exist_ok=True)
    원본자료 = juuri_polku / 'C_kääntäjä'
    yläpuolinen = juuri_polku / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    ohjelmankehityspaketti = juuri_polku / 'vendor/sdk'
    if not (ohjelmankehityspaketti/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((ohjelmankehityspaketti/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    määritys_Background_Intelligent_Transfer_Service = [Asetukset_ARVO for Asetukset_ARVO in määritys_Background_Intelligent_Transfer_Service if Asetukset_ARVO != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', yläpuolinen, '-I', juuri_polku/'käyttäjätila', '-I', KR_data, '-isystem', ohjelmankehityspaketti/'usr/include']
    Suorita_komento([C_kääntäjä]+määritys_Background_Intelligent_Transfer_Service+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'käynnistys_Tuki.c','-o',KR_data/'crt.o'])
    Suorita_komento([C_kääntäjä]+määritys_Background_Intelligent_Transfer_Service+['-I',säilö_polku/'posix-kor/arm64-native/esittelyt']+포함인수+['-c',원본자료/'AOT_CLR.c','-o',KR_data/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+data_toimi.name,data_toimi) for data_toimi in sorted((säilö_polku/'posix-kor/arm64-native/esittelyt').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_toimi.name,data_toimi) for data_toimi in sorted((yläpuolinen/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_toimi.name,data_toimi) for data_toimi in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',juuri_polku/'build/user/start.o'),('/sdk/lib/crt.o',KR_data/'crt.o'),('/sdk/lib/aot-runtime.o',KR_data/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',juuri_polku/'build/libposix-kor-user.a')]
    otsikko_ARVO=['typedef struct { const char *Nimi; const unsigned char *data; unsigned Koko; } kääntäjä_resurssi;']
    for 순번,(_,polku_2) in enumerate(탑재자료):
        otsikko_ARVO.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in polku_2.read_bytes())))
    otsikko_ARVO.append('static const kääntäjä_resurssi kääntäjä_Resurssit[] = {')
    for 순번,(Nimi,polku_2) in enumerate(탑재자료): otsikko_ARVO.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Nimi,ensure_ascii=False),순번,polku_2.stat().st_size))
    otsikko_ARVO.append('};');(KR_data/'resources.h').write_text('\n'.join(otsikko_ARVO)+'\n',encoding='utf-8')
    kohde_Files=[]
    for Nimi in ('kääntäjä_työkalu.c','CLR_Tuki.c','Suorita_2.c','미리번역.c','palauttaa_silta.S'):
        kohdetiedosto=KR_data/(Path(Nimi).stem+'.o');kohde_Files.append(kohdetiedosto)
        Suorita_komento([C_kääntäjä]+määritys_Background_Intelligent_Transfer_Service+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Nimi,'-o',kohdetiedosto])
    suoritettava_tiedosto=juuri_polku/'build/user/cc.elf'
    Suorita_komento([linkitin_työkalu,'--gc-sections','-T',juuri_polku/'käyttäjätila/linkitysasettelu.ld','-z','max-page-size=4096','-o',suoritettava_tiedosto,
         juuri_polku/'build/user/start.o',juuri_polku/'build/user/runtime.o']+kohde_Files+
         [juuri_polku/'build/user'/Nimi for Nimi in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
