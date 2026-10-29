"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def Ustvari_C_prevajalnik(koren_pot, shramba_pot, C_prevajalnik, 연결편집기, konfiguracija_storitev_Background_Intelligent_Transfer_Service, Izvedi_ukaz):
    KR_podatki = koren_pot / 'build/ccompiler'; KR_podatki.mkdir(exist_ok=True)
    원본자료 = koren_pot / 'C_prevajalnik'
    protitočno = koren_pot / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    razvijalski_komplet = koren_pot / 'vendor/sdk'
    if not (razvijalski_komplet/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((razvijalski_komplet/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfiguracija_storitev_Background_Intelligent_Transfer_Service = [Nastavitve_VALUE for Nastavitve_VALUE in konfiguracija_storitev_Background_Intelligent_Transfer_Service if Nastavitve_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', protitočno, '-I', koren_pot/'uporabnik', '-I', KR_podatki, '-isystem', razvijalski_komplet/'usr/include']
    Izvedi_ukaz([C_prevajalnik]+konfiguracija_storitev_Background_Intelligent_Transfer_Service+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'zagnati_Podpora.c','-o',KR_podatki/'crt.o'])
    Izvedi_ukaz([C_prevajalnik]+konfiguracija_storitev_Background_Intelligent_Transfer_Service+['-I',shramba_pot/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',KR_podatki/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+podatki_položaj.name,podatki_položaj) for podatki_položaj in sorted((shramba_pot/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+podatki_položaj.name,podatki_položaj) for podatki_položaj in sorted((protitočno/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+podatki_položaj.name,podatki_položaj) for podatki_položaj in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',koren_pot/'build/user/start.o'),('/sdk/lib/crt.o',KR_podatki/'crt.o'),('/sdk/lib/aot-runtime.o',KR_podatki/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',koren_pot/'build/libposix-kor-user.a')]
    Glava_VALUE=['typedef struct { const char *Ime; const unsigned char *podatki; unsigned Velikost; } prevajalnik_vir;']
    for 순번,(_,POT) in enumerate(탑재자료):
        Glava_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in POT.read_bytes())))
    Glava_VALUE.append('static const prevajalnik_vir prevajalnik_Viri[] = {')
    for 순번,(Ime,POT) in enumerate(탑재자료): Glava_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Ime,ensure_ascii=False),순번,POT.stat().st_size))
    Glava_VALUE.append('};');(KR_podatki/'resources.h').write_text('\n'.join(Glava_VALUE)+'\n',encoding='utf-8')
    cilj_Datoteke=[]
    for Ime in ('prevajalnik_orodje.c','skupni_jezikovni_izvajalnik_Podpora.c','Zaženi.c','미리번역.c','vrni_most.S'):
        ciljna_datoteka=KR_podatki/(Path(Ime).stem+'.o');cilj_Datoteke.append(ciljna_datoteka)
        Izvedi_ukaz([C_prevajalnik]+konfiguracija_storitev_Background_Intelligent_Transfer_Service+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Ime,'-o',ciljna_datoteka])
    실행파일=koren_pot/'build/user/cc.elf'
    Izvedi_ukaz([연결편집기,'--gc-sections','-T',koren_pot/'uporabnik/Povezava_Krmarjenje.ld','-z','max-page-size=4096','-o',실행파일,
         koren_pot/'build/user/start.o',koren_pot/'build/user/runtime.o']+cilj_Datoteke+
         [koren_pot/'build/user'/Ime for Ime in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
