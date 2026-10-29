"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def készít_C_fordítóprogram(gyök_útvonal, adattár_útvonal, C_fordítóprogram, kapcsolószerkesztő_eszköz, konfiguráció_BITS, végrehajt_parancs):
    KR_adat = gyök_útvonal / 'build/ccompiler'; KR_adat.mkdir(exist_ok=True)
    원본자료 = gyök_útvonal / 'C_fordítóprogram'
    kiinduló = gyök_útvonal / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    fejlesztőkészlet = gyök_útvonal / 'vendor/sdk'
    if not (fejlesztőkészlet/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((fejlesztőkészlet/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfiguráció_BITS = [Gépház_ÉRTÉK for Gépház_ÉRTÉK in konfiguráció_BITS if Gépház_ÉRTÉK != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', kiinduló, '-I', gyök_útvonal/'felhasználó', '-I', KR_adat, '-isystem', fejlesztőkészlet/'usr/include']
    végrehajt_parancs([C_fordítóprogram]+konfiguráció_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'rendszerindítás_támogat.c','-o',KR_adat/'crt.o'])
    végrehajt_parancs([C_fordítóprogram]+konfiguráció_BITS+['-I',adattár_útvonal/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'AOT_CLR.c','-o',KR_adat/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+adat_pozíció.name,adat_pozíció) for adat_pozíció in sorted((adattár_útvonal/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+adat_pozíció.name,adat_pozíció) for adat_pozíció in sorted((kiinduló/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+adat_pozíció.name,adat_pozíció) for adat_pozíció in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',gyök_útvonal/'build/user/start.o'),('/sdk/lib/crt.o',KR_adat/'crt.o'),('/sdk/lib/aot-runtime.o',KR_adat/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',gyök_útvonal/'build/libposix-kor-user.a')]
    fejléc_ÉRTÉK=['typedef struct { const char *Név; const unsigned char *adat; unsigned Méret; } fordítóprogram_erőforrás;']
    for 순번,(_,ÚTVONAL) in enumerate(탑재자료):
        fejléc_ÉRTÉK.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in ÚTVONAL.read_bytes())))
    fejléc_ÉRTÉK.append('static const fordítóprogram_erőforrás fordítóprogram_Források[] = {')
    for 순번,(Név,ÚTVONAL) in enumerate(탑재자료): fejléc_ÉRTÉK.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Név,ensure_ascii=False),순번,ÚTVONAL.stat().st_size))
    fejléc_ÉRTÉK.append('};');(KR_adat/'resources.h').write_text('\n'.join(fejléc_ÉRTÉK)+'\n',encoding='utf-8')
    cél_Files=[]
    for Név in ('fordítóprogram_eszköz.c','CLR_támogat.c','Futtatás.c','미리번역.c','visszaküld_híd.S'):
        célfájl=KR_adat/(Path(Név).stem+'.o');cél_Files.append(célfájl)
        végrehajt_parancs([C_fordítóprogram]+konfiguráció_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Név,'-o',célfájl])
    végrehajtható_Fájl=gyök_útvonal/'build/user/cc.elf'
    végrehajt_parancs([kapcsolószerkesztő_eszköz,'--gc-sections','-T',gyök_útvonal/'felhasználó/csatol_Navigáció.ld','-z','max-page-size=4096','-o',végrehajtható_Fájl,
         gyök_útvonal/'build/user/start.o',gyök_útvonal/'build/user/runtime.o']+cél_Files+
         [gyök_útvonal/'build/user'/Név for Név in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
